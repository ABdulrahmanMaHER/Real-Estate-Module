from odoo import models, fields

class Property(models.Model):
    _name = 'property.history'
    _description = 'History of Properties'
    _rec_name ='user_id'

    user_id = fields.Many2one('res.users')
    property_id=fields.Many2one('property')
    old_status = fields.Char()
    new_status = fields.Char()
    reason=fields.Char()
    date=fields.Datetime()
    bedroom_ids=fields.One2many('property.history.bedrooms','bedroom_id')









