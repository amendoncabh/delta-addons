# -*- coding: utf-8 -*-
# © 2017 Raphael Rodrigues <raphael0608@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api

class ResCompany(models.Model):
    _inherit = 'res.company'
    
    id_token_csc = fields.Char(string='Código CSC')
    csc = fields.Char(string=u'Código de Segurança do Contribuinte')
    fiscal_position_default = fields.Many2one('account.fiscal.position', string=u'Posição Fiscal Padrão')