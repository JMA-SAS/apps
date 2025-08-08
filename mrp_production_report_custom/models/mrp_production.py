# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Módulo: Reporte personalizado de órdenes de producción
# Autor: Luis Felipe Paternina
# Descripción: Añade un reporte PDF consolidado por centro de trabajo a las OP.
# -----------------------------------------------------------------------------

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    sale_id = fields.Many2one(
        'sale.order',
        string="Orden de venta",
        compute="_compute_sale_id",
        store=True)

    @api.depends('origin')
    def _compute_sale_id(self):
        for record in self:
            if record.origin:
                sale_order = self.env['sale.order'].search([('name', '=', record.origin)], limit=1)
                record.sale_id = sale_order.id if sale_order else False
            else:
                record.sale_id = False

    def get_component_lines_grouped(self):
        self.ensure_one()
        agrupadas = {}
        for move in self.move_raw_ids:
            centro = "Sin centro"
            bom_line = self.bom_id.bom_line_ids.filtered(lambda l: l.product_id == move.product_id)
            if bom_line and bom_line[0].operation_id and bom_line[0].operation_id.workcenter_id:
                centro = bom_line[0].operation_id.workcenter_id.name

            clave = (centro, move.product_id.id, self.name)  # <-- incluir OP name en clave
            if clave not in agrupadas:
                agrupadas[clave] = {
                    'centro': centro,
                    'product': move.product_id,
                    'uom': move.product_uom,
                    'qty': 0,
                    'op_name': self.name,
                }
            agrupadas[clave]['qty'] += move.product_uom._compute_quantity(move.product_uom_qty, agrupadas[clave]['uom'])

        resultado = {}
        for clave, data in agrupadas.items():
            centro = clave[0]
            resultado.setdefault(centro, []).append(data)

        return sorted(resultado.items())


class ReportMRPProductionResumen(models.AbstractModel):
    _name = 'report.mrp_production_report.report_compumuebles'
    _description = 'Resumen OP consolidado por centro de trabajo'

    def _get_report_values(self, docids, data=None):
        docs = self.env['mrp.production'].browse(docids)
        grupos_consolidados = {}

        for doc in docs:
            for centro, lineas in doc.get_component_lines_grouped():
                if centro not in grupos_consolidados:
                    grupos_consolidados[centro] = {}

                for linea in lineas:
                    key = linea['product'].id

                    if key not in grupos_consolidados[centro]:
                        grupos_consolidados[centro][key] = {
                            'product': linea['product'],
                            'uom': linea['uom'],
                            'qty': 0,
                            'op_names': set(),
                        }

                    grupos_consolidados[centro][key]['qty'] += linea['qty']
                    grupos_consolidados[centro][key]['op_names'].add(linea['op_name'])

        for centro in grupos_consolidados:
            grupos_consolidados[centro] = [
                {
                    'product': data['product'],
                    'uom': data['uom'],
                    'qty': data['qty'],
                    'op_names': sorted(data['op_names']),
                }
                for data in grupos_consolidados[centro].values()
            ]

        return {
            'docs': docs,
            'grupos_consolidados': sorted(grupos_consolidados.items()),  # lista de tuplas (centro, [lineas])
        }

