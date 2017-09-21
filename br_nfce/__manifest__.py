# -*- coding: utf-8 -*-
{
    'name': "Emissão de NFC-e",
    'summary': """
           Permite a emissão de NFC-e através das Vendas no Odoo
           """,
    'description': """
        Permite a emissão de NFC-e através das Vendas no Odoo
    """,
    'author': "Raphael Rodrigues",
    'website': "",
    'category': 'account',
    'version': '10.0.1.0.1b',
    'depends': ['base',
                'account_accountant',
                'br_sale',
                'br_nfe'],
    
    'external_dependencies': {
        'python': [
            'pytrustnfe', 'pytrustnfe.nfe',
            'pytrustnfe.certificado', 'pytrustnfe.utils'
        ],
    },
    'data': [
        'views/views.xml',
        'views/templates.xml',
        'views/res_company.xml',
        'views/account_fiscal_position.xml',
        'views/account_journal.xml',
        'views/account_invoice.xml',
        'views/account_config_settings.xml',
        'data/br_nfce.xml',
        'reports/br_nfce_reports.xml',
        'reports/danfce_report.xml',
	'views/invoice_eletronic.xml',
    ],
    'installable': True,
    'aplication': True,
}
