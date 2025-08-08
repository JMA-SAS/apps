# Bandeja de Correos para Compras (mail_purchase_inbox)

Este módulo de Odoo permite capturar correos electrónicos entrantes de proveedores, analizar sus archivos PDF adjuntos y generar automáticamente órdenes de compra basadas en los productos detectados.

## Características

- Registra correos entrantes dirigidos al área de compras.
- Extrae texto desde archivos PDF adjuntos usando `pdfplumber`.
- Detecta productos, cantidades y precios desde el texto del PDF.
- Crea órdenes de compra automáticamente en Odoo.
- Asocia el correo con el contacto del proveedor (creándolo si es necesario).
- Sincroniza adjuntos del chatter con los registros de la bandeja.

## Instalación

1. Clona este repositorio dentro del directorio de addons de tu instancia de Odoo:
   ```bash
   git clone https://github.com/tu_usuario/mail_purchase_inbox.git
