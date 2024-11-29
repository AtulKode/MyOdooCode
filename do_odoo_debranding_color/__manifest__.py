
{
    'name': "Do Odoo Debranding Theme",
    'summary': """
        """,
    'description': """
    """,
    'author': "Do Incredible",
    'website': "https://doincredible.com/",
    'category': 'Tools',
    'version': '17.0.0.0',
    'depends': ['base','web'],
    'data': [
            "views/views.xml",
            ],
            
    'assets': {
        'web.assets_backend': [
            'do_odoo_debranding_color/static/src/js/change_theme_colour.js',
        ],

        'web._assets_primary_variables': [
            (
                'after', 
                'web/static/src/scss/primary_variables.scss', 
                'do_odoo_debranding_color/static/navbar/navbar.variable.scss',
            ),
        ],
    },
    'license': "AGPL-3",
    'installable': True,
    'application': True,
}
