# -*- coding: utf-8 -*-
# © 2017 Raphael Rodrigues <raphael0608@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api, _
from datetime import datetime
from lxml import etree
import os, base64
from odoo.http import Controller, route, request

try:
    from pytrustnfe.nfe import autorizar_nfe
    from pytrustnfe.nfe import retorno_autorizar_nfe
    from pytrustnfe.nfe import recepcao_evento_cancelamento
    from pytrustnfe.certificado import Certificado
    from pytrustnfe.utils import ChaveNFe, gerar_chave
except ImportError:
    _logger.debug('Cannot import pytrustnfe', exc_info=True)

metodos = [
    ('01', u'Dinheiro'),
    ('02', u'Cheque'),
    ('03', u'Cartão de Crédito'),
    ('04', u'Cartão de Débito'),
    ('05', u'Crédito Loja'),
    ('10', u'Vale Alimentacão'),
    ('11', u'Vale Presente'),
    ('13', u'Vale Combustível'),
    ('99', u'Outros'),
]

class InvoiceEletronic(models.Model):
    _inherit = 'invoice.eletronic'
    
    qrcode_hash = fields.Char(string='QR-Code Hash')
    qrcode_url = fields.Text(string='QR-Code URL')
    metodo_pagamento = fields.Selection(metodos, string='Método de Pagamento')
    
    #função para buscar e gravar o qrcode e qrcode_hash    
    def qrcode_generate(self):
        qrcode = self.qrcode_hash
        qrcode = qrcode.replace('&', '%26')
        return qrcode

        
    @api.multi
    def _hook_validation(self):
        errors = super(InvoiceEletronic, self)._hook_validation()
        if self.model != '65':
            return errors
        if not self.company_id.partner_id.inscr_est:
            errors.append(u'Emitente / Inscrição Estadual')
        if len(self.company_id.id_token_csc or '') != 6:
            errors.append(u'Identificador do CSC inválido')
        if not len(self.company_id.csc or ''):
            errors.append(u'CSC inválido')
        if self.partner_id.cnpj_cpf is None:
            errors.append(u'CNPJ/CPF do cliente inválido')
        if len(self.serie) == 0:
            errors.append(u'Número de Série da Nota Fiscal inválido')
        if self.model == '65' and self.partner_id.name != 'CONSUMIDOR':
            return errors
        
        #Caso o consumidor não seja identificado não deve retornar os erros abaixo
        errors.remove(u'Destinatário / Endereço - Logradouro')
        errors.remove(u'Destinatário / Endereço - Número')
        errors.remove(u'Destinatário / Endereço - País')
         
        
        return errors
    
    @api.multi
    def _prepare_eletronic_invoice_values(self):
        vals = super(InvoiceEletronic, self)._prepare_eletronic_invoice_values()
        if self.model != '65':
            return vals
        
        codigo_seguranca = {
                'cid_token': self.company_id.id_token_csc,
                'csc': self.company_id.csc,
            }
        vals['codigo_seguranca'] = codigo_seguranca
        if self.model == '65':
            vals['pag'] = self.metodo_pagamento
            
        if self.model == '65' and self.partner_id.name == 'CONSUMIDOR':
            del(vals['dest'])
            
        
        return vals
    
    @api.multi
    def _prepare_eletronic_invoice_item(self, item, invoice):
        res = super(InvoiceEletronic, self)._prepare_eletronic_invoice_item(
            item, invoice)
        if self.model not in ('55', '65'):
            return res
        
        if self.model == ('65'):
            del(res['imposto']['II'])

        if self.ambiente == 'homologacao':
            res['prod']['xProd'] = 'NOTA FISCAL EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL' 
            
        return res
            
    @api.multi
    def action_send_eletronic_invoice(self):
        super(InvoiceEletronic, self).action_send_eletronic_invoice()

        if self.model not in ('55', '65') or self.state in ('done', 'denied', 'cancel'):
            return

        self.state = 'error'
        self.data_emissao = datetime.now()

        nfe_values = self._prepare_eletronic_invoice_values()
        lote = self._prepare_lote(self.id, nfe_values)
        cert = self.company_id.with_context({'bin_size': False}).nfe_a1_file
        cert_pfx = base64.decodestring(cert)

        certificado = Certificado(cert_pfx, self.company_id.nfe_a1_password)

        resposta_recibo = None
        resposta = autorizar_nfe(certificado, self.model, **lote)
        retorno = resposta['object'].Body.nfeAutorizacaoLoteResult
        retorno = retorno.getchildren()[0]
        
        if self.model == '65':
            xml = resposta['sent_xml']
            qr_code = etree.XML(resposta['sent_xml'])
            qr_code = qr_code.find(".//{http://www.portalfiscal.inf.br/nfe}qrCode")
            self.qrcode_hash = qr_code.text
            self.qrcode_url = qr_code.text.split('?')[0]
        
        if retorno.cStat == 103:
            obj = {
                'estado': self.company_id.partner_id.state_id.ibge_code,
                'ambiente': 1 if self.ambiente == 'producao' else 2,
                'obj': {
                    'ambiente': 1 if self.ambiente == 'producao' else 2,
                    'numero_recibo': retorno.infRec.nRec
                }
            }
            self.recibo_nfe = obj['obj']['numero_recibo']
            import time
            while True:
                time.sleep(2)
                resposta_recibo = retorno_autorizar_nfe(certificado, self.model, **obj)
                retorno = resposta_recibo['object'].Body.\
                    nfeRetAutorizacaoLoteResult.retConsReciNFe
                if retorno.cStat != 105:
                    break

        if retorno.cStat != 104:
            self.codigo_retorno = retorno.cStat
            self.mensagem_retorno = retorno.xMotivo
        else:
            self.codigo_retorno = retorno.protNFe.infProt.cStat
            self.mensagem_retorno = retorno.protNFe.infProt.xMotivo
            if self.codigo_retorno == '100':
                self.write({
                    'state': 'done', 'nfe_exception': False,
                    'protocolo_nfe': retorno.protNFe.infProt.nProt,
                    'data_autorizacao': retorno.protNFe.infProt.dhRecbto})
            # Duplicidade de NF-e significa que a nota já está emitida
            # TODO Buscar o protocolo de autorização, por hora só finalizar
            if self.codigo_retorno == '204':
                self.write({'state': 'done', 
                            'codigo_retorno': '100',
                            'nfe_exception': False,
                            'mensagem_retorno': 'Autorizado o uso da NF-e'})

        self.env['invoice.eletronic.event'].create({
            'code': self.codigo_retorno,
            'name': self.mensagem_retorno,
            'invoice_eletronic_id': self.id,
        })
        self._create_attachment('nfe-envio', self, resposta['sent_xml'])
        self._create_attachment('nfe-ret', self, resposta['received_xml'])
        if resposta_recibo:
            self._create_attachment('rec', self, resposta_recibo['sent_xml'])
            self._create_attachment('rec-ret', self,
                                    resposta_recibo['received_xml'])
            
