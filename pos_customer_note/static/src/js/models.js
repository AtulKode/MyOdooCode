odoo.define('pos_customer_note.models', function (require) {
  "use strict";
  const {Order} = require('point_of_sale.models');
  
   const Registries = require('point_of_sale.Registries');

 

  const MyOrder = (Order) => class MyOrder extends Order {
         constructor(obj, options) {
            super(...arguments);
            this.customerNotedata = "";
         }
     

   export_for_printing() {
      const result = super.export_for_printing(...arguments);
      result.pos_customer_note = this.get_customer_note_data();
      return result;
    }

   init_from_JSON(json) {
      super.init_from_JSON(...arguments);
      this.set_customer_note_data(json.pos_customer_note);
    }

    export_as_JSON(){
      const json = super.export_as_JSON(...arguments);
      json.pos_customer_note = this.get_customer_note_data();
      return json;
    }

    set_customer_note_data(note){
      this.customerNotedata = note;
    }

    get_customer_note_data(){
      return this.customerNotedata;
    }
 }
   Registries.Model.extend(Order, MyOrder);
});
