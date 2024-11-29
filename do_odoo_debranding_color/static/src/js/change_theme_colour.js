/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";
import { onWillStart } from "@odoo/owl";
import { WebClient } from "@web/webclient/webclient";

patch(WebClient.prototype, {
    /**
     * @override
     */
    setup() {
        super.setup();
        this.orm = useService("orm");
        onWillStart(async () => {
            var data = await this.orm.call(
                "res.company",
                "get_color"
            ); 
            console.log("===color=",data)
            if (data.theme_color) {
                let root = document.documentElement;
                root.style.setProperty('--o-enterprise-color', data.theme_color);
            }        
        });

            
    }

});