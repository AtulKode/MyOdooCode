odoo.define('pos_customer_note.CustomDatePopup', function (require) {
    'use strict';

    
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    const { DatePicker} = require('web.DatePickerOwl');
    const {useState} = owl;
    const { _lt } = require('@web/core/l10n/translation');
 
    class CustomDatePopup extends AbstractAwaitablePopup {
        setup() {
            super.setup();
            this.state = useState({
                dt: "",
            });
        }

        getPayload() {
            return this.state.dt;
        }
    }
    
    CustomDatePopup.template = 'SelectDatePopup';
    CustomDatePopup.defaultProps = {
        confirmText: _lt('Ok'),
        cancelText: _lt('Cancel'),
        title: _lt('Confirm ?'),
        body: '',
    };

    Registries.Component.add(CustomDatePopup);
    return CustomDatePopup;
});

