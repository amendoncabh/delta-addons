# -*- coding: utf-8 -*-
# © 2017 Raphael Rodrigues <raphael0608@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    '''
    Incluir o método de pagamento na Invoice caso o documento fiscal seja NFC-e
    '''
    @api.multi
    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        if self.fiscal_position_id.nfe_serie.fiscal_document_id.code == '65':
            res['metodo_pagamento'] = '01'
        return res
    
    '''
    Complemento da função 'onchange_partner_shipping_id', testa se o parceiro possui
    Posição Fiscal definida no cadastro, caso contrário será definida na venda a Posição
    Fiscal padrão definida no cadastro da empresa, esta função deve ser utilizada para vendas
    com NFC-e aonde o cliente não possui cadastro e a venda é feita com um cliente genérico
    pré-cadastrado.
    '''
    @api.multi
    @api.onchange('partner_shipping_id', 'partner_id')
    def onchange_partner_shipping_id(self):
        super(SaleOrder, self).onchange_partner_shipping_id()
        if not self.partner_id.property_account_position_id.id:
            self.fiscal_position_id = self.env.user.company_id.fiscal_position_default
            return {}
    
    def _get_default_partner(self):
        partner = self.env['res.partner'].search([['name', '=', 'CONSUMIDOR']])
        return partner
        
    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True, 
                                 states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, 
                                 required=True, change_default=True, index=True, track_visibility='always',
                                 default=_get_default_partner)
        