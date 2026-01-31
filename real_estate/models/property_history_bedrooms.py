from odoo import models, fields, api

class PropertyHistoryBedrooms(models.Model):
    _name = 'property.history.bedrooms'
    _description = 'History of Properties Bedrooms'


    bedroom_id = fields.Many2one('property.history',string='Creator')
    name=fields.Char(related='bedroom_id.property_id.line_ids.ref',readonly=1)
    description = fields.Text()
    area = fields.Float()
