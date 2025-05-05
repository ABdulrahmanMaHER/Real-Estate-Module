from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Change_Status_Wizard(models.TransientModel):
    _name = 'change.status'

    property_id=fields.Many2one('property',string='Property')
    status=fields.Selection([
        ('draft','Draft'),
        ('pending','Pending')
    ],string='Status',default='draft')
    reason=fields.Char()

    def action_confirm(self):
        if self.property_id.state != 'closed':
            raise ValidationError('THIS OPTION WORK ONLY FOR "CLOSED PROPERTIES" !')
        else:
            self.property_id.state = self.status
            self.property_id.p_history('closed',self.status,self.reason)
