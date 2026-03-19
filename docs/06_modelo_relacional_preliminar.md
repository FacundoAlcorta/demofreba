# Modelo relacional preliminar

## Sistema de gestión de comunicaciones FREBA

Documento de trabajo para traducir el modelo conceptual del sistema a una propuesta relacional preliminar, pensada como base para implementación en Django + Django REST Framework.

Este documento no define todavía el código final ni las migraciones, pero sí propone:

- entidades persistentes
- relaciones
- cardinalidades
- claves principales y foráneas
- restricciones conceptuales
- decisiones estructurales iniciales

---

## 1. Objetivo del documento

Este archivo busca responder:

- qué tablas principales deberían existir
- cómo se relacionan entre sí
- cuáles son configurables y cuáles operativas
- qué entidades conviene separar
- cómo modelar subtipos de comunicación
- cómo modelar asignaciones, documentos, respuestas, chats, expedientes e historial

---

## 2. Principios de modelado

### 2.1 La tabla central es `communication`
Toda la operación del sistema gira alrededor de la comunicación.

### 2.2 Separar configuración de operación
Debe haber una separación clara entre:

- tablas configurables
- tablas operativas

### 2.3 Evitar genericidad excesiva
No se propone una tabla única con campos dinámicos indefinidos para todos los tipos de comunicación.

### 2.4 Mantener trazabilidad
Toda acción importante debe poder rastrearse mediante relaciones y eventos.

### 2.5 Preparar crecimiento sin sobreingeniería
El modelo debe soportar evolución futura, pero sin obligar a resolver desde el día uno toda la complejidad posible.

---

## 3. Esquema general del modelo

El modelo puede agruparse en estos bloques:

### 3.1 Estructura organizacional
- `organization`
- `user_organization_membership`

### 3.2 Configuración
- `communication_type`
- `workflow`
- `workflow_state`
- `inbox`
- `inbox_user`

### 3.3 Operación principal
- `communication`
- `communication_assignment`
- `formal_response`

### 3.4 Soporte documental
- `document`
- `document_version`
- `formal_response_document`

### 3.5 Colaboración
- `communication_message`

### 3.6 Relación entre comunicaciones
- `communication_relation`

### 3.7 Contexto administrativo
- `expedient`
- `communication_expedient`

### 3.8 Auditoría
- `communication_event`

### 3.9 Subtipos por tipo de comunicación
- tablas one-to-one específicas por tipo, por ejemplo:
  - `communication_type_x_data`
  - `communication_type_y_data`

---

## 4. Tablas de estructura organizacional

## 4.1 `organization`

### Propósito
Representa a FREBA, cooperativas, distribuidoras, organismos u otras organizaciones participantes.

### Campos preliminares
- `id`
- `name`
- `code` (opcional)
- `organization_kind` o `organization_type`
- `is_active`
- `created_at`
- `updated_at`

### Observaciones
- FREBA también es una organización dentro del modelo
- el tipo de organización puede ser catálogo o choice, según necesidad real

---

## 4.2 `user_organization_membership`

### Propósito
Relaciona usuarios con organizaciones que pueden representar.

### Campos preliminares
- `id`
- `user_id` → user
- `organization_id` → organization
- `is_default`
- `is_active`
- `created_at`

### Cardinalidad
- un usuario puede pertenecer a una o más organizaciones
- una organización puede tener muchos usuarios

### Observaciones
Aunque inicialmente la mayoría de usuarios representen una sola organización, esta tabla deja preparado el soporte para múltiples representaciones.

---

## 5. Tablas configurables

## 5.1 `workflow`

### Propósito
Representa un workflow reutilizable para uno o más tipos de comunicación.

### Campos preliminares
- `id`
- `name`
- `code`
- `description`
- `is_default`
- `is_active`
- `created_at`
- `updated_at`

---

## 5.2 `workflow_state`

### Propósito
Representa los estados posibles dentro de un workflow.

### Campos preliminares
- `id`
- `workflow_id` → workflow
- `name`
- `code`
- `description`
- `is_initial`
- `is_final`
- `display_order`
- `is_active`

### Restricciones sugeridas
- un workflow debería tener un solo estado inicial activo
- los `code` deberían ser únicos dentro de cada workflow

