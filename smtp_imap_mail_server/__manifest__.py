{
    'name' : 'MP-SMTP and IMAP Mail Server By Company & User',
    'version' : '16.0.0.0',
    'company': 'Mp Technolabs',
    'category': 'mail',
    'author': "MP Technolabs",
    'website': 'https://www.mptechnolabs.com/',
    'summary' : 'SMTP and IMAP Mail Server By Company & User with multiple Alias Domain selection',
    'description' : """COMPANY-WISE AND USER-WISE OUTGOING EMAIL CONFIGURATION.
        IMAP MAIL ALIASES WITH MULTIPLE DOMAIN""",
    'depends' : ['base','sale_management','crm','project','mail','account','hr_recruitment'],
    'data' : [
        'security/ir.model.access.csv',
        'views/mail_server_view.xml',
        'views/alias_mail_and_domain_view.xml',
        'views/res_config_settings_view.xml',
      
    ],
    'images': ['static/description/banner.png'],
    "license": "LGPL-3",
    'installable': True,
    'auto_install': False,
    'application': False,
    
}