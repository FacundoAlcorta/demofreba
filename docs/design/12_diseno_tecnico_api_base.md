# Diseno Tecnico de API Base (v0.2)

## Sistema de gestion de comunicaciones FREBA

## 1. Objetivo y alcance

Este documento define una propuesta tecnica de API base para Django REST Framework, alineada con:

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

No incluye codigo, serializers concretos ni contrato OpenAPI completo.  
Define recursos, endpoints base, criterios de payload y reglas de diseno para pasar a implementacion.

---

## 2. Principios generales de diseno de API

## 2.1 Recursos con ownership de dominio

Los endpoints deben reflejar ownership funcional:

- `communications` para ciclo de vida principal
- `documents` para ciclo documental
- `chats` para mensajes por scope
- `expedients` para agrupacion administrativa
- `audit` para historial

## 2.2 Separar lectura y mutacion cuando agrega claridad

- lecturas: `GET` de listado/detalle/subrecursos de consulta
- mutaciones: `POST`, `PATCH`, `PUT`, `DELETE` en recursos o acciones explicitas

## 2.3 No exponer por API lo que el dominio no cerro

No se incorporan en `v0.2`:

- motor avanzado de transiciones persistentes
- politicas ultra-finas por tipo fuera de lo ya definido
- endpoints paralelos por escenario sin necesidad real

## 2.4 Misma API, proyeccion distinta por permisos

Se evita duplicar API interna/externa si el mismo recurso puede proyectarse distinto por:

- tipo de actor
- organizacion activa
- escenario
- asignacion/rol
- reglas de visibilidad

## 2.5 Visibilidad y payload condicionados por autorizacion

La API no decide negocio por frontend.  
Backend aplica filtros de visibilidad y autorizacion reutilizable (segun `design/09...`).

## 2.6 Consistencia por encima de hiper-REST dogmatico

Se prioriza API clara y mantenible:

- subrecursos para contenido propio de una comunicacion
- acciones explicitas para operaciones de dominio no triviales (estado, cierre, reapertura, respuesta formal)

---

## 3. Recursos principales de la API

| Recurso API | Proposito | Owner principal |
|---|---|---|
| `communications` | Entidad central: alta, detalle, edicion, estado, respuesta, relaciones | `communications` |
| `communication-types` | Catalogo de tipos habilitados y metadatos de alta | `communication_config` |
| `workflow-states` (lookup) | Estados disponibles por tipo/workflow para UI y validacion | `communication_config` |
| `participants` (subrecurso) | Asignaciones de usuarios sobre comunicacion | `communications` |
| `formal-response` (subrecurso) | Respuesta formal unica e inmutable por comunicacion | `communications` |
| `documents` (subrecurso) | Documento logico de la comunicacion | `documents` |
| `document-versions` (subrecurso) | Versionado de cada documento | `documents` |
| `messages` (subrecurso) | Chat interno y compartido por `scope` | `chats` |
| `children` / `relations` (subrecurso) | Subcomunicaciones y relaciones `child_of` | `communications` |
| `expedient` (subrecurso) | Expediente principal operativo de la comunicacion | `expedients` |
| `history` (subrecurso) | Historial/eventos de comunicacion | `audit` |
| `me` y `memberships` | Contexto usuario actual y organizacion activa | `accounts` / `organizations` |

---

## 4. Estructura base de endpoints

## 4.1 Convenciones recomendadas

- prefijo de version: `/api/v1/`
- identificadores en path: `{communication_id}`, `{document_id}`, etc.
- subrecurso cuando la entidad depende semanticamente de comunicacion
- accion explicita con `POST` para operaciones de dominio no modelables como update parcial simple

## 4.2 Endpoints base recomendados

### 4.2.1 Comunicaciones

