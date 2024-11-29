# -*- coding: utf-8 -*-
{
    'name': 'ChatBot',
    'version': '17.0',
    'author': 'Do Incredible',
    'company': 'Do Incredible',
    'maintainer': 'Do Incredible',
    'website': 'http://doincredible.com',
    'license': 'OPL-1',
    'category': 'Chatbot',
    'summary': '''
        ChatBot
    ''',
    'depends': ['website'],
    "external_dependencies": {
        "python": [
            'numpy',
            'torch',
            'nltk',
            'autocorrect'
        ],
    },
    'data':[
        'data/chatboat_data.xml',
        'security/ir.model.access.csv',
        'views/website_layout_inherit.xml',
        'views/chatbot_chatbot_view.xml',
        'views/tag_view.xml',
    ],

    'assets': {
        'web.assets_frontend': [
            'do_website_chatbot/static/src/css/chatbot.scss',
            'do_website_chatbot/static/src/js/chatbot.js',
        ],
    },
    'installable': True,
    'images': ['static/description/banner.png'],
    'price': 100,
    'currency': 'EUR',
}
