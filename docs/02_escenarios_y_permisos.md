# Escenarios y permisos

## Sistema de gestión de comunicaciones FREBA

Documento de trabajo para describir cómo se comportan los distintos actores del sistema según el escenario en el que participan dentro de una comunicación.

Este documento no reemplaza el glosario ni el levantamiento de requerimientos.  
Su objetivo es aterrizar el dominio en reglas operativas concretas de:

- visibilidad
- edición
- interacción
- respuesta
- documentos
- estados
- colaboración

---

## 1. Objetivo del documento

Este archivo busca responder de forma operativa preguntas como:

- qué puede hacer un usuario externo cuando crea una comunicación
- qué puede hacer un usuario externo cuando debe responder una comunicación enviada por FREBA
- qué puede hacer un usuario interno de FREBA
- qué ve cada actor
- qué cosas son internas y cuáles son compartidas
- qué acciones dependen del rol y cuáles dependen del escenario

---

## 2. Criterios generales

### 2.1 Los permisos dependen de tres cosas

Los permisos de una persona sobre una comunicación dependen de:

- su organización
- su asignación a la comunicación
- su rol dentro de esa comunicación

Y además, en algunos casos, dependen también del **escenario operativo**.

---

### 2.2 No todo se define solo por rol

El mismo rol no siempre implica exactamente el mismo comportamiento si cambia el escenario.

Ejemplo:
- un externo que creó una comunicación para consultar algo a FREBA no opera igual que un externo que recibió una comunicación de FREBA y debe responderla

Por eso este documento organiza los permisos por **escenario + rol**.

---

### 2.3 Regla general de acceso externo

Los externos solo pueden actuar dentro de comunicaciones vinculadas a su propia organización.

Nunca pueden:

- asignar usuarios de otra organización
- ver expedientes
- acceder a chat interno FREBA
- ver historial interno completo
- ver documentos internos de trabajo de FREBA

---

### 2.4 Regla general de acceso interno FREBA

FREBA administra el dominio completo del sistema.

Los usuarios internos pueden tener acceso mucho más amplio, aunque dentro de una comunicación concreta sus acciones también dependen del rol que tengan asignado.

---

## 3. Escenarios principales

En esta etapa se reconocen cinco escenarios principales:

1. **Externo que crea una comunicación y espera respuesta**
2. **Externo que recibe una comunicación de FREBA y debe responder**
3. **Usuario interno FREBA que crea una comunicación**
4. **Usuario interno FREBA que trabaja activamente sobre una comunicación**
5. **Usuario interno FREBA con participación limitada o de seguimiento**

---

## 4. Escenario 1: externo que crea una comunicación y espera respuesta

### 4.1 Descripción

Es el caso en el que un usuario de una organización externa inicia una comunicación hacia FREBA.

Ejemplos:
- consulta
- nota
- pedido
- requerimiento

En este escenario, el externo:

- crea la comunicación
- carga los datos iniciales
- adjunta documentos iniciales
- y luego queda a la espera del tratamiento por parte de FREBA

---

### 4.2 Qué puede hacer

Puede:

- crear la comunicación
- completar el formulario del tipo correspondiente
- adjuntar documentación inicial
- ver la comunicación creada
- ver el estado actual
- ver la respuesta formal cuando exista
- participar del chat compartido mientras la comunicación esté abierta, si ese canal está habilitado para ese tipo de interacción
- generar una nueva comunicación relacionada por continuidad luego de una respuesta formal final (normalmente sobre una comunicación ya cerrada o finalizada) que pertenezca a su organización

---

### 4.3 Qué no puede hacer

No puede:

- seguir modificando libremente la comunicación como flujo normal después del envío inicial
- agregar nuevos usuarios a la comunicación
- ver usuarios internos de FREBA asignados
- ver historial interno
- ver expediente
- ver documentos internos de trabajo de FREBA
- ver chat interno FREBA
- responder formalmente esa misma comunicación en este escenario
- cambiar estados como operador activo de tratamiento

---

### 4.4 Qué ve

