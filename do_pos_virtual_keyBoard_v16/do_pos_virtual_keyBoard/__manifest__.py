# -*- encoding: utf-8 -*-
{
    'name': 'POS Virtual KeyBoard',
    'category': 'POS',
    'author': 'Do Incredible',
    'license': 'OPL-1',
    'sequence': '10',
    'summary': 'Use a virtual keyboard for touchscreens',
    'website': 'https://doincredible.com',
    'version': '1.0',
    'description': """
    Use a virtual keyboard for touchscreens
    """,
    'depends': [
        'point_of_sale'
    ],
    'data': [
        'views/pos_config_views.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'do_pos_virtual_keyBoard/static/src/css/keyboard.css',
            'do_pos_virtual_keyBoard/static/src/js/Screens/ProductScreen/OnscreenKeyboard.js',
            'do_pos_virtual_keyBoard/static/src/js/Screens/ProductScreen/ProductsWidgetControlPanel.js',
            'do_pos_virtual_keyBoard/static/src/js/Screens/ClientScreen/PartnerListScreen.js',
            'do_pos_virtual_keyBoard/static/src/js/Screens/ClientScreen/PartnerDetailsEdit.js',
            'do_pos_virtual_keyBoard/static/src/js/Popups/TextAreaPopup.js',
            'do_pos_virtual_keyBoard/static/src/js/Popups/ClosePosPopup.js',
            'do_pos_virtual_keyBoard/static/src/js/Popups/CashOpeningPopup.js',
            'do_pos_virtual_keyBoard/static/src/js/Misc/SearchBar.js',
            'do_pos_virtual_keyBoard/static/src/js/Popups/CashMovePopup.js',
            'do_pos_virtual_keyBoard/static/src/js/Popups/MoneyDetailsPopup.js',
            'do_pos_virtual_keyBoard/static/src/xml/**/*',
        ],
    },
    'installable': True,
    'application': True,
    'price': 50,
    'currency': 'USD',
    'images': ['static/description/images/1.png'],
    'live_test_url': '',
}
