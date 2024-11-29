odoo.define('pos_agent_matrix.CustomAgentPopup', function (require) {
    'use strict';

    
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    const {useState} = owl;
    
    const { _lt } = require('@web/core/l10n/translation');
 

    class CustomAgentPopup extends AbstractAwaitablePopup {
        setup() {
            super.setup();
            this.state = useState({
                dt: '',
            });
        }
        


        async confirm() {
            const currentDate = new Date();
            const dateInputValue = $("#dateInput").val();
            const agent_name = $("#agent-detail").val();


            if (dateInputValue && agent_name) {
                const selectedDate = new Date(dateInputValue);

                if (isNaN(selectedDate.getTime())) {
                    
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('User error'),
                        body: this.env._t('Please select a valid date.'),
                    });
                } else if (selectedDate < currentDate) {
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('User error'),
                        body: this.env._t('Please select a date greater than yesterday.'),
                    });
                } else {
                    super.confirm();
                }
            } else {
                this.showPopup('ErrorPopup', {
                    title: this.env._t('User error'),
                    body: this.env._t('Please select both date and agent.'),
                });
            }
        }


        getPayload() {
            const dateInputValue = $("#dateInput").val();
            const agent_name = $("#agent-detail").val();
            

            return {dateInputValue,agent_name};
        }
    }
    
    CustomAgentPopup.template = 'CustomAgentPopup';
    CustomAgentPopup.defaultProps = {
        confirmText: _lt('Ok'),
        cancelText: _lt('Cancel'),
        title: _lt("select a date"),
        body: '',
    };

    Registries.Component.add(CustomAgentPopup);
    return CustomAgentPopup;
})

