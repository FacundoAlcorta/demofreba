# Plan de implementación

## Sistema de gestión de comunicaciones FREBA
## Backend con Django + Django REST Framework

Documento de trabajo para organizar la implementación incremental del sistema en backend, priorizando coherencia de dominio, trazabilidad y capacidad de evolución.

Este plan está pensado para:

- desarrollar por fases cortas
- no perder el contexto funcional
- evitar reescrituras grandes
- poder validar el dominio mientras se implementa
- construir una base estable antes de agregar complejidad

---

## 1. Objetivo del plan

Este plan busca transformar el diseño funcional y conceptual del sistema en una implementación backend concreta sobre Django REST Framework, de forma incremental y controlada.

El criterio principal es:

- primero construir el núcleo del dominio
- luego agregar capacidades operativas
- después sumar contexto, trazabilidad y administración
- y recién al final refinar automatismos, performance y mejoras

---

## 2. Principios de implementación

### 2.1 El dominio manda
La implementación debe respetar los documentos base:

- `00_requerimientos_base_v0_2.md`
- `01_glosario_dominio.md`
- `02_escenarios_y_permisos.md`
- `03_modelo_conceptual.md`
- `04_decisiones_y_supuestos.md`

No debe inventarse comportamiento por fuera de esos documentos sin dejarlo explícito.

---

### 2.2 Primero simple, después refinado
En la primera implementación se prioriza:

- claridad de dominio
- consistencia de permisos
- trazabilidad
- y orden del modelo

No se debe arrancar con automatismos complejos ni hiperconfiguración.

---

### 2.3 Separar configuración de operación
Desde el inicio debe distinguirse entre:

- entidades de configuración
- entidades operativas

Esto evita mezclar catálogos, workflows y tipos con comunicaciones reales.

---

### 2.4 Implementar por módulos pequeños
Cada fase debe dejar algo funcional y comprobable, aunque sea acotado.

No conviene esperar a “tener todo” para recién probar.

---

### 2.5 No optimizar demasiado temprano
Primero debe quedar bien modelado y testeado.  
La optimización de performance, cache, consultas complejas y automatismos queda para una etapa posterior.

---

## 3. Stack propuesto

### Backend base
- Python
- Django
- Django REST Framework

### Complementos recomendados
- PostgreSQL
- django-filter
- drf-spectacular o drf-yasg para documentación
- pytest o Django TestCase para tests
- factory_boy para fixtures si querés escalar testing
- celery más adelante si incorporás notificaciones o procesos diferidos

---

## 4. Estructura modular sugerida

Se recomienda dividir el backend en apps de dominio relativamente claras.

### 4.1 Apps sugeridas

#### `organizations`
- organizaciones
- tipos de organización si hiciera falta

#### `users`
- usuario
- perfiles
- relación usuario-organización
- representaciones múltiples si más adelante se habilitan

#### `communication_config`
- tipo de comunicación
- workflow
- estados
- bandejas
- configuraciones base

#### `communications`
- comunicación base
- datos particulares por tipo
- relaciones entre comunicaciones
- asignaciones
- roles sobre comunicación
- respuesta formal

#### `documents`
- documento
- versión de documento
- exposición documental

#### `chats`
- mensajes
- ámbitos de chat
- visibilidad

#### `expedients`
- expediente
- asociación comunicación-expediente

#### `audit`
- eventos de historial
- trazabilidad

#### `permissions`
- reglas reutilizables de acceso
- permission classes
- servicios de validación de permisos

No es obligatorio usar exactamente esta separación, pero sí conviene mantener una división equivalente.

---

## 5. Orden general de implementación

El orden recomendado es este:

1. base del proyecto y autenticación
2. organizaciones y usuarios
3. configuración de tipos y workflows
4. comunicación base
5. asignaciones y roles
6. permisos mínimos por escenario
7. documentos y versionado
8. respuesta formal
9. chats
10. subcomunicaciones
11. expedientes
12. historial / auditoría
13. listados, filtros y vistas de operación
14. endurecimiento de permisos
15. tests integrales
16. documentación y preparación para frontend

---

## 6. Fase 0 — Preparación del proyecto

### Objetivo
Dejar el proyecto listo para comenzar a construir sin mezclar decisiones de dominio con setup técnico improvisado.

