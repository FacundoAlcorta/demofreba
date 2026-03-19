# Diseno Tecnico de Modelos Django (v0.2)

## Sistema de gestion de comunicaciones FREBA

## 1. Objetivo y alcance

Este documento define una propuesta tecnica de modelado de datos para backend Django + Django REST Framework, basada en:

- `00_requerimientos_base_v0_2.md` (fuente principal de verdad)
- `01_glosario_dominio.md`
- `02_escenarios_y_permisos.md`
- `03_modelo_conceptual.md`
- `04_decisiones_y_supuestos.md`
- `05_plan_implementacion.md`
- `06_modelo_relacional_preliminar.md`
- `07_matriz_permisos_y_transiciones.md`

El objetivo es dejar una base implementable y revisable para `v0.2` sin escribir codigo aun.

Queda fuera de alcance de este documento:

- serializers
- views
- permisos DRF detallados por endpoint
- migraciones
- SQL especifico

---

## 2. Principios de modelado adoptados

### 2.1 Comunicacion como entidad central

La estructura de datos se organiza alrededor de `Communication`.  
Expediente, documentos, chat, respuesta formal y asignaciones orbitan sobre esa entidad.

### 2.2 Separacion configuracion vs operacion

Se separan entidades configurables (tipo, workflow, estado, bandeja) de entidades operativas (comunicacion, asignacion, documentos, chat, respuesta, expediente, eventos).

### 2.3 Trazabilidad obligatoria

Toda accion relevante debe dejar huella estructural suficiente para reconstruir quien hizo que, cuando y sobre que comunicacion.

### 2.4 Simplificacion consciente v0.2

Se prioriza una base clara y mantenible, dejando capacidades futuras preparadas pero no activadas por defecto.

---

## 3. Estructura general de apps Django recomendada

Se recomienda una modularizacion por dominio funcional:

### 3.1 `organizations`

Responsable de entidades institucionales.

- `Organization`

### 3.2 `users` (o `accounts`)

Responsable de identidad y representacion organizacional.

- `User` (custom o extendido)
- `UserOrganizationMembership`

### 3.3 `communication_config`

Responsable de configuracion de tipos y ciclo de vida.

- `Workflow`
- `WorkflowState`
- `CommunicationType`
- `Inbox`
- `InboxUser`

### 3.4 `communications`

Responsable del nucleo operativo del caso.

- `Communication`
- subtablas por tipo (`Communication<Tipo>Data`)
- `CommunicationAssignment`
- `FormalResponse`
- `FormalResponseDocument`
- `CommunicationRelation`

### 3.5 `documents`

Responsable del versionado documental.

- `Document`
- `DocumentVersion`

### 3.6 `chats`

Responsable de intercambio conversacional.

- `CommunicationMessage`

### 3.7 `expedients`

Responsable de agrupacion administrativa.

- `Expedient`
- `CommunicationExpedient`

### 3.8 `audit`

Responsable de eventos trazables.

- `CommunicationEvent`

### 3.9 `permissions_support` (opcional de soporte)

Sin dominio propio persistente obligatorio en `v0.2`.  
Puede alojar reglas, matrices compiladas o helpers, pero no es requisito crear tablas nuevas en esta etapa.

---

## 4. Entidades configurables

## 4.1 `Organization`

### Proposito
Representar cada entidad institucional participante (FREBA y externos).

### Por que existe
El dominio opera sobre usuarios que actuan en nombre de organizaciones.

### Relacion con el dominio
Define origen/destino institucional de comunicaciones y acota visibilidad externa.

### Campos conceptuales minimos

- `id`
- `name`
- `code`
- `organization_type` (ver criterios de catalogos)
- `is_active`
- timestamps

### Relaciones principales

- 1:N con `UserOrganizationMembership`
- 1:N con `Communication` como origen institucional
- 1:N con `Communication` como destino institucional
- 1:N con `CommunicationAssignment` (organizacion desde la que participa el usuario)

### Observaciones de diseno

- Conviene separar claramente la organizacion institucional de origen (`origin_organization`) de la organizacion desde la cual actuo el creador (`created_by_organization`).

---

## 4.2 `UserOrganizationMembership`

### Proposito
Relacionar usuarios con organizaciones que pueden representar.

