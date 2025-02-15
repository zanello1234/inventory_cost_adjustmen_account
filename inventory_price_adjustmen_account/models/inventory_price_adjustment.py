from odoo import models, fields

class InventoryPriceAdjustment(models.Model):
    _name = 'inventory.price.adjustment'
    _description = 'Inventory Price Adjustment'

    name = fields.Char(string='Name', required=True)
    adjustment_date = fields.Date(string='Adjustment Date', required=True)
    adjustment_amount = fields.Float(string='Adjustment Amount', required=True)