### Tareas
- crear proyecto Django
- definir settings por ambiente
- conectar PostgreSQL
- configurar DRF
- definir convención de apps
- definir convención de serializers, services y permissions
- configurar documentación de API
- configurar linting / formateo si lo vas a usar
- definir estrategia de tests

### Entregables
- proyecto base corriendo
- estructura de carpetas definida
- documentación mínima de arranque
- app de salud o endpoint simple de verificación

### Criterio de cierre
El proyecto puede levantarse localmente, conectarse a DB y exponer una API mínima documentada.

---

## 7. Fase 1 — Usuarios, organizaciones y autenticación

### Objetivo
Implementar la base de identidad del sistema.

### Incluye
- modelo de Organización
- modelo de Usuario
- relación usuario-organización
- tipo interno / externo
- posibilidad futura de multi-organización, aunque no necesariamente habilitada al inicio
- autenticación
- endpoint de perfil actual

### Tareas
- definir modelos
- definir si extendés `AbstractUser` o usás perfil asociado
- exponer endpoints mínimos:
  - login / auth
  - usuario actual
  - listado básico de organizaciones
- definir flags funcionales:
  - usuario interno
  - usuario externo
  - organización activa

### Entregables
- usuarios autenticados
- organizaciones persistidas
- relación usuario-organización operativa

### Criterio de cierre
El backend puede identificar correctamente:
- quién es el usuario
- a qué organización representa
- si es interno o externo

---

## 8. Fase 2 — Configuración base de comunicaciones

### Objetivo
Construir el módulo configurable mínimo para que el dominio de comunicación no quede hardcodeado.

### Incluye
- Tipo de Comunicación
- Workflow
- Estado
- Bandeja

### Tareas
- modelar `CommunicationType`
- modelar `Workflow`
- modelar `WorkflowState`
- modelar `Inbox` o equivalente simple
- permitir asociar:
  - tipo ↔ workflow
  - tipo ↔ bandeja
  - tipo ↔ reglas mínimas de creación
- dejar validado que el estado inicial de una comunicación pertenece al workflow asociado a su tipo
- exponer endpoints de consulta para configuración

### Entregables
- catálogo de tipos
- catálogo de estados
- bandejas configuradas
- workflow por defecto

### Criterio de cierre
Ya se puede decir:
- qué tipo existe
- con qué estado inicial arranca
- a qué bandeja cae
- quién puede iniciarlo

---

## 9. Fase 3 — Comunicación base

### Objetivo
Implementar la entidad principal del sistema.

### Incluye
- modelo `Communication`
- campos comunes
- emisor / destino
- estado actual
- tipo
- timestamps
- datos de creación y edición

### Tareas
- modelar `Communication`
- definir:
  - creador
  - organización emisora
  - organización destino
  - tipo
  - estado actual
  - título
  - descripción
  - fechas
- validar que `current_state` pertenezca al workflow asociado al tipo de comunicación
- definir reglas iniciales de creación:
  - creación por externo
  - creación por FREBA
- exponer CRUD base controlado

### Entregables
- creación de comunicación
- lectura de comunicación
- edición de comunicación abierta
- cierre básico de comunicación

### Criterio de cierre
Ya existe una comunicación persistida y navegable como objeto principal.

---

## 10. Fase 4 — Datos particulares por tipo

### Objetivo
Resolver la especialización estructural de las comunicaciones.

### Incluye
- tablas específicas por tipo
- validación de datos particulares
- acoplamiento limpio con la comunicación base

### Tareas
- elegir estrategia concreta:
  - one-to-one por subtipo
  - tabla especializada por tipo
- implementar al menos un subtipo real de ejemplo
- definir cómo crear y leer:
  - comunicación base
  - datos particulares del tipo
- unificar respuesta API para que el frontend no reciba todo fragmentado

### Entregables
- estructura base + especialización funcionando
- un tipo de comunicación real implementado de punta a punta

### Criterio de cierre
Ya podés crear una comunicación con:
- datos comunes
- datos particulares según el tipo

---

## 11. Fase 5 — Asignaciones y roles sobre comunicación

### Objetivo
Implementar la participación real de usuarios dentro de cada comunicación.