Ve:

- título
- descripción
- datos generales que él mismo cargó
- documentos iniciales cargados por su organización
- estado actual
- respuesta formal, si existe
- documentos finales incluidos en la respuesta
- chat compartido, si corresponde

No ve:

- asignaciones internas FREBA
- historial detallado de gestión
- chat interno
- documentos internos/intermedios cargados por FREBA
- expediente/s asociados

---

## 5. Escenario 2: externo que recibe una comunicación de FREBA y debe responder

### 5.1 Descripción

Es el caso en el que FREBA inicia una comunicación dirigida a una organización externa y espera una respuesta formal de esa organización.

Ejemplos:
- pedido de información
- solicitud documental
- requerimiento de respuesta
- consulta formal iniciada por FREBA

En este escenario, el externo pasa a tener un rol más activo.

---

### 5.2 Qué puede hacer

Puede:

- ver la comunicación recibida
- ver los documentos adjuntos visibles del envío inicial
- editar los datos habilitados de la comunicación
- cargar nuevos documentos
- generar nuevas versiones de documentos
- usar el chat compartido
- agregar usuarios de su misma organización
- cambiar el estado dentro del flujo operativo permitido
- emitir la respuesta formal
- ver la respuesta emitida una vez generada

---

### 5.3 Qué no puede hacer

No puede:

- asignar usuarios de otras organizaciones
- acceder al chat interno de FREBA
- ver historial interno detallado
- ver expediente
- ver documentos internos de trabajo de FREBA no expuestos al exterior
- administrar globalmente la comunicación fuera del alcance de su organización
- crear subcomunicaciones como regla general en `v0.2` (queda pendiente de definición de negocio)
- ejecutar el cierre administrativo final de la comunicación en `v0.2`

---

### 5.4 Qué ve

Ve:

- los datos generales de la comunicación
- el estado actual
- los documentos del envío inicial que FREBA expuso
- los documentos cargados por su propia organización
- el chat compartido
- la respuesta formal final

No ve:

- el chat interno FREBA
- el expediente
- usuarios internos FREBA no expuestos
- historial interno completo
- documentos de trabajo interno no publicados

---

### 5.5 Regla especial de colaboración organizacional externa

Cuando el externo está en escenario de respuesta, puede sumar usuarios de su misma organización para colaborar.

Esos usuarios:

- quedan limitados al ámbito de su organización
- no adquieren acceso a otras organizaciones
- no adquieren autoridad global sobre la comunicación
- participan solo dentro del alcance permitido por el sistema

---

## 6. Escenario 3: usuario interno FREBA que crea una comunicación

### 6.1 Descripción

Es el caso en el que un usuario de FREBA inicia una comunicación, ya sea:

- hacia una organización externa
- o como parte de una gestión interna vinculada al tratamiento de otra comunicación

---

### 6.2 Qué puede hacer

Puede:

- seleccionar el tipo de comunicación
- completar el formulario
- definir organización destino
- seleccionar uno o más usuarios destino
- adjuntar documentos
- enviar la comunicación
- asociarla a expediente si tiene el rol correspondiente
- crearla como comunicación relacionada a otra ya existente
- iniciar una gestión nueva desde cero

---

### 6.3 Consideraciones especiales

Cuando FREBA crea una comunicación hacia un externo:

- esa comunicación queda visible para la organización destino una vez enviada
- si más adelante FREBA necesita ajustar algo, puede quitar temporalmente la asignación externa, editar y volver a asignar

---

## 7. Escenario 4: usuario interno FREBA que trabaja activamente sobre una comunicación

### 7.1 Descripción

Es el caso típico de usuarios internos que analizan, gestionan y resuelven una comunicación.

Puede tratarse de usuarios de:

- mesa de entrada
- áreas técnicas
- áreas administrativas
- usuarios que deban intervenir para construir la solución o la respuesta

---

### 7.2 Qué puede hacer

Según rol operativo, puede:

