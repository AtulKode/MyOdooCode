/** @odoo-module */

import { Order, Orderline, Payment} from "@point_of_sale/app/store/models";
import { roundPrecision as round_pr } from "@web/core/utils/numbers";
import { patch } from "@web/core/utils/patch";

patch(Order.prototype, {
    setup() {
        super.setup(...arguments);
		this.total_bank_charge = this.total_bank_charge || 0;
    },

  	set_bnk_chrg (charge) {
		this.total_bank_charge = charge
	},

    get_total_bank_charge() {
        return round_pr(
            this.paymentlines.reduce((sum, paymentLine) => {
                if (paymentLine.is_done() && paymentLine.payment_method.is_bank_charge) {
                    sum += paymentLine.get_curamount();
                }
                return sum;
            }, 0),
            this.pos.currency.rounding
        );
    },


    get_total_without_tax() {
        return round_pr(
            this.orderlines.reduce((sum, orderLine) => {
                return sum + (orderLine.is_bankCharge ? 0 : orderLine.get_price_without_tax());
            }, 0),
            this.pos.currency.rounding
        );
    },


    get_total_with_tax() {
        return round_pr(
            this.orderlines.reduce((sum, orderLine) => {
                return sum + (orderLine.is_bankCharge ? 0 : orderLine.get_price_with_tax());
            }, 0),
            this.pos.currency.rounding
        );
    },

    add_paymentline(payment_method) {
        this.assert_editable();
        if (this.electronic_payment_in_progress()) {
            return false;
        } else {
            var bank_charge_prod_id = this.pos.db.product_by_id[payment_method.bank_charge_prod_id[0]];

            if(payment_method.is_bank_charge == true){

                if(bank_charge_prod_id){


		            var newPaymentline = new Payment(
		                { env: this.env },
		                { order: this, payment_method: payment_method, pos: this.pos }
		            );


		            this.paymentlines.add(newPaymentline);
		            this.select_paymentline(newPaymentline);
		            if (this.pos.config.cash_rounding) {
		                this.selected_paymentline.set_amount(0);
		            }
		            newPaymentline.set_amount(this.get_due());

		            if (payment_method.payment_terminal) {
		                newPaymentline.set_payment_status("pending");
		            }

		            let orderlines = this.get_orderlines()

                    if(orderlines){
                        const result = orderlines.filter(isBankCharge);

                        function isBankCharge(line) {
                          	return line.is_bankCharge == true;
                        }
                        if(result.length == 0){
                            var line = new Orderline({}, {pos: this.pos, order: this, product: bank_charge_prod_id});            
                            line.set_is_bankCharge(true)
                            line.set_quantity(1)
                            this.orderlines.add(line);
                        }
                    } 

		            return newPaymentline;	
                }else{
                	return false
                }
            }else{
		            var newPaymentline = new Payment(
		                { env: this.env },
		                { order: this, payment_method: payment_method, pos: this.pos }
		            );
		            this.paymentlines.add(newPaymentline);
		            this.select_paymentline(newPaymentline);
		            if (this.pos.config.cash_rounding) {
		                this.selected_paymentline.set_amount(0);
		            }
		            newPaymentline.set_amount(this.get_due());

		            if (payment_method.payment_terminal) {
		                newPaymentline.set_payment_status("pending");
		            }
	            return newPaymentline;
            }

            
        }
    },
    
    //@override
    export_for_printing() {
        const result = super.export_for_printing(...arguments);
        result.total_bank_charge = this.total_bank_charge;
        return result;
    },

    //@override  	
	init_from_JSON(json) {
		super.init_from_JSON(...arguments);
		this.total_bank_charge = json.total_bank_charge;
	},

    //@override
	export_as_JSON() {
		const json = super.export_as_JSON(...arguments);
		json.total_bank_charge = this.total_bank_charge;
		return json;
	},
});
patch(Orderline.prototype, {
    setup() {
        super.setup(...arguments);
		this.is_bankCharge = this.is_bankCharge || false;
    },
    set_is_bankCharge(is_bankCharge){
		this.is_bankCharge = is_bankCharge;
	},

    //@override
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.is_bankCharge = this.is_bankCharge || false;
        return json;
    },

    //@override
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.is_bankCharge = json.is_bankCharge ||false;
    },

    //@override
    export_for_printing() {
        const json = super.export_for_printing(...arguments);
        json.is_bankCharge = this.is_bankCharge || false;
        return json;
    },
});
patch(Payment.prototype, {
    setup() {
        super.setup(...arguments);
            this.currency_amount = this.currency_amount || 0.0;
    },
    
    set_curamount(currency_amount){
		this.currency_amount = currency_amount;
	},
	
	get_curamount() {
		return this.currency_amount
	},


    //@override
    init_from_JSON(json){
        super.init_from_JSON(...arguments);
        this.currency_amount = json.currency_amount || 0.0;
    },

    //@override
    export_as_JSON(){
        const json = super.export_as_JSON(...arguments);
        json.currency_amount = this.currency_amount || 0.0;
        return json;
    },

    //@override
    export_for_printing() {
        const json = super.export_for_printing(...arguments);
        json.currency_amount = this.currency_amount || 0.0;
        return json;
    },
});
