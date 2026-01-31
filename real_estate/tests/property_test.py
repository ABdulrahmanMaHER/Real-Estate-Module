from odoo.tests.common import TransactionCase
from odoo import fields

class PropertyTransaction(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(PropertyTransaction, cls).setUpClass()
        cls.property_record = cls.env['property'].create({
            'name': 'p1',
            'ref': 'PRT1236',
            'description': 'description of PRT1236 ',
            'expected_price': 1000,
            'date_availability': fields.Date.today(),
            'selling_price': 15700
        })

    def test_case_01(self):
        record = self.property_record
        self.assertRecordValues(record, [{
            'name': 'p1',
            'ref': 'PRT1236',
            'description': 'description of PRT1236 ',
            'expected_price': 1000,  # ✅ Corrected
            'selling_price': 15700
        }])