- ver toda la comunicación
- ver historial completo
- usar chat interno
- usar chat compartido, si corresponde
- editar los datos de la comunicación mientras esté abierta
- cargar documentos
- generar nuevas versiones
- agregar o quitar usuarios
- cambiar estado
- asociar o desasociar expediente
- mover la comunicación de expediente
- crear subcomunicaciones
- emitir la respuesta formal
- reabrir la comunicación si el flujo lo permite y no existe respuesta final emitida

---

### 7.3 Qué ve

Ve:

- datos completos de la comunicación
- historial completo
- documentos y sus versiones
- asignaciones
- vínculos con otras comunicaciones
- expediente asociado
- chat interno
- chat compartido
- respuesta formal emitida

---

## 8. Escenario 5: usuario interno FREBA con participación limitada o de seguimiento

### 8.1 Descripción

Es el caso de usuarios de FREBA que no trabajan activamente sobre una comunicación, pero necesitan seguirla, observarla o estar informados.

En `v0.2`, este escenario se implementa como rol **observador**.

---

### 8.2 Qué puede hacer

Puede:

- ver la comunicación
- seguir su estado
- ver historial
- ver documentos
- ver relación con expediente
- ver la respuesta formal cuando exista

---

### 8.3 Qué no puede hacer en `v0.2`

No puede:

- editar
- cambiar estado
- responder
- reasignar usuarios
- asociar expedientes
- crear subcomunicaciones
- usar chat interno
- usar chat compartido

---

## 9. Matriz resumida por escenario

## 9.1 Externo que crea y espera respuesta

| Acción | Permitido |
|---|---|
| Crear comunicación | Sí |
| Editar luego del envío | No, como flujo normal |
| Ver estado | Sí |
| Ver respuesta formal | Sí |
| Subir más documentos luego del envío | No |
| Agregar usuarios | No |
| Usar chat compartido | Sí, cuando corresponda |
| Ver chat interno | No |
| Cambiar estado | No |
| Responder formalmente | No |
| Ver expediente | No |
| Crear réplica / hija tras respuesta formal final | Sí |

Operativamente, esta continuidad suele darse cuando la comunicación original ya quedó cerrada o finalizada.

---

## 9.2 Externo que recibe y debe responder

| Acción | Permitido |
|---|---|
| Ver comunicación | Sí |
| Editar datos habilitados | Sí |
| Subir documentos | Sí |
| Versionar documentos | Sí |
| Agregar usuarios de su organización | Sí |
| Usar chat compartido | Sí |
| Ver chat interno | No |
| Cambiar estado operativo | Sí |
| Cerrar comunicación (cierre administrativo) | No en `v0.2` |
| Emitir respuesta formal | Sí |
| Ver expediente | No |
| Crear subcomunicación | No habilitado en `v0.2` (pendiente de definición de negocio) |

---

## 9.3 Interno FREBA operativo

| Acción | Permitido |
|---|---|
| Crear comunicación | Sí |
| Editar comunicación abierta | Sí |
| Cambiar estado | Sí |
| Agregar o quitar usuarios | Sí |
| Asociar expediente | Sí |
| Crear subcomunicaciones | Sí |
| Usar chat interno | Sí |
| Usar chat compartido | Sí |
| Emitir respuesta formal | Sí |
| Ver historial completo | Sí |

---

## 10. Permisos por rol dentro de una comunicación

## 10.1 Observador

### Puede:
- ver la información permitida por su escenario
- seguir el estado
- consultar la respuesta formal cuando exista

### No puede:
- editar
- cambiar estado
- responder formalmente
- gestionar usuarios
- asociar expediente
- ver chat interno

### Observación:
En `v0.2`, el rol observador no usa chat compartido.

---

## 10.2 Editor

### Puede:
- editar comunicación abierta
- cambiar estado
- cargar documentos
- versionar documentos
- usar chat habilitado
- agregar o quitar usuarios
- asociar expediente
- crear subcomunicaciones
- emitir respuesta formal

---

## 10.3 Responsable

En `v0.2`, tiene el mismo alcance operativo que Editor.

