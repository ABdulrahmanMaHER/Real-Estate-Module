from odoo import models, fields

class Owner(models.Model):
    _name = 'owner'
    _description = 'Owners of the Properties'

    name = fields.Char(required=True)
    phone = fields.Char()
    address = fields.Text()
    properties = fields.One2many('property', 'owner', string="Properties",readonly=1)
