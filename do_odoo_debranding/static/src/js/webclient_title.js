/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { WebClient } from "@web/webclient/webclient";
import { onWillStart } from "@odoo/owl";

patch(WebClient.prototype, {
    setup() {
    	super.setup();
    	this.orm = useService("orm");
        onWillStart(async () =>{
		const webaction = await this.orm.call('website', 'search_read', [],{limit : 1});
		const company = webaction[0]['company_name'];
        this.title.setParts({ zopenerp: company && company || ''});   
        });
    }
});