### Por que existe
El emisor real del dominio es `usuario + organizacion representada`.

### Relacion con el dominio
Base para trazabilidad, permisos y representacion activa.

### Campos conceptuales minimos

- `id`
- `user_id`
- `organization_id`
- `is_default`
- `is_active`
- `created_at`

### Relaciones principales

- N:1 con `User`
- N:1 con `Organization`

### Observaciones de diseno

- Aunque la operacion inicial sea simple, esta estructura deja preparado soporte multi-organizacion sin sobrecoste alto.

---

## 4.3 `Workflow`

### Proposito
Definir ciclos de vida reutilizables.

### Por que existe
Cada tipo de comunicacion necesita un workflow configurable.

### Relacion con el dominio
Evita estados hardcodeados y habilita workflows por tipo y workflow por defecto.

### Campos conceptuales minimos

- `id`
- `name`
- `code`
- `description`
- `is_default`
- `is_active`
- timestamps

### Relaciones principales

- 1:N con `WorkflowState`
- 1:N con `CommunicationType`

### Observaciones de diseno

- Debe existir al menos un workflow por defecto operativo.

---

## 4.4 `WorkflowState`

### Proposito
Representar estados configurables dentro de un workflow.

### Por que existe
El estado de una comunicacion debe pertenecer a su workflow y no ser un string libre.

### Relacion con el dominio
Implementa estado unico visible para quienes tienen acceso.

### Campos conceptuales minimos

- `id`
- `workflow_id`
- `name`
- `code`
- `description`
- `is_initial`
- `is_final`
- `display_order`
- `is_active`

### Relaciones principales

- N:1 con `Workflow`
- 1:N con `Communication` (estado actual)

### Observaciones de diseno

- Recomendable unicidad de `code` por `workflow`.
- Recomendable restriccion para un solo estado inicial activo por workflow.
- En `v0.2` no obliga a persistir matriz fina de transiciones en BD.

---

## 4.5 `CommunicationType`

### Proposito
Configurar comportamiento funcional de cada tipo de comunicacion.

### Por que existe
El tipo define formulario, workflow, bandeja y reglas base de inicio/visibilidad.

### Relacion con el dominio
Es la clave de parametrizacion principal.

### Campos conceptuales minimos

- `id`
- `name`
- `code`
- `description`
- `workflow_id`
- `default_inbox_id`
- `allows_external_creation` (filtro base)
- `allows_internal_creation` (filtro base)
- `is_active`
- timestamps

### Relaciones principales

- N:1 con `Workflow`
- N:1 con `Inbox`
- 1:N con `Communication`

### Observaciones de diseno

- `allows_external_creation` / `allows_internal_creation` no alcanzan solos: la habilitacion real tambien depende de escenario, rol/perfil y contexto.

---

## 4.6 `Inbox`

### Proposito
Representar la bandeja inicial de recepcion.

### Por que existe
Las comunicaciones entrantes a FREBA requieren un punto inicial de trabajo.

### Relacion con el dominio
En `v0.2` la bandeja se entiende como lista de usuarios.

### Campos conceptuales minimos

- `id`
- `name`
- `code`
- `description`
- `is_active`

### Relaciones principales

- 1:N con `CommunicationType`
- 1:N con `InboxUser`

### Observaciones de diseno

- No sobredisenar la bandeja como motor de colas complejo en esta etapa.

---

## 4.7 `InboxUser`

### Proposito
Vincular usuarios a bandejas.

### Por que existe
Permite resolver composicion inicial de participantes FREBA.

### Relacion con el dominio
Soporta la regla operativa de asignacion inicial desde bandeja.

### Campos conceptuales minimos

- `id`
- `inbox_id`
- `user_id`
- `is_active`
- `created_at`

### Relaciones principales

- N:1 con `Inbox`
- N:1 con `User`

### Observaciones de diseno

- En comunicaciones creadas por FREBA hacia externo, la seleccion de usuarios destino reemplaza esta logica de bandeja.

---

## 5. Entidades operativas

## 5.1 `Communication`

### Proposito
Representar el caso operativo principal del sistema.

### Por que existe
Es la unidad de gestion formal sobre la que se aplican estados, documentos, chat, respuesta y permisos.

