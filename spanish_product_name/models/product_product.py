# -*- encoding: utf-8 -*-
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    spanish_name = fields.Char()
