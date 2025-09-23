Server Time Check
=================

Consulta y visualiza la hora del Servidor, Odoo y PostgreSQL directamente desde Odoo.

Este módulo añade un menú dentro de Odoo que permite comparar tres referencias de tiempo clave:

- **Hora del Servidor (OS)**: obtenida desde el sistema operativo.
- **Hora de Odoo**: generada con ``fields.Datetime.now()``.
- **Hora de PostgreSQL**: consultada directamente mediante ``SELECT NOW()``.

Características
---------------

- Menú dedicado dentro de Odoo.
- Modelo transitorio para evitar acumulación de registros.
- Seguridad configurable mediante grupos de usuarios.
- Compatible con Odoo 17 Community y Enterprise.

Instalación
-----------

1. Copiar el módulo en la carpeta de addons de Odoo.
2. Actualizar la lista de aplicaciones.
3. Buscar **Server Time Check** e instalarlo.

Uso
---

1. Ir al menú **Herramientas > Server Time Check**.
2. Presionar el botón para obtener la hora del Servidor, de Odoo y de PostgreSQL.
3. Visualizar la información en la vista de formulario.

Capturas de pantalla
--------------------

.. image:: static/description/screenshot.png
   :alt: Vista del módulo Server Time Check
   :width: 800px

Autor
-----

- **JMA**
- Sitio web: https://fsf3cj7zbi8.cloudpepper.site/
- Licencia: LGPL-3
