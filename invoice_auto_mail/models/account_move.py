from odoo import models
import logging

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        res = super().action_post()
        for move in self:
            if move.move_type == "out_invoice":
                template = self.env.ref("account.email_template_edi_invoice", raise_if_not_found=False)
                if template:
                    try:
                        move.message_post_with_template(
                            template.id,
                            email_layout_xmlid="mail.mail_notification_paynow"
                        )
                        _logger.info("Factura %s enviada y registrada en el chatter de %s",
                                     move.name, move.partner_id.display_name)
                    except Exception as e:
                        _logger.error("Error enviando factura %s a %s: %s",
                                      move.name, move.partner_id.display_name, e)
                else:
                    _logger.warning("No se encontró la plantilla de correo para la factura %s", move.name)
        return res
