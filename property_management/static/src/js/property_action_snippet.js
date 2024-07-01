/** @odoo-module */
import PublicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToElement } from "@web/core/utils/render";

console.log('hii')
export function _chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}
var LatestProperty = publicWidget.Widget.extend({
    	selector: '.property_snippet_content',
    	willStart: async function() {
    	    console.log('fetch latest properties');
    	    var self = this;
    	    await jsonrpc('/latest_properties', {}).then((data) => {
            	this.data = data;
            	console.log('data fetched',this.data);
        	});
    	},
    	start: function() {
    	    console.log('hii');
        	var chunks = _.chunk(this.data, 4)
        	chunks[0].is_active = true
        	this.$el.find('#carousel').html(
            	qweb.render('property_management.property_snippet_carousel', {
                	chunks
            	})
        	)
    	},
	publicWidget.registry.property_snippet_content = LatestProperty;
	return LatestProperty;
});