### Observaciones
- esta tabla modela estados, no la matriz fina de transiciones por actor y escenario
- en `v0.2`, la validación de transiciones se resuelve principalmente en la capa lógica de aplicación, alineada con la matriz funcional
- como extensión futura podría evaluarse una estructura complementaria (por ejemplo `workflow_transition` y reglas por rol/escenario), sin volverla obligatoria en esta etapa
- el contrato mínimo con `communication` exige que el estado actual y el estado inicial de cada comunicación pertenezcan al workflow asociado a su tipo

---

## 5.3 `communication_type`

### Propósito
Configura el comportamiento general de una comunicación.

### Campos preliminares
- `id`
- `name`
- `code`
- `description`
- `workflow_id` → workflow
- `default_inbox_id` → inbox
- `is_active`
- `allows_external_creation`
- `allows_internal_creation`
- `created_at`
- `updated_at`

### Observaciones
- `allows_external_creation` y `allows_internal_creation` funcionan como filtros base iniciales
- la habilitación real para crear una comunicación depende además del contexto, rol/perfil y escenario operativo del usuario
- por eso esos campos no alcanzan por sí solos para modelar toda la regla de negocio de creación por tipo
- más adelante podrían agregarse reglas configurables adicionales, pero en `v0.2` conviene mantenerlo relativamente simple

---

## 5.4 `inbox`

### Propósito
Representa la bandeja inicial a la que ingresa una comunicación.

### Campos preliminares
- `id`
- `name`
- `code`
- `description`
- `is_active`

---

## 5.5 `inbox_user`

### Propósito
Relaciona una bandeja con sus usuarios miembros.

### Campos preliminares
- `id`
- `inbox_id` → inbox
- `user_id` → user
- `is_active`
- `created_at`

### Observaciones
En `v0.2`, la bandeja se entiende como lista de usuarios.

---

## 6. Tabla central de operación

## 6.1 `communication`

### Propósito
Representa la comunicación como entidad principal del dominio.

### Campos preliminares
- `id`
- `communication_type_id` → communication_type
- `current_state_id` → workflow_state
- `title`
- `description`
- `origin_organization_id` → organization
- `destination_organization_id` → organization, nullable
- `created_by_user_id` → user
- `created_by_organization_id` → organization
- `updated_by_user_id` → user, nullable
- `closed_at`, nullable
- `closed_by_user_id` → user, nullable
- `created_at`
- `updated_at`

### Campos opcionales recomendados
- `is_closed`
- `last_activity_at`

### Observaciones
- `created_by_organization_id` registra la organización desde la cual actuó el usuario al crear la comunicación
- `origin_organization_id` representa la organización institucional que figura como origen/emisora de la comunicación
- muchas veces `created_by_organization_id` y `origin_organization_id` coinciden, pero no necesariamente
- `destination_organization_id` completa el sentido institucional de origen/destino de la comunicación

### Restricciones conceptuales
- una comunicación debe tener tipo
- una comunicación debe tener estado actual
- una comunicación debe tener usuario creador
- una comunicación debe tener organización creadora o emisora
- el `current_state_id` debe pertenecer al workflow asociado al `communication_type_id` de la comunicación
- al crear la comunicación, el estado inicial debe ser un `workflow_state` inicial del workflow asociado a su tipo
- los cambios de estado válidos se controlan en capa lógica/servicio alineada con la matriz funcional
- la lógica de transiciones detallada puede formalizarse más adelante con una estructura complementaria, sin volverla obligatoria en `v0.2`

---

## 7. Estrategia para atributos particulares por tipo

## 7.1 Decisión estructural propuesta
Modelar una tabla base `communication` y tablas one-to-one por subtipo.

### Ejemplo
- `communication_consulta_tecnica_data`
- `communication_pedido_documentacion_data`
- `communication_nota_formal_data`

### Estructura general de cada subtipo
- `id`
- `communication_id` → communication (unique)
- campos propios del tipo
- timestamps si hiciera falta

### Ventajas
- tipado fuerte
- validación clara
- consultas previsibles
- buen alineamiento con lo ya definido funcionalmente

### Desventajas
- más tablas
- más trabajo cuando crecen los tipos

