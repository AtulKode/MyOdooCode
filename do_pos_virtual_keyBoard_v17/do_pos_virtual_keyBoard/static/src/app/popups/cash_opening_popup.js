
/** @odoo-module **/
import { OnscreenKeyboardSimple } from "@do_pos_virtual_keyBoard/app/screens/productscreen/onscreenkeyboard";
import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { CashOpeningPopup } from "@point_of_sale/app/store/cash_opening_popup/cash_opening_popup";


patch(CashOpeningPopup.prototype, {
    /**
     * Needs to be set to true to show the loyalty points in the partner list.
     * @override
     */
    setup() {
        super.setup(...arguments);
      },

    _onClickProductSearch(event) {
        ;
        if(this.pos.config.iface_vkeyboard){

            OnscreenKeyboardSimple.prototype.connect(event.currentTarget);
        }
    },
});
