# Plan Real de Implementacion Backend (v0.2)

## Sistema de gestion de comunicaciones FREBA

## 1. Objetivo y alcance

Este documento define el plan real de construccion del backend en Django + DRF para `v0.2`, alineado con:

- `00_requerimientos_base_v0_2.md` (fuente principal)
- `01_glosario_dominio.md`
- `02_escenarios_y_permisos.md`
- `03_modelo_conceptual.md`
- `04_decisiones_y_supuestos.md`
- `05_plan_implementacion.md`
- `06_modelo_relacional_preliminar.md`
- `07_matriz_permisos_y_transiciones.md`
- `design/08_diseno_tecnico_modelos_django.md`
- `design/09_diseno_tecnico_permisos_backend.md`
- `design/10_diseno_tecnico_apps_y_modulos.md`
- `design/11_diseno_tecnico_servicios_y_casos_de_uso.md`
- `design/12_diseno_tecnico_api_base.md`

No incluye codigo.  
Define orden, fases, dependencias, entregables y criterio de cierre para ejecutar implementacion real sin interpretacion excesiva.

---

## 2. Principios del plan de implementacion

### 2.1 Primero nucleo, despues colaboracion y contexto

Primero se cierra `communication` + estado + asignacion + permisos base.  
Luego documentos y respuesta formal.  
Despues chat, subcomunicaciones, expediente e historial.

### 2.2 Primero contrato de dominio, despues API completa

No conviene abrir todos los endpoints al inicio.  
Cada fase cierra primero modelos + servicios + reglas, y luego expone API de forma incremental.

### 2.3 Permisos nucleo primero, fine-tuning despues

Se implementa primero la capa reusable de autorizacion para acciones nucleo.  
El endurecimiento fino por escenario extremo queda para fases finales.

### 2.4 Evitar paralelismo que rompa dependencias

No abrir muchas apps sin base comun.  
Paralelizar solo cuando el contrato owner/colaborador este cerrado.

### 2.5 Cada fase debe dejar un incremento usable

Cada fase cierra con:

- entregables verificables
- endpoints operativos minimos
- validaciones funcionales y de permisos
- criterio de pase a la fase siguiente

---

## 3. Estrategia general de construccion

Estrategia recomendada: **fases secuenciales con hitos de integracion**, con paralelismo controlado en tareas de soporte.

1. Construir base tecnica y de identidad.
2. Cerrar configuracion de tipos/workflow/estados.
3. Implementar comunicacion central y estado inicial.
4. Incorporar asignacion, escenario y permisos operativos.
5. Cerrar documentos/versionado y luego respuesta formal.
6. Agregar colaboracion (chat), continuidad (`child_of`) y contexto (`expedient`).
7. Integrar auditoria/historial interno y endurecer contratos API.

Justificacion:

- sigue el orden de `05_plan_implementacion.md`
- respeta ownership de apps de `design/10`
- respeta orden de modelos de `design/08`
- respeta secuencia de servicios de `design/11`
- respeta orden de API de `design/12`

---

## 4. Mapa de fases y dependencias

| Fase | Nombre | Depende de | Habilita |
|---|---|---|---|
| 0 | Bootstrap tecnico | - | Base de trabajo estable |
| 1 | Identidad y organizaciones | 0 | Contexto de actor y organizacion activa |
| 2 | Configuracion de comunicacion | 1 | Tipo, workflow, estados e inbox usables |
| 3 | Comunicacion nucleo | 2 | CU-01/CU-02/CU-03 y lectura base |
| 4 | Asignaciones y permisos nucleo | 3 | Operacion activa por escenario y rol |
| 5 | Documentos y versionado | 4 | CU-13/CU-14 y visibilidad documental |
| 6 | Respuesta formal | 5 | CU-09, cierre funcional y continuidad |
| 7 | Chats | 6 | CU-15/CU-16 separados de respuesta formal |
| 8 | Subcomunicaciones (`child_of`) | 6 | CU-10 y continuidad post-respuesta |
| 9 | Expediente principal | 4 | CU-11/CU-12 contexto administrativo |
| 10 | Auditoria + historial interno | 6 | CU-19 trazabilidad interna |
| 11 | Endurecimiento API y validaciones | 7,8,9,10 | Backend listo para integracion frontend |

