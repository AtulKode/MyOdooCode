/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { BarcodeScanner } from "@barcodes/components/barcode_scanner";
import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useBus, useService } from "@web/core/utils/hooks";
import { FormController } from "@web/views/form/form_controller";

export class BarcodeScannerView extends Component {

    setup() {
        alert("Dssssssssssss");
        this.notification = useService("notification");
        this.orm = useService("orm");
        this.rpc = useService("rpc");
        const { default_event_id, active_model, active_id } = this.props.action.context;
        this.eventId = default_event_id || (active_model === "stock.picking" && active_id);
        this.isMultiEvent = !this.eventId;
        const barcode = useService("barcode");
        useBus(barcode.bus, "barcode_scanned", (ev) => this.onBarcodeScanned(ev.detail.barcode));

        onWillStart(this.onWillStart);
    }

    /**
     * @override
     * Fetch barcode init information. Notably eventId triggers mono- or multi-
     * event mode (Registration Desk in multi event allow to manage attendees
     * from several events and tickets without reloading / changing event in UX.
     */
    async onWillStart() {
        this.data = await this.rpc("/event/init_barcode_interface", {
            event_id: this.eventId,
        });
    }

    async onBarcodeScanned(barcode) {
        const result = await this.orm.call("stock.picking", "onchange_product_barcode_scan", [], {
            barcode: barcode,
           
        });
        console.log("sssssssssssssssssss",result);
        if (result.warning) {
           if (fields === '_barcode_scanned' || fields === 'product_barcode_scan') {
             if (result.warning.title === "Successfully Added") {
                this.displayNotification({
                 type: 'success',
                 title: _t(result.warning.title),
                 message: _t(result.warning.message),
                 sticky: false
               });
               // this.__parentedParent.saveRecord();
             } else {
               this.displayNotification({
                 type: 'warning',
                 title: _t(result.warning.title),
                 message: _t(result.warning.message),
                 sticky: false
               });
               $('body').append('<audio src="/do_stock_barcode/static/src/sounds/error.wav" autoplay="true"></audio>');
             }
           } else {
             $('.o_notification_manager').removeClass('success');
             $('.o_notification_manager').removeClass('notification_center');
             this.trigger_up('warning', result.warning);
             record._warning = true;
           }
         }
    }

   

// EventScanView.template = "event.EventScanView";
// BarcodeScannerView.components = { BarcodeScanner };

// registry.category("actions").add("event.event_barcode_scan_view", BarcodeScannerView);

}
BarcodeScanner.components = {
    ...BarcodeScanner.components,
    BarcodeScannerView,
};


















// console.log("Barcode JS Called ===");
// import { _t } from "@web/core/l10n/translation";
// import { FormController } from "@web/views/form/form_controller";
// import { Component, EventBus, onWillStart, useSubEnv, useState } from "@odoo/owl";
// // console.log("basic Model =====", Component);

// export class StockBarcode extends Component {
//     setup() {
//         super.setup();
//         this.orm = useService("orm");
//         this.actionService = useService("action");
//     }

//     async _performOnChange(record, fields, options = {}) {
//         console.log("==== First Onchange ====");
//     }
// }
//  EventBus.include({
//    async _performOnChange(record, fields, options = {}) {
//      const firstOnChange = options.firstOnChange;
//      let { hasOnchange, onchangeSpec } = this._buildOnchangeSpecs(record, options.viewType);
//      if (!firstOnChange && !hasOnchange) {
//        return;
//      }
//      var idList = record.data.id ? [record.data.id] : [];
//      const ctxOptions = {
//        full: true,
//      };
//      if (fields.length === 1) {
//        fields = fields[0];
//        // if only one field changed, add its context to the RPC context
//        ctxOptions.fieldName = fields;
//      }
//      var context = this._getContext(record, ctxOptions);
//      var currentData = this._generateOnChangeData(record, {
//        changesOnly: false,
//        firstOnChange,
//      });
//
//      const result = await this._rpc({
//        model: record.model,
//        method: 'onchange',
//        args: [idList, currentData, fields, onchangeSpec],
//        context: context,
//      });
//      if (!record._changes) {
//        // if the _changes key does not exist anymore, it means that
//        // it was removed by discarding the changes after the rpc
//        // to onchange. So, in that case, the proper response is to
//        // ignore the onchange.
//        return;
//      }
//      if (result.warning) {
//        if (fields === '_barcode_scanned' || fields === 'product_barcode_scan') {
//          if (result.warning.title === "Successfully Added") {
//             this.displayNotification({
//              type: 'success',
//              title: _t(result.warning.title),
//              message: _t(result.warning.message),
//              sticky: false
//            });
//            // this.__parentedParent.saveRecord();
//          } else {
//            this.displayNotification({
//              type: 'warning',
//              title: _t(result.warning.title),
//              message: _t(result.warning.message),
//              sticky: false
//            });
//            $('body').append('<audio src="/do_stock_barcode/static/src/sounds/error.wav" autoplay="true"></audio>');
//          }
//        } else {
//          $('.o_notification_manager').removeClass('success');
//          $('.o_notification_manager').removeClass('notification_center');
//          this.trigger_up('warning', result.warning);
//          record._warning = true;
//        }
//      }
//      if (result.domain) {
//        record._domains = Object.assign(record._domains, result.domain);
//      }
//      await this._applyOnChange(result.value, record, { firstOnChange });
//      return result;
//    },
//  });
//  FormController.include({
//    _barcodeAddX2MQuantity: function(barcode, activeBarcode) {
//      if (this.mode === 'readonly') {
//        if (activeBarcode.name == '_barcode_scanned') {
//          this._setMode('edit');
//        } else {
//          this.do_warn(_t('Error: Document not editable'),
//            _t('To modify this document, please first start edition.'));
//          return Promise.reject();
//        }
//      }
//
//      var record = this.model.get(this.handle);
//      var candidate = this._getBarCodeRecord(record, barcode, activeBarcode);
//      if (candidate) {
//        return this._barcodeSelectedCandidate(candidate, record, barcode, activeBarcode);
//      } else {
//        return this._barcodeWithoutCandidate(record, barcode, activeBarcode);
//      }
//    },
//    _barcodeScanned: function(barcode, target) {
//      var self = this;
//      var resource = this._super.apply(this, arguments);
//      if (self.modelName === "stock.picking") {
//        self.saveRecord();
//      }
//      return resource;
//    },
//  });