# Diseno Tecnico de Permisos y Workflow Backend (v0.2)

## Sistema de gestion de comunicaciones FREBA

## 1. Objetivo y alcance

Este documento define la arquitectura tecnica de permisos/backend para el sistema de comunicaciones FREBA, tomando como fuente principal:

- `00_requerimientos_base_v0_2.md`

Y como apoyo obligatorio:

- `01_glosario_dominio.md`
- `02_escenarios_y_permisos.md`
- `03_modelo_conceptual.md`
- `04_decisiones_y_supuestos.md`
- `05_plan_implementacion.md`
- `06_modelo_relacional_preliminar.md`
- `07_matriz_permisos_y_transiciones.md`
- `design/08_diseno_tecnico_modelos_django.md`

El objetivo es dejar una base ejecutable para implementar autorizacion y control de workflow en backend Django/DRF, sin escribir codigo aun.

Fuera de alcance:

- codigo Python
- permission classes concretas
- views/endpoints detallados
- SQL/migraciones

---

## 2. Principios generales de autorizacion backend

## 2.1 No alcanza con "interno vs externo"

La autorizacion se determina por combinacion de:

- tipo de usuario (interno/externo)
- organizacion representada
- asignacion sobre la comunicacion
- rol sobre la comunicacion
- escenario operativo
- estado actual

## 2.2 Ver no es operar

Debe separarse explicitamente:

- visibilidad de comunicacion
- visibilidad de contenido (documentos, chats, historial)
- capacidad de accion (editar, estado, responder, asignar, etc.)

## 2.3 Visibilidad externa deliberada

Nada externo debe exponerse por defecto.  
Toda visibilidad externa debe surgir de reglas explicitas de negocio y escenario.

## 2.4 La asignacion define operacion activa

Para acciones operativas, la asignacion activa es pieza central.  
Puede existir visibilidad organizacional externa basica sin operacion activa.

## 2.5 Escenario condiciona permisos

Un mismo rol no implica mismas acciones en todos los escenarios.

## 2.6 Estado condiciona acciones validas

No basta con "puede cambiar estado": cada accion sobre workflow debe pasar por validacion de estado actual + transicion aceptable en `v0.2`.

## 2.7 Respuesta formal y chat no se mezclan

La respuesta formal es unica, final e inmutable; el chat es intercambio operativo no formal.

---

## 3. Determinacion del escenario operativo en backend

## 3.1 Escenarios a resolver

Para autorizacion se consideran, al menos:

- E1: externo iniciador que espera respuesta
- E2: externo respondedor que recibio comunicacion de FREBA
- I2: interno FREBA operativo
- I3: interno FREBA seguimiento/observador

## 3.2 Fuente de verdad recomendada para inferencia de escenario

La inferencia debe derivarse de datos persistidos, no de parametros enviados por frontend:

- `User` (interno/externo)
- organizacion activa del usuario (`UserOrganizationMembership`)
- `Communication`:
  - `origin_organization_id`
  - `destination_organization_id`
  - `created_by_organization_id`
  - `current_state_id`
- `CommunicationAssignment` activa del usuario sobre esa comunicacion

## 3.3 Regla de inferencia recomendada (opcion principal)

Precedencia estable recomendada para `v0.2`:

1. resolver organizacion activa del actor
2. determinar si actua como FREBA o como externo
3. evaluar relacion institucional de esa organizacion con la comunicacion
4. evaluar asignacion activa y rol sobre la comunicacion
5. si persiste ambiguedad, aplicar la regla mas restrictiva
6. el estado actual no define escenario; solo condiciona acciones dentro del escenario ya resuelto

## 3.4 Errores de diseno a evitar

- aceptar `scenario` informado por frontend como fuente de verdad
- inferir escenario solo por rol (`editor`, `observer`, etc.)
- inferir escenario solo por interno/externo
- ignorar direccion institucional origen/destino de comunicacion
- no considerar estado actual en decisiones de accion

---

## 4. Separacion arquitectura: visibilidad vs accion

## 4.1 Visibilidad de comunicacion

Pregunta: "puede ver esta comunicacion?"

Evaluar:

- pertenencia organizacional y alcance del escenario
- asignacion activa (si corresponde por tipo de visibilidad)
- restricciones externas de acceso

Resultado esperado:

- `denegado`
- `visible parcial` (externo con alcance acotado)
- `visible operativo` (interno/externo con participacion activa)

## 4.2 Visibilidad de contenido dentro de la comunicacion

