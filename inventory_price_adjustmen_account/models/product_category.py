from odoo import fields, models

class ProductCategory(models.Model):
    _inherit = 'product.category'

    property_stock_valuation_manual_adjustment_account_id = fields.Many2one(
        'account.account',
        string='Stock Valuation Manual Adjustment Account',
        company_dependent=True,
        domain="[('deprecated', '=', False), ('company_id', '=', current_company_id)]",
        help="Account used for manual adjustments in stock valuation"
    )
