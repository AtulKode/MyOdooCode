
{
    'name': "Do Odoo Debranding",
    'summary': """
        """,
    'description': """
    """,
    'author': "Do Incredible",
    'website': "https://doincredible.com/",
    'category': 'Tools',
    'version': '17.0.0.0',
    'depends': ['crm','website','web','crm_iap_mine','auth_signup','portal'],
    'data': [
            'data/mail_template.xml',
            'data/calendar_event.xml',
            'data/calendar_mail_template.xml',
            'data/calendar_invitation.xml',
            'data/calendar_reminder.xml',
            'data/mail_new_user_invite.xml',
            'data/mail_lead_generation.xml',
            'data/mail_setting_invitation.xml',
            'data/portal_mail.xml',
            'data/portal_signup.xml',
            "views/views.xml",
            "views/remove_about_section.xml",
            "views/web_layout.xml",
            ],
            
    'assets': {
        'web.assets_backend': [
            'do_odoo_debranding/static/src/xml/hide_user_menu.xml',
            'do_odoo_debranding/static/src/xml/error_dialog.xml',
            'do_odoo_debranding/static/src/js/webclient_title.js',
        ],
        'web._assets_primary_variables': [
            (
                'after', 
                'web/static/src/scss/primary_variables.scss', 
                'do_odoo_debranding/static/navbar/navbar.variable.scss',
            ),
            (
                'before', 
                'web/static/src/scss/primary_variables.scss', 
                'do_odoo_debranding/static/navbar/btn.varibale.scss',
            ),
        ],
        'web._assets_core': [
            'do_odoo_debranding/static/src/js/error_dialogs_modified.js',
        ],
    },
    'license': "AGPL-3",
    'installable': True,
    'application': True,
}