Notas de secuencia:

- Fases `7`, `8` y `9` pueden avanzar en paralelo una vez cerrada fase `6`.
- Fase `10` puede iniciar en paralelo con `7/8/9` pero se recomienda cerrarla antes de `11`.

---

## 5. Fases reales de implementacion

## 5.1 Fase 0 - Bootstrap tecnico del backend

- Objetivo de la fase: dejar proyecto Django/DRF ejecutable, con convenciones de arquitectura y testing.
- Por que va en este momento: evita que decisiones de dominio queden mezcladas con setup.
- Apps/modulos involucrados: proyecto base, `accounts` (minimo), `organizations` (minimo), `permissions_support` (esqueleto).
- Modelos involucrados: ninguno de negocio cerrado aun.
- Servicios/casos de uso involucrados: ninguno de dominio; solo infraestructura.
- Endpoints/API involucrados: `GET /health` (o equivalente tecnico), base de autenticacion.
- Permisos o reglas criticas involucradas: autenticacion base y contexto de usuario autenticado.
- Entregables concretos de la fase:
  - proyecto inicial operativo
  - configuracion por ambientes
  - pipeline minimo de tests/lint
  - convencion de carpetas para servicios/autorizacion
- Riesgos principales:
  - extender fase tecnica y frenar dominio
  - definir arquitectura demasiado compleja temprano
- Criterios de cierre de la fase:
  - backend levanta en local y CI
  - hay base de autenticacion y estructura modular inicial
- Que no conviene intentar todavia en esta fase:
  - endpoints de negocio
  - reglas de permisos por escenario
  - modelo de comunicacion

## 5.2 Fase 1 - Identidad, organizaciones y contexto activo

- Objetivo de la fase: resolver actor, membresia y organizacion activa como base de autorizacion.
- Por que va en ese momento: toda inferencia de escenario depende de esto (`design/09`).
- Apps/modulos involucrados: `organizations`, `accounts`.
- Modelos involucrados:
  - `Organization`
  - `UserOrganizationMembership`
- Servicios/casos de uso involucrados:
  - resolucion de membresias activas
  - cambio de organizacion activa
- Endpoints/API involucrados:
  - `GET /api/v1/me/`
  - `GET /api/v1/me/memberships/`
  - `POST /api/v1/me/active-membership/`
- Permisos o reglas criticas involucradas:
  - actor siempre opera en contexto de organizacion activa
  - base para distinguir FREBA vs externo
- Entregables concretos de la fase:
  - identidad organizacional usable por todo servicio
  - endpoints `me` operativos
  - datos semilla de organizaciones/membresias
- Riesgos principales:
  - no fijar correctamente organizacion activa y romper permisos luego
- Criterios de cierre de la fase:
  - backend identifica actor + organizacion activa + tipo de actor
  - servicios pueden consumir ese contexto de forma uniforme
- Que no conviene intentar todavia en esta fase:
  - reglas completas de escenario
  - workflow de comunicacion

## 5.3 Fase 2 - Configuracion base de comunicacion

- Objetivo de la fase: dejar tipologia, workflow y estados listos para crear comunicaciones validas.
- Por que va en ese momento: `communication` depende de `communication_type` + `workflow` + `workflow_state`.
- Apps/modulos involucrados: `communication_config`.
- Modelos involucrados:
  - `Workflow`
  - `WorkflowState`
  - `CommunicationType`
  - `Inbox`
  - `InboxUser`
- Servicios/casos de uso involucrados:
  - lookup de tipos y estados por tipo
  - validacion de estado inicial
- Endpoints/API involucrados:
  - `GET /api/v1/communication-types/`
  - `GET /api/v1/communication-types/{type_id}/`
  - `GET /api/v1/communication-types/{type_id}/states/`
  - `GET /api/v1/inboxes/`
- Permisos o reglas criticas involucradas:
  - cada tipo referencia workflow valido
  - estado inicial pertenece al workflow del tipo
- Entregables concretos de la fase:
  - catalogos cargables y consultables
  - contrato `type -> workflow -> state` validado
- Riesgos principales:
  - hardcodear estados en servicios/endpoints
- Criterios de cierre de la fase:
  - se puede resolver estado inicial valido por tipo
  - catologos listos para UI y servicios
