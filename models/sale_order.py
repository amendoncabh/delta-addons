# -*- coding: utf-8 -*-
# © 2017 Raphael Rodrigues <raphael0608@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    @api.multi
    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        if self.fiscal_position_id.nfe_serie.fiscal_document_id.code == '65':
            res['metodo_pagamento'] = '01'
        return res