| Metodo | Endpoint | Tipo | Uso principal |
|---|---|---|---|
| `GET` | `/api/v1/communications/` | Lectura | Listado visible segun actor/escenario |
| `GET` | `/api/v1/communications/{communication_id}/` | Lectura | Detalle visible |
| `POST` | `/api/v1/communications/external/` | Mutacion | Crear comunicacion externa (E1) |
| `POST` | `/api/v1/communications/internal/` | Mutacion | Crear comunicacion interna (I1/I2) |
| `PATCH` | `/api/v1/communications/{communication_id}/` | Mutacion | Editar comunicacion abierta (campos habilitados) |
| `POST` | `/api/v1/communications/{communication_id}/state-transitions/` | Mutacion | Cambiar estado (CU-06) |
| `POST` | `/api/v1/communications/{communication_id}/close/` | Mutacion | Cierre administrativo (CU-07) |
| `POST` | `/api/v1/communications/{communication_id}/reopen/` | Mutacion | Reapertura sin respuesta final (CU-08) |

### 4.2.2 Participantes

| Metodo | Endpoint | Tipo | Uso principal |
|---|---|---|---|
| `GET` | `/api/v1/communications/{communication_id}/participants/` | Lectura | Ver participantes visibles segun actor |
| `POST` | `/api/v1/communications/{communication_id}/participants/` | Mutacion | Agregar participante (CU-04) |
| `DELETE` | `/api/v1/communications/{communication_id}/participants/{participant_id}/` | Mutacion | Quitar participante (CU-05) |

Regla operativa de visibilidad para externos en `v0.2`:

- un externo solo ve participantes de su propia organizacion
- no ve participantes internos de FREBA
- no ve participantes de otras organizaciones externas ajenas

### 4.2.3 Respuesta formal

| Metodo | Endpoint | Tipo | Uso principal |
|---|---|---|---|
| `GET` | `/api/v1/communications/{communication_id}/formal-response/` | Lectura | Ver respuesta formal si existe |
| `POST` | `/api/v1/communications/{communication_id}/formal-response/` | Mutacion | Emitir respuesta formal (CU-09) |

Contrato `v0.2` para `GET formal-response`:

- si la comunicacion es visible y aun no existe respuesta formal, responder `200` con cuerpo `null` (o equivalente semantico vacio consistente)
- no usar `404` para "sin respuesta formal" en una comunicacion visible
- si la comunicacion no es visible, aplicar politica general de visibilidad/denegacion

### 4.2.4 Documentos y versiones

| Metodo | Endpoint | Tipo | Uso principal |
|---|---|---|---|
| `GET` | `/api/v1/communications/{communication_id}/documents/` | Lectura | Listar documentos visibles |
| `POST` | `/api/v1/communications/{communication_id}/documents/` | Mutacion | Alta de documento nuevo (CU-13) |
| `GET` | `/api/v1/communications/{communication_id}/documents/{document_id}/versions/` | Lectura | Listar versiones visibles |
| `POST` | `/api/v1/communications/{communication_id}/documents/{document_id}/versions/` | Mutacion | Nueva version (CU-14) |

### 4.2.5 Chat

| Metodo | Endpoint | Tipo | Uso principal |
|---|---|---|---|
| `GET` | `/api/v1/communications/{communication_id}/messages/` | Lectura | Listar mensajes por `scope` |
| `POST` | `/api/v1/communications/{communication_id}/messages/` | Mutacion | Publicar mensaje en `internal` o `shared` |

### 4.2.6 Subcomunicaciones y relaciones

| Metodo | Endpoint | Tipo | Uso principal |
|---|---|---|---|
| `GET` | `/api/v1/communications/{communication_id}/children/` | Lectura | Ver subcomunicaciones directas |
| `POST` | `/api/v1/communications/{communication_id}/children/` | Mutacion | Crear subcomunicacion (`child_of`) |
| `GET` | `/api/v1/communications/{communication_id}/relations/` | Lectura | Ver contexto madre/hijas |

### 4.2.7 Expediente

