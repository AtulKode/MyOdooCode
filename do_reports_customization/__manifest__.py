# -*- coding: utf-8 -*-
{
    'name': 'Albanna Report Customisation',
    'version': '16.0.1.0',
    'category': 'Studio',
    'description': u"""
Albanna Report
""",
    'author': 'Dar Albanna Group Co. Ltd.',
    'depends': [
        'purchase', 'web', 'account', 'stock', 'hr','report_enhancements'
    ],
    'data': [
        'security/ir.model.access.csv',
        'report/delivery_report_templates.xml',
        'report/invoice_report_templates.xml',
        'report/purchase_report_templates.xml',
        'report/report_views.xml',
        'views/res_partner_views.xml',
        'views/terms_condition_views.xml',
    ],
    'application': False,
    'license': 'OPL-1',
}

