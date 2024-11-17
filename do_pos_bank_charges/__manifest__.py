# -*- coding: utf-8 -*-
{
    'name': "Pos Bank Charges",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    'category': 'point_of_sale',
    'version': '0.1',

    'depends': ['base','point_of_sale'],

    'data': [
        'views/pos_order_view.xml',
        'views/pos_payment_views.xml',
    ],

    'assets': {
        'point_of_sale._assets_pos': [
            'do_pos_bank_charges/static/src/app/js/models.js',
            'do_pos_bank_charges/static/src/app/js/payment_screen.js',
            'do_pos_bank_charges/static/src/app/js/payment_status.js',
            'do_pos_bank_charges/static/src/app/xml/payment_screen.xml',
        ],
    },
    'installable': True,
    'license': 'LGPL-3',
}

