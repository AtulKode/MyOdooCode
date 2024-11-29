odoo.define('pos_customer_note.CustomerNoteButton', function(require){
	'use strict';
	const PosComponent = require('point_of_sale.PosComponent');
	const ProductScreen = require('point_of_sale.ProductScreen');
	const Registries = require('point_of_sale.Registries');
	const { useListener } = require("@web/core/utils/hooks");

	class CustomerNoteButton extends PosComponent{

        setup(){
        	super.setup();
        	useListener('click', this.onClick);
        }

        get selectedOrder() {
            return this.env.pos.get_order()
        }
        async onClick() {
            if (!this.selectedOrder) return;
            console.log("this.selectedOrder.get_customer_note_data()",this.selectedOrder.get_customer_note_data());
            const { confirmed, payload: inputNote } = await this.showPopup('TextAreaPopup', {
                startingValue: this.selectedOrder.get_customer_note_data(),
                title: this.env._t('Add Note'),
            });

            if (confirmed) {
                this.selectedOrder.set_customer_note_data(inputNote);
            }
        }

	}

	CustomerNoteButton.template = 'CustomerNoteButton';

	ProductScreen.addControlButton({
		component : CustomerNoteButton,
		condition : function(){
			return ! this.env.pos.config.customer_note_config;
		},
		position : ['after', 'RefundButton'],
	});


	Registries.Component.add(CustomerNoteButton);
	return CustomerNoteButton;

});



        // _onDateChange(event) {
        //     this.state.selectedDate = new Date(event.target.value);
        // }