odoo.define('pos_customer_note.PosOrderDate', function(require){
	"use strict";
	const PosComponent = require("point_of_sale.PosComponent");
	const ProductScreen = require('point_of_sale.ProductScreen');
	const Registries = require('point_of_sale.Registries');
	const { useListener } = require("@web/core/utils/hooks");

	const CustomDatePopup = require("pos_customer_note.CustomDatePopup");

	class PosOrderDate extends PosComponent{

		setup(){
        	super.setup();
        	useListener('click', this.onClick);
        }

        async onClick() {

            const { confirmed, payload } = await this.showPopup('CustomDatePopup', {
			        title: "Select Date",
			    });


		    if (confirmed) {
		        console.log("Selected Date:", payload);
		    }
        }

	}
	PosOrderDate.template = 'PosOrderDate';
	ProductScreen.addControlButton({
		component : PosOrderDate,
		condition : function(){
			return ! this.env.pos.config.pos_config_date;
		},
		position : ['before', 'RefundButton'],
	});


	Registries.Component.add(PosOrderDate);
	return PosOrderDate;

});