### Recomendación
Para `v0.2`, esta es la estrategia más alineada con el dominio actual.

---

## 8. Participación y roles

## 8.1 `communication_assignment`

### Propósito
Relaciona usuarios con comunicaciones y define su participación concreta.

### Campos preliminares
- `id`
- `communication_id` → communication
- `user_id` → user
- `organization_id` → organization
- `role`
- `assigned_by_user_id` → user, nullable
- `assigned_at`
- `removed_at`, nullable
- `is_active`

### Valores iniciales sugeridos para `role`
- `observer`
- `editor`
- `responsible`

### Restricciones sugeridas
- evitar múltiples asignaciones activas idénticas para el mismo usuario y comunicación
- `organization_id` debe reflejar la organización desde la cual participa ese usuario en esa comunicación

### Observaciones
Esta tabla es central para permisos y visibilidad.

---

## 9. Respuesta formal

## 9.1 `formal_response`

### Propósito
Representa la respuesta formal única de una comunicación.

### Campos preliminares
- `id`
- `communication_id` → communication (unique)
- `response_text`
- `created_by_user_id` → user
- `created_by_organization_id` → organization
- `created_at`

### Restricciones sugeridas
- una sola respuesta formal por comunicación
- una vez creada, no se edita ni elimina como flujo normal

### Observaciones
La respuesta no tiene estado propio ni workflow propio.

---

## 9.2 `formal_response_document`

### Propósito
Relaciona una respuesta formal con las versiones documentales incluidas en esa respuesta.

### Campos preliminares
- `id`
- `formal_response_id` → formal_response
- `document_version_id` → document_version
- `display_order`

### Motivo de diseño
Conviene referenciar la **versión exacta** usada en la respuesta, no solo el documento lógico, para preservar trazabilidad.

---

## 10. Documentos y versionado

## 10.1 `document`

### Propósito
Representa el documento lógico asociado a una comunicación.

### Campos preliminares
- `id`
- `communication_id` → communication
- `logical_name`
- `document_kind` o `document_type`, nullable
- `created_by_user_id` → user
- `created_at`
- `is_active`

### Observaciones
El documento lógico agrupa sus distintas versiones.

---

## 10.2 `document_version`

### Propósito
Representa una versión concreta de un documento.

### Campos preliminares
- `id`
- `document_id` → document
- `version_number`
- `storage_path` o `file`
- `original_filename`
- `mime_type`
- `uploaded_by_user_id` → user
- `uploaded_by_organization_id` → organization
- `uploaded_at`
- `is_current`
- `is_visible_to_external`, default false
- `notes`, nullable

### Restricciones sugeridas
- una sola versión actual por documento
- `version_number` único por documento

### Observaciones
- regla funcional `v0.2`: el externo ve documentos cargados por su propia organización
- regla funcional `v0.2`: el externo ve adjuntos expuestos en el envío inicial
- regla funcional `v0.2`: el externo ve documentos incluidos en la respuesta formal
- regla funcional `v0.2`: el externo no ve documentos internos de trabajo de FREBA
- `is_visible_to_external` puede usarse como ayuda técnica de implementación, pero no reemplaza por sí solo la regla funcional

---

## 11. Chat y mensajes

## 11.1 `communication_message`

### Propósito
Representa mensajes cronológicos vinculados a una comunicación.

### Campos preliminares
- `id`
- `communication_id` → communication
- `scope`
- `message_text`
- `created_by_user_id` → user
- `created_by_organization_id` → organization
- `created_at`

### Valores sugeridos para `scope`
- `internal`
- `shared`

### Observaciones
- no admite adjuntos propios en `v0.2`
- el control de visibilidad dependerá de `scope` + permisos del usuario

---

## 12. Relaciones entre comunicaciones

## 12.1 `communication_relation`

### Propósito
Representa relaciones entre comunicaciones, principalmente madre-hija.

### Campos preliminares
- `id`
- `parent_communication_id` → communication
- `child_communication_id` → communication
- `relation_type`
- `created_by_user_id` → user
- `created_at`

### Valores iniciales sugeridos para `relation_type`
- `child_of`

### Restricciones sugeridas
- no permitir relación de una comunicación consigo misma
- no permitir duplicados exactos activos del mismo vínculo

