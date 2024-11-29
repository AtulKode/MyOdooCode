{
    'name': 'DO Dairy Management Kiosk',
    'version': '1.0',
    'category': 'Dairy',
    'description': """
Dairy Management sytem Kiosk
============================
    """,
    'depends': ['web','base','do_dairy_management','do_dairy_mgmt_portal'],
    'data': [
            'views/dairy_kiosk_view.xml',
        ],
    'assets': {
    'web.assets_backend': [
        'do_dairy_mgmt/static/src/**/*',
    ],
  
    },
    'module_type': 'official',
    'application': True,
    'license': 'LGPL-3',
}
