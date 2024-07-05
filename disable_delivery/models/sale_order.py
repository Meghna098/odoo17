from odoo import Command, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_sales_delivery(self):
        picking = self.env['stock.picking'].create({
            'partner_id': self.partner_shipping_id.id,
            'scheduled_date': self.date_order,
            'origin': self.name,
            'picking_type_id': self.env.ref('stock.picking_type_out').id,
            'move_ids': [Command.create({
                'name': line.name,
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty,
                'quantity': line.qty_delivered,
                'location_id': self.env.ref('stock.stock_location_stock').id,
                'location_dest_id': self.partner_shipping_id.property_stock_customer.id,
            })for line in self.order_line]
        })
        picking.action_confirm()

        return {
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_model': 'stock.picking',
            'view_mode': 'form',
            'res_id': picking.id,
        }
