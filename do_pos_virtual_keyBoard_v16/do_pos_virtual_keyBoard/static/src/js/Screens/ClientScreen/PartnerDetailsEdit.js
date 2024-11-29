odoo.define('do_pos_virtual_keyBoard.PartnerDetailsEdit', function(require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const PartnerDetailsEdit = require('point_of_sale.PartnerDetailsEdit');
    const keyboard = require('do_pos_virtual_keyBoard.OnscreenKeyboardSimple');

    const ResClientDetailsEdit = PartnerDetailsEdit =>
        class extends PartnerDetailsEdit {
            constructor() {
                super(...arguments);
            }
            _onClickProductSearch(event) {
                if(this.env.pos.config.iface_vkeyboard){
                    keyboard.prototype.connect(event.currentTarget);
                }
            }

        };
    Registries.Component.extend(PartnerDetailsEdit, ResClientDetailsEdit);
    return PartnerDetailsEdit;
});