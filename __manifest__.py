{
    'name': 'Real Estate',
    'author': 'Abdulrahman Maher',
    'version': '18.0.0.1.0',
    'depends': ['base','sale_management','account','mail','contacts','web'],
    'data': [
      # 'security/security.xml',
      'security/ir.model.access.csv',
      'data/seq.xml',
      'xml_files/property_base_menu.xml',
      'xml_files/owner_base_menu.xml',
      'xml_files/property_view.xml',
      'xml_files/owner_view.xml',
      'xml_files/property_history_view.xml',
      'xml_files/property_orders_view.xml',
      'xml_files/res_partner_view.xml',
      'wizard/change_status_wizard_view.xml',
      'reports/property_report.xml'
    ],
    'category': '',
    'license': 'LGPL-3',
    'images': ['static/description/icon.png'],
    'assets': {
        'web.assets_backend': [
            "TEST_APP/static/src/components/listviews/listView.xml",
            "TEST_APP/static/src/components/listviews/listView.js",
            "TEST_APP/static/src/components/listviews/listView.css"
        ],
        'web.report_assets_common': ['TEST_APP/static/src/fonts.css']
    },
    'application': True
}