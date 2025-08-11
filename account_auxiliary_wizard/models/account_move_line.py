# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    partner_vat = fields.Char(related="partner_id.vat",string="NIT")
    origin = fields.Char(string="Origen")
