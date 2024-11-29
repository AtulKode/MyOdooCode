/** @odoo-module */

import { ProductsWidget } from "@point_of_sale/app/screens/product_screen/product_list/product_list";
import { patch } from "@web/core/utils/patch"
import { useService } from "@web/core/utils/hooks";
import { onWillStart } from "@odoo/owl";
import { CategorySelector } from "@point_of_sale/app/generic_components/category_selector/category_selector";
import { usePos } from "@point_of_sale/app/store/pos_hook";

patch(CategorySelector.prototype, {
        setup() {
        super.setup(...arguments);
        this.pos = usePos();
        this.show_prod_filter = this.pos.config.show_prod_filter;
    }
});

patch(ProductsWidget.prototype, {
    setup() {
        super.setup(...arguments);
        this.orm = useService("orm");

        onWillStart(async () => {
            this.product_ids = await this.orm.call(
                "do.pos.product.sold", 
                "search_read",
                [],
                {
                	fields: ["product_id"],
            	}
            );
            var most_sales_prod_ids = [];
            this.product_ids.forEach((prod) => { 
                most_sales_prod_ids.push(prod.product_id[0]);
            });
            this.most_sales_prod_ids = most_sales_prod_ids;
        });
    },

    get productsToDisplay() {
    	let user_filter = this.pos.config.user_selected_filter || this.pos.config.default_filter;
        let new_list = super.productsToDisplay;
        if (user_filter === "price_desc"){
        	return new_list.sort((a, b) => b.lst_price - a.lst_price);
        }
        else if(user_filter === "price_asc"){
        	return new_list.sort((a, b) => a.lst_price - b.lst_price);
        }
        else if(user_filter === "name_desc"){
        	return new_list.sort((a, b) => b.display_name.localeCompare(a.display_name));
        }
        else if(user_filter === "name_asc"){
            return new_list.sort((a, b) => a.display_name.localeCompare(b.display_name));
        }
        else if(user_filter === "new_arrivals"){
        	return new_list.sort((a, b) => new Date(b.create_date) - new Date(a.create_date));
        }
        else if(user_filter === "most_sold"){
            const sortedList = [];
            var new_list_by_id = {};
            new_list.forEach((prod) => {
                new_list_by_id[prod.id] = prod;
            });
            this.most_sales_prod_ids.forEach((prod_id) => {
                var prod = new_list_by_id[prod_id];
                if (prod) {
                    sortedList.push(prod);
                }
            });
        	return sortedList;
        }
        else if(user_filter === "least_sold"){
            const sortedList = [];
            var new_list_by_id = {};
            new_list.forEach((prod) => {
                new_list_by_id[prod.id] = prod;
            });
            this.most_sales_prod_ids.forEach((prod_id) => {
                var prod = new_list_by_id[prod_id];
                if (prod) {
                    sortedList.push(prod);
                }
            });
            return sortedList.reverse();            
        }
        else{
        	return new_list;
        }  
    },
});
