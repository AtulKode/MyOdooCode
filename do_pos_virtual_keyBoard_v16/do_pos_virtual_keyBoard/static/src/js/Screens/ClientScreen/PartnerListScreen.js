odoo.define('do_pos_virtual_keyBoard.PartnerListScreen', function(require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const PartnerListScreen = require('point_of_sale.PartnerListScreen');
    const keyboard = require('do_pos_virtual_keyBoard.OnscreenKeyboardSimple');

    const ResClientListScreen = PartnerListScreen =>
        class extends PartnerListScreen {
            constructor() {
                super(...arguments);
            }
            _onClickProductSearch(event) {
                 if(this.env.pos.config.iface_vkeyboard){
                    keyboard.prototype.connect(event.currentTarget);
                }
            }

        };
    Registries.Component.extend(PartnerListScreen, ResClientListScreen);
    return PartnerListScreen;
});