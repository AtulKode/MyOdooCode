odoo.define('do_pos_virtual_keyBoard.TextAreaPopup', function(require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const TextAreaPopup = require('point_of_sale.TextAreaPopup');
    const keyboard = require('do_pos_virtual_keyBoard.OnscreenKeyboardSimple');

    const ResTextAreaPopup = TextAreaPopup =>
        class extends TextAreaPopup {
            constructor() {
                super(...arguments);
            }
            _onClickProductSearch(event) {
                if(this.env.pos.config.iface_vkeyboard){
                    keyboard.prototype.connect(event.currentTarget);
                }
            }

        };
    Registries.Component.extend(TextAreaPopup, ResTextAreaPopup);
    return TextAreaPopup;
});