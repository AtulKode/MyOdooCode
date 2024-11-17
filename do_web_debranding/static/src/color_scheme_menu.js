/** @odoo-module */

import { ColorSchemeService } from "@web_enterprise/webclient/color_scheme/color_scheme_service";
import { cookie } from "@web/core/browser/cookie";
import { patch } from "@web/core/utils/patch";

patch(ColorSchemeService.prototype, {
    get activeColorScheme() {
        return cookie.get("configured_color_scheme") || cookie.get("color_scheme") || "dark";
    },
});