### Incluye
- asignación usuario ↔ comunicación
- roles sobre comunicación
- reglas mínimas de visibilidad

### Tareas
- modelar `CommunicationAssignment`
- modelar catálogo o choices de rol:
  - observador
  - editor
  - responsable
- implementar:
  - agregar usuario
  - quitar usuario
  - consultar participantes
- contemplar regla externa:
  - solo usuarios de su misma organización cuando asigna un externo en escenario de respuesta

### Entregables
- asignaciones operativas
- roles por comunicación funcionando

### Criterio de cierre
Ya se puede saber con precisión:
- quién participa de una comunicación
- con qué rol
- y desde qué organización

---

## 12. Fase 6 — Permisos mínimos por escenario

### Objetivo
Bajar a código las reglas principales de acceso.

### Incluye
- permisos por escenario
- permisos por rol
- restricciones internas / externas

### Tareas
- implementar `permission classes`
- implementar helpers o servicios como:
  - `can_view_communication(user, communication)`
  - `can_edit_communication(user, communication)`
  - `can_change_state(user, communication)`
  - `can_answer_communication(user, communication)`
  - `can_assign_users(user, communication)`
- cubrir al menos estos escenarios:
  - externo que crea y espera respuesta
  - externo que recibe y debe responder
  - interno FREBA operativo
  - interno FREBA observador
- cerrar perfil MVP ejecutable para acciones núcleo sin interpretación libre por endpoint:
  - ver comunicación
  - editar comunicación
  - cambiar estado
  - emitir respuesta formal
  - ver/subir/versionar documentos
  - usar chat interno y chat compartido
  - agregar/quitar participantes
  - crear subcomunicación
- implementar en `v0.2` equivalencia operativa estricta entre roles editor y responsable

### Entregables
- permisos mínimos consistentes
- endpoints protegidos por reglas reales

### Criterio de cierre
Ya no dependés de permisos globales solo por tipo de usuario, sino por contexto real de la comunicación.

---

## 13. Fase 7 — Documentos y versionado

### Objetivo
Implementar el soporte documental central del sistema.

### Incluye
- documento
- versión de documento
- metadatos
- exposición restringida a externos

### Tareas
- modelar `Document`
- modelar `DocumentVersion`
- definir estrategia de storage
- implementar:
  - subir documento
  - listar documentos de una comunicación
  - subir nueva versión
  - obtener última versión
- definir visibilidad:
  - documentos cargados por su propia organización
  - adjuntos expuestos en el envío inicial
  - documentos incluidos en la respuesta formal
  - documentos internos de trabajo no visibles para externos

### Entregables
- documentos versionados funcionando
- reglas mínimas de exposición

### Criterio de cierre
Una comunicación ya puede trabajar documentos de forma seria y trazable.

---

## 14. Fase 8 — Respuesta formal

### Objetivo
Implementar la pieza formal y final de la comunicación.

### Incluye
- modelo de respuesta formal
- texto de respuesta
- selección de documentos incluidos en la respuesta
- congelamiento posterior

### Tareas
- modelar `FormalResponse`
- modelar relación por `communication_id` único como fuente única de verdad (sin referencia paralela en `Communication`)
- modelar selección de documentos de respuesta referenciando versiones documentales concretas
- implementar endpoint para emitir respuesta
- bloquear edición posterior
- exponer visibilidad de respuesta a todos los participantes con acceso

### Entregables
- emisión de respuesta formal
- respuesta congelada e inmutable

### Criterio de cierre
El sistema ya puede resolver un caso formalmente.

---

## 15. Fase 9 — Chat interno y chat compartido

### Objetivo
Implementar la colaboración conversacional.

### Incluye
- chat interno FREBA
- chat compartido con externos
- cronología de mensajes

### Tareas
- modelar `CommunicationMessage`
- definir campo `scope` o equivalente:
  - `internal`
  - `shared`
- implementar:
  - publicar mensaje
  - listar mensajes según visibilidad
- validar:
  - externo nunca ve chat interno
  - externo solo accede al chat compartido cuando el escenario lo permite

### Entregables
- conversaciones separadas por ámbito
- visibilidad consistente

### Criterio de cierre
La comunicación ya soporta colaboración operativa sin mezclarla con la respuesta formal.

---

