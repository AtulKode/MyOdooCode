/* @odoo-module */

import { evaluateExpr } from "@web/core/py_js/py";
import { registry } from "@web/core/registry";
import { SIZES } from "@web/core/ui/ui_service";
import { patch } from "@web/core/utils/patch";
import { append, createElement, setAttributes } from "@web/core/utils/xml";
import { FormCompiler } from "@web/views/form/form_compiler";

patch(FormCompiler.prototype, {
    compile(node, params) {
        // TODO no chatter if in dialog?
        const res = super.compile(node, params);
        const chatterContainerHookXml = res.querySelector(".o-mail-Form-chatter");
        if (!chatterContainerHookXml) {
            return res; // no chatter, keep the result as it is
        }
        const chatterContainerXml = chatterContainerHookXml.querySelector(
            "t[t-component='__comp__.mailComponents.Chatter']"
        );
        setAttributes(chatterContainerXml, {
            isChatterAside: "false", // Remove any aside positioning
            isInFormSheetBg: "false", // Ensure it doesn't float within sheet
            saveRecord: "__comp__.props.saveRecord",
        });

        // Ensure the chatter is below the form
        const formSheetBgXml = res.querySelector(".o_form_sheet_bg");
        const parentXml = formSheetBgXml && formSheetBgXml.parentNode;
        if (!parentXml) {
            return res; // miss-config: a sheet-bg is required for the rest
        }

        // Remove any conditional size-based logic
        const webClientViewAttachmentViewHookXml = res.querySelector(".o_attachment_preview");
        if (webClientViewAttachmentViewHookXml) {
            setAttributes(webClientViewAttachmentViewHookXml, {
                "t-if": `__comp__.hasFileViewer() and __comp__.uiService.size >= ${SIZES.XXL}`,
            });

            // Remove the conditional logic for left/right movement
            const sheetBgChatterContainerHookXml = chatterContainerHookXml.cloneNode(true);
            sheetBgChatterContainerHookXml.classList.add("o-isInFormSheetBg", "w-auto");

            append(formSheetBgXml, sheetBgChatterContainerHookXml);
            const sheetBgChatterContainerXml = sheetBgChatterContainerHookXml.querySelector(
                "t[t-component='__comp__.mailComponents.Chatter']"
            );
            setAttributes(sheetBgChatterContainerXml, {
                isInFormSheetBg: "true",
                isChatterAside: "false",
            });
        }

        // Ensure the chatter stays below the form (No shifting right)
        setAttributes(chatterContainerXml, {
            isInFormSheetBg: "false",
            isChatterAside: "false", // No aside positioning
        });

        // Apply a style to prevent shifting to the right and set width 100%
        setAttributes(chatterContainerHookXml, {
            "t-attf-class": `mt-4 mt-md-0 w-100 overflow-hidden`, // Full width and margin below form
        });

        // Ensure the parent container also has proper styling
        setAttributes(parentXml, {
            "t-attf-class": `position-relative` // Ensure proper positioning
        });

        append(parentXml, chatterContainerHookXml);
        return res;
    },
});

