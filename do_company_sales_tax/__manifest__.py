{
    'name': "Do Company Sales Tax",
    'summary': """This module help Company to apply tax state wise and based on its thresold sales limit""",
    'description': """This module help Company to apply tax state wise and based on its thresold sales limit""",
    'author': "Do Incredible",
    'website': "",
    'category': 'Sales',
    'version': '17.0.0.0',
    # any module necessary for this one to work correctly
    'depends': ['sale','sale_management','contacts','account'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_country_state_views.xml',
        'views/res_company_views.xml',
        'wizard/sale_tax_wizard_views.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
