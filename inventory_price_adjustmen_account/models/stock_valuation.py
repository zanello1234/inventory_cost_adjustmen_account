# models/stock_valuation.py
from odoo import models, fields, api
from odoo.tools import float_compare

class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _change_standard_price(self, new_price):
        """Sobrescribe el método para usar la cuenta específica"""
        self.ensure_one()

        if self.valuation != 'real_time':
            return super()._change_standard_price(new_price)

        # Si tiene cuenta específica, crear nuestro asiento
        adjustment_account = self.categ_id.property_stock_valuation_manual_adjustment_account_id
        if adjustment_account:
            # Calcular la diferencia de valoración
            qty_available = self.with_company(self.env.company).qty_available
            old_price = self.standard_price
            diff_per_unit = new_price - old_price
            value_diff = qty_available * diff_per_unit

            if float_compare(value_diff, 0.0, precision_rounding=self.currency_id.rounding) != 0:
                # Crear el asiento contable con la nueva cuenta
                move_vals = {
                    'journal_id': self.categ_id.property_stock_journal.id,
                    'company_id': self.env.company.id,
                    'ref': f'Manual price adjustment: {self.display_name} from {old_price} to {new_price}',
                    'move_type': 'entry',
                    'line_ids': [
                        (0, 0, {
                            'name': f'Manual price adjustment: {diff_per_unit} per unit',
                            'account_id': self.categ_id.property_stock_valuation_account_id.id,
                            'debit': value_diff if value_diff > 0 else 0,
                            'credit': -value_diff if value_diff < 0 else 0,
                        }),
                        (0, 0, {
                            'name': f'Manual price adjustment: {diff_per_unit} per unit',
                            'account_id': adjustment_account.id,
                            'debit': -value_diff if value_diff < 0 else 0,
                            'credit': value_diff if value_diff > 0 else 0,
                        }),
                    ],
                }
                move = self.env['account.move'].sudo().create(move_vals)
                move._post()
            return True

        # Si no tiene cuenta específica, usar el comportamiento nativo
        return super()._change_standard_price(new_price)

class ProductCategory(models.Model):
    _inherit = 'product.category'

    property_stock_valuation_manual_adjustment_account_id = fields.Many2one(
        'account.account',
        string='Manual Adjustment Valuation Account',
        company_dependent=True,
        domain="[('deprecated', '=', False)]",
        help="This account will be used for manual standard price adjustments"
    )
