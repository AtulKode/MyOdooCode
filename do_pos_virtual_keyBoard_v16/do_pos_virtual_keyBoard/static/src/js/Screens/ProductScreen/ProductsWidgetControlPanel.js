odoo.define('do_pos_virtual_keyBoard.ProductsWidgetControlPanel', function(require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const ProductsWidgetControlPanel = require('point_of_sale.ProductsWidgetControlPanel');
    const keyboard = require('do_pos_virtual_keyBoard.OnscreenKeyboardSimple');
    alert(keyboard);
    const ResProductsWidgetControlPanel = ProductsWidgetControlPanel =>
        class extends ProductsWidgetControlPanel {
            constructor() {
                super(...arguments);
            }
            _onClickProductSearch(event) {
                if (this.env.pos.config.iface_vkeyboard) {
                    console.log("ProductsWidgetControlPanel",keyboard);
                    keyboard.prototype.connect(event.currentTarget);
                }
            }

        };
    Registries.Component.extend(ProductsWidgetControlPanel, ResProductsWidgetControlPanel);
    return ProductsWidgetControlPanel;
});