- Que no conviene intentar todavia en esta fase:
  - transiciones finas persistidas
  - permisos de mutacion por escenario

## 5.4 Fase 3 - Comunicacion nucleo y estado inicial

- Objetivo de la fase: implementar entidad central `Communication` y operaciones base de alta/edicion/consulta.
- Por que va en ese momento: es el nucleo del dominio y habilita casi todas las fases siguientes.
- Apps/modulos involucrados: `communications`, `communication_config`, `accounts`, `organizations`.
- Modelos involucrados:
  - `Communication`
  - subtabla por tipo (`Communication<tipo>Data`) para primeros tipos activos
- Servicios/casos de uso involucrados:
  - CU-01 crear comunicacion externa
  - CU-02 crear comunicacion interna
  - CU-03 editar comunicacion abierta
  - CU-17 consultar detalle
- Endpoints/API involucrados:
  - `GET /api/v1/communications/`
  - `GET /api/v1/communications/{communication_id}/`
  - `POST /api/v1/communications/external/`
  - `POST /api/v1/communications/internal/`
  - `PATCH /api/v1/communications/{communication_id}/`
- Permisos o reglas criticas involucradas:
  - estado inicial obligatorio del workflow
  - sin borradores en `v0.2`
  - visibilidad inicial por organizacion/escenario
- Entregables concretos de la fase:
  - comunicacion creada y persistida con estado inicial valido
  - listado/detalle base operativo
  - edicion de abierta con validaciones minimas
- Riesgos principales:
  - intentar resolver todos los escenarios externos de una vez
  - mezclar reglas de documentos/respuesta formal prematuramente
- Criterios de cierre de la fase:
  - CU-01/CU-02/CU-03/CU-17 funcionales en happy path y denegaciones basicas
- Que no conviene intentar todavia en esta fase:
  - chat
  - expediente
  - respuesta formal completa

## 5.5 Fase 4 - Asignaciones, escenario y permisos nucleo

- Objetivo de la fase: cerrar operacion activa por asignacion + rol + escenario.
- Por que va en ese momento: sin esto no hay control robusto de mutaciones.
- Apps/modulos involucrados: `communications`, `permissions_support`, `accounts`, `organizations`.
- Modelos involucrados:
  - `CommunicationAssignment`
- Servicios/casos de uso involucrados:
  - CU-04 asignar participante
  - CU-05 quitar participante
  - CU-06 cambiar estado
  - CU-07 cerrar comunicacion
  - CU-08 reabrir comunicacion
- Endpoints/API involucrados:
  - `GET/POST/DELETE /api/v1/communications/{id}/participants/...`
  - `POST /api/v1/communications/{id}/state-transitions/`
  - `POST /api/v1/communications/{id}/close/`
  - `POST /api/v1/communications/{id}/reopen/`
- Permisos o reglas criticas involucradas:
  - precedencia estable para inferir escenario (6 pasos de `design/09`)
  - `editor` y `responsible` equivalentes en `v0.2`
  - externos ven participantes solo de su organizacion
  - E2 no realiza cierre administrativo final
  - estado no define escenario; solo condiciona accion
- Entregables concretos de la fase:
  - autorizacion reusable central
  - transiciones validas en capa de servicio (sin motor persistente completo)
  - matriz nucleo de permisos implementada para acciones base
- Riesgos principales:
  - dispersar autorizacion en views/serializers
  - no separar visibilidad de accion
- Criterios de cierre de la fase:
  - CU-04..CU-08 operan con denegaciones correctas por actor/escenario
  - no hay mutacion permitida fuera de asignacion/rol habilitante
- Que no conviene intentar todavia en esta fase:
  - reglas finas por todos los tipos especiales
  - optimizacion avanzada de querysets

## 5.6 Fase 5 - Documentos y versionado

- Objetivo de la fase: implementar ciclo documental base y regla funcional de visibilidad externa.
- Por que va en ese momento: respuesta formal depende de documentos/versiones.
- Apps/modulos involucrados: `documents`, `communications`, `permissions_support`.
- Modelos involucrados:
  - `Document`
  - `DocumentVersion`
