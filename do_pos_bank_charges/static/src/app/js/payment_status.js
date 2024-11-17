/** @odoo-module */


import { PaymentScreenStatus } from "@point_of_sale/app/screens/payment_screen/payment_status/payment_status";
import { patch } from "@web/core/utils/patch";

patch(PaymentScreenStatus.prototype, {
    get totalBankCharge() {
    	var totalBankChargeAmt = this.props.order.get_total_bank_charge()
    	let orderlines = this.props.order.get_orderlines()


        if(orderlines){
            const result = orderlines.filter(isBankCharge);

            function isBankCharge(line) {
              	return line.is_bankCharge == true;
            }

            if(!this.props.order.finalized){
                if(result.length > 0){
                    result[0].set_unit_price(totalBankChargeAmt)
                    result[0].price_manually_set = true;
                }
            }
        }
        return this.env.utils.formatCurrency(totalBankChargeAmt);
    },

    get allTheTotal(){
        let total = this.props.order.get_total_with_tax() - this.props.order.get_total_bank_charge()
        return this.env.utils.formatCurrency(total)
    },	
});