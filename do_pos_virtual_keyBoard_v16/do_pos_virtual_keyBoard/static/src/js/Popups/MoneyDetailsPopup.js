odoo.define('do_pos_virtual_keyBoard.MoneyDetailsPopup', function(require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const MoneyDetailsPopup = require('point_of_sale.MoneyDetailsPopup');
    const keyboard = require('do_pos_virtual_keyBoard.OnscreenKeyboardSimple');

    const ResMoneyDetailsPopup = MoneyDetailsPopup =>
        class extends MoneyDetailsPopup {
            constructor() {
                super(...arguments);
            }
            _onClickProductSearch(event) {
                if(this.env.pos.config.iface_vkeyboard){
                    keyboard.prototype.connect(event.currentTarget);
                }
            }

        };
    Registries.Component.extend(MoneyDetailsPopup, ResMoneyDetailsPopup);
    return MoneyDetailsPopup;
});