| Metodo | Endpoint | Tipo | Uso principal |
|---|---|---|---|
| `GET` | `/api/v1/communications/{communication_id}/expedient/` | Lectura | Ver expediente principal (internos) |
| `PUT` | `/api/v1/communications/{communication_id}/expedient/` | Mutacion | Asociar o mover expediente principal |
| `DELETE` | `/api/v1/communications/{communication_id}/expedient/` | Mutacion | Quitar asociacion principal |

### 4.2.8 Historial

| Metodo | Endpoint | Tipo | Uso principal |
|---|---|---|---|
| `GET` | `/api/v1/communications/{communication_id}/history/` | Lectura | Historial de eventos (solo interno en `v0.2`) |

### 4.2.9 Contexto de usuario y catalogos base

| Metodo | Endpoint | Tipo | Uso principal |
|---|---|---|---|
| `GET` | `/api/v1/me/` | Lectura | Perfil y contexto actual |
| `GET` | `/api/v1/me/memberships/` | Lectura | Membresias y organizaciones disponibles |
| `POST` | `/api/v1/me/active-membership/` | Mutacion | Cambiar organizacion activa de sesion |
| `GET` | `/api/v1/communication-types/` | Lectura | Tipos disponibles para actor |
| `GET` | `/api/v1/communication-types/{type_id}/` | Lectura | Detalle tipo |
| `GET` | `/api/v1/communication-types/{type_id}/states/` | Lectura | Estados posibles (lookup para UI) |
| `GET` | `/api/v1/inboxes/` | Lectura | Bandejas visibles (internos) |

---

## 5. Lectura vs mutacion

## 5.1 Endpoints de lectura

Objetivo:

- listar recursos visibles
- obtener detalle/proyeccion
- consultar subrecursos contextuales (documentos, mensajes, historial)

Criterios:

- filtros de visibilidad aplicados en queryset/capa de lectura
- respuesta parcial segun actor/escenario
- nunca asumir que por poder ver, puede mutar

## 5.2 Endpoints de mutacion

Objetivo:

- ejecutar casos de uso de negocio (CU-01..CU-16)

Criterios:

- validacion de autorizacion reusable
- validacion de invariantes de dominio
- validacion workflow/estado/transicion cuando aplica
- auditoria explicita de la accion

## 5.3 Criterio recomendado por metodo

- `POST`:
  - crear recurso nuevo (`communications`, `documents`, `versions`, `children`)
  - ejecutar accion de negocio (`state-transitions`, `close`, `reopen`, `formal-response`)
- `PATCH`:
  - edicion parcial de datos permitidos de comunicacion abierta
- `PUT`:
  - reemplazo determinista de subrecurso unico (`expedient` principal)
- `DELETE`:
  - baja de participante o desasociacion de expediente
- `GET`:
  - listados, detalle y consultas especializadas

---

## 6. Diseno de payloads a alto nivel

## 6.1 Proyecciones de comunicacion

### Resumen de comunicacion (listado)

Incluye, como minimo:

- `id`, identificador visible, `communication_type`
- asunto/titulo breve y datos generales
- `current_state`
- origen/destino organizacional visible para actor
- `created_at`, `updated_at`
- flags operativos derivados (si tiene respuesta formal, si tiene hijas, etc.)

### Detalle de comunicacion

Extiende resumen con:

- datos comunes completos
- datos particulares por tipo (normalizados para API)
- estado y tipo/workflow de referencia
- respuesta formal (si existe)
- resumen de documentos/mensajes/subcomunicaciones segun visibilidad
- expediente solo para internos habilitados

## 6.2 Payloads de mutacion principales

### Creacion externa

- `communication_type_id`
- campos comunes requeridos
- bloque de campos particulares por tipo
- adjuntos iniciales opcionales

### Creacion interna

- lo mismo que creacion externa
- datos de destino externo/interno segun tipo
- participantes iniciales opcionales

### Edicion

- solo campos habilitados por estado/escenario
- bloque de datos particulares editable

### Cambio de estado

- identificador de estado destino (`state_id` o `state_code`)

### Respuesta formal