### Relacion con el dominio
Entidad central definida por `00`.

### Campos conceptuales minimos

- `id`
- `communication_type_id`
- `current_state_id`
- `title`
- `description`
- `origin_organization_id`
- `destination_organization_id` (nullable segun escenario)
- `created_by_user_id`
- `created_by_organization_id`
- `updated_by_user_id` (nullable)
- `closed_at` (nullable)
- `closed_by_user_id` (nullable)
- `created_at`
- `updated_at`

Campos tecnicos opcionales utiles:

- `is_closed`
- `last_activity_at`

### Relaciones principales

- N:1 con `CommunicationType`
- N:1 con `WorkflowState` (estado actual)
- 1:N con `CommunicationAssignment`
- 1:N con `Document`
- 1:N con `CommunicationMessage`
- 1:0..1 con `FormalResponse` (inversa por unique)
- 1:N con `CommunicationRelation` como madre e hija
- 1:N con `CommunicationExpedient`
- 1:N con `CommunicationEvent`

### Observaciones de diseno

- No debe tener `formal_response_id` como fuente paralela de verdad.
- Debe registrar tanto origen institucional como organizacion desde la cual actuo el creador.

---

## 5.2 Subtablas por tipo de comunicacion (`Communication<tipo>Data`)

### Proposito
Modelar atributos particulares por tipo con validacion fuerte.

### Por que existe
El dominio ya adopta base comun + tablas especificas por tipo (evitar genericidad excesiva).

### Relacion con el dominio
Implementa especializacion estructural sin convertir todo en campos opcionales o JSON.

### Campos conceptuales minimos

- `id`
- `communication_id` (unique, one-to-one)
- campos especificos del tipo
- timestamps opcionales

### Relaciones principales

- 1:1 con `Communication`

### Observaciones de diseno

- Estrategia principal recomendada para `v0.2`.
- Riesgo a vigilar: explosion de subtablas cuando crezcan tipos.

---

## 5.3 `CommunicationAssignment`

### Proposito
Formalizar participacion de usuarios por comunicacion.

### Por que existe
La asignacion es base de permisos y operacion activa.

### Relacion con el dominio
Implementa combinacion usuario + organizacion + rol + vigencia.

### Campos conceptuales minimos

- `id`
- `communication_id`
- `user_id`
- `organization_id`
- `role`
- `assigned_by_user_id` (nullable)
- `assigned_at`
- `removed_at` (nullable)
- `is_active`

### Relaciones principales

- N:1 con `Communication`
- N:1 con `User`
- N:1 con `Organization`

### Observaciones de diseno

- Recomendable evitar asignaciones activas duplicadas equivalentes para mismo usuario/comunicacion.
- En externos puede haber visibilidad organizacional basica aun sin asignacion, pero operacion activa depende de esta tabla.

---

## 5.4 `FormalResponse`

### Proposito
Representar respuesta formal unica, final e inmutable de una comunicacion.

### Por que existe
La respuesta formal no es chat ni subcomunicacion; es pieza oficial del cierre funcional.

### Relacion con el dominio
Una sola respuesta por comunicacion.

### Campos conceptuales minimos

- `id`
- `communication_id` (unique)
- `response_text`
- `created_by_user_id`
- `created_by_organization_id`
- `created_at`

### Relaciones principales

- 1:1 (logica) con `Communication`, materializada por unique en `communication_id`
- 1:N con `FormalResponseDocument`

### Observaciones de diseno

- `formal_response.communication_id` es la unica fuente de verdad de vinculacion.
- No tiene workflow ni estado propio.
- No se modela anulacion/edicion como flujo normal en `v0.2`.

---

## 5.5 `FormalResponseDocument`

### Proposito
Vincular respuesta formal con versiones documentales exactas incluidas.

### Por que existe
La respuesta debe congelar evidencia documental trazable.

### Relacion con el dominio
Permite materializar "documentos incluidos en respuesta formal".

### Campos conceptuales minimos

- `id`
- `formal_response_id`
- `document_version_id`
- `display_order`

### Relaciones principales

- N:1 con `FormalResponse`
- N:1 con `DocumentVersion`

### Observaciones de diseno

- Se recomienda vincular versiones, no solo documentos logicos.

