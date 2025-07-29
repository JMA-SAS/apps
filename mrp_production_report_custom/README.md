# MRP Production Report

### 👨‍💻 Desarrollado por **JMA**

### 📦 Módulo Odoo - Reporte Personalizado de Órdenes de Producción

Este módulo extiende el módulo de manufactura (`mrp`) de Odoo para generar reportes PDF personalizados y consolidados por centro de trabajo. Es ideal para empresas que necesitan mayor trazabilidad y control visual de los materiales utilizados en cada orden de producción (OP).

---

## ✨ Funcionalidades

- Agrega un reporte PDF personalizado a las órdenes de producción.
- Muestra los productos requeridos organizados por centro de trabajo.
- Agrupa materiales y cantidades por operación, unidad de medida y orden de producción.
- Enlaza automáticamente la orden de venta relacionada, si existe.
- Totalmente integrado con `stock`, `sale_management` y `mrp`.

---

## 🧩 Dependencias

Este módulo depende de los siguientes módulos de Odoo:

- `mrp`
- `sale_management`
- `stock`

---

## 🛠 Instalación

1. Copia este módulo en tu carpeta de addons personalizados:
   ```bash
   cp -r mrp_production_report /odoo/custom_addons/