- Servicios/casos de uso involucrados:
  - CU-13 subir documento
  - CU-14 subir nueva version documental
  - CU-18 consultar documentos visibles
- Endpoints/API involucrados:
  - `GET/POST /api/v1/communications/{id}/documents/`
  - `GET/POST /api/v1/communications/{id}/documents/{document_id}/versions/`
- Permisos o reglas criticas involucradas:
  - visibilidad externa por regla funcional (no solo flag tecnico):
    - propios de su organizacion
    - expuestos en envio inicial
    - incluidos en respuesta formal
    - no internos FREBA
- Entregables concretos de la fase:
  - alta documental y versionado operativo
  - filtro de visibilidad documental interno/externo consistente
- Riesgos principales:
  - mezclar versionado con emision formal en una sola operacion
- Criterios de cierre de la fase:
  - CU-13/CU-14/CU-18 pasan validaciones de visibilidad y autorizacion
- Que no conviene intentar todavia en esta fase:
  - metadatos documentales avanzados no necesarios para `v0.2`

## 5.7 Fase 6 - Respuesta formal

- Objetivo de la fase: cerrar respuesta formal unica, final e inmutable.
- Por que va en ese momento: requiere estado, permisos y documentos ya consolidados.
- Apps/modulos involucrados: `communications`, `documents`, `permissions_support`.
- Modelos involucrados:
  - `FormalResponse`
  - `FormalResponseDocument`
- Servicios/casos de uso involucrados:
  - CU-09 emitir respuesta formal
- Endpoints/API involucrados:
  - `GET /api/v1/communications/{id}/formal-response/`
  - `POST /api/v1/communications/{id}/formal-response/`
- Permisos o reglas criticas involucradas:
  - una sola respuesta formal por comunicacion
  - inmutabilidad una vez emitida
  - separacion estricta respecto de chat
  - `GET formal-response` en visible sin respuesta: `200` con `null`
- Entregables concretos de la fase:
  - flujo de emision formal operativo
  - contrato API cerrado para lectura sin respuesta existente
- Riesgos principales:
  - permitir doble emision
  - convertir respuesta formal en pseudo-chat editable
- Criterios de cierre de la fase:
  - CU-09 estable en escenarios habilitados
  - denegaciones correctas de duplicado e inmutabilidad
- Que no conviene intentar todavia en esta fase:
  - anulacion o versionado de respuesta formal

## 5.8 Fase 7 - Chats interno y compartido

- Objetivo de la fase: habilitar colaboracion conversacional separada de lo formal.
- Por que va en ese momento: requiere permisos de escenario maduros y respuesta formal ya cerrada.
- Apps/modulos involucrados: `chats`, `communications`, `permissions_support`.
- Modelos involucrados:
  - `CommunicationMessage`
- Servicios/casos de uso involucrados:
  - CU-15 publicar mensaje interno
  - CU-16 publicar mensaje compartido
- Endpoints/API involucrados:
  - `GET /api/v1/communications/{id}/messages/?scope=internal|shared`
  - `POST /api/v1/communications/{id}/messages/`
- Permisos o reglas criticas involucradas:
  - `scope=internal` solo internos
  - externos solo `shared` cuando escenario lo habilita
  - nunca reemplaza respuesta formal
- Entregables concretos de la fase:
  - chat interno y compartido operativos con filtrado por scope
- Riesgos principales:
  - filtrar mal y exponer chat interno
- Criterios de cierre de la fase:
  - CU-15/CU-16 con validacion estricta de scope y actor
- Que no conviene intentar todavia en esta fase:
  - adjuntos en chat
  - hilos avanzados o menciones complejas

## 5.9 Fase 8 - Subcomunicaciones y relacion `child_of`

- Objetivo de la fase: habilitar continuidad formal por nueva comunicacion relacionada.
- Por que va en ese momento: depende de flujo principal ya estable.
- Apps/modulos involucrados: `communications`, `permissions_support`, `expedients` (si ya existe).
- Modelos involucrados:
  - `CommunicationRelation` (`relation_type=child_of`)
- Servicios/casos de uso involucrados:
  - CU-10 crear subcomunicacion
  - CU-20 consultar subcomunicaciones relacionadas
- Endpoints/API involucrados:
  - `GET/POST /api/v1/communications/{id}/children/`
  - `GET /api/v1/communications/{id}/relations/`
