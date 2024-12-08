/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { useBarcodeReader } from "@point_of_sale/app/barcode/barcode_reader_hook";
import { patch } from "@web/core/utils/patch";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

patch(ProductScreen.prototype, {
getNumpadButtons() {
    return [
        { value: "1" },
        { value: "2" },
        { value: "3" },
        { value: "quantity", text: _t("Qty"), class: "btn-blue" },
        { value: "4" },
        { value: "5" },
        { value: "6" },
        { value: "discount", text: _t("% Disc"), disabled: !this.pos.config.manual_discount, class: "btn-orange" },
        { value: "7" },
        { value: "8" },
        { value: "9" },
        {
            value: "price",
            text: _t("Price"),
            disabled: !this.pos.cashierHasPriceControlRights(),
            class: "btn-green",
        },
        { value: "-", text: "+/-", class: "btn-gray" },
        { value: "0" },
        { value: this.env.services.localization.decimalPoint },
        // Unicode: https://www.compart.com/en/unicode/U+232B
        { value: "Backspace", text: "⌫", class: "btn-red" },
    ].map((button) => ({
        ...button,
        class: `${button.class || ""} ${this.pos.numpadMode === button.value ? "active border-primary" : ""}`.trim(),
    }));
},
});
