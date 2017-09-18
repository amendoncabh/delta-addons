# -*- coding: utf-8 -*-
# © 2017 Raphael Rodrigues <raphael0608@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    metodo_pagamento = fields.Selection([
                        ('01', u'Dinheiro'),
                        ('02', u'Cheque'),
                        ('03', u'Cartão de Crédito'),
                        ('04', u'Cartão de Débito'),
                        ('05', u'Crédito Loja'),
                        ('10', u'Vale Alimentacão'),
                        ('11', u'Vale Presente'),
                        ('13', u'Vale Combustível'),
                        ('99', u'Outros')], 
                        string='Método de Pagamento')
    
    @api.multi
    def _get_fiscal_document_code(self):
        res = ''
        if self.fiscal_document_id:
            res = self.fiscal_document_id.code
        return res
    
    def _prepare_edoc_vals(self, invoice):
        vals = super(AccountInvoice, self)._prepare_edoc_vals(invoice)
        if vals['model'] == '65':
            vals['metodo_pagamento'] = invoice.metodo_pagamento
        print 'fazer teste'
        if invoice.partner_id.name == 'CONSUMIDOR':
            print 'teste ok'
            vals['ind_dest'] = '1'
        return vals