- contenido formal
- lista de versiones documentales incluidas

### Alta documental

- metadatos del documento logico
- archivo/version inicial

### Nueva version documental

- archivo/metadatos de nueva version

### Mensaje

- `scope`: `internal` o `shared`
- contenido textual

### Expediente

- `expedient_id` para asociar/mover

## 6.3 Interno vs externo: misma estructura, campos condicionados

Recomendacion principal:

- evitar payloads completamente distintos por endpoint interno/externo
- usar misma base de recurso y condicionar:
  - campos visibles
  - validaciones
  - acciones permitidas

---

## 7. API para comunicaciones (recurso central)

## 7.1 Endpoints clave

- `GET /api/v1/communications/`
- `GET /api/v1/communications/{communication_id}/`
- `POST /api/v1/communications/external/`
- `POST /api/v1/communications/internal/`
- `PATCH /api/v1/communications/{communication_id}/`
- `POST /api/v1/communications/{communication_id}/state-transitions/`
- `POST /api/v1/communications/{communication_id}/close/`
- `POST /api/v1/communications/{communication_id}/reopen/`
- `POST /api/v1/communications/{communication_id}/formal-response/`
- `POST /api/v1/communications/{communication_id}/children/`

## 7.2 Detalle enriquecido recomendado

Para evitar un mega-endpoint fijo y pesado:

- mantener `GET /communications/{id}/` como detalle base
- permitir expansion controlada via query params (`include=participants,documents,children,formal_response`)
- aplicar expansion segun permisos del actor

## 7.3 Filtros minimos recomendados en listado

- `type`
- `state`
- `created_by_org`
- `counterparty_org`
- `has_formal_response`
- `parent_id`
- `created_from` / `created_to`
- `search` sobre datos generales

Filtros internos adicionales posibles:

- `assigned_to_me`
- `expedient_id`

## 7.4 Reglas funcionales clave reflejadas en API

- creacion sin borrador en `v0.2`
- edicion de abierta segun escenario
- cierre y respuesta formal como acciones distintas
- reapertura solo si no existe respuesta formal
- continuidad post-respuesta final por subcomunicacion

---

## 8. API para documentos y versiones

## 8.1 Endpoints recomendados

- `GET /api/v1/communications/{communication_id}/documents/`
- `POST /api/v1/communications/{communication_id}/documents/`
- `GET /api/v1/communications/{communication_id}/documents/{document_id}/versions/`
- `POST /api/v1/communications/{communication_id}/documents/{document_id}/versions/`

## 8.2 Diferencia documento logico vs version

- `Document`: entidad logica (nombre, tipo, pertenencia a comunicacion)
- `DocumentVersion`: materializacion versionada del archivo/contenido

La API debe separar claramente:

- alta de documento nuevo
- versionado de documento existente

## 8.3 Visibilidad documental externa por regla funcional

La lectura documental para externos se filtra por:

- documentos cargados por su organizacion
- adjuntos expuestos en envio inicial
- documentos incluidos en respuesta formal
- exclusion de documentos internos de trabajo FREBA

Un flag tecnico puede asistir, pero no reemplaza esta regla.

## 8.4 Referencia/descarga de version vigente

La respuesta de documento/versions debe incluir referencia clara a version vigente y mecanismo de descarga autorizado (URL de descarga o referencia equivalente), manteniendo el mismo control de visibilidad.

---

## 9. API para chats

## 9.1 Recomendacion principal: endpoint unico con `scope`

Propuesta:

- `GET /api/v1/communications/{communication_id}/messages/?scope=internal|shared`
- `POST /api/v1/communications/{communication_id}/messages/` con `scope` obligatorio

Motivo:

- `CommunicationMessage` es un recurso unico con atributo `scope`
- evita duplicar endpoints y serializaciones
- mantiene consistencia entre lectura y escritura

## 9.2 Validaciones backend minimas

- `scope=internal`: solo internos habilitados
- `scope=shared`: internos operativos y externos segun escenario/asignacion
- nunca mezclar chat con emision de respuesta formal

