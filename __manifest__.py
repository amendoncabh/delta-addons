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
    'version': '10.0.1.0.0',
    'depends': ['base',
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
    ],
    'installable': True,
    'aplication': True,
}