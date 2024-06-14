from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    is_vendor_products = fields.Boolean(string='Is Vendor Products')
    vendor_product_ids = fields.Many2many('product.product', compute='_compute_product_ids', store=True)

    @api.depends('is_vendor_products', 'partner_id')
    def _compute_product_ids(self):
        for rec in self:
            if rec.is_vendor_products:
                rec.vendor_product_ids = self.env['product.product'].search([]).filtered(
                    lambda product: rec.partner_id.id in product.seller_ids.partner_id.ids).ids
                rec.order_line.write({
                    'product_id': [fields.Command.link(record.id) for record in rec.vendor_product_ids]
                })
            else:
                rec.vendor_product_ids = self.env['product.product'].search([])
