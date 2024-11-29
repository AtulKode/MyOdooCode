odoo.define('do_pos_virtual_keyBoard.CashOpeningPopup', function(require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const CashOpeningPopup = require('point_of_sale.CashOpeningPopup');
    const keyboard = require('do_pos_virtual_keyBoard.OnscreenKeyboardSimple');

    const ResCashOpeningPopup = CashOpeningPopup =>
        class extends CashOpeningPopup {
            constructor() {
                super(...arguments);
            }
            _onClickProductSearch(event) {
                if(this.env.pos.config.iface_vkeyboard){
                    keyboard.prototype.connect(event.currentTarget);
                }
            }

        };
    Registries.Component.extend(CashOpeningPopup, ResCashOpeningPopup);
    return CashOpeningPopup;
});