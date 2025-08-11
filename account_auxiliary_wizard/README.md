# 🧾 Asistente de Balance Auxiliar - Odoo

Este módulo proporciona un asistente (wizard) en Odoo que permite generar una vista filtrada del balance auxiliar contable de forma dinámica, sin necesidad de generar un reporte PDF.

---

## 📌 Características

- Filtro por fechas (`date_from`, `date_to`).
- Selección de tipo de reporte: **Resumen** o **Detalle**.
- Opción para mostrar solo movimientos `Publicado`, `Borrador` o `Todos`.
- Filtros adicionales:
  - Agrupar por cuenta.
  - Agrupar por tercero.
  - Convertir a la moneda de la compañía.
  - Omitir saldos en cero.
- Filtro por múltiples cuentas (`account.account`) y terceros (`res.partner`).
- Vista previa en formato árbol (`tree view`).
- Notificación de confirmación con mensaje personalizado.

---

## 🛠 Modelo

- `account.auxiliary.wizard`: modelo transitorio para generar la vista previa con los filtros seleccionados.

---

## 🖼 Vista Previa

La función `preview_html()` genera una acción de ventana que muestra los resultados en una vista tipo árbol, usando la vista definida como:

```xml
<tree string="Líneas Auxiliares">
  <!-- Campos como cuenta, fecha, tercero, débito, crédito, saldo -->
</tree>