Pregunta: "si ve la comunicacion, que puede ver adentro?"

Separar por contenido:

- datos generales
- estado actual
- participantes
- historial interno
- chat interno
- chat compartido
- documentos/versions
- expediente

Cada tipo de contenido tiene reglas propias.

Reglas minimas de `v0.2` a mantener explicitas:

- historial interno: solo para internos habilitados; externos no ven historial de comunicacion
- participantes para externos: solo participantes de su propia organizacion
- externos no ven participantes internos de FREBA ni participantes de otras organizaciones externas

## 4.3 Capacidad de accion sobre la comunicacion

Pregunta: "puede ejecutar accion X?"

Evaluar en conjunto:

- escenario inferido
- asignacion activa
- rol sobre comunicacion
- estado actual
- restricciones de organizacion
- reglas de accion especifica (por ejemplo, respuesta formal unica)

---

## 5. Diseno de capa de permisos backend (sin dispersion)

## 5.1 Criterio general recomendado

Implementar autorizacion en cuatro niveles coordinados:

1. filtros de consulta (queryset/lectura)
2. autorizador reutilizable de dominio (decision principal)
3. servicio de accion (reglas de negocio + workflow + consistencia)
4. endpoint (control final y mapeo de error)

## 5.2 Que conviene resolver en filtros/querysets

Objetivo: evitar exposicion accidental.

Resolver aqui:

- listado de comunicaciones visibles para el usuario
- exclusion de comunicaciones externas fuera de su organizacion
- exclusion de expediente para externos
- exclusion de contenido no visible por scope (chat interno, docs internos, etc.)
- exclusion de historial para externos
- exclusion de participantes no visibles para externos (internos FREBA y otras organizaciones externas)

No resolver aqui:

- decisiones complejas de accion mutante
- transiciones de estado
- emision de respuesta formal

## 5.3 Que conviene resolver en autorizadores reutilizables

Objetivo: centralizar reglas de "can_*" por accion.

Resolver aqui:

- determinacion de escenario
- evaluacion de combinacion rol/asignacion/organizacion
- precondiciones comunes (por ejemplo, comunicacion visible, asignacion activa, rol operativo)

Este nivel debe ser la fuente de verdad de autorizacion para servicios y endpoints.

## 5.4 Que conviene resolver en servicios de dominio

Objetivo: validar y ejecutar acciones con invariantes de negocio.

Resolver aqui:

- control de workflow y estado
- control de unicidad/inmutabilidad de respuesta formal
- control de consistencia documental (versionado y exposicion)
- reglas de colaboracion (agregar/quitar participantes)
- reglas de subcomunicacion y expediente
- registro de auditoria como side-effect no bloqueante en `v0.2`

## 5.5 Que conviene validar en endpoints

Objetivo: capa final de seguridad y ergonomia.

Resolver aqui:

- autenticacion
- existencia del recurso
- invocacion al autorizador y al servicio correspondiente
- conversion de denegaciones a respuestas API consistentes

No usar endpoint como lugar principal de reglas de negocio.

---

## 6. Combinacion de factores de permiso

## 6.1 Matriz conceptual de evaluacion

Para toda accion, backend debe evaluar:

1. usuario autenticado valido
2. organizacion activa valida
3. comunicacion visible para ese actor
4. escenario operativo inferido
5. asignacion activa (si aplica)
6. rol habilitante (si aplica)
7. estado actual y reglas de transicion/accion
8. restricciones especificas de accion

## 6.2 Factores por tipo de regla

### Visibilidad basica

Pesa mas:

- tipo de usuario
- organizacion
- escenario

### Operacion activa

Pesa mas:

- asignacion activa
- rol
- escenario
- estado

### Acciones estructurales (respuesta, cierre, expediente, subcomunicacion)

Pesa mas:

- invariantes de dominio
- estado y workflow
- restricciones de negocio v0.2

---

## 7. Acciones nucleo de `v0.2` (arquitectura y validaciones)

En cada accion se detalla:

- quien puede
- precondiciones
- modelos involucrados
- validaciones minimas

## 7.1 Crear comunicacion

### Quien puede

- externo iniciador (E1), si tipo permite creacion externa y cumple contexto
- interno FREBA, si tipo permite creacion interna y cumple contexto

### Precondiciones

- tipo de comunicacion activo
- organizacion activa valida
- regla de creacion por tipo/contexto cumplida
- estado inicial definido en workflow del tipo

### Modelos involucrados

