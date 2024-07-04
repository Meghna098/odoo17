/** @odoo-module **/

import { jsonrpc } from "@web/core/network/rpc_service";
import publicWidget from "@web/legacy/js/public/public_widget";

    var publicWidget = require('web.public.widget');

    publicWidget.registry.QuantityToggle = publicWidget.Widget.extend({
        selector: '#toggle_quantity_buttons',
        events: {
            'click': '_onToggleQuantityButtons',
        },
        _onToggleQuantityButtons: function () {
            var $quantityButtons = $('#quantity_buttons');
            if ($quantityButtons.is(':visible')) {
                $quantityButtons.hide();
            } else {
                $quantityButtons.show();
            }
        },
    });
});