## 9.3 Si falta `scope`

Recomendado en `v0.2`: responder error de validacion, evitando defaults ambiguos.

---

## 10. API para expedientes e historial

## 10.1 Expediente por comunicacion

Endpoints:

- `GET /api/v1/communications/{communication_id}/expedient/`
- `PUT /api/v1/communications/{communication_id}/expedient/`
- `DELETE /api/v1/communications/{communication_id}/expedient/`

Criterio:

- representa expediente principal operativo de `v0.2`
- `PUT` cubre asociar y mover sin endpoint duplicado
- solo internos con rol operativo habilitado

## 10.2 Historial/eventos

Endpoint:

- `GET /api/v1/communications/{communication_id}/history/`

Criterio `v0.2`:

- para internos: historial operativo completo segun permisos
- para externos: no existe endpoint de historial equivalente al interno en `v0.2`
- el seguimiento externo se resuelve por detalle de comunicacion + estado actual + respuesta formal + documentos visibles + chat compartido

---

## 11. API de configuracion y catalogos

## 11.1 Catalogos de comunicacion

Endpoints sugeridos (lookup/read-only para operacion normal):

- `GET /api/v1/communication-types/`
- `GET /api/v1/communication-types/{type_id}/`
- `GET /api/v1/communication-types/{type_id}/states/`

Opcional para administracion interna:

- `GET /api/v1/workflows/`
- `GET /api/v1/workflows/{workflow_id}/states/`

## 11.2 Bandejas

En `v0.2`, exponer principalmente lookup:

- `GET /api/v1/inboxes/`

Sin sobrecargar API con administracion avanzada de bandejas en esta etapa.

## 11.3 Contexto de usuario y organizacion activa

- `GET /api/v1/me/`
- `GET /api/v1/me/memberships/`
- `POST /api/v1/me/active-membership/`

Esto permite resolver reglas por organizacion activa sin endpoints paralelos.

---

## 12. Diferencias entre proyeccion interna y externa

## 12.1 Usuario interno FREBA

Ve y opera, segun rol/asignacion:

- detalle completo
- participantes internos
- historial completo
- chat interno y compartido (segun escenario)
- expediente
- documentos/versiones internas y externas

## 12.2 Externo iniciador (E1)

Ve:

- datos generales
- estado actual
- respuesta formal (si existe)
- documentos propios + expuestos iniciales + incluidos en respuesta
- chat compartido cuando corresponda
- participantes de su propia organizacion

No opera como flujo normal:

- no cambia estado
- no emite respuesta formal en su misma comunicacion
- no administra participantes
- no accede a historial de comunicacion

Puede crear subcomunicacion de continuidad luego de respuesta formal final.

## 12.3 Externo respondedor (E2)

Ve/Opera segun reglas de escenario:

- puede editar campos habilitados
- puede cargar/versionar documentos permitidos
- puede cambiar estado en tramo operativo habilitado
- puede emitir respuesta formal
- puede gestionar participantes de su organizacion
- ve participantes de su propia organizacion

Restricciones `v0.2`:

- no cierre administrativo final
- no subcomunicacion general habilitada
- no acceso a expediente/historial interno/chat interno

## 12.4 Estrategia API recomendada

Mantener mismos endpoints base y variar por:

- filtros de visibilidad
- proyecciones de serializer
- validadores de accion

Evitar APIs paralelas completas `internal/*` vs `external/*`, salvo en creacion de comunicacion donde la separacion aporta claridad operativa.

---

## 13. Errores y respuestas de alto nivel

## 13.1 Criterios generales

- denegaciones claras y trazables para acciones no permitidas
- no filtrar informacion sensible en mensajes de error para externos
- homogeneidad de codigos y estructura de error

## 13.2 Casos de error relevantes