- `CommunicationType`, `Workflow`, `WorkflowState`, `Communication`
- `UserOrganizationMembership`
- `Inbox`/`InboxUser` o seleccion manual de destino segun origen

### Validaciones minimas backend

- `current_state` inicial pertenece al workflow asociado al tipo
- origen/destino institucional consistente con escenario
- asignaciones iniciales segun reglas operativas de v0.2

## 7.2 Editar comunicacion abierta

### Quien puede

- interno operativo asignado (editor/responsable)
- externo respondedor (E2) en datos habilitados

### Precondiciones

- comunicacion visible
- comunicacion no cerrada como flujo normal
- rol/asignacion habilitante

### Modelos involucrados

- `Communication`
- `CommunicationAssignment`

### Validaciones minimas backend

- distinguir campos editables por escenario
- rechazar edicion si la accion contradice continuidad post-respuesta final

## 7.3 Cambiar estado

### Quien puede

- interno operativo habilitado
- externo respondedor (E2) en estados operativos permitidos
- externo iniciador (E1): no cambia workflow principal

### Precondiciones

- asignacion activa y rol habilitante (cuando aplique)
- estado actual valido dentro del workflow del tipo
- transicion aceptable para escenario/accion en `v0.2`

### Modelos involucrados

- `Communication.current_state`
- `WorkflowState`
- `CommunicationType.workflow`
- `CommunicationAssignment`

### Validaciones minimas backend

- pertenencia de estado actual y destino al workflow asociado
- control de transicion por escenario
- registrar evento de cambio de estado

## 7.4 Cerrar comunicacion

### Quien puede

- interno FREBA operativo con rol habilitante
- externo respondedor (E2): no ejecuta cierre administrativo final en `v0.2`

### Precondiciones

- comunicacion en estado compatible de cierre
- actor con capacidad de cierre segun escenario

### Modelos involucrados

- `Communication` (estado/cierre)
- `CommunicationAssignment`

### Validaciones minimas backend

- bloqueo de cierre final por E2
- coherencia con reglas de respuesta formal y workflow

## 7.5 Reabrir comunicacion

### Quien puede

- interno operativo habilitado

### Precondiciones

- comunicacion cerrada
- no existe respuesta formal emitida

### Modelos involucrados

- `Communication`
- `FormalResponse`

### Validaciones minimas backend

- negar reapertura si existe `FormalResponse`
- registrar evento de reapertura

## 7.6 Emitir respuesta formal

### Quien puede

- FREBA en escenario donde corresponde responder
- externo respondedor (E2) cuando la comunicacion fue enviada por FREBA para respuesta

### Precondiciones

- actor habilitado por escenario + asignacion + rol
- no existe respuesta formal previa
- documentos de respuesta seleccionados validos

### Modelos involucrados

- `FormalResponse`
- `FormalResponseDocument`
- `DocumentVersion`
- `Communication`

### Validaciones minimas backend

- unicidad por `communication_id`
- inmutabilidad posterior
- bloqueo de emision duplicada

## 7.7 Subir documento

### Quien puede

- interno operativo
- externo respondedor (E2)
- externo iniciador (E1): en la creacion inicial

### Precondiciones

- comunicacion visible
- accion habilitada por escenario

### Modelos involucrados

- `Document`
- `DocumentVersion`
- `Communication`

### Validaciones minimas backend

- asociacion obligatoria a comunicacion
- trazabilidad de usuario/organizacion cargadora

## 7.8 Subir nueva version documental

### Quien puede

- interno operativo
- externo respondedor (E2)
- externo iniciador (E1): no como flujo normal posterior

### Precondiciones

- existencia de documento logico
- permiso de versionado para escenario/actor

### Modelos involucrados

- `Document`
- `DocumentVersion`

### Validaciones minimas backend

- version incremental consistente
- unica version vigente por documento

## 7.9 Ver documentos visibles

### Quien puede

- todo actor con visibilidad de comunicacion, segun reglas documentales de su escenario

### Precondiciones

- comunicacion visible
- filtro documental por regla funcional (no solo por flag tecnico)

### Modelos involucrados

- `Document`
- `DocumentVersion`
- `FormalResponseDocument`

### Validaciones minimas backend

- separar vista interna completa vs vista externa acotada

## 7.10 Publicar mensaje en chat interno

### Quien puede

- internos FREBA operativos habilitados

### Precondiciones

- actor interno
- participacion operativa habilitada
- scope `internal`

### Modelos involucrados

