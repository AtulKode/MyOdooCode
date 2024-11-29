# -*- coding: utf-8 -*-
{
    'name': "do_user_access",

    'summary': """
""",

    'description': """
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts'],

    # always loaded
    'data': [
        'security/record_rule.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
