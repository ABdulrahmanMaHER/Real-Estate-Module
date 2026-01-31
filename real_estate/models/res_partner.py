from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_ids = fields.Many2one('property', string="Property")
    price = fields.Float(related='property_ids.selling_price', string="Price", readonly=False)
