odoo.define('do_pos_virtual_keyBoard.ClosePosPopup', function(require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const ClosePosPopup = require('point_of_sale.ClosePosPopup');
    const keyboard = require('do_pos_virtual_keyBoard.OnscreenKeyboardSimple');

    const ResClosePosPopup = ClosePosPopup =>
        class extends ClosePosPopup {
            constructor() {
                super(...arguments);
            }
            _onClickProductSearch(event) {
                if(this.env.pos.config.iface_vkeyboard){
                    keyboard.prototype.connect(event.currentTarget);
                }
            }

        };
    Registries.Component.extend(ClosePosPopup, ResClosePosPopup);
    return ClosePosPopup;
});