### Observaciones
- en `v0.2`, el caso operativo principal para `relation_type` es `child_of`
- la apertura a otros tipos de relación queda como extensión potencial futura, no como eje activo en esta etapa

---

## 13. Expedientes

## 13.1 `expedient`

### Propósito
Representa un agrupador administrativo visible solo para FREBA.

### Campos preliminares
- `id`
- `code` o `identifier`
- `title` o `caratula`
- `subject`
- `created_by_user_id` → user
- `created_at`
- `updated_at`

### Observaciones
No tiene estado propio ni responsables propios en esta etapa.

---

## 13.2 `communication_expedient`

### Propósito
Relaciona comunicaciones con expedientes.

### Campos preliminares
- `id`
- `communication_id` → communication
- `expedient_id` → expedient
- `is_primary`
- `associated_by_user_id` → user
- `associated_at`

### Estrategia recomendada para `v0.2`
- permitir estructuralmente múltiples asociaciones
- operar funcionalmente con una sola asociación primaria por comunicación

### Restricciones sugeridas
- solo una asociación primaria activa por comunicación

---

## 14. Historial y auditoría

## 14.1 `communication_event`

### Propósito
Registrar eventos relevantes del ciclo de vida de una comunicación.

### Campos preliminares
- `id`
- `communication_id` → communication
- `event_type`
- `performed_by_user_id` → user, nullable
- `performed_by_organization_id` → organization, nullable
- `metadata` o `payload` controlado
- `created_at`

### Valores iniciales sugeridos para `event_type`
- `created`
- `updated`
- `state_changed`
- `assigned`
- `unassigned`
- `document_created`
- `document_version_uploaded`
- `formal_response_created`
- `expedient_associated`
- `expedient_changed`
- `child_created`

### Observaciones
Acá sí podría tolerarse un `metadata/payload` acotado para detalles variables del evento, porque es auditoría, no el núcleo del dominio.

---

## 15. Cardinalidades principales

## 15.1 Organización ↔ Usuario
- muchos a muchos, resuelto por `user_organization_membership`

## 15.2 Workflow ↔ WorkflowState
- uno a muchos

## 15.3 CommunicationType ↔ Workflow
- muchos a uno

## 15.4 CommunicationType ↔ Inbox
- muchos a uno

## 15.5 Communication ↔ CommunicationType
- muchos a uno

## 15.6 Communication ↔ WorkflowState
- muchos a uno

## 15.7 Communication ↔ CommunicationAssignment
- uno a muchos

## 15.8 Communication ↔ FormalResponse
- uno a cero/uno

## 15.9 Communication ↔ Document
- uno a muchos

## 15.10 Document ↔ DocumentVersion
- uno a muchos

## 15.11 Communication ↔ CommunicationMessage
- uno a muchos

## 15.12 Communication ↔ CommunicationRelation
- uno a muchos, tanto como padre como hija

## 15.13 Communication ↔ CommunicationExpedient
- uno a muchos a nivel estructural

## 15.14 Expedient ↔ CommunicationExpedient
- uno a muchos

## 15.15 Communication ↔ CommunicationEvent
- uno a muchos

---

## 16. Restricciones conceptuales importantes

## 16.1 Una sola respuesta formal por comunicación
Debe garantizarse con restricción única en `formal_response.communication_id`.

## 16.2 Una sola versión vigente por documento
Debe garantizarse por lógica de aplicación y, si se puede, constraint parcial.

## 16.3 Un solo estado actual por comunicación
La comunicación guarda una sola referencia a `workflow_state`.

## 16.4 Una sola asignación activa equivalente por usuario y comunicación
Debe evitarse duplicar filas activas innecesarias en `communication_assignment`.

## 16.5 Una sola asociación principal de expediente por comunicación en v0.2
Aunque el modelo soporte más, el uso operativo inicial será único.

## 16.6 Estado vigente consistente con workflow del tipo
`communication.current_state_id` debe pertenecer al workflow asociado a `communication.communication_type_id`.

## 16.7 Estado inicial consistente al crear
La comunicación debe iniciar en un `workflow_state` marcado como inicial dentro del workflow asociado a su tipo.