---

## 5.6 `Document`

### Proposito
Representar documento logico asociado a una comunicacion.

### Por que existe
Permite separar identidad documental de sus versiones.

### Relacion con el dominio
Los documentos pertenecen a la comunicacion y son versionables.

### Campos conceptuales minimos

- `id`
- `communication_id`
- `logical_name`
- `document_kind` (nullable en `v0.2` si no hay catalogo cerrado)
- `created_by_user_id`
- `created_at`
- `is_active`

### Relaciones principales

- N:1 con `Communication`
- 1:N con `DocumentVersion`

### Observaciones de diseno

- No mezclar versionado dentro de esta tabla.

---

## 5.7 `DocumentVersion`

### Proposito
Representar cada version concreta de un documento.

### Por que existe
Se requiere trazabilidad historica y version vigente sin destruir anteriores.

### Relacion con el dominio
Base para seleccion documental de respuesta y visibilidad externa acotada.

### Campos conceptuales minimos

- `id`
- `document_id`
- `version_number`
- `storage_path` o referencia a archivo
- `original_filename`
- `mime_type`
- `uploaded_by_user_id`
- `uploaded_by_organization_id`
- `uploaded_at`
- `is_current`
- `is_visible_to_external` (auxiliar tecnico)
- `notes` (nullable)

### Relaciones principales

- N:1 con `Document`
- N:1 con `User`
- N:1 con `Organization`
- N:1 desde `FormalResponseDocument`

### Observaciones de diseno

- `is_visible_to_external` no reemplaza la regla funcional contextual:
  - propios de su organizacion
  - adjuntos expuestos en envio inicial
  - incluidos en respuesta formal
  - no internos FREBA de trabajo

---

## 5.8 `CommunicationMessage`

### Proposito
Registrar mensajes de chat vinculados a una comunicacion.

### Por que existe
Separar intercambio operativo (chat) de respuesta formal.

### Relacion con el dominio
Soporta chat interno y chat compartido.

### Campos conceptuales minimos

- `id`
- `communication_id`
- `scope`
- `message_text`
- `created_by_user_id`
- `created_by_organization_id`
- `created_at`

### Relaciones principales

- N:1 con `Communication`
- N:1 con `User`
- N:1 con `Organization`

### Observaciones de diseno

- En `v0.2` no admitir adjuntos propios en mensajes.
- Visibilidad depende de `scope` + permisos/escenario.

---

## 5.9 `CommunicationRelation`

### Proposito
Representar relacion entre comunicaciones independientes.

### Por que existe
La continuidad post-respuesta final se resuelve con nueva comunicacion vinculada.

### Relacion con el dominio
Madre/hija con independencia de ciclos de vida.

### Campos conceptuales minimos

- `id`
- `parent_communication_id`
- `child_communication_id`
- `relation_type`
- `created_by_user_id`
- `created_at`

### Relaciones principales

- N:1 con `Communication` como madre
- N:1 con `Communication` como hija

### Observaciones de diseno

- Caso canonico `v0.2`: `child_of`.
- Evitar self-link y duplicados exactos activos.
- Otros tipos de relacion quedan como extension futura, no eje actual.

---

## 5.10 `Expedient`

### Proposito
Agrupar comunicaciones en contexto administrativo interno.

### Por que existe
El dominio requiere orden y agrupacion sin mover el centro fuera de comunicacion.

### Relacion con el dominio
Entidad secundaria, visible solo para FREBA.

### Campos conceptuales minimos

- `id`
- `code` o identificador
- `title` o caratula
- `subject`
- `created_by_user_id`
- `created_at`
- `updated_at`

### Relaciones principales

- 1:N con `CommunicationExpedient`

### Observaciones de diseno

- En `v0.2` no tiene estado propio ni responsables propios.

---

## 5.11 `CommunicationExpedient`

### Proposito
Vincular comunicaciones con expedientes.

### Por que existe
Permite soporte estructural de multiples asociaciones sin forzar complejidad operativa inicial.

### Relacion con el dominio
Operacion actual simplificada a expediente principal por comunicacion.

### Campos conceptuales minimos

- `id`
- `communication_id`
- `expedient_id`
- `is_primary`
- `associated_by_user_id`
- `associated_at`

