odoo.define('pos_agent_matrix.ProductScreen', function (require) {
    'use strict';

    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');
    const useListener  = require("@web/core/utils/hooks");
    const CustomAgentPopup = require("pos_agent_matrix.CustomAgentPopup");
    var AgentModel = require('point_of_sale.models');

    const PosAgentProductScreen = (ProductScreen) =>
        class extends ProductScreen {
            setup() {
                super.setup();
            }

            get selectedOrder() {
                return this.env.pos.get_order().get_selected_orderline();

            }

        async _clickProduct(event) {
            
            const new_product = event.detail;
            

            // if(!this.selectedOrder) return;
            if (this.env.pos.config.is_agent && new_product.is_service_agent){
                const { confirmed, payload :inputNote} = await this.showPopup('CustomAgentPopup');

                await super._clickProduct(...arguments);
                if (confirmed) {
                     
                     const startingValue = this.selectedOrder;
                     startingValue.agent_id = inputNote['agent_name'];
                     startingValue.date = inputNote['dateInputValue'];
                     console.log("SDDFSd",startingValue)
                }

            }
            await super._clickProduct(...arguments);
            }
        };

    Registries.Component.extend(ProductScreen, PosAgentProductScreen);
});