## 16. Fase 10 — Subcomunicaciones / relaciones entre comunicaciones

### Objetivo
Implementar la relación madre-hija.

### Incluye
- vínculos entre comunicaciones
- navegación contextual
- continuidad del caso

### Tareas
- modelar relación recursiva
- operar en `v0.2` con vínculo canónico `child_of`
- implementar creación de hija desde una madre
- listar hijas de una comunicación
- mostrar madre de una comunicación
- exponer resumen contextual

### Entregables
- comunicaciones relacionadas funcionando
- continuidad del caso correctamente modelada

### Criterio de cierre
Ya se puede abrir una nueva gestión formal relacionada con otra.

---

## 17. Fase 11 — Expedientes

### Objetivo
Incorporar el agrupador administrativo sin romper el foco en comunicación.

### Incluye
- expediente
- asociación a comunicación
- propagación a hijas

### Tareas
- modelar `Expedient`
- modelar asociación comunicación-expediente
- implementar:
  - crear expediente
  - asociar comunicación
  - mover comunicación a otro expediente
- implementar propagación básica a hijas según la regla acordada

### Entregables
- expedientes funcionales
- comunicaciones agrupadas administrativamente

### Criterio de cierre
FREBA ya puede ordenar casos complejos dentro de expedientes.

---

## 18. Fase 12 — Historial y auditoría

### Objetivo
Dar trazabilidad completa al sistema.

### Incluye
- eventos de historial
- auditoría interna
- exposición externa limitada

### Tareas
- modelar `CommunicationEvent`
- registrar eventos al menos para:
  - creación
  - edición
  - cambio de estado
  - asignación
  - carga documental
  - nueva versión
  - respuesta emitida
  - asociación a expediente
  - creación de hija
- exponer historial completo para FREBA
- exponer solo lo mínimo para externos, si corresponde

### Entregables
- historial navegable
- trazabilidad real del caso

### Criterio de cierre
Ya se puede reconstruir de punta a punta el ciclo de vida de una comunicación.

---

## 19. Fase 13 — Listados y vistas operativas

### Objetivo
Hacer usable la API para la operación real.

### Incluye
- listados
- filtros
- vistas por escenario
- resumen de comunicaciones

### Tareas
- endpoint de listado de comunicaciones
- filtros por:
  - tipo
  - estado
  - organización
  - fecha
  - expediente
  - participación del usuario
- vistas específicas:
  - bandeja de entrada FREBA
  - comunicaciones creadas por mí
  - comunicaciones donde participo
  - comunicaciones externas de mi organización
- optimizar serializers de resumen vs detalle

### Entregables
- API usable para pantallas principales

### Criterio de cierre
El frontend ya puede construir la mayor parte de las pantallas operativas.

---

## 20. Fase 14 — Endurecimiento de permisos y reglas finas

### Objetivo
Refinar el modelo para hacerlo más seguro y cercano a producción.

### Incluye
- reglas más estrictas por transición
- refinamiento de visibilidad
- restricciones externas más finas

### Tareas
- revisar todos los endpoints
- refinar:
  - quién ve qué
  - quién puede mover qué estado
  - qué documentos se exponen
  - cuándo puede responder un externo
- preparar una matriz más fina de permisos

### Entregables
- permisos más robustos
- reducción de ambigüedades funcionales

### Criterio de cierre
El backend ya no depende de supuestos demasiado abiertos para operar.

---

## 21. Fase 15 — Tests funcionales y de integración

### Objetivo
Asegurar que el sistema no se rompa al crecer.

### Incluye
- tests de modelo
- tests de permisos
- tests de flujos principales
- tests de API

### Tareas
Cubrir al menos:

- creación por externo
- creación por FREBA
- asignaciones
- documentos y versiones
- respuesta formal
- subcomunicaciones
- expediente
- permisos por escenario
- visibilidad externa restringida

### Entregables
- suite mínima confiable de tests

### Criterio de cierre
El sistema puede evolucionar sin romper fácilmente las reglas centrales del dominio.

---

## 22. Fase 16 — Documentación técnica y preparación para frontend

### Objetivo
Dejar el backend claro, consumible y listo para integración.

### Incluye
- documentación de endpoints
- ejemplos de payloads
- errores esperables
- convenciones de respuesta

