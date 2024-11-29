
{
    'name': "Do Expiry Mail",
    'summary': """
        Expiry Mail
    """,
    'category': 'Base',
    'version': '16.0.1.0.1',
    'depends': ['base_setup', 'mail','web_enterprise'],
    'data' : [
    'views/res_config_setting.xml',
    'data/ir_cron.xml',
    'data/mail_template.xml',
   ],
    'application': True,
    "auto_install": False,
    "installable": True,
}
