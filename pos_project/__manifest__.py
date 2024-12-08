# -*- coding: utf-8 -*-
{
    'name': "Pos Project",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','point_of_sale', 'mail', 'website'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
    ],
    'installable': True,
    'application': True,
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_project/static/src/app/bill_button/bill_button.js',
            'pos_project/static/src/app/bill_button/bill_button.xml',
            'pos_project/static/src/app/payment_screen/payment_screen.xml',
            'pos_project/static/src/app/product_screen/screen.css',
            'pos_project/static/src/app/product_screen/product_screen.js',
        ],
        'web.assets_backend': [
            'pos_project/static/src/mail/form/form_compiler.js',
        ],
    }

}

