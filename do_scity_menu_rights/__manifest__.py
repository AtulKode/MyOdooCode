# -*- coding: utf-8 -*-
{
    # Module Info.
    'name': 'Do Scity Menu Rights',
    'version': '17.0.0.0',
    'sequence': 70,
    'summary': """Do Scity Menu Rights""",
    'description': 'Do Scity Menu Rights',
    'category': '',

    # Author
    'author': "Do Incredible",
    'website': "https://doincredible.com/",

    # Dependencies
    'depends': ['web'],

    # Data File
    'data': [
        'security/ir.model.access.csv',
        'views/res_users_view.xml',
    ],

    # Technical Specifications
    'installable': True,
    'auto_install': False,
    'application': True,
}
