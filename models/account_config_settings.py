# -*- coding: utf-8 -*-

from odoo import api, fields, models

class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'
    
    fiscal_position_default = fields.Many2one('account.fiscal.position', string=u'Posição Fiscal Padrão')
    
    
    def get_fiscal_position_default(self, fields):
        return {'fiscal_position_default':
                self.env.user.company_id.fiscal_position_default.id}

    @api.multi
    def set_fiscal_position_default(self):
        self.env.user.company_id.fiscal_position_default = self.fiscal_position_default