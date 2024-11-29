/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";
import { CategorySelector } from "@point_of_sale/app/generic_components/category_selector/category_selector";
import { Component, useState} from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class SortProduct extends Component {
    static template = "do_pos_product_sort.SortProduct";

    setup() {
        this.pos = usePos();
        this.popup = useService("popup");
        this.currentFilter = this.pos.config.default_filter; 
        this.pos.config.user_selected_filter = this.currentFilter;
        const filterOptions = {
            'default_order': 'Default Order',
            'most_sold': 'Most Sold',
            'new_arrivals': 'New Arrivals',
            'price_asc': 'Price ASC',
            'price_desc': 'Price DESC',
            'name_asc': 'Name ASC',
            'name_desc': 'Name DESC',
            'least_sold': 'Least Sold'
        };
        this.state = useState({
            selectedFilterLabel : filterOptions[this.pos.config.default_filter],
        });
    }

    async sortBy() {
        const select = [
            {
                id: 1,
                label: _t("Default Order"),
                item: "default_order",
                isSelected: this.currentFilter === "default_order",
            },
            {
                id: 2,
                label: _t("Most Sold"),
                item: "most_sold",
                isSelected: this.currentFilter === "most_sold",
            },
            {
                id: 3,
                label: _t("New Arrivals"),
                item: "new_arrivals",
                isSelected: this.currentFilter === "new_arrivals",
            },
            {
                id: 4,
                label: _t("Price ASC"),
                item: "price_asc",
                isSelected: this.currentFilter === "price_asc",
            },
            {
                id: 5,
                label: _t("Price DESC"),
                item: "price_desc",
                isSelected: this.currentFilter === "price_desc",
            },
            {
                id: 6,
                label: _t("Name ASC"),
                item: "name_asc",
                isSelected: this.currentFilter === "name_asc",
            },
            {
                id: 7,
                label: _t("Name DESC"),
                item: "name_desc",
                isSelected: this.currentFilter === "name_desc",
            },
            {
                id: 8,
                label: _t("Least Sold"),
                item: "least_sold",
                isSelected: this.currentFilter === "least_sold",
            },
        ];
        const { confirmed, payload: selectedFilter } = await this.popup.add(
            SelectionPopup,
            {
                title: _t("Select Option"),
                list: select,
            }
        );
        if (confirmed && selectedFilter) {
            this.pos.config.user_selected_filter = selectedFilter;
            this.currentFilter = selectedFilter;
            this.state.selectedFilterLabel = select.find(option => option.item === selectedFilter)?.label || null;
        }
    }
}
CategorySelector.components = { SortProduct };