- Permisos o reglas criticas involucradas:
  - `child_of` como relacion canonica de `v0.2`
  - externo iniciador puede continuidad post-respuesta final
  - externo respondedor no habilitado para crear subcomunicacion en `v0.2`
- Entregables concretos de la fase:
  - creacion de hija con vinculo correcto y trazable
- Riesgos principales:
  - usar subcomunicacion para reemplazar edicion o participacion normal
- Criterios de cierre de la fase:
  - CU-10/CU-20 con reglas de continuidad y visibilidad correctas
- Que no conviene intentar todavia en esta fase:
  - tipos adicionales de relacion
  - arboles profundos con UX compleja

## 5.10 Fase 9 - Expediente principal operativo

- Objetivo de la fase: agregar contexto administrativo sin desplazar centralidad de comunicacion.
- Por que va en ese momento: el flujo operativo principal ya esta cerrado.
- Apps/modulos involucrados: `expedients`, `communications`, `permissions_support`.
- Modelos involucrados:
  - `Expedient`
  - `CommunicationExpedient`
- Servicios/casos de uso involucrados:
  - CU-11 asociar expediente
  - CU-12 mover expediente
- Endpoints/API involucrados:
  - `GET/PUT/DELETE /api/v1/communications/{id}/expedient/`
- Permisos o reglas criticas involucradas:
  - externos no ven ni operan expediente
  - operacion con expediente principal unico en `v0.2`
- Entregables concretos de la fase:
  - asociacion/movimiento de expediente principal estable
- Riesgos principales:
  - hacer crecer `expedients` como dominio central
- Criterios de cierre de la fase:
  - CU-11/CU-12 operativos con restricciones de visibilidad correctas
- Que no conviene intentar todavia en esta fase:
  - multiples expedientes operativos simultaneos
  - workflow propio del expediente

## 5.11 Fase 10 - Auditoria e historial interno

- Objetivo de la fase: consolidar trazabilidad operativa interna sin bloquear negocio.
- Por que va en ese momento: requiere acciones de dominio ya estables para registrar eventos utiles.
- Apps/modulos involucrados: `audit`, `communications`, `permissions_support`.
- Modelos involucrados:
  - `CommunicationEvent`
- Servicios/casos de uso involucrados:
  - CU-19 consultar historial (interno)
  - registro de eventos de mutacion (side-effect)
- Endpoints/API involucrados:
  - `GET /api/v1/communications/{id}/history/` (solo interno en `v0.2`)
- Permisos o reglas criticas involucradas:
  - no existe historial externo equivalente al interno
  - auditoria es side-effect no bloqueante
- Entregables concretos de la fase:
  - timeline interno consultable
  - registro consistente de eventos relevantes
- Riesgos principales:
  - acoplar negocio a persistencia de auditoria
- Criterios de cierre de la fase:
  - CU-19 solo interno y sin sobreexposicion
  - falla de auditoria no invalida la mutacion principal
- Que no conviene intentar todavia en esta fase:
  - timeline externo enriquecido
  - auditoria de lectura exhaustiva obligatoria

## 5.12 Fase 11 - Endurecimiento final de API y validaciones

- Objetivo de la fase: cerrar contratos para integracion estable con frontend.
- Por que va en ese momento: requiere endpoints y servicios nucleares ya implementados.
- Apps/modulos involucrados: todas las apps owner + `permissions_support`.
- Modelos involucrados: no agrega nuevos, consolida validaciones.
- Servicios/casos de uso involucrados: CU-01 a CU-20 segun alcance `v0.2`.
- Endpoints/API involucrados:
  - cierre de contratos de payload
  - filtros de listado minimos
  - errores consistentes de negocio/autorizacion
- Permisos o reglas criticas involucradas:
  - coherencia total visibilidad vs accion
  - reglas de estado/workflow en todos los endpoints de mutacion
- Entregables concretos de la fase:
  - API base congelable para frontend
  - paquete minimo de pruebas funcionales por escenario
  - documentacion tecnica actualizada
- Riesgos principales:
  - cambios tardios de contrato por no validar escenarios reales
- Criterios de cierre de la fase:
  - smoke end-to-end de CU prioritarios
  - no hay contradicciones entre servicios, permisos y API
