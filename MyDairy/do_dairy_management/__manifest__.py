{
    'name': 'DO Dairy Management',
    'version': '1.0',
    'category': 'Dairy',
    'description': """
Dairy Management sytem
======================
    """,
    'depends': ['base','mail'],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'security/security_rule.xml',
        'data/dairy_cust_seq.xml',
        'views/animal_animal_views.xml',
        'views/milk_dairy_views.xml',
        'views/customer_registration_views.xml',
        'views/milk_intake_management_views.xml',
        'views/rate_management_views.xml',
        'views/dairy_menus.xml',
        ],
    'module_type': 'official',
    'application': True,
    'license': 'LGPL-3',
}
