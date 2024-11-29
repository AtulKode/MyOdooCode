# -*- coding: utf-8 -*-

{
    'name': 'DO Product Label Customise',
    'version': '1.0',
    'author': 'Do Incredible',
    'website': 'www.doincredible.com',
    'category': 'Product',
    'summary': 'DO Product Label Customise',
    'description': """
DO Product Label Customise
==========================

Changes
-------
* Add Measuring Unit on Product Template
* Product Label Report
""",
    'depends': ['product'],
    'data': [
        'views/product_views.xml',
        'report/ir_actions_report.xml',
        'report/ir_actions_report_templates.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
