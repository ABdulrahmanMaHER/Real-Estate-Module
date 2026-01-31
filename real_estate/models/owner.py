from odoo import models, fields

class Owner(models.Model):
    _name = 'owner'
    _description = 'Owners of the Properties'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    image_1920 = fields.Image(string="Image", max_width=1920, max_height=1920)
    name = fields.Char(required=True)
    phone = fields.Char()
    address = fields.Text()
    properties = fields.One2many('property', 'owner', string="Properties",readonly=1)
