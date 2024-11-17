/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { ConfirmPopup } from "@point_of_sale/app/utils/confirm_popup/confirm_popup";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";

patch(PaymentScreen.prototype, {
    async click_back(){
        let self = this;

        let orderlines = this.currentOrder.get_orderlines()

        if(orderlines){
            const result = orderlines.filter(isBankCharge);
            function isBankCharge(line) {
                return line.is_bankCharge == true;
            }

            if(result.length > 0){
                const { confirmed } = await this.popup.add(ConfirmPopup, {
                    title: _t('Cancel Payment ?'),
                    body: _t('If you go back to product screen bank charge line will be remove'),
                });
                if (confirmed) {
                    const BnkPayment = this.paymentLines.filter(isBankChargePayment);

                    function isBankChargePayment(line) {
                        self.currentOrder.remove_paymentline(line)
                    }
                    
                    this.currentOrder.removeOrderline(result[0])
                    self.pos.showScreen('ProductScreen');
                }
            }else{
                self.pos.showScreen('ProductScreen');
            }
        }
    },

    /**
     * @override
     */
    deletePaymentLine(cid) {
        super.deletePaymentLine(cid)

        let orderlines = this.currentOrder.get_orderlines()
        if(this.paymentLines.length == 0){
            if(orderlines){
                const result = orderlines.filter(isBankCharge);
                function isBankCharge(line) {
                    return line.is_bankCharge == true;
                }
                if(result.length > 0){
                    this.currentOrder.removeOrderline(result[0])
                }
            }
        }else{
            const BnkPayment = this.paymentLines.filter(isBankChargePayment);
            function isBankChargePayment(line) {
                return line.payment_method.is_bank_charge == true
            }
            if(BnkPayment.length == 0){
                const result = orderlines.filter(isBankCharge);

                function isBankCharge(line) {
                    return line.is_bankCharge == true;
                }

                if(result.length > 0){
                    this.currentOrder.removeOrderline(result[0])
                }
            }
        }
    },

    /**
     * @override
     */  
    updateSelectedPaymentline(amount = false) {
        if (this.paymentLines.every((line) => line.paid)) {
            this.currentOrder.add_paymentline(this.payment_methods_from_config[0]);
        }
        if (!this.selectedPaymentLine) {
            return;
        } // do nothing if no selected payment line
        if (amount === false) {
            if (this.numberBuffer.get() === null) {
                amount = null;
            } else if (this.numberBuffer.get() === "") {
                amount = 0;
            } else {
                amount = this.numberBuffer.getFloat();
            }
        }
        // disable changing amount on paymentlines with running or done payments on a payment terminal
        const payment_terminal = this.selectedPaymentLine.payment_method.payment_terminal;
        const hasCashPaymentMethod = this.payment_methods_from_config.some(
            (method) => method.type === "cash"
        );
        if (
            !hasCashPaymentMethod &&
            amount > this.currentOrder.get_due() + this.selectedPaymentLine.amount
        ) {
            this.selectedPaymentLine.set_amount(0);
            this.numberBuffer.set(this.currentOrder.get_due().toString());
            amount = this.currentOrder.get_due();
            this.showMaxValueError();
        }
        if (
            payment_terminal &&
            !["pending", "retry"].includes(this.selectedPaymentLine.get_payment_status())
        ) {
            return;
        }
        if (amount === null) {
            this.deletePaymentLine(this.selectedPaymentLine.cid);
        } else {
            this.selectedPaymentLine.set_amount(amount);
            var pay_method = this.selectedPaymentLine.payment_method
            if (pay_method.cahrges_type == "percentage"){

                var bank_charge_amount = ((pay_method.cahrges_amount * amount)/100)
                this.selectedPaymentLine.set_curamount(bank_charge_amount);
                
            }            
        }
    },
    //@Override
    async _finalizeValidation() {
        await this.currentOrder.set_bnk_chrg(await this.currentOrder.get_total_bank_charge());
        super._finalizeValidation();        
    },

    /**
     * @override
     */
    addNewPaymentLine(paymentMethod) {
        const result = this.currentOrder.add_paymentline(paymentMethod);
        if (!this.pos.get_order().check_paymentlines_rounding()) {
            this._display_popup_error_paymentlines_rounding();
        }
        if (result) {
            if (paymentMethod.cahrges_type == "percentage"){
                var bank_amount = result.get_amount()

                var bank_charge_amount = ((paymentMethod.cahrges_amount * bank_amount)/100)
                this.selectedPaymentLine.set_curamount(bank_charge_amount);
                var order = this.pos.get_order()
            }            
            this.numberBuffer.reset();
            return true;
        }
        else {
            this.popup.add(ErrorPopup, {
                title: _t("Error"),
                body: _t("There is already an electronic payment in progress."),
            });
            return false;
        }   
     },

});
