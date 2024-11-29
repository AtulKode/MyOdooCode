/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";

import { odooExceptionTitleMap } from "@web/core/errors/error_dialogs";

import { ErrorDialog } from "@web/core/errors/error_dialogs";
import { ClientErrorDialog } from "@web/core/errors/error_dialogs";
import { NetworkErrorDialog } from "@web/core/errors/error_dialogs";
import { WarningDialog } from "@web/core/errors/error_dialogs";
import { RedirectWarningDialog } from "@web/core/errors/error_dialogs";
import { SessionExpiredDialog } from "@web/core/errors/error_dialogs";
import { RPCErrorDialog } from "@web/core/errors/error_dialogs";


ErrorDialog.title = _t("Server Error");
ClientErrorDialog.title = _t("Client Error");
NetworkErrorDialog.title = _t("Network Error");
SessionExpiredDialog.title = _t("Session Expired");

patch(WarningDialog.prototype, {
    inferTitle() {
        if (this.props.exceptionName && odooExceptionTitleMap.has(this.props.exceptionName)) {
            return odooExceptionTitleMap.get(this.props.exceptionName).toString();
        }
        return this.props.title || _t("Server Warning");
    }
});

patch(RedirectWarningDialog.prototype, {
    setup() {
        super.setup();
        this.title = capitalize(subType) || _t("Server Warning");
    }
});

patch(RPCErrorDialog.prototype, {
    inferTitle() {
        // If the server provides an exception name that we have in a registry.
        if (this.props.exceptionName && odooExceptionTitleMap.has(this.props.exceptionName)) {
            this.title = odooExceptionTitleMap.get(this.props.exceptionName).toString();
            return;
        }
        // Fall back to a name based on the error type.
        if (!this.props.type) {
            return;
        }
        switch (this.props.type) {
            case "server":
                this.title = _t("Server Error");
                break;
            case "script":
                this.title = _t("Client Error");
                break;
            case "network":
                this.title = _t("Network Error");
                break;
        }
    }
});