### Relaciones principales

- N:1 con `Communication`
- N:1 con `Expedient`
- N:1 con `User` (quien asocia)

### Observaciones de diseno

- Recomendable asegurar una sola asociacion primaria activa por comunicacion.
- Soporta evolucion futura a multiples expedientes.

---

## 5.12 `CommunicationEvent`

### Proposito
Registrar eventos relevantes de ciclo de vida.

### Por que existe
La trazabilidad es requisito de dominio.

### Relacion con el dominio
Permite reconstruccion historica transversal.

### Campos conceptuales minimos

- `id`
- `communication_id`
- `event_type`
- `performed_by_user_id` (nullable en eventos de sistema)
- `performed_by_organization_id` (nullable)
- `metadata` acotado
- `created_at`

### Relaciones principales

- N:1 con `Communication`
- N:1 con `User` (nullable)
- N:1 con `Organization` (nullable)

### Observaciones de diseno

- Usar set controlado de tipos de evento para evitar un historial ilegible.

---

## 6. Contratos minimos y restricciones clave

## 6.1 Contrato `CommunicationType` -> `Workflow` -> `WorkflowState` -> `Communication`

Se recomienda cerrar estas invariantes:

- cada `Communication` referencia un `CommunicationType`
- cada `CommunicationType` referencia un `Workflow`
- `Communication.current_state` debe pertenecer al `Workflow` del tipo de esa comunicacion
- al crear una comunicacion, el estado inicial debe ser un `WorkflowState.is_initial = true` del workflow asociado
- cambios de estado validos se controlan en capa logica/servicio en `v0.2`

Nota `v0.2`: no se exige tabla persistente de transiciones tipo `workflow_transition` en esta etapa.

## 6.2 Contrato de respuesta formal

- unica respuesta formal por comunicacion
- vinculacion por `FormalResponse.communication_id` unico
- sin `formal_response_id` en `Communication` como fuente paralela
- respuesta inmutable una vez emitida

## 6.3 Contrato de asignacion y operacion activa

- operacion activa sobre comunicacion se apoya en `CommunicationAssignment`
- permisos dependen de rol + asignacion + escenario + organizacion
- visibilidad externa basica organizacional puede existir segun escenario, sin reemplazar la necesidad de asignacion para operar

## 6.4 Contrato de relacion entre comunicaciones

- relaciones entre comunicaciones no fusionan ciclos de vida
- `child_of` es el tipo canonico de `v0.2`
- continuidad luego de respuesta formal final: nueva comunicacion relacionada, no continuidad normal sobre la misma

## 6.5 Contrato de expediente

- modelo puede soportar multiples asociaciones
- operacion `v0.2`: expediente principal unico por comunicacion

## 6.6 Contrato documental externo

La regla funcional manda sobre flags tecnicos:

- externo ve documentos cargados por su propia organizacion
- externo ve adjuntos expuestos en envio inicial
- externo ve documentos incluidos en respuesta formal
- externo no ve documentos internos de trabajo FREBA

---

## 7. Criterios de choices, catalogos y relaciones

## 7.1 Donde conviene usar tabla

Usar tabla cuando haya configuracion administrable o alta variabilidad:

- `Workflow`
- `WorkflowState`
- `CommunicationType`
- `Inbox`
- `Organization`

Motivo: son catálogos de negocio vivos y con relaciones fuertes.

## 7.2 Donde conviene usar choice/enum en `v0.2`

Usar enum cuando el conjunto actual es chico, estable y operacional:

- `CommunicationAssignment.role`: `observer`, `editor`, `responsible`
- `CommunicationMessage.scope`: `internal`, `shared`
- `CommunicationRelation.relation_type`: `child_of` (activo en `v0.2`)
- `CommunicationEvent.event_type`: set controlado de eventos
- `organization_type`: enum inicial (si no hay necesidad inmediata de administracion dinamica)

## 7.3 Donde conviene dejar criterio mixto

- `Document.document_kind`: iniciar como enum/choice o nullable controlado; migrar a tabla solo si negocio necesita gestion rica de tipos documentales.

---

## 8. Simplificaciones conscientes de `v0.2`

Estas simplificaciones quedan explicitas para implementacion:

