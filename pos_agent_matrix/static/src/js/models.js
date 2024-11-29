odoo.define('pos_agent_matrix.models', function (require) {
"use strict";


var { PosGlobalState } = require('point_of_sale.models');
const Registries = require('point_of_sale.Registries');
var { Orderline } = require('point_of_sale.models');

const NewPosGlobalState = (PosGlobalState) => class NewPosGlobalState extends PosGlobalState {
   async _processData(loadedData) {
  
 await super._processData(...arguments);
 if(this.env.pos.config.is_agent){
   this.product_agent = loadedData['agent.model'];

 }
  
 }
}
Registries.Model.extend(PosGlobalState, NewPosGlobalState);



const PosAgentOrderline = (Orderline) => class PosAgentOrderline extends Orderline {
  constructor(obj, options) {
      super(...arguments);
      this.agent_id = "";
      this.date = new Date() || '';
  }
  init_from_JSON(json) {
      super.init_from_JSON(...arguments);
      this.agent_id =  json.agent_id;
      this.date = json.date;
      alert("init_from_JSONthis.date",this.date)
    
  }
  export_as_JSON() {
      const json = super.export_as_JSON(...arguments);
      json.agent_id =  this.agent_id;
      json.date = this.date;
      alert("export_as_JSON.date",json.date)
      return json;
  }

  export_for_printing() {
    var json = super.export_for_printing(...arguments);
    json.agent_id =  this.agent_id;
    json.date = this.date;
    return json;
  }

}


Registries.Model.extend(Orderline, PosAgentOrderline);
});