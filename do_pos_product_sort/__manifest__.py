# -*- coding: utf-8 -*-
{
    'name': 'POS Product Sort',
    'version': '17.0.0.0',
    'category': 'Point of Sale/Products',
    'sequence': 1,
    'author': 'Do Incredible',
    'website': 'https://doincredible.com/',
    'summary': 'Pos Product Sort',
    'description': """
We have added various filter functionalities in Point of Sale, allowing users to sort and view products by their sales volume, new arrivals, price in ascending or descending order, and name in ascending or descending order, as well as filter by the least sold items.
""",
    'depends': ['point_of_sale'],
    'data': [
        "security/ir.model.access.csv",
        "views/res_config_setting_view_from.xml",
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'do_pos_product_sort/static/src/app/xml/sort_product.xml',
            'do_pos_product_sort/static/src/app/xml/product_filter_button.xml',
            'do_pos_product_sort/static/src/app/js/product_list_screen.js',
            'do_pos_product_sort/static/src/app/js/product_filter_button.js',
        ],
    },
    'installable': True,
    'license': 'LGPL-3',
}