- Que no conviene intentar todavia en esta fase:
  - optimizaciones prematuras
  - motor avanzado de transiciones persistidas

---

## 6. Dependencias entre fases (detalle operativo)

### 6.1 Dependencias estrictas

- Fase `3` no puede iniciar sin fase `2` (tipo/workflow/estado).
- Fase `4` no puede cerrar sin fase `3` (no hay asignacion sobre entidad inexistente).
- Fase `5` requiere fase `4` (visibilidad documental depende de permisos/escenario).
- Fase `6` requiere fase `5` (respuesta formal vincula versiones).
- Fase `11` requiere `7/8/9/10` cerradas o explicitamente fuera de alcance.

### 6.2 Paralelizables con control

- `7` (chat), `8` (subcomunicacion), `9` (expediente) pueden avanzar en paralelo despues de `6`.
- `10` (audit/historial) puede avanzar en paralelo a `7/8/9`, pero validando no bloqueo.

### 6.3 Lo que no conviene adelantar

- historial antes de cerrar flujo principal
- expediente antes de cerrar asignacion/permisos base
- subcomunicaciones antes de respuesta formal y estados operativos

---

## 7. MVP backend real mas temprano

MVP recomendado al cierre de **fase 6**:

- crear comunicacion externa/interna (CU-01, CU-02)
- listar y detallar comunicacion (CU-17)
- editar abierta en alcance permitido (CU-03)
- asignar/quitar participante (CU-04, CU-05)
- cambiar estado, cerrar, reabrir (CU-06, CU-07, CU-08)
- subir documento y versionar (CU-13, CU-14)
- emitir respuesta formal unica e inmutable (CU-09)
- consulta de respuesta formal con contrato `200 + null` cuando no existe y la comunicacion es visible

Queda fuera de este MVP temprano:

- chats (CU-15, CU-16)
- subcomunicaciones (CU-10, CU-20)
- expediente (CU-11, CU-12)
- historial interno consultable (CU-19)

---

## 8. CU y endpoints prioritarios (orden de construccion)

### 8.1 Ola 1 (fases 1 a 3)

- CU: CU-01, CU-02, CU-03, CU-17
- Endpoints:
  - `/me`, `/me/memberships`, `/me/active-membership`
  - `/communication-types`, `/communication-types/{id}/states`
  - `/communications` (list/detail/create external/create internal/patch)

### 8.2 Ola 2 (fases 4 a 6)

- CU: CU-04, CU-05, CU-06, CU-07, CU-08, CU-13, CU-14, CU-18, CU-09
- Endpoints:
  - `/communications/{id}/participants`
  - `/communications/{id}/state-transitions`, `/close`, `/reopen`
  - `/communications/{id}/documents`
  - `/communications/{id}/documents/{document_id}/versions`
  - `/communications/{id}/formal-response`

### 8.3 Ola 3 (fases 7 a 11)

- CU: CU-15, CU-16, CU-10, CU-20, CU-11, CU-12, CU-19
- Endpoints:
  - `/communications/{id}/messages`
  - `/communications/{id}/children`, `/relations`
  - `/communications/{id}/expedient`
  - `/communications/{id}/history`

---

## 9. Riesgos reales de implementacion

### 9.1 Riesgos de secuencia

- abrir demasiadas apps al mismo tiempo
- implementar expediente o historial antes del flujo principal
- intentar cubrir todos los escenarios externos en la primera iteracion

### 9.2 Riesgos de autorizacion

- duplicar permisos en views/serializers/servicios
- no centralizar inferencia de escenario
- mezclar visibilidad y mutacion

### 9.3 Riesgos de dominio

- mezclar chat con respuesta formal
- permitir reapertura con respuesta formal emitida
- romper equivalencia `editor/responsible` en `v0.2`

### 9.4 Riesgos de API

- exponer informacion interna a externos por serializer no condicionado
- cambiar contratos de endpoint en cada sprint por falta de congelamiento temprano

---

## 10. Simplificaciones conscientes de implementacion (`v0.2`)

Estas simplificaciones deben respetarse durante toda la ejecucion:

