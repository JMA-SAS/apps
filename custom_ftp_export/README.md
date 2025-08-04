# Exportar Inventario y Ventas Diarias a FTP

Este módulo personalizado para Odoo permite exportar automáticamente:

- El **inventario actual por producto**
- Las **ventas del día por producto**

Ambos se exportan en formato CSV y se suben a un servidor FTP cada día mediante una acción programada.

## Características

- Exportación de inventario con cantidades disponibles.
- Exportación de ventas diarias por producto, cantidad y total.
- Archivos CSV con nombre dinámico por fecha (`inventario_YYYYMMDD.csv`, `ventas_YYYYMMDD.csv`).
- Envío automático a un servidor FTP configurado en el código.

## Requisitos

- Odoo 17+ (puede adaptarse fácilmente a otras versiones).
- Módulos instalados:
  - `sale`
  - `stock`
- Acceso a un servidor FTP con credenciales.

## Instalación

1. Copia este módulo en el directorio `addons` de tu instalación de Odoo.
2. Reinicia el servidor Odoo.
3. Activa el modo desarrollador.
4. Instala el módulo desde la interfaz de Odoo.

## Configuración

Los datos de conexión al FTP están codificados en el archivo `ftp_export.py`:

```python
ftp_host = 'ftp.tuservidor.com'
ftp_user = 'tu_usuario'
ftp_pass = 'tu_contraseña'
ruta_remota = '/ruta/ftp/'
