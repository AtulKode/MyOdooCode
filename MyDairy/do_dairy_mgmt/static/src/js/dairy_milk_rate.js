/** @odoo-module **/

import { registry } from "@web/core/registry";
import { session } from "@web/session";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, useState} from  "@odoo/owl";
import { View } from "@web/views/view";

class DairyKioskView extends Component {
    setup(){
        this.orm = useService("orm");
        this.rpc = useService("rpc");
        this.current_date = new Date().toLocaleString();
        this.actionService = useService("action");
        this.session = session;
        this.user = session.name;
        this.resModel = this.props.action.context.resModel; 
        this.resId = this.props.action.context.active_id || false;
        this.selected_dairy_id = this.props.action.context.dairy_id;
        this.mydairy = this.props.action.context.dairy;
        this.myAnimal = this.props.action.context.animals;
        this.customers = [];
        this.formViewId = false;
        this.state = useState({
            view: "", 
            displayNote: false,
        });

        onWillStart(async () => {
            await this.fetchCustomers();
        });
    }

    exit(ev) {
        this.env.config.historyBack();
    }

    async startIntake() {
        var animalDictionary = {};
        $('.animal-rate').each(function() {
            var animal = $(this).find('h3').text().trim();
            var rate = parseFloat($(this).find('input').val().trim());
            if (animal && !isNaN(rate)) {
                animalDictionary[animal] = rate;
            }
        });

        this.rpc('/update_rate_management', {
            dairy_id: this.selected_dairy_id,
            animal_rates: animalDictionary,
        });
        this.state.view = "IntakeFormView";

        const cusData = await this.rpc(
            '/milk_intake_management/get_customer_data',
            { model: this.resModel, res_id: this.resId }
        );
        this.formViewId = cusData.data;
    }

    get IntakeFormViewProps() {
        $('.card-container').hide();
        return {
            resId: this.resId,
            resModel: "milk.intake.management",
            context: {default_milk_dairy_id : this.selected_dairy_id},
            display: {controlPanel: true},
            viewId: this.formViewId,
            mode: "edit",
            type: "form",
        };
    }

    async fetchCustomers() {
        try {
            const customers = await this.orm.call(
                'customer.registration', 
                'get_customers_for_dairy', 
                [this.selected_dairy_id] 
            );
            this.customers = customers;
        } catch (error) {
            console.error('Error fetching customers:', error);
        }
    } 
}

DairyKioskView.template = "do_dairy_mgmt.dairyview";
DairyKioskView.components = {
    View,
};

registry.category("actions").add("do_dairy_mgmt.DairyKioskView", DairyKioskView);
export default DairyKioskView;