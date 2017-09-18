#!/usr/bin/env python
# -*- coding: utf-8 -*-
# © 2017 Raphael Rodrigues <raphael0608@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api

class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'
    
    nfe_serie = fields.Many2one('br_account.document.serie',
                                string=u'Série da Nota Fiscal')