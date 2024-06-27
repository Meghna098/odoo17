/** @odoo-module **/

import { jsonrpc } from "@web/core/network/rpc_service";
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.propertyWebsiteTypeCustom = publicWidget.Widget.extend({
    selector: '.new-form',
    events: {
        'change .property-checks': '_onSelectCheckbox',
        'change #prop_type': '_onSelectType',
        'click .btn-submit': '_onSubmit',
    },

    updateAmount: function() {
        var propType = $("#prop_type").val();
        var totalAmount = '';
        var sum = 0;
        if (propType == 'rent') {
            totalAmount = 'data-rent';
        } else if (propType == 'lease') {
            totalAmount = 'data-lease';
        }
        var allRecords = $('[data-checked="true"]');
        if (totalAmount && allRecords.length > 0) {
            for (let i = 0; i < allRecords.length; i++) {
                sum += parseInt(allRecords[i].getAttribute(totalAmount));
            }
        }
        return sum;
    },

    _onSelectCheckbox: function(e) {
        e.target.setAttribute('data-checked', e.target.getAttribute('data-checked') == 'false' ? 'true' : 'false');
        $("#amount").prop('value', this.updateAmount());
    },

    _onSelectType: function(e) {
        $("#amount").prop('value', this.updateAmount());
    },

    _onSubmit: async function() {
        var all_properties = this.$el.find('.property-checks');
        var type_input = this.$el.find('#prop_type').val();
        var start_date_input = this.$el.find('#start_date').val();
        var end_date_input = this.$el.find('#end_date').val();
        var rent_lease_price = this.$el.find('#amount').val();

        var all_property_list = [];
        for (var key in all_properties) {
            var elements = all_properties[key];
            if (key < all_properties.length && elements.getAttribute('data-checked') == 'true') {
                all_property_list.push(parseInt(elements.getAttribute('value')));
            }
        }

        let values = {
            'properties': all_property_list,
            'type': type_input,
            'start_date': start_date_input,
            'end_date': end_date_input,
            'rent_lease_amount': rent_lease_price
        };

        if (all_property_list.length > 0 && type_input && start_date_input && end_date_input && rent_lease_price) {
            await jsonrpc('/webform_submit', values).then((result) => {
                window.location.href = '/thank_you';
            });
        }
    }
});