- `editor` y `responsible` equivalentes en permisos y operaciones
- `child_of` como relacion canonica entre comunicaciones
- una sola respuesta formal por comunicacion
- un expediente principal operativo por comunicacion (aunque el modelo soporte mas)
- sin motor persistente completo de transiciones en BD
- validacion de transiciones en capa logica
- chat sin adjuntos propios
- sin borradores formales de comunicacion ni de respuesta formal en esta etapa

Punto abierto explicitado:

- creacion de subcomunicacion por externo respondedor: no habilitada en `v0.2` y pendiente de definicion de negocio futura.

---

## 9. Riesgos de modelado y puntos delicados

## 9.1 Explosion de subtablas por tipo

Riesgo: crecimiento acelerado de tablas especificas por tipo.  
Mitigacion: gobernanza de tipos y alta disciplina de naming/ownership.

## 9.2 Ambiguedad `origin_organization` vs `created_by_organization`

Riesgo: confundir origen institucional con organizacion de actuacion del creador.  
Mitigacion: semantica estricta documentada y validaciones de consistencia.

## 9.3 Visibilidad documental externa contextual

Riesgo: implementar visibilidad solo con un booleano y filtrar de mas o de menos.  
Mitigacion: regla funcional explicitada + pruebas por escenario.

## 9.4 Complejidad de relacion recursiva entre comunicaciones

Riesgo: arboles profundos dificiles de operar/entender.  
Mitigacion: `child_of` canonico, vistas iniciales padre-hijas directas y restricciones de consistencia.

## 9.5 Multiples expedientes en el futuro

Riesgo: sobrecomplejidad funcional temprana.  
Mitigacion: soporte estructural con `CommunicationExpedient`, operacion simple con `is_primary`.

## 9.6 Complejidad acumulada en permisos

Riesgo: cruce de rol, asignacion, escenario y organizacion dificil de mantener.  
Mitigacion: centralizar reglas en servicios y no dispersarlas en multiples capas.

---

## 10. Recomendacion general de arquitectura de modelos

Se recomienda una arquitectura con:

- nucleo operativo centrado en `Communication`
- configuracion separada (`communication_config`)
- participacion y permisos apoyados en `CommunicationAssignment`
- versionado documental explicito (`Document` + `DocumentVersion`)
- respuesta formal separada e inmutable (`FormalResponse`)
- relacion madre/hija explicita (`CommunicationRelation`)
- expediente secundario y desacoplado (`Expedient` + puente)
- auditoria transversal (`CommunicationEvent`)

Esta opcion mantiene coherencia de dominio y baja ambiguedad para implementacion Django.

---

## 11. Orden sugerido de implementacion de modelos en Django

Orden recomendado:

1. `Organization`
2. `UserOrganizationMembership` (y `User` si corresponde)
3. `Workflow`
4. `WorkflowState`
5. `Inbox`
6. `InboxUser`
7. `CommunicationType`
8. `Communication`
9. primera subtabla por tipo (`Communication<tipo>Data`)
10. `CommunicationAssignment`
11. `Document`
12. `DocumentVersion`
13. `FormalResponse`
14. `FormalResponseDocument`
15. `CommunicationMessage`
16. `CommunicationRelation`
17. `Expedient`
18. `CommunicationExpedient`
19. `CommunicationEvent`

---

## 12. Que conviene no modelar de mas todavia

Para `v0.2`, conviene evitar:

- motor persistente de transiciones ultra fino (tabla de transiciones por actor/escenario) si aun no aporta valor inmediato
- tipos de relacion entre comunicaciones adicionales a `child_of`
- modelo de bandeja como estructura organizacional compleja
- multiplicidad operativa de expedientes por comunicacion
- metadatos avanzados de respuesta formal no requeridos por negocio actual
- catalogos excesivos para todo campo si no existe variabilidad real

---

## 13. Estado de cierre del diseno de modelos

Con este diseno, el backend puede pasar a una fase de implementacion Django con:

- decisiones estructurales principales cerradas
- simplificaciones `v0.2` explicitas
- crecimiento futuro previsto sin sobreingenieria temprana

Los pendientes funcionales abiertos quedan marcados como tales y no se transforman en verdades nuevas de negocio.
