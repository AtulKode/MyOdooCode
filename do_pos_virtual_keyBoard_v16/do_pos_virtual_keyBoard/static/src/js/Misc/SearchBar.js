odoo.define('do_pos_virtual_keyBoard.SearchBar', function(require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const SearchBar = require('point_of_sale.SearchBar');
    // alert(SearchBar);
    const keyboard = require('do_pos_virtual_keyBoard.OnscreenKeyboardSimple');
    
    const ResSearchBar = SearchBar =>
        class extends SearchBar {
            constructor() {
                super(...arguments);
            }
            _onClickProductSearch(event) {
                if(this.env.pos.config.iface_vkeyboard){
                    keyboard.prototype.connect(event.currentTarget);
                }
            }

        };
    Registries.Component.extend(SearchBar, ResSearchBar);
    return SearchBar;
});