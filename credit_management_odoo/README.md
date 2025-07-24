# Módulo de Gestión de Créditos para Odoo 17

## Descripción

Este módulo personalizado proporciona funcionalidades avanzadas de gestión de créditos completamente integradas con el módulo nativo de contactos de Odoo 17. Permite el control y monitoreo de créditos a clientes con alertas informativas, validación antes de impuestos y soporte completo multimoneda.

## Características Principales

### 🔗 Integración con Contactos (res.partner)

El módulo extiende el modelo `res.partner` agregando los siguientes campos especializados:

- **credit_limit**: Campo monetario editable que representa el límite máximo de crédito permitido para el cliente
- **enable_credit_validation**: Campo booleano que indica si se debe activar la validación de crédito para este cliente específico
- **total_credit_used**: Campo monetario calculado automáticamente que representa el total actualmente adeudado por el cliente basado en facturas pendientes
- **available_credit**: Campo calculado que muestra el crédito disponible restante (Límite - Usado)

Todos estos campos están disponibles en una nueva pestaña llamada "Crédito" dentro del formulario de contactos, con visibilidad controlada por permisos de usuario.

### 🔔 Sistema de Alertas Informativas

Al validar una factura de cliente (`account.move` con `move_type='out_invoice'`), el sistema:

- Calcula automáticamente si el total antes de impuestos más la deuda actual excede el `credit_limit`
- Muestra una alerta visual informativa detallada (tipo toast/popup) con información completa del estado crediticio
- **No bloquea** la creación ni validación de la factura, permitiendo el flujo normal de trabajo
- Solo aplica la validación si el cliente tiene `enable_credit_validation` activado
- Considera únicamente facturas de cliente (no aplica a proveedores)
- Calcula el total basado en el subtotal antes de IVA, sumado al `total_credit_used` actual

### 📊 Reporte Integral de Clientes con Crédito

El módulo incluye un sistema completo de reportes accesible desde **Contactos > Reporte de Crédito**, disponible solo para usuarios con permisos contables o administrativos.

#### Información Incluida en los Reportes:
- Nombre completo del cliente
- Información de contacto (email, teléfono)
- Límite de crédito configurado
- Total adeudado actual
- Diferencia entre límite y deuda (crédito disponible)
- Moneda utilizada
- Fecha de última factura vencida
- Responsable comercial asignado

#### Formatos de Salida:
- **PDF**: Reporte profesional con formato tabular y resumen ejecutivo
- **Excel**: Archivo descargable con formato condicional (filas rojas para clientes que exceden el límite)

#### Filtros Avanzados:
- Por responsable comercial específico
- Por moneda particular
- Por estado crediticio (dentro del límite / excedido)
- Por clientes específicos

### 🌍 Compatibilidad Multimoneda Completa

El sistema maneja automáticamente múltiples monedas:

- **Visualización**: Siempre muestra la moneda original en vistas y reportes
- **Cálculos**: Utiliza la tasa de cambio (`currency_rate`) vigente al día del movimiento contable para validaciones
- **Conversión**: Proporciona métodos para convertir información de crédito a cualquier moneda objetivo
- **Consistencia**: Mantiene todos los cálculos en la moneda base de la compañía para validaciones internas

### 🔐 Sistema de Permisos y Seguridad

#### Control de Acceso:
- Solo usuarios del grupo "Contabilidad" (`account.group_account_manager`) o "Administración" (`base.group_system`) pueden:
  - Modificar `credit_limit` y `enable_credit_validation`
  - Acceder al reporte general de créditos
  - Visualizar la pestaña "Crédito" en contactos

#### Reglas de Seguridad:
- Vendedores pueden ver únicamente sus propios clientes asignados
- Contadores y administradores tienen acceso completo a todos los clientes
- Cada usuario solo puede acceder a sus propios asistentes de reportes

## Instalación

### Requisitos Previos
- Odoo 17.0 o superior
- Módulos dependientes: `contacts`, `account`, `base`

### Pasos de Instalación

1. **Clonar o descargar el módulo**:
   ```bash
   git clone [URL_DEL_REPOSITORIO]
   # o descargar y extraer el archivo ZIP
   ```

2. **Copiar a la carpeta de addons de Odoo**:
   ```bash
   cp -r credit_management_odoo /path/to/odoo/addons/
   ```

3. **Actualizar la lista de aplicaciones**:
   - Ir a Aplicaciones > Actualizar Lista de Aplicaciones
   - Buscar "Credit Management Odoo"

4. **Instalar el módulo**:
   - Hacer clic en "Instalar"
   - El sistema instalará automáticamente las dependencias necesarias

### Instalación en Odoo.sh

1. Subir el módulo al repositorio Git de tu proyecto Odoo.sh
2. Hacer push de los cambios
3. Instalar desde la interfaz de Odoo.sh

## Configuración Inicial

### 1. Configurar Clientes
1. Ir a **Contactos**
2. Seleccionar un cliente existente o crear uno nuevo
3. En la pestaña **"Crédito"**:
   - Activar "Activar Validación de Crédito"
   - Establecer el "Límite de Crédito" deseado
   - Guardar los cambios

### 2. Asignar Permisos
1. Ir a **Configuración > Usuarios y Compañías > Usuarios**
2. Seleccionar usuarios que necesiten acceso a gestión de créditos
3. Agregar al grupo "Facturación y Contabilidad / Contador" o "Administración / Configuración"

### 3. Configurar Monedas (si es necesario)
1. Ir a **Contabilidad > Configuración > Monedas**
2. Activar las monedas necesarias
3. Configurar las tasas de cambio

## Uso del Sistema

