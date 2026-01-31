{
    'name': 'Real Estate',
    'author': 'Abdulrahman Maher',
    'version': '18.0.0.1.0',
    'depends': ['base','sale_management','account','mail','contacts','web'],
    'data': [
      'security/security.xml',
      'security/ir.model.access.csv',
      'data/seq.xml',
      'data/properties.xml',
      'xml_files/property_base_menu.xml',
      'xml_files/property_view.xml',
      'xml_files/owner_view.xml',
      'xml_files/property_history_view.xml',
      'xml_files/res_partner_view.xml',
      'wizard/change_status_wizard_view.xml',
      'reports/property_report.xml'
    ],
    'category': '',
    'license': 'LGPL-3',
    'images': ['static/description/icon.png'],
    'assets': {
        'web.assets_backend': [
            "real_estate\static\src\components/formView/formView.js",
            "real_estate\static\src\components/formView/formView.xml",
            "real_estate\static\src\components/formView/formView.css",
            "real_estate/static/src/components/listviews/listView.js",
            "real_estate/static/src/components/listviews/listView.xml",
            "real_estate/static/src/components/listviews/listView.css",
            "real_estate/static/src/components/property/property.css"
        ],
        'web.report_assets_common': ['real_estate/static/src/components/property/fonts.css']
    },
    'application': True
}