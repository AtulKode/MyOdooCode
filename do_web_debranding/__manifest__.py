
{
    'name': "Do Web Debranding",
    'summary': """
        """,
    'description': """
    """,
    'author': "Do Incredible",
    'website': "https://doincredible.com/",
    'category': 'Tools',
    'version': '17.0.0.0',
    'depends': ['base','web','web_enterprise', 'sign'],
    'data': [
    ],
            
    'assets': {
        'web.assets_backend': [
            'do_web_debranding/static/src/color_scheme_menu.js',
        ],
        'sign.assets_pdf_iframe': [
            'do_web_debranding/static/src/css/iframe.css',
        ],
        'web._assets_primary_variables': [
            (
                'before', 
                'web_enterprise/static/src/scss/primary_variables.scss', 
                'do_web_debranding/static/src/scss/primary_button.scss',
            ),
        ],
        "web.assets_web_dark": [
            (
                'before', 
                'web_enterprise/static/src/scss/bootstrap_overridden.dark.scss',
                'do_web_debranding/static/src/scss/dark_button.scss'
            ),
        ],
    },
    'license': "AGPL-3",
    'installable': True,
    'application': True,
}
# 'sign/static/src/css/iframe.css',