### Gestión de Crédito de Clientes

1. **Configurar límites de crédito**:
   - Acceder al formulario del cliente
   - Ir a la pestaña "Crédito"
   - Activar la validación y establecer el límite

2. **Monitorear estado crediticio**:
   - El campo "Crédito Total Usado" se actualiza automáticamente
   - El campo "Crédito Disponible" muestra el saldo restante
   - Las alertas visuales indican cuando se excede el límite

### Facturación con Validación de Crédito

1. **Crear factura normalmente**:
   - El proceso de facturación no cambia
   - Las validaciones ocurren automáticamente

2. **Interpretar alertas**:
   - Las alertas aparecen al validar facturas
   - Proporcionan información detallada del estado crediticio
   - No bloquean el proceso de facturación

### Generación de Reportes

1. **Acceder al asistente**:
   - Ir a **Contactos > Reporte de Crédito**

2. **Configurar filtros**:
   - Seleccionar clientes específicos (opcional)
   - Filtrar por responsable comercial
   - Elegir monedas específicas
   - Seleccionar estado crediticio

3. **Generar reporte**:
   - Elegir formato (PDF o Excel)
   - Hacer clic en "Generar Reporte"

## Estructura del Módulo

```
credit_management_odoo/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── res_partner.py          # Extensión del modelo de contactos
│   └── credit_report.py        # Modelos para reportes
├── views/
│   └── credit_management_views.xml  # Vistas y menús
├── reports/
│   ├── credit_report.xml       # Definiciones de reportes
│   └── credit_report_templates.xml  # Plantillas PDF
├── security/
│   ├── credit_security.xml     # Reglas de seguridad
│   └── ir.model.access.csv     # Permisos de acceso
└── tests/
    ├── __init__.py
    └── test_credit_management.py  # Pruebas unitarias
```

## API y Métodos Disponibles

### Métodos del Modelo res.partner

#### `get_credit_info()`
Retorna información completa del crédito del cliente:
```python
credit_info = partner.get_credit_info()
# Retorna: {
#     'credit_limit': float,
#     'total_credit_used': float,
#     'available_credit': float,
#     'credit_exceeded': bool,
#     'enable_validation': bool,
#     'currency': res.currency,
#     'currency_symbol': str,
#     'currency_name': str
# }
```

#### `get_credit_info_in_currency(target_currency)`
Obtiene información de crédito convertida a una moneda específica:
```python
usd_currency = env['res.currency'].search([('name', '=', 'USD')])
credit_info_usd = partner.get_credit_info_in_currency(usd_currency)
```

#### `get_last_overdue_invoice_date()`
Obtiene la fecha de la última factura vencida:
```python
last_overdue = partner.get_last_overdue_invoice_date()
# Retorna: date o False si no hay facturas vencidas
```

### Campos Computados

- **total_credit_used**: Se recalcula automáticamente cuando cambian las facturas
- **available_credit**: Se actualiza cuando cambian credit_limit o total_credit_used

## Solución de Problemas

### Problemas Comunes

1. **La pestaña "Crédito" no aparece**:
   - Verificar que el usuario tenga permisos de contabilidad
   - Confirmar que el módulo esté instalado correctamente

2. **Las alertas no se muestran**:
   - Verificar que `enable_credit_validation` esté activado en el cliente
   - Confirmar que `credit_limit` sea mayor a 0
   - Verificar que sea una factura de cliente (out_invoice)

3. **Los cálculos multimoneda son incorrectos**:
   - Verificar las tasas de cambio en Contabilidad > Configuración > Monedas
   - Confirmar que las fechas de las facturas sean correctas

4. **Errores en reportes**:
   - Verificar permisos de usuario
   - Confirmar que existan clientes con validación de crédito activada

### Logs y Depuración

Para habilitar logs detallados, agregar en el archivo de configuración de Odoo:
```ini
[logger_credit_management]
level = DEBUG
handlers = console
qualname = odoo.addons.credit_management_odoo
```

## Desarrollo y Personalización

### Extender Funcionalidades

El módulo está diseñado para ser extensible. Ejemplos de personalizaciones:

1. **Agregar campos adicionales**:
```python
class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    custom_credit_field = fields.Float('Campo Personalizado')
```

2. **Modificar lógica de validación**:
```python
class AccountMove(models.Model):
    _inherit = 'account.move'
    
    def action_post(self):
        # Lógica personalizada antes de la validación
        result = super().action_post()
        # Lógica personalizada después de la validación
        return result
```

### Pruebas

Ejecutar las pruebas unitarias:
```bash
odoo-bin -c /path/to/config -d database_name -i credit_management_odoo --test-enable --stop-after-init
```

## Contribución

### Reportar Problemas
1. Crear un issue en el repositorio
2. Incluir información detallada del problema
3. Proporcionar pasos para reproducir el error

### Contribuir Código
1. Fork del repositorio
2. Crear una rama para la nueva funcionalidad
3. Implementar cambios con pruebas
4. Crear pull request con descripción detallada

## Licencia

Este módulo se distribuye bajo la licencia LGPL-3.0. Ver archivo LICENSE para más detalles.

## Soporte

Para soporte técnico y consultas:
- Email: support@manus.ai
- Documentación: [URL_DOCUMENTACION]
- Issues: [URL_REPOSITORIO]/issues

## Changelog

### Versión 1.0
- Implementación inicial
- Integración con módulo de contactos
- Sistema de alertas informativas
- Reportes PDF y Excel
- Soporte multimoneda completo
- Sistema de permisos y seguridad
- Pruebas unitarias básicas

---

**Desarrollado por Manus AI** - Soluciones inteligentes para Odoo