- `editor` y `responsible` equivalentes en permisos y operaciones
- `child_of` como unica relacion operativa entre comunicaciones
- una sola respuesta formal por comunicacion, final e inmutable
- expediente principal unico por comunicacion en operacion
- historial externo inexistente
- auditoria como side-effect no bloqueante
- visibilidad documental externa contextual por regla funcional simple
- sin motor persistente completo de transiciones (validacion en capa logica)

---

## 11. Estrategia de validacion por fase

| Fase | Validacion minima funcional | Validacion de permisos | Validacion de integridad |
|---|---|---|---|
| 0 | Proyecto levanta + health | autenticacion base | CI y entorno |
| 1 | `me` y membership operativos | actor/organizacion activa | consistencia membership |
| 2 | tipos/workflows/estados consultables | acceso lectura catalogos | estado inicial por workflow |
| 3 | create/list/detail/edit comunicacion | visibilidad base interna/externa | `current_state` valido |
| 4 | participantes + estado/cierre/reapertura | asignacion+rol+escenario | transiciones validas en servicio |
| 5 | alta documento + versionado + consulta visibles | politica documental externa | version vigente y pertenencia |
| 6 | emitir y consultar respuesta formal | actor habilitado por escenario | unicidad e inmutabilidad |
| 7 | publicar/leer chat por scope | interno vs shared por actor | separacion con respuesta formal |
| 8 | crear hija y consultar relaciones | reglas de continuidad | `relation_type=child_of` |
| 9 | asociar/mover expediente principal | solo internos habilitados | unica asociacion principal |
| 10 | historial interno consultable | bloqueo externos | evento auditable no bloqueante |
| 11 | smoke end-to-end CU prioritarios | coherencia cross-endpoint | contrato API estable |

---

## 12. Que conviene congelar primero (para evitar retrabajo)

Congelar temprano:

1. estructura de apps y ownership (`design/10`)
2. modelos nucleo y contratos (`design/08`)
3. contrato de respuesta formal (`design/08`, `design/12`)
4. reglas nucleo de permisos y precedencia de escenario (`design/09`)
5. endpoints base de `communications` + `participants` + `state` + `documents` + `formal-response` (`design/12`)

---

## 13. Que no conviene sofisticar todavia

Evitar en `v0.2`:

- motor avanzado de workflow persistido
- politicas ultra finas por tipo antes de cerrar nucleo comun
- relaciones entre comunicaciones adicionales a `child_of`
- historial externo
- modularizacion extrema sin necesidad
- APIs paralelas completas por escenario
- optimizacion de performance prematura sin metricas reales

---

## 14. Propuesta principal y alternativa compacta

### 14.1 Propuesta principal recomendada

Implementar las fases `0` a `11` con MVP al cierre de `6` y paralelismo controlado en `7/8/9/10`.

Ventajas:

- minimiza retrabajo de permisos/API
- permite validar negocio temprano
- llega a integracion frontend con contratos estables

### 14.2 Alternativa compacta (si el equipo arranca mas chico)

Recortar primera iteracion a fases `0` a `6` y posponer `7/8/9/10` a una segunda ola.

Ventajas:

- tiempo menor a primer valor funcional

Costo:

- frontend sin chat/subcomunicaciones/expediente/historial en primera integracion

Recomendacion: usar alternativa compacta solo si hay restriccion fuerte de tiempo.  
Para reducir riesgo global, se recomienda la propuesta principal.

---

## 15. Cierre del plan

### 15.1 Recomendacion general de ejecucion

Ejecutar por fases cortas con demo interna al cierre de cada fase y gates de pase estrictos por permisos + integridad.

### 15.2 Orden sugerido definitivo

`0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> (7,8,9,10 en paralelo controlado) -> 11`

### 15.3 Fase que conviene empezar inmediatamente

**Fase 0** (bootstrap tecnico) con foco en estructura modular, convenciones de servicios/autorizacion y base de testing.

### 15.4 Criterio de backend listo para integrar frontend

Se considera listo cuando:

- MVP de fases `0` a `6` esta estable y validado
- endpoints nucleo tienen contratos congelados
- denegaciones y visibilidad interna/externa son consistentes
- respuesta formal cumple unicidad e inmutabilidad
- no hay contradicciones entre modelos, servicios, permisos y API
- existe smoke end-to-end de CU prioritarios