- `CommunicationMessage`
- `CommunicationAssignment`

### Validaciones minimas backend

- bloqueo total para externos
- no mezclar mensaje con respuesta formal

## 7.11 Publicar mensaje en chat compartido

### Quien puede

- interno operativo habilitado
- externo iniciador (E1) cuando el flujo lo permite
- externo respondedor (E2) en su escenario

### Precondiciones

- comunicacion visible
- scope `shared`
- escenario habilitante

### Modelos involucrados

- `CommunicationMessage`
- `Communication`
- `CommunicationAssignment`

### Validaciones minimas backend

- externos nunca publican en scope interno
- mantener reglas de apertura/habilitacion por flujo

## 7.12 Agregar participante

### Quien puede

- interno operativo
- externo respondedor (E2) solo para usuarios de su misma organizacion

### Precondiciones

- actor con capacidad de administracion de participantes
- usuario objetivo valido

### Modelos involucrados

- `CommunicationAssignment`
- `User`
- `Organization`

### Validaciones minimas backend

- no permitir alta cruzada entre organizaciones externas
- evitar duplicados activos equivalentes

## 7.13 Quitar participante

### Quien puede

- interno operativo
- externo respondedor (E2) con restricciones organizacionales

### Precondiciones

- existencia de asignacion activa objetivo

### Modelos involucrados

- `CommunicationAssignment`

### Validaciones minimas backend

- respetar limites de organizacion para externos
- trazabilidad de baja

## 7.14 Crear subcomunicacion

### Quien puede

- interno operativo
- externo iniciador (E1) como continuidad post-respuesta final
- externo respondedor (E2): no habilitado en `v0.2`

### Precondiciones

- regla de continuidad del caso cumplida
- actor habilitado por escenario

### Modelos involucrados

- `Communication`
- `CommunicationRelation` (`child_of`)

### Validaciones minimas backend

- crear nueva comunicacion independiente
- vincular con `child_of`
- no tratarla como edicion de la madre

## 7.15 Asociar/mover expediente

### Quien puede

- interno operativo (editor/responsable equivalentes en `v0.2`)
- externos: no

### Precondiciones

- comunicacion visible internamente
- actor con rol operativo habilitado

### Modelos involucrados

- `Expedient`
- `CommunicationExpedient`

### Validaciones minimas backend

- externos no ven ni operan expediente
- mantener una asociacion principal operativa por comunicacion en `v0.2`

---

## 8. Diseno tecnico del control de estados y transiciones

## 8.1 Contrato minimo ejecutable

Backend debe garantizar:

1. `Communication.current_state` pertenece al workflow del tipo de comunicacion
2. el estado inicial al crear comunicacion pertenece al mismo workflow y es inicial
3. toda transicion pasa por validacion central en capa logica

## 8.2 Validacion de transicion en `v0.2` (sin motor persistente completo)

Propuesta tecnica:

- usar reglas de transicion mantenidas en capa de servicio/autorizador (fuente unica)
- validar por:
  - estado actual
  - estado destino
  - escenario
  - rol/asignacion
  - accion concreta solicitada

## 8.3 Dependencias de la transicion

### Depende del escenario

- E1 no opera transiciones principales
- E2 opera estados de trabajo y puede dejar "Respondida"
- cierre administrativo final en E2 queda reservado a FREBA

### Depende de rol/asignacion

- actor sin rol operativo no cambia estado
- operacion activa requiere asignacion habilitante

### Depende de la accion concreta

- cerrar, reabrir, responder y continuar por subcomunicacion tienen reglas adicionales

## 8.4 Reapertura y respuesta formal

Regla tecnica obligatoria:

- si existe respuesta formal emitida, negar reapertura como flujo normal
- continuidad se resuelve con nueva comunicacion relacionada

---

## 9. Visibilidad documental externa (backend-side)

## 9.1 Regla funcional obligatoria

Para actor externo, el backend debe permitir ver solo:

- documentos/versiones cargados por su organizacion
- adjuntos expuestos en el envio inicial
- documentos/versiones incluidos en respuesta formal

Y debe negar:

- documentos internos de trabajo de FREBA

## 9.2 Datos del modelo relevantes

Para evaluar visibilidad documental externa, backend debe apoyarse en:

- `DocumentVersion.uploaded_by_organization_id`
- contexto de comunicacion (origen/destino y escenario)
- vinculacion de version en `FormalResponseDocument`
- marcador tecnico de exposicion inicial (si se usa), siempre subordinado a la regla funcional

