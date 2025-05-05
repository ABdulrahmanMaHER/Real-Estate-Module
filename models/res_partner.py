from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_ids = fields.Many2one('property', string="Property")
    price = fields.Float(related='property_ids.selling_price', string="Price", readonly=False)
    # price=fields.Float(compute='compute_selling_price')

    # @api.depends('property_ids')
    # def compute_selling_price(self):
    #     for rec in self:
    #         rec.price = rec.property_ids.selling_price if rec.property_ids else 0.0