### Tareas
- documentar con OpenAPI / Swagger
- definir contratos claros para:
  - comunicación detalle
  - comunicación resumen
  - respuesta formal
  - documentos
  - historial
  - mensajes
- documentar endpoints por módulo

### Entregables
- API documentada
- base estable para frontend

### Criterio de cierre
El frontend puede integrarse sin adivinar el comportamiento del backend.

---

## 23. Orden sugerido de construcción de modelos

El orden recomendado de implementación de modelos sería:

1. Organización
2. Usuario
3. Workflow
4. Estado
5. Bandeja
6. Tipo de Comunicación
7. Comunicación
8. Datos particulares por tipo
9. Asignación de Usuario a Comunicación
10. Documento
11. Versión de Documento
12. Respuesta Formal
13. Mensaje / Chat
14. Relación entre Comunicaciones
15. Expediente
16. Asociación Comunicación–Expediente
17. Evento / Historial

---

## 24. Orden sugerido de construcción de APIs

1. autenticación / usuario actual
2. organizaciones
3. tipos de comunicación y catálogos
4. comunicaciones base
5. asignaciones
6. documentos
7. respuesta formal
8. mensajes
9. subcomunicaciones
10. expedientes
11. historial
12. listados y filtros avanzados

---

## 25. Qué no conviene implementar demasiado temprano

No conviene arrancar por:

- automatismos de notificaciones
- reglas hiperfinas de transición
- métricas complejas
- expedientes múltiples reales
- administración ultra rica de bandejas
- configuración dinámica excesiva desde interfaz
- optimizaciones prematuras de performance

Primero tiene que quedar sólido el núcleo.

---

## 26. Hitos recomendados

### Hito 1 — Núcleo básico operativo
Hasta Fase 6.
Ya existe:
- usuario
- organización
- tipo
- workflow
- comunicación
- asignaciones
- permisos mínimos

### Hito 2 — Comunicación resoluble
Hasta Fase 8.
Ya existe:
- documento
- versiones
- respuesta formal

### Hito 3 — Comunicación colaborativa real
Hasta Fase 10.
Ya existe:
- chat
- subcomunicaciones

### Hito 4 — Contexto administrativo completo
Hasta Fase 12.
Ya existe:
- expediente
- historial

### Hito 5 — Base lista para frontend real
Hasta Fase 16.
Ya existe:
- API documentada
- filtros
- permisos endurecidos
- tests

---

## 27. Recomendación de estrategia de desarrollo

### 27.1 Enfoque recomendado
Desarrollo por iteraciones cortas, cerrando cada fase antes de abrir demasiados frentes en paralelo.

### 27.2 Regla práctica
Cada fase debería terminar con:

- modelos listos
- serializers listos
- endpoints mínimos funcionando
- tests mínimos
- documentación actualizada

### 27.3 Regla de control de contexto
Antes de empezar una fase nueva, revisar:

- qué decisiones del dominio impacta
- qué supuestos usa
- qué pendientes deja abiertos
- si contradice algo del `v0.2`

---

## 28. Riesgos a vigilar durante la implementación

### 28.1 Pérdida del centro del dominio
Riesgo: empezar a modelar todo alrededor de expedientes o documentos en vez de comunicaciones.

### 28.2 Permisos dispersos
Riesgo: meter lógica de permisos repartida por serializers, views y modelos sin una capa clara.

### 28.3 Demasiada complejidad en tipos
Riesgo: que los subtipos de comunicación se vuelvan inmanejables.

### 28.4 Exposición externa accidental
Riesgo: filtrar información interna a usuarios externos por no modelar bien visibilidad.

### 28.5 Mezcla entre chat y respuesta
Riesgo: terminar usando el chat como respuesta oficial o al revés.

---

## 29. Uso recomendado de este documento

Este archivo debe usarse para:

- organizar sprints o etapas
- dar instrucciones a agentes de implementación
- revisar dependencias entre módulos
- evitar arrancar por piezas adelantadas
- mantener el contexto del dominio durante el desarrollo

Debe leerse junto con:

- `00_requerimientos_base_v0_2.md`
- `01_glosario_dominio.md`
- `02_escenarios_y_permisos.md`
- `03_modelo_conceptual.md`
- `04_decisiones_y_supuestos.md`

---