## 9.3 Que no conviene asumir

- no asumir que `is_visible_to_external` alcanza por si solo
- no asumir que "si participa en la comunicacion ve todo documento"
- no asumir que "ultimo versionado interno" se expone automaticamente

## 9.4 Por que un flag tecnico no alcanza solo

Porque la visibilidad externa es contextual por escenario y por origen documental.  
Un flag sin contexto puede sobreexponer o subexponer informacion.

---

## 10. Chats: diseno backend de acceso y escritura

## 10.1 Chat interno (`scope=internal`)

### Lectura

- solo usuarios internos habilitados

### Escritura

- solo usuarios internos con alcance operativo

### Validaciones minimas

- bloqueo total a externos
- no confundir observador de seguimiento con rol operativo

## 10.2 Chat compartido (`scope=shared`)

### Lectura

- internos operativos
- externos habilitados por escenario

### Escritura

- internos operativos
- E1 cuando el flujo compartido este habilitado
- E2 en escenario de respuesta

### Validaciones minimas

- coherencia de escenario
- no exponer trazas internas por error de scope

## 10.3 Regla de separacion con respuesta formal

- chat no reemplaza respuesta formal
- respuesta formal no se emite ni modifica via chat

---

## 11. Simplificaciones conscientes de `v0.2`

Quedan explicitamente adoptadas:

- `editor` y `responsible` equivalentes en implementacion
- `child_of` como relacion canonica operativa
- externo respondedor sin habilitacion general para crear subcomunicacion
- cierre administrativo final de E2 del lado FREBA
- visibilidad documental externa evaluada por regla funcional contextual
- validacion de transiciones en capa logica, sin motor persistente completo en esta etapa

Estas simplificaciones deben marcarse como `v0.2` para no convertirlas en verdades absolutas de largo plazo.

---

## 12. Riesgos y anti-patrones a evitar

## 12.1 Riesgos

- dispersion de reglas de permisos en demasiadas capas
- inconsistencia entre listado visible y detalle autorizable
- fuga de documentos internos por filtros incompletos
- mezcla de logica de chat con logica de respuesta formal
- reglas de transicion diferentes entre endpoints para la misma accion

## 12.2 Anti-patrones

- usar serializers como fuente principal de autorizacion
- resolver permisos solo en frontend
- no separar visibilidad de accion
- no centralizar determinacion de escenario
- hardcodear transiciones en frontend
- permitir bypass de servicios de dominio desde endpoints

---

## 13. Recomendacion general de arquitectura de permisos backend

Se recomienda una arquitectura con:

- un resolvedor central de contexto de autorizacion (actor, organizacion, escenario, asignacion, rol, estado)
- filtros de visibilidad consistentes para lectura
- autorizadores reutilizables para acciones
- servicios de dominio que apliquen invariantes y reglas de workflow
- endpoint como capa final de control, no como origen de reglas

Esta opcion reduce arbitrariedad, evita contradicciones y mejora mantenibilidad.

---

## 14. Orden sugerido de implementacion de la capa de permisos

1. Resolver contexto de actor y organizacion activa
2. Implementar filtros de visibilidad de comunicacion (listado/detalle)
3. Implementar inferencia central de escenario
4. Implementar autorizadores de acciones nucleo (`can_*`)
5. Implementar validador central de transiciones
6. Implementar validador documental externo contextual
7. Integrar reglas de chat por scope y escenario
8. Integrar reglas de participantes, subcomunicacion y expediente
9. Unificar manejo de denegaciones en endpoints
10. Cubrir con pruebas funcionales de permisos por escenario

---

## 15. Que no conviene sofisticar de mas en `v0.2`

Para esta etapa se recomienda no sobredisenar:

- motor persistente completo de transiciones por rol/escenario
- parametrizacion dinamica extrema de reglas de permisos
- multiples estrategias de relacion entre comunicaciones mas alla de `child_of`
- modelos adicionales de exposicion documental si aun no aportan valor claro

Primero debe consolidarse una capa de autorizacion central, consistente y testeable.

---

## 16. Estado de cierre para pasar a implementacion

Con esta propuesta, backend puede avanzar a implementacion con:

- reglas de autorizacion explicitadas por capas
- contrato minimo de workflow operativo
- acciones nucleo de `v0.2` definidas con precondiciones y validaciones
- simplificaciones de etapa declaradas

Los pendientes funcionales abiertos quedan marcados como pendientes y no se convierten en reglas nuevas de negocio.
