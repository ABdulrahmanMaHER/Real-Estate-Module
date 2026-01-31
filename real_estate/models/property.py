from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime
import requests

class Property(models.Model):
    _name = 'property'
    _description = 'Real Estate Property App'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    image_1920 = fields.Image(string="Image", max_width=1920, max_height=1920)
    name = fields.Char(required=1,tracking=1)
    ref=fields.Char(default='New',readonly=1)
    description = fields.Text()
    post_code = fields.Char(tracking=1)
    date_availability = fields.Date(default=datetime.date.today(),tracking=1)
    expected_selling_date = fields.Date(tracking=1)
    is_late = fields.Boolean(compute='check_expected_selling_date')
    expected_price = fields.Float(digits=(0, 2))
    selling_price = fields.Float(digits=(0, 2))
    diff=fields.Float(compute='price_diff')
    bedrooms = fields.Integer(compute="check_bedroom_count")
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Float()
    garage_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], string="Garage Orientation", default='north')
    state=fields.Selection([
        ('draft','Draft'),
        ('pending','Pending'),
        ('sold','Sold'),
        ('closed','Closed')
    ],string='State',default='draft',tracking=1)
    owner = fields.Many2one('owner',tracking=1)
    owner_phone=fields.Char(related='owner.phone',readonly=1)
    line_ids=fields.One2many('property.lines','property_id')
    active = fields.Boolean(default=1)

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'THIS NAME IS ALRREDY USED!'),
        ('not_null_name', 'CHECK(name IS NOT NULL)', 'PLEASE ENTER A VALID NAME!')
    ]

    @api.constrains('expected_selling_date', 'date_availability')
    def _expected_selling_date_constraint(self):
        for rec in self:
            if rec.expected_selling_date and rec.date_availability:
                if rec.expected_selling_date < rec.date_availability:
                    raise ValidationError(
                        "YOU CAN NOT ENTER AN EXPECTED SELLING DATE THAT IS LESS THAN THE AVAILABILITY DATE!")

    @api.constrains('garden')
    def _garden_constraint(self):
        for rec in self:
            if rec.garden and rec.garden_area <= 0.0:
                raise ValidationError("PLEASE ENTER A VALID GARDEN AREA!")

    @api.depends('bedrooms', 'line_ids')
    def check_bedroom_count(self):
        for rec in self:
            rec.bedrooms=len(rec.line_ids)

    @api.depends('expected_price','selling_price')
    def price_diff(self):
        for rec in self:
            rec.diff=rec.selling_price-rec.expected_price


    def draft_act(self):
        for rec in self:
            rec.p_history(rec.state,'draft')
            rec.state='draft'

    def pending_act(self):
        for rec in self:
            rec.p_history(rec.state,'pending')
            rec.state='pending'

    def sold_act(self):
        for rec in self:
            rec.p_history(rec.state, 'sold')
            rec.state='sold'

    def closed_act(self):
        for rec in self:
            rec.p_history(rec.state,'closed')
            rec.state='closed'

    def p_history(self, old, new, reason=" "):
        history_model = self.env['property.history']
        for rec in self:
            history_model.create({
                'user_id': rec.env.user.id,
                'property_id': rec.id,
                'old_status': old,
                'new_status': new,
                'reason': reason or '',
                'date': fields.Datetime.now(),
                'bedroom_ids':[(0,0,{'description':line.description,'area':line.area})for line in rec.line_ids]
            })

    def open_owner_action(self):
        action = self.env['ir.actions.actions']._for_xml_id('real_estate.owner_action_rec')
        view_id = self.env.ref('real_estate.owner_list_form').id
        action['views'] = [[view_id, 'form']]
        action['res_id'] = self.owner.id
        return action

    @api.depends('is_late')
    def check_expected_selling_date(self):
        today = fields.Date.today()
        properties = self.search([])

        for rec in properties:
            if (rec.expected_selling_date and rec.expected_selling_date < today
                    and rec.state not in ('sold', 'closed')):
                rec.is_late = True
            else:
                rec.is_late = False

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.ref=='New':
            res.ref=self.env['ir.sequence'].next_by_code('property_seq')
        return res

    def change_status_wizard(self):
        action=self.env['ir.actions.actions']._for_xml_id('real_estate.change_status_wizard_action_rec')
        action['context']={
            'default_property_id':self.id,
        }
        return action


    def update_property_request(self):
        try:
            property = self.env['property'].search([('id','=',self.id)], limit=1)
            if not property:
                raise ValidationError("No property found to update!")

            property_id = property.id

            payload = dict({
                'owner': 'Mohamed',
                'description': 'Updated via odoo as 3rd party app',
                'date_availability' : '1/10/2026',
                'line_ids.area' : 125
            } )

            response = requests.put(
                f'http://127.0.0.1:8070/v1/property/{property_id}',
                json=payload
            )

            if response.status_code == 200:
                print('Success:', response.json())
            else:
                print(f'Failed! Status: {response.status_code}, Response: {response.text}')

        except Exception as error:
            raise ValidationError(f"Error while updating property: {error}")

    def generate_property_excel(self):
        return {
            'type' : 'ir.actions.act_url',
            'url' :f"/property/excel/report?ids={','.join(map(str, self.ids))}",
            'target' : 'new'
        }


class Property_Lines(models.Model):
    _name = 'property.lines'
    _rec_name = 'ref'

    property_id = fields.Many2one('property', readonly=True)
    area = fields.Float("Area")
    description = fields.Text()
    ref = fields.Char(default='New', readonly=True,string='Room')

    @api.model
    def create(self, vals):
        res = super(Property_Lines, self).create(vals)
        if res.area < 10000:
            current_seconds = datetime.datetime.now().second
            res.ref = "BDR%04d%02d" % (int(res.area), current_seconds)
        else:
            raise ValidationError("PLEASE ENTER VALID AREA OF BEDROOM!")
        return res

    def write(self, vals):
        res = super(Property_Lines, self).write(vals)
        if 'area' in vals:
            for rec in self:
                if rec.area and rec.area < 10000:
                    current_seconds = datetime.datetime.now().second
                    rec.ref = "BDR%04d%02d" % (int(rec.area), current_seconds)
                else:
                    raise ValidationError("PLEASE ENTER VALID AREA OF BEDROOM!")
            return res






