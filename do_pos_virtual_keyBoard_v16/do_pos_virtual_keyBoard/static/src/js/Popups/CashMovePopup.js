odoo.define('do_pos_virtual_keyBoard.CashMovePopup', function(require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const CashMovePopup = require('point_of_sale.CashMovePopup');
    const keyboard = require('do_pos_virtual_keyBoard.OnscreenKeyboardSimple');

    const ResCashMovePopup = CashMovePopup =>
        class extends CashMovePopup {
            constructor() {
                super(...arguments);
            }
            _onClickProductSearch(event) {
                if(this.env.pos.config.iface_vkeyboard){
                    keyboard.prototype.connect(event.currentTarget);
                }
            }

        };
    Registries.Component.extend(CashMovePopup, ResCashMovePopup);
    return CashMovePopup;
});