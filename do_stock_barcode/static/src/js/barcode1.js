// /* @odoo-module */

// import { patch } from "@web/core/utils/patch";
// import { FormController } from "@web/views/form/form_controller";
// import { x2ManyCommands } from "@web/core/orm_service";
// import { useSubEnv } from "@odoo/owl";

// patch(FormController.prototype, {
//     setup() {
//         super.setup(...arguments);
//         useSubEnv({
//             chatter: {
//                 fetchData: true,
//                 fetchMessages: true,
//             },
//         });
//     },
//     onWillLoadRoot(nextConfiguration) {
//         super.onWillLoadRoot(...arguments);
//         this.env.chatter.fetchData = true;
//         this.env.chatter.fetchMessages = true;
//         const isSameThread =
//             this.model.root?.resId === nextConfiguration.resId &&
//             this.model.root?.resModel === nextConfiguration.resModel;
//         if (isSameThread) {
//             // not first load
//             const { resModel, resId } = this.model.root;
//             this.env.bus.trigger("MAIL:RELOAD-THREAD", { model: resModel, id: resId });
//         }
//     },

//     async onWillSaveRecord(record, changes) {
//         if (record.resModel === "mail.compose.message") {
//             const parser = new DOMParser();
//             const htmlBody = parser.parseFromString(changes.body, "text/html");
//             const partnerElements = htmlBody.querySelectorAll('[data-oe-model="res.partner"]');
//             const partnerIds = Array.from(partnerElements).map((element) =>
//                 parseInt(element.dataset.oeId)
//             );
//             if (partnerIds.length) {
//                 if (changes.partner_ids[0] && changes.partner_ids[0][0] === x2ManyCommands.SET) {
//                     partnerIds.push(...changes.partner_ids[0][2]);
//                 }
//                 changes.partner_ids = [x2ManyCommands.set(partnerIds)];
//             }
//         }
//     },
// });







/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { BarcodeScanner } from "@barcodes/components/barcode_scanner";
import { Component, onWillStart } from "@odoo/owl";
// import { registry } from "@web/core/registry";
import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";
import { useBus, useService } from "@web/core/utils/hooks";
alert("ssssssssss")

patch(BarcodeScanner.prototype, {
    /**
     * Needs to be set to true to show the loyalty points in the partner list.
     * @override
     */
    
    setup() {
        super.setup(...arguments);
        this.notification = useService("notification");
        this.orm = useService("orm");
        this.rpc = useService("rpc");
        const barcode = useService("barcode");
    },
    
    async onBarcodeScanned(barcode) {
        const result = await this.orm.call("stock.picking", "onchange_product_barcode_scan", [], {
            barcode: barcode,
        });
        console.log("sssssssssssssssssss",result);
        if (result.warning) {
           // if (fields === '_barcode_scanned' || fields === 'product_barcode_scan') {
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
           // } else {
           //   $('.o_notification_manager').removeClass('success');
           //   $('.o_notification_manager').removeClass('notification_center');
           //   this.trigger_up('warning', result.warning);
           //   record._warning = true;
           // }
         }
    },
});