- acceso denegado por rol/asignacion/escenario
- recurso no visible para actor (puede resolverse como no encontrado segun politica)
- transicion de estado invalida para workflow/escenario
- respuesta formal duplicada
- en `GET formal-response`, ausencia de respuesta sobre comunicacion visible no es error: `200` con `null` (o equivalente)
- versionado documental invalido
- accion fuera de escenario (ej. cierre E2 por externo)
- expediente no accesible o no visible

## 13.3 Resultado esperado para frontend

Errores deben permitir distinguir:

- denegacion funcional
- validacion de datos
- conflicto de estado de negocio

Sin delegar al frontend la interpretacion de reglas centrales.

---

## 14. Riesgos y anti-patrones de API

## 14.1 Riesgos principales

- API distinta por cada escenario cuando bastaria proyeccion por permisos
- endpoint de detalle sobredimensionado con demasiadas dependencias
- acciones de dominio heterogeneas en un endpoint ambiguo
- exposicion accidental de chat interno/documentos internos
- workflow hardcodeado en contrato API sin pasar por backend

## 14.2 Anti-patrones a evitar

- dejar reglas reales en frontend
- duplicar logica de autorizacion en cada serializer/view
- mezclar estado, respuesta, documentos y chat en un unico endpoint mutador
- exponer historial completo a externos por conveniencia de UI
- crear endpoints para futuros no requeridos en `v0.2`

---

## 15. Propuesta principal y alternativa mas simple

## 15.1 Propuesta principal recomendada

API centrada en `communications` con subrecursos explicitos:

- participantes
- formal-response
- documents/versions
- messages
- children/relations
- expedient
- history

Y acciones de dominio separadas:

- `state-transitions`
- `close`
- `reopen`

Beneficios:

- legibilidad
- ownership claro
- alineacion directa con CU-01..CU-20
- menor riesgo de sobrefragmentacion

## 15.2 Alternativa mas simple/minimalista

Reducir endpoints de accion y resolver mas por:

- `PATCH /communications/{id}/` para cambios de estado/cierre/reapertura
- menos subrecursos especializados

Costo:

- menor claridad semantica
- mas riesgo de condicionales complejos en una sola operacion

Para FREBA `v0.2`, se recomienda la propuesta principal.

---

## 16. Orden sugerido para definir/implementar la API

Orden alineado con `05`, `08`, `09`, `10` y `11`:

1. contexto base: `me`, `memberships`, `communication-types`, `states` lookup
2. `communications` lectura (`list`/`detail`) con visibilidad correcta
3. creacion (`external` e `internal`)
4. participantes (`GET/POST/DELETE`)
5. estado/cierre/reapertura
6. documentos y versiones con filtro de visibilidad externa
7. respuesta formal
8. chat (`messages` con `scope`)
9. subcomunicaciones (`children`/`relations`)
10. expediente principal (`GET/PUT/DELETE`)
11. historial (`history`)
12. endurecimiento de errores, filtros y contratos de payload

---

## 17. Cierre del documento

## 17.1 Recomendacion general de arquitectura de API

Adoptar una API resource-oriented, centrada en comunicacion, con subrecursos coherentes y acciones de dominio explicitas, evitando duplicacion por escenario.

## 17.2 Endpoints a congelar primero

- `communications` (`list`, `detail`, `external`, `internal`, `patch`)
- `participants`
- `state-transitions`, `close`, `reopen`
- `documents` + `versions`
- `formal-response`
- `messages` por `scope`

## 17.3 Que no conviene sofisticar todavia en `v0.2`

- OpenAPI exhaustiva desde el primer sprint
- endpoints alternativos por cada escenario
- motor avanzado de transiciones persistidas
- timeline externo rica que exponga historial interno
- variantes de relacion entre comunicaciones mas alla de `child_of`

## 17.4 Simplificaciones vigentes de etapa

- `editor` y `responsable` equivalentes en implementacion
- una sola respuesta formal por comunicacion, inmutable
- `child_of` como relacion canonica actual
- un expediente principal operativo por comunicacion
- visibilidad documental externa contextual y testeable por regla funcional
