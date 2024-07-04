/** @odoo-module */
import publicWidget from '@web/legacy/js/public/public_widget';
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToFragment } from "@web/core/utils/render";

export function _chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}

var LatestProperty = publicWidget.Widget.extend({
    selector: '#property_snippet',
    willStart: async function () {
        var self = this;
        await jsonrpc('/latest_properties', {}).then((data) => {
            this.data = data;
        });
    },
    start: function () {
        var chunks = _chunk(this.data, 4);
        chunks[0].is_active = true;
        this.$el.find('#carousel').html(
            renderToFragment('property_management.property_snippet_carousel', {
                chunks
            })
        );
    },
});
publicWidget.registry.property_snippet_content = LatestProperty;
return LatestProperty;
