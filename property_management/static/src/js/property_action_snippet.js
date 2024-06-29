/** @odoo-module */
import PublicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToElement } from "@web/core/utils/render";
export function _chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}
var LatestProperty = PublicWidget.Widget.extend({
    	selector: '.property_snippet_content',
    	willStart: async function() {
        	var self = this;
        	await rpc.query({
            	route: '/latest_properties',
        	}).then((data) => {
            	this.data = data;
        	});
    	},
    	start: function() {
        	var chunks = _.chunk(this.data, 4)
        	chunks[0].is_active = true
        	 refEl.html(renderToElement(property_management.property_snippet_courosel', {
                'property': chunk
            }))
        }
	PublicWidget.registry.property_snippet_content = LatestProperty;
	return LatestProperty;
});