Se mantiene como rol separado porque más adelante negocio podría definir diferencias, por ejemplo de ownership, seguimiento o decisión final.

---

## 11. Reglas de visibilidad

### 11.1 Visibilidad interna FREBA

Los usuarios internos con acceso operativo pueden ver:

- historial completo
- versiones documentales
- asignaciones
- expediente
- relación entre comunicaciones
- chat interno
- chat compartido

---

### 11.2 Visibilidad externa

Los usuarios externos no ven:

- expediente
- historial interno completo
- chat interno
- documentos internos no expuestos
- asignaciones internas completas de FREBA

Los usuarios externos sí pueden ver, según escenario:

- datos generales de la comunicación
- estado actual
- sus propios documentos
- adjuntos visibles del envío inicial
- respuesta formal
- documentos incluidos en la respuesta
- chat compartido cuando corresponda

---

## 12. Reglas de documentos

### 12.1 Regla general

Los documentos pertenecen a la comunicación y se versionan.

### 12.2 Regla de exposición externa

No todos los documentos de una comunicación son automáticamente visibles al externo.

Como criterio operativo:

- el externo ve los documentos que cargó
- el externo ve los documentos del envío inicial visibles para él
- el externo ve los documentos finales incluidos en la respuesta
- el externo no ve documentos internos de trabajo de FREBA

---

## 13. Reglas de chat

### 13.1 Chat interno

Visible solo para FREBA.

### 13.2 Chat compartido

Visible entre FREBA y la contraparte externa cuando el escenario lo requiera.

### 13.3 Restricciones

- no se borra
- no admite adjuntos propios
- mantiene cronología
- no reemplaza la respuesta formal

---

## 14. Reglas de cierre y continuidad

### 14.1 Cierre

Una comunicación puede cerrarse con o sin respuesta formal.

### 14.2 Reapertura

Puede reabrirse si no tiene respuesta final emitida y el rol lo permite.

### 14.3 Continuidad luego de una respuesta final

Si ya existe una respuesta formal final y el tema continúa, la continuación debe resolverse mediante una nueva comunicación relacionada, no sobre la misma comunicación como flujo normal.

---

## 15. Reglas de subcomunicaciones

### 15.1 Cuándo crear una subcomunicación

Debe crearse una subcomunicación cuando haga falta abrir una gestión formal separada, aunque vinculada al caso original.

Ejemplo:
- llega una comunicación principal
- para poder responderla, FREBA necesita pedir información a otras organizaciones
- se crean nuevas comunicaciones hijas hacia esas organizaciones

### 15.2 Cuándo no hace falta crear subcomunicación

No hace falta crear una subcomunicación cuando solo se necesita que más personas trabajen sobre la misma comunicación original.

En ese caso corresponde:
- asignar nuevos usuarios
- seguir trabajando sobre la comunicación existente

---

## 16. Pendientes que todavía deben refinarse

### 16.1 Diferencia fina entre Editor y Responsable
Por ahora se consideran equivalentes.

### 16.2 Transiciones exactas por estado
Todavía falta definir qué estados concretos puede mover cada actor según tipo.

### 16.3 Visibilidad organizacional externa fina
Todavía falta bajar con más precisión:
- qué ve cualquier usuario de una organización
- qué ve solo un usuario asignado

### 16.4 Roles de los usuarios agregados por externos
Todavía puede refinarse si esos usuarios entran siempre con el mismo rol o si eso será configurable.

### 16.5 Casos reales por tipo
Faltan casos reales para probar si esta matriz cubre bien los escenarios del negocio.

---

## 17. Uso recomendado de este documento

Este archivo debe usarse como base para:

- diseño de pantallas
- definición de API y permisos
- diseño de backend
- revisión funcional
- instrucciones a agentes de análisis o implementación

No debe usarse aislado.  
Debe leerse junto con:

- `00_requerimientos_base_v0_2.md`
- `01_glosario_dominio.md`
- `03_modelo_conceptual.md`
- `04_decisiones_y_supuestos.md`
- `05_plan_implementacion.md`

---
