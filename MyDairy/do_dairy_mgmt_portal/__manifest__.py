{
    'name': 'DO Dairy Management Portal',
    'version': '1.0',
    'category': 'Dairy/portal',
    'description': """
Dairy Management Portal
=======================
    """,
    'depends': ['do_dairy_management','portal','contacts','website'],
    'data': [
        
        'views/res_config_settings_view.xml',
        'views/auth_signup_template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'do_dairy_mgmt_portal/static/css/dairy.css',
            'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
            'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.bundle.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.0.3/css/font-awesome.css',
            'do_dairy_mgmt_portal/static/src/js/animal_selection.js',
            'do_dairy_mgmt_portal/static/src/js/dairy_signup.js',
            
        ],
  
    },

    'module_type': 'official',
    'application': True,
    'license': 'LGPL-3',
}