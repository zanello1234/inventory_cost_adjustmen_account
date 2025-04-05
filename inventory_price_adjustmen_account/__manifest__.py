{
    'name': 'Stock Valuation Account Adjustment',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Adds specific account for manual standard price adjustments',
    'depends': ['stock_account'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_valuation_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