## 16.8 Transiciones válidas en capa lógica
En `v0.2`, la validación de transiciones se implementa en servicios/capa lógica.  
Como extensión futura puede formalizarse una estructura persistente de transiciones, sin volverla obligatoria en esta etapa.

---

## 17. Decisiones de modelado recomendadas

## 17.1 Subtipos de comunicación
### Recomendación
Usar tablas one-to-one por subtipo.

### Justificación
Es lo más alineado con el dominio actual y evita soluciones genéricas débiles.

---

## 17.2 Respuesta formal
### Recomendación
Modelarla como tabla separada con unique sobre `communication_id`.

### Justificación
Preserva claridad conceptual e inmutabilidad.

### Regla estructural de fuente única
- `formal_response.communication_id` (unique) es la única fuente de verdad para vincular respuesta y comunicación
- `communication` no debe tener `formal_response_id` como relación paralela

---

## 17.3 Versionado documental
### Recomendación
Separar documento lógico de versión.

### Justificación
Es la forma más robusta de preservar trazabilidad y vigencia.

---

## 17.4 Relaciones entre comunicaciones
### Recomendación
Usar tabla explícita `communication_relation`.

### Justificación
Mantiene el vínculo como entidad propia sin perder simplicidad operativa.

### Regla operativa `v0.2`
- el caso canónico actual de `relation_type` es `child_of`
- otros tipos de relación quedan como extensión potencial futura y no forman parte del eje operativo actual

---

## 17.5 Asociación a expedientes
### Recomendación
Usar tabla puente `communication_expedient`.

### Justificación
Permite operar con uno solo hoy y quedar preparado para múltiples mañana.

---

## 18. Riesgos del modelo

## 18.1 Explosión de subtablas por tipo
Si aparecen demasiados tipos muy distintos, el modelo puede crecer rápido.

## 18.2 Complejidad por visibilidad documental
La exposición de documentos a externos no debería resolverse solo mirando pertenencia, sino también reglas de visibilidad.

## 18.3 Ambigüedad entre `origin_organization_id` y `created_by_organization_id`
Hay que cuidar bien su sentido para no duplicar semántica de forma confusa.

## 18.4 Complejidad de relaciones entre comunicaciones
Si más adelante se habilitan varios tipos de relación, la UX puede volverse compleja aunque el modelo lo soporte.

## 18.5 Eventos demasiado pobres o demasiado genéricos
`communication_event` debe registrar lo necesario sin volverse un cajón de sastre ilegible.

---

## 19. Recomendación de base para pasar a Django

Tomar como base inicial este orden de modelado:

1. `organization`
2. `user_organization_membership`
3. `workflow`
4. `workflow_state`
5. `inbox`
6. `inbox_user`
7. `communication_type`
8. `communication`
9. subtabla real de un primer tipo de comunicación
10. `communication_assignment`
11. `document`
12. `document_version`
13. `formal_response`
14. `formal_response_document`
15. `communication_message`
16. `communication_relation`
17. `expedient`
18. `communication_expedient`
19. `communication_event`

---

## 20. Pendientes a validar más adelante

- diferencia futura de negocio entre editor y responsable (sin impacto en implementación `v0.2`)
- si se habilitarán tipos de relación adicionales a `child_of`
- si conviene formalizar una estructura persistente de transiciones (por ejemplo `workflow_transition`) o mantenerlas en capa lógica en esta etapa
- si `document_kind` necesita catálogo propio
- si `organization_type` necesita tabla o alcanza con choice
- cuántos subtipos reales existen al inicio
- si algunos estados finales deben restringirse solo a FREBA
- si más adelante la respuesta formal necesita más metadatos

---

## 21. Uso recomendado de este documento

Este archivo debe servir como base para:

- diseñar modelos Django
- armar el primer ERD
- validar si el backend refleja el dominio
- discutir relaciones y cardinalidades antes de codificar
- preparar serializers y endpoints futuros

Debe leerse junto con:

- `00_requerimientos_base_v0_2.md`
- `01_glosario_dominio.md`
- `02_escenarios_y_permisos.md`
- `03_modelo_conceptual.md`
- `04_decisiones_y_supuestos.md`
- `05_plan_implementacion.md`

---
