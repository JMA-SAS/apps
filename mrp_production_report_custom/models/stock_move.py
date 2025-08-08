# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Módulo: Reporte personalizado de órdenes de producción
# Autor: Luis Felipe Paternina
# Descripción: Añade un reporte PDF consolidado por centro de trabajo a las OP.
# -----------------------------------------------------------------------------

from odoo import models, fields, api
import logging

class StockMove(models.Model):
    _inherit = 'stock.move'

    workorder_id = fields.Many2one(
        'mrp.workorder',
        string='Centro de trabajo relacionado',
        compute='_compute_workorder_id',
        store=False)

    @api.depends('raw_material_production_id', 'product_id')
    def _compute_workorder_id(self):
        for move in self:
            workorder = False
            if move.raw_material_production_id and move.product_id:
                workorders = move.raw_material_production_id.workorder_ids
                for wo in workorders:
                    if move.product_id in wo.production_id.bom_id.bom_line_ids.mapped('product_id'):
                        workorder = wo
                        break
            move.workorder_id = workorder
