
# Diseno Tecnico de Servicios y Casos de Uso Backend (v0.2)

## Sistema de gestion de comunicaciones FREBA

## 1. Objetivo y alcance

Este documento define la propuesta tecnica de servicios backend y casos de uso para implementar FREBA en Django + DRF, tomando como fuente principal:

- `00_requerimientos_base_v0_2.md`

Y como apoyo:

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

No incluye codigo. Define ownership, validaciones y flujos de alto nivel para pasar de arquitectura a implementacion.

---

## 2. Principios generales de diseno de servicios

## 2.1 Los servicios orquestan negocio

Los servicios/casos de uso son el punto principal de orquestacion de reglas de dominio, no las views o serializers.

## 2.2 Ownership claro por app

Cada caso de uso debe tener una app owner principal y apps colaboradoras explicitas.

## 2.3 Autorizacion reusable, no dispersa

La autorizacion reusable se apoya en la capa definida en `design/09_diseno_tecnico_permisos_backend.md`.

## 2.4 Validar invariantes de dominio

Cada servicio debe validar invariantes clave:

- comunicacion como entidad central
- respuesta formal unica e inmutable
- contrato workflow-estado
- reglas de asignacion/escenario
- visibilidad documental externa contextual

## 2.5 Auditoria explicita y desacoplada

Los servicios deben registrar eventos relevantes de forma explicita, pero sin acoplar el dominio a `audit` como dependencia bloqueante.
En `v0.2`, la auditoria se trata como side-effect no bloqueante: la operacion principal del caso de uso owner no debe fallar solo por una falla de persistencia de auditoria.

## 2.6 Pragmatismo v0.2

Evitar una capa de servicios sobredimensionada. Un servicio por caso de uso principal suele ser suficiente en esta etapa.

---

## 3. Que es un caso de uso en este backend

Un caso de uso en FREBA es una operacion de negocio con:

- actor definido
- escenario operativo definido
- precondiciones
- validaciones criticas
- mutacion o lectura sobre modelos
- resultado esperado
- efectos secundarios controlados
- eventos de auditoria
- errores/denegaciones esperables

Un caso de uso puede tocar una o varias apps, pero siempre conserva ownership claro en una app principal. No debe quedar repartido arbitrariamente entre view, serializer y modelo.

---

## 4. Mapa general de casos de uso principales `v0.2`

| ID | Caso de uso | Tipo | App owner |
|---|---|---|---|
| CU-01 | Crear comunicacion externa | Mutacion | `communications` |
| CU-02 | Crear comunicacion interna | Mutacion | `communications` |
| CU-03 | Editar comunicacion abierta | Mutacion | `communications` |
| CU-04 | Asignar participante | Mutacion | `communications` |
| CU-05 | Quitar participante | Mutacion | `communications` |
| CU-06 | Cambiar estado | Mutacion | `communications` |
| CU-07 | Cerrar comunicacion | Mutacion | `communications` |
| CU-08 | Reabrir comunicacion | Mutacion | `communications` |
| CU-09 | Emitir respuesta formal | Mutacion | `communications` |
| CU-10 | Crear subcomunicacion | Mutacion | `communications` |
| CU-11 | Asociar expediente | Mutacion | `expedients` |
| CU-12 | Mover expediente | Mutacion | `expedients` |
| CU-13 | Subir documento | Mutacion | `documents` |
| CU-14 | Subir nueva version documental | Mutacion | `documents` |
| CU-15 | Publicar mensaje interno | Mutacion | `chats` |
| CU-16 | Publicar mensaje compartido | Mutacion | `chats` |
| CU-17 | Consultar detalle de comunicacion | Lectura | `communications` |
| CU-18 | Consultar documentos visibles | Lectura | `documents` |
| CU-19 | Consultar historial | Lectura | `audit` |
| CU-20 | Consultar subcomunicaciones relacionadas | Lectura | `communications` |

---

## 5. Casos de uso principales (ficha tecnica uniforme)

Formato aplicado en todas las fichas:

- proposito
- actor/es posibles
- escenario/s aplicables
- app owner principal
- apps colaboradoras
- modelos involucrados
- precondiciones
- validaciones criticas
- pasos de alto nivel del flujo backend
- efectos secundarios
- eventos de auditoria sugeridos
- errores o denegaciones esperables
- observaciones de `v0.2`

## 5.1 CU-01 Crear comunicacion externa

- Proposito: permitir que un externo iniciador cree una comunicacion hacia FREBA.
- Actor/es posibles: usuario externo.
- Escenario/s aplicables: E1.
- App owner principal: `communications`.
- Apps colaboradoras: `accounts`, `organizations`, `communication_config`, `permissions_support`, `audit`.
- Modelos involucrados: `Communication`, `CommunicationType`, `Workflow`, `WorkflowState`, `CommunicationAssignment`, `UserOrganizationMembership`.
- Precondiciones: usuario externo activo; organizacion activa; tipo habilitado para creacion externa; estado inicial disponible.
- Validaciones criticas: coherencia origen/destino; estado inicial pertenece al workflow del tipo; reglas de creacion por tipo/contexto.
- Pasos de alto nivel del flujo backend:
1. Resolver contexto de actor y organizacion activa.
2. Validar autorizacion de creacion externa para tipo seleccionado.
3. Resolver workflow y estado inicial.
4. Persistir comunicacion.
5. Crear asignaciones iniciales segun regla de etapa.
6. Registrar evento.
- Efectos secundarios: comunicacion enviada y visible segun escenario.
- Eventos de auditoria sugeridos: `created`, `assigned`.
- Errores o denegaciones esperables: tipo no habilitado; organizacion invalida; estado inicial no configurado; denegacion de escenario.
- Observaciones de `v0.2`: sin borrador formal; envio inmediato al crear.

## 5.2 CU-02 Crear comunicacion interna

- Proposito: permitir creacion de comunicacion por usuario interno FREBA.
- Actor/es posibles: usuario interno operativo.
- Escenario/s aplicables: I1/I2.
- App owner principal: `communications`.
- Apps colaboradoras: `accounts`, `organizations`, `communication_config`, `permissions_support`, `audit`.
- Modelos involucrados: `Communication`, `CommunicationType`, `WorkflowState`, `CommunicationAssignment`.
- Precondiciones: tipo activo y habilitado para creacion interna; organizacion de origen FREBA valida.
- Validaciones criticas: estado inicial valido; coherencia de destino externo si aplica; asignaciones iniciales consistentes.
- Pasos de alto nivel del flujo backend:
1. Resolver contexto interno.
2. Validar creacion por tipo.
3. Resolver estado inicial.
4. Crear comunicacion y asignaciones iniciales.
5. Registrar evento.
- Efectos secundarios: para salientes a externos, visibilidad de organizacion destino al enviarse.
- Eventos de auditoria sugeridos: `created`, `assigned`.
- Errores o denegaciones esperables: tipo inactivo; destino inconsistente; denegacion por perfil.
- Observaciones de `v0.2`: la seleccion de destino reemplaza logica de bandeja externa.

## 5.3 CU-03 Editar comunicacion abierta

- Proposito: actualizar datos permitidos de comunicacion mientras este abierta.
- Actor/es posibles: interno operativo; externo respondedor en datos habilitados.
- Escenario/s aplicables: I2, E2.
- App owner principal: `communications`.
- Apps colaboradoras: `permissions_support`, `audit`.
- Modelos involucrados: `Communication`, subtabla por tipo, `CommunicationAssignment`.
- Precondiciones: comunicacion visible; comunicacion abierta; actor habilitado por escenario.
- Validaciones criticas: campos editables por escenario; bloqueo en casos no permitidos; consistencia de subtipo.
- Pasos de alto nivel del flujo backend:
1. Cargar comunicacion y contexto.
2. Autorizar accion de edicion.
3. Validar datos permitidos.
4. Persistir cambios.
5. Registrar evento.
- Efectos secundarios: actualizacion de `updated_by` y `updated_at`.
- Eventos de auditoria sugeridos: `updated`.
- Errores o denegaciones esperables: comunicacion cerrada; actor sin rol operativo; campo no editable.
- Observaciones de `v0.2`: externo iniciador no edita como flujo normal post envio.

## 5.4 CU-04 Asignar participante

- Proposito: agregar usuario participante a comunicacion.
- Actor/es posibles: interno operativo; externo respondedor con restricciones.
- Escenario/s aplicables: I2, E2.
- App owner principal: `communications`.
- Apps colaboradoras: `accounts`, `organizations`, `permissions_support`, `audit`.
- Modelos involucrados: `CommunicationAssignment`, `Communication`, `UserOrganizationMembership`.
- Precondiciones: actor con capacidad de administrar participantes.
- Validaciones criticas: evitar duplicado activo; restriccion organizacional para externo.
- Pasos de alto nivel del flujo backend:
1. Resolver contexto y escenario.
2. Autorizar alta de participante.
3. Validar usuario objetivo.
4. Crear asignacion activa.
5. Registrar evento.
- Efectos secundarios: ampliacion de colaboracion operativa.
- Eventos de auditoria sugeridos: `assigned`.
- Errores o denegaciones esperables: usuario inexistente; asignacion duplicada; externo intentando asignar otra organizacion.
- Observaciones de `v0.2`: para externos en E2, solo misma organizacion.

## 5.5 CU-05 Quitar participante

- Proposito: remover participacion activa de un usuario.
- Actor/es posibles: interno operativo; externo respondedor con restricciones.
- Escenario/s aplicables: I2, E2.
- App owner principal: `communications`.
- Apps colaboradoras: `permissions_support`, `audit`.
- Modelos involucrados: `CommunicationAssignment`.
- Precondiciones: asignacion activa existente; actor habilitado.
- Validaciones criticas: restricciones por organizacion para externos.
- Pasos de alto nivel del flujo backend:
1. Resolver contexto.
2. Autorizar baja.
3. Marcar asignacion como inactiva/removida.
4. Registrar evento.
- Efectos secundarios: perdida de operacion activa para usuario removido.
- Eventos de auditoria sugeridos: `unassigned`.
- Errores o denegaciones esperables: asignacion no existente; actor no habilitado.
- Observaciones de `v0.2`: mantener criterio simple, sin politicas complejas de ownership.

## 5.6 CU-06 Cambiar estado

- Proposito: mover comunicacion entre estados validos del workflow.
- Actor/es posibles: interno operativo; externo respondedor en alcance permitido.
- Escenario/s aplicables: I2, E2.
- App owner principal: `communications`.
- Apps colaboradoras: `communication_config`, `permissions_support`, `audit`.
- Modelos involucrados: `Communication`, `WorkflowState`, `CommunicationType`, `CommunicationAssignment`.
- Precondiciones: actor autorizado; estado actual valido; estado destino solicitado.
- Validaciones criticas: estado actual y destino pertenecen al workflow del tipo; transicion aceptable en `v0.2`; reglas por escenario.
- Pasos de alto nivel del flujo backend:
1. Resolver contexto y autorizacion.
2. Validar contrato workflow-estado.
3. Validar regla de transicion.
4. Persistir nuevo estado.
5. Registrar evento.
- Efectos secundarios: impacto en acciones posteriores (respuesta, cierre, colaboracion).
- Eventos de auditoria sugeridos: `state_changed`.
- Errores o denegaciones esperables: estado fuera de workflow; transicion no permitida; actor sin rol operativo.
- Observaciones de `v0.2`: cierre administrativo final en E2 queda del lado FREBA.

## 5.7 CU-07 Cerrar comunicacion

- Proposito: cerrar comunicacion como parte del flujo administrativo.
- Actor/es posibles: interno operativo habilitado.
- Escenario/s aplicables: I2.
- App owner principal: `communications`.
- Apps colaboradoras: `permissions_support`, `audit`.
- Modelos involucrados: `Communication`.
- Precondiciones: estado compatible de cierre; actor habilitado.
- Validaciones criticas: restriccion por escenario (E2 no cierra administrativamente en `v0.2`).
- Pasos de alto nivel del flujo backend:
1. Autorizar cierre.
2. Validar consistencia de estado.
3. Marcar cierre.
4. Registrar evento.
- Efectos secundarios: bloqueo de operacion normal sobre comunicacion cerrada.
- Eventos de auditoria sugeridos: `state_changed` a estado de cierre o evento de cierre administrativo.
- Errores o denegaciones esperables: actor externo; estado invalido para cierre.
- Observaciones de `v0.2`: cierre y respuesta se distinguen como acciones.

## 5.8 CU-08 Reabrir comunicacion

- Proposito: reactivar comunicacion cerrada sin respuesta formal emitida.
- Actor/es posibles: interno operativo habilitado.
- Escenario/s aplicables: I2.
- App owner principal: `communications`.
- Apps colaboradoras: `permissions_support`, `audit`.
- Modelos involucrados: `Communication`, `FormalResponse`.
- Precondiciones: comunicacion cerrada; actor autorizado.
- Validaciones criticas: inexistencia de respuesta formal emitida.
- Pasos de alto nivel del flujo backend:
1. Autorizar reapertura.
2. Verificar ausencia de `FormalResponse`.
3. Cambiar a estado operativo de reapertura.
4. Registrar evento.
- Efectos secundarios: comunicacion vuelve a flujo activo.
- Eventos de auditoria sugeridos: `state_changed` a estado reabierto.
- Errores o denegaciones esperables: existe respuesta formal; actor no habilitado.
- Observaciones de `v0.2`: con respuesta formal final se recomienda continuidad via hija.

## 5.9 CU-09 Emitir respuesta formal

- Proposito: emitir respuesta formal unica y final de una comunicacion.
- Actor/es posibles: interno FREBA o externo respondedor, segun escenario.
- Escenario/s aplicables: E1 (responde FREBA), E2 (responde externo), I2 segun flujo.
- App owner principal: `communications`.
- Apps colaboradoras: `documents`, `permissions_support`, `audit`.
- Modelos involucrados: `FormalResponse`, `FormalResponseDocument`, `Communication`, `DocumentVersion`.
- Precondiciones: actor habilitado; comunicacion apta para respuesta; no existe respuesta previa.
- Validaciones criticas: unicidad por `communication_id`; inmutabilidad posterior; versiones documentales validas para incluir.
- Pasos de alto nivel del flujo backend:
1. Autorizar emision por escenario/rol/asignacion.
2. Verificar inexistencia de respuesta formal.
3. Validar contenido y documentos incluidos.
4. Persistir respuesta formal y sus documentos.
5. Registrar evento.
- Efectos secundarios: cambio fuerte de ciclo de vida; continuidad posterior via nueva comunicacion relacionada.
- Eventos de auditoria sugeridos: `formal_response_created`.
- Errores o denegaciones esperables: respuesta ya existente; actor no autorizado; documento invalido.
- Observaciones de `v0.2`: respuesta formal no se edita ni anula como flujo normal.

## 5.10 CU-10 Crear subcomunicacion

- Proposito: abrir gestion formal nueva, independiente y vinculada a una comunicacion madre.
- Actor/es posibles: interno operativo; externo iniciador por continuidad post respuesta final.
- Escenario/s aplicables: I2, E1 (continuidad).
- App owner principal: `communications`.
- Apps colaboradoras: `communication_config`, `permissions_support`, `expedients`, `audit`.
- Modelos involucrados: `Communication`, `CommunicationRelation`, `CommunicationExpedient` (si aplica propagacion).
- Precondiciones: criterio funcional de nueva gestion separada; actor habilitado.
- Validaciones criticas: no usar subcomunicacion para reemplazar colaboracion simple; crear `relation_type=child_of`; reglas de escenario externo.
- Pasos de alto nivel del flujo backend:
1. Autorizar creacion de subcomunicacion.
2. Crear nueva comunicacion independiente.
3. Crear relacion madre-hija (`child_of`).
4. Aplicar asociacion de expediente segun regla vigente.
5. Registrar evento.
- Efectos secundarios: nueva unidad de trabajo con workflow propio.
- Eventos de auditoria sugeridos: `child_created`.
- Errores o denegaciones esperables: actor no habilitado; intento de usar subcomunicacion en lugar de asignacion.
- Observaciones de `v0.2`: externo respondedor no habilitado en regla general.

## 5.11 CU-11 Asociar expediente

- Proposito: vincular comunicacion a expediente.
- Actor/es posibles: interno operativo (editor/responsable equivalentes en `v0.2`).
- Escenario/s aplicables: I2.
- App owner principal: `expedients`.
- Apps colaboradoras: `communications`, `permissions_support`, `audit`.
- Modelos involucrados: `Expedient`, `CommunicationExpedient`, `Communication`.
- Precondiciones: actor interno autorizado; expediente existente.
- Validaciones criticas: respetar operacion con expediente principal unico.
- Pasos de alto nivel del flujo backend:
1. Autorizar asociacion.
2. Validar expediente objetivo.
3. Crear/ajustar asociacion primaria.
4. Registrar evento.
- Efectos secundarios: contextualizacion administrativa.
- Eventos de auditoria sugeridos: `expedient_associated`.
- Errores o denegaciones esperables: externo intentando asociar; expediente inexistente.
- Observaciones de `v0.2`: se simplifica a un principal operativo.

## 5.12 CU-12 Mover expediente

- Proposito: cambiar asociacion de expediente de la comunicacion.
- Actor/es posibles: interno operativo autorizado.
- Escenario/s aplicables: I2.
- App owner principal: `expedients`.
- Apps colaboradoras: `communications`, `permissions_support`, `audit`.
- Modelos involucrados: `CommunicationExpedient`.
- Precondiciones: asociacion existente; expediente destino valido.
- Validaciones criticas: mantener una sola asociacion primaria activa.
- Pasos de alto nivel del flujo backend:
1. Autorizar movimiento.
2. Validar expediente destino.
3. Ajustar asociacion principal.
4. Registrar evento.
- Efectos secundarios: cambio de contexto administrativo.
- Eventos de auditoria sugeridos: `expedient_changed`.
- Errores o denegaciones esperables: actor no autorizado; destino invalido.
- Observaciones de `v0.2`: logica simple, sin matriz compleja de expedientes multiples.

## 5.13 CU-13 Subir documento

- Proposito: crear documento logico y su primera version.
- Actor/es posibles: interno operativo; externo respondedor; externo iniciador al crear.
- Escenario/s aplicables: E1 (alta inicial), E2, I2.
- App owner principal: `documents`.
- Apps colaboradoras: `communications`, `permissions_support`, `audit`.
- Modelos involucrados: `Document`, `DocumentVersion`, `Communication`.
- Precondiciones: comunicacion visible y operable para actor en ese escenario.
- Validaciones criticas: distinguir alta de documento nuevo vs versionado; ownership de organizacion cargadora.
- Pasos de alto nivel del flujo backend:
1. Autorizar carga documental.
2. Crear documento logico.
3. Crear version inicial.
4. Registrar evento.
- Efectos secundarios: nuevo artefacto documental disponible para flujo.
- Eventos de auditoria sugeridos: `document_created`, `document_version_uploaded`.
- Errores o denegaciones esperables: actor sin permiso; carga fuera de escenario permitido.
- Observaciones de `v0.2`: externos no acceden a documentos internos de trabajo FREBA.

## 5.14 CU-14 Subir nueva version documental

- Proposito: agregar version sobre documento existente.
- Actor/es posibles: interno operativo; externo respondedor habilitado.
- Escenario/s aplicables: E2, I2.
- App owner principal: `documents`.
- Apps colaboradoras: `communications`, `permissions_support`, `audit`.
- Modelos involucrados: `DocumentVersion`, `Document`.
- Precondiciones: documento existente; actor habilitado para versionar.
- Validaciones criticas: unicidad de version por documento; una sola version vigente.
- Pasos de alto nivel del flujo backend:
1. Autorizar versionado.
2. Validar version actual.
3. Crear nueva version y actualizar vigente.
4. Registrar evento.
- Efectos secundarios: historial documental trazable.
- Eventos de auditoria sugeridos: `document_version_uploaded`.
- Errores o denegaciones esperables: documento inexistente; actor sin permiso; versionado inconsistente.
- Observaciones de `v0.2`: no confundir versionado con alta de documento nuevo.

## 5.15 CU-15 Publicar mensaje interno

- Proposito: permitir colaboracion interna FREBA en comunicacion.
- Actor/es posibles: internos habilitados.
- Escenario/s aplicables: I2.
- App owner principal: `chats`.
- Apps colaboradoras: `communications`, `permissions_support`, `audit`.
- Modelos involucrados: `CommunicationMessage` (`scope=internal`), `Communication`.
- Precondiciones: actor interno; comunicacion visible; scope interno.
- Validaciones criticas: bloqueo total de externos; validacion de scope.
- Pasos de alto nivel del flujo backend:
1. Autorizar publicacion interna.
2. Validar scope y pertenencia de actor.
3. Persistir mensaje.
4. Registrar evento.
- Efectos secundarios: enriquecimiento de colaboracion interna.
- Eventos de auditoria sugeridos: evento de mensaje interno publicado.
- Errores o denegaciones esperables: externo intentando publicar; scope invalido.
- Observaciones de `v0.2`: chat interno nunca visible a externos.

## 5.16 CU-16 Publicar mensaje compartido

- Proposito: intercambio operativo entre FREBA y contraparte externa.
- Actor/es posibles: interno operativo; externo habilitado por escenario.
- Escenario/s aplicables: E1 (cuando corresponda), E2, I2.
- App owner principal: `chats`.
- Apps colaboradoras: `communications`, `permissions_support`, `audit`.
- Modelos involucrados: `CommunicationMessage` (`scope=shared`), `CommunicationAssignment` (cuando aplique).
- Precondiciones: comunicacion visible; flujo compartido habilitado para actor.
- Validaciones criticas: validacion de escenario; prohibicion de usar scope interno para externos.
- Pasos de alto nivel del flujo backend:
1. Resolver escenario y autorizacion.
2. Validar scope compartido.
3. Persistir mensaje.
4. Registrar evento.
- Efectos secundarios: trazabilidad de intercambio no formal.
- Eventos de auditoria sugeridos: evento de mensaje compartido publicado.
- Errores o denegaciones esperables: actor no habilitado; escenario no compatible.
- Observaciones de `v0.2`: chat compartido no reemplaza respuesta formal.

## 5.17 CU-17 Consultar detalle de comunicacion

- Proposito: devolver vista de detalle segun visibilidad del actor.
- Actor/es posibles: internos y externos habilitados.
- Escenario/s aplicables: E1, E2, I2, I3.
- App owner principal: `communications`.
- Apps colaboradoras: `permissions_support`, `documents`, `chats`, `expedients`.
- Modelos involucrados: `Communication`, `CommunicationAssignment`, relaciones de lectura asociadas.
- Precondiciones: comunicacion visible para actor.
- Validaciones criticas: separar campos internos de externos; no exponer contexto interno por error.
- Pasos de alto nivel del flujo backend:
1. Filtrar visibilidad de comunicacion.
2. Cargar detalle acorde a alcance.
3. Retornar vista de detalle.
- Efectos secundarios: ninguno de dominio.
- Eventos de auditoria sugeridos: opcional segun politicas de trazabilidad de lectura.
- Errores o denegaciones esperables: acceso denegado por visibilidad.
- Observaciones de `v0.2`: externos ven datos generales + estado + alcance permitido; si no existe respuesta formal aun, el detalle debe exponer ese campo en `null` (u equivalente semantico vacio) cuando la comunicacion es visible.

## 5.18 CU-18 Consultar documentos visibles

- Proposito: listar documentos/versiones visibles para actor.
- Actor/es posibles: internos y externos con visibilidad de comunicacion.
- Escenario/s aplicables: E1, E2, I2, I3.
- App owner principal: `documents`.
- Apps colaboradoras: `communications`, `permissions_support`.
- Modelos involucrados: `Document`, `DocumentVersion`, `FormalResponseDocument`.
- Precondiciones: comunicacion visible.
- Validaciones criticas: aplicar regla funcional externa contextual; no confiar solo en flag tecnico.
- Pasos de alto nivel del flujo backend:
1. Resolver visibilidad de comunicacion.
2. Aplicar politica documental por actor/escenario.
3. Retornar documentos/versiones permitidos.
- Efectos secundarios: ninguno de dominio.
- Eventos de auditoria sugeridos: opcional segun politicas.
- Errores o denegaciones esperables: acceso denegado; intento de ver documentos internos.
- Observaciones de `v0.2`: externos ven propios, expuestos iniciales, incluidos en respuesta.

## 5.19 CU-19 Consultar historial

- Proposito: exponer trazabilidad interna de la comunicacion para actores FREBA habilitados.
- Actor/es posibles: internos con acceso.
- Escenario/s aplicables: I2, I3.
- App owner principal: `audit`.
- Apps colaboradoras: `communications`, `permissions_support`.
- Modelos involucrados: `CommunicationEvent`, `Communication`.
- Precondiciones: comunicacion visible.
- Validaciones criticas: historial completo interno segun permisos; negar historial para actores externos en `v0.2`.
- Pasos de alto nivel del flujo backend:
1. Autorizar lectura de historial.
2. Filtrar eventos segun alcance interno del actor.
3. Retornar secuencia temporal.
- Efectos secundarios: ninguno de dominio.
- Eventos de auditoria sugeridos: opcional lectura.
- Errores o denegaciones esperables: externo solicitando historial interno.
- Observaciones de `v0.2`: no existe historial externo equivalente al interno; para externos el seguimiento se resuelve por detalle + estado actual + respuesta formal + documentos visibles + chat compartido.

## 5.20 CU-20 Consultar subcomunicaciones relacionadas

- Proposito: navegar continuidad madre-hija del caso.
- Actor/es posibles: internos y externos con alcance de visibilidad.
- Escenario/s aplicables: E1, E2, I2, I3.
- App owner principal: `communications`.
- Apps colaboradoras: `permissions_support`.
- Modelos involucrados: `CommunicationRelation`, `Communication`.
- Precondiciones: comunicacion base visible.
- Validaciones criticas: filtrar hijas/relaciones segun visibilidad del actor.
- Pasos de alto nivel del flujo backend:
1. Autorizar lectura de relaciones.
2. Buscar relaciones `child_of`.
3. Devolver resumen de madre/hijas visibles.
- Efectos secundarios: ninguno de dominio.
- Eventos de auditoria sugeridos: opcional lectura.
- Errores o denegaciones esperables: acceso denegado a relaciones internas.
- Observaciones de `v0.2`: foco operativo en `child_of`.

## 6. Ownership de servicios por app

## 6.1 Recomendacion de ownership principal

- `communications`: CU-01 a CU-10, CU-17, CU-20
- `documents`: CU-13, CU-14, CU-18
- `chats`: CU-15, CU-16
- `expedients`: CU-11, CU-12
- `audit`: CU-19

## 6.2 Justificacion

- La app owner mantiene invariantes del objeto que gobierna.
- Apps colaboradoras aportan datos/reglas, sin aduenarse de la operacion.
- Se evita acoplamiento cruzado y mega-servicios.

---

## 7. Servicios transversales o de apoyo

## 7.1 Servicios de dominio owner

Son servicios que mutan estado de negocio en su app owner.

## 7.2 Servicios de apoyo reutilizables

En `permissions_support`, al menos:

- resolvedor de contexto de actor/escenario
- autorizadores reutilizables por accion
- politicas de visibilidad reusable

## 7.3 Servicios de lectura especializada

Pueden existir servicios de lectura cuando una consulta cruza multiples apps, por ejemplo:

- detalle enriquecido de comunicacion
- vista documental filtrada por escenario
- historial filtrado por actor interno

## 7.4 Limite recomendado

No inflar con una "application layer" abstracta si no agrega valor real en `v0.2`.

---

## 8. Relacion entre servicios, permisos y workflow

## 8.1 Secuencia conceptual recomendada en mutaciones

1. Endpoint valida formato basico y autenticacion.
2. Servicio owner carga recurso y contexto.
3. Capa de permisos autoriza accion.
4. Servicio owner valida invariantes de negocio.
5. Validador de workflow/estado valida transicion si aplica.
6. Servicio persiste cambios.
7. Servicio dispara registro de auditoria explicita como side-effect no bloqueante en `v0.2`.
8. Endpoint retorna resultado.

## 8.2 Que valida cada capa

- Capa de permisos: quien puede hacer que segun escenario/asignacion/rol/visibilidad (con precedencia estable de inferencia definida en `design/09`).
- Servicio de negocio: si esta accion tiene sentido de dominio ahora.
- Workflow: si el cambio de estado es aceptable para este tipo/estado/escenario.
- Filtros de visibilidad: que se puede leer.

## 8.3 Que no conviene duplicar

- no duplicar la misma regla de autorizacion en view y servicio
- no duplicar validaciones de transicion en multiples endpoints
- no duplicar politicas documentales en `documents` y `communications` sin contrato comun

---

## 9. Casos especialmente delicados

## 9.1 Crear comunicacion (externo vs interno)

Puntos clave:

- escenarios distintos, misma entidad central
- validacion de tipo habilitado por contexto
- estado inicial siempre desde workflow del tipo
- control de visibilidad inicial segun origen/destino y escenario

## 9.2 Emitir respuesta formal

Puntos clave:

- unicidad por comunicacion
- inmutabilidad post emision
- inclusion de versiones documentales concretas
- actor habilitado segun escenario (FREBA o externo respondedor)

## 9.3 Cambiar estado

Puntos clave:

- escenario condiciona alcance
- asignacion/rol condicionan operacion activa
- contrato workflow-estado obligatorio
- cierre administrativo final de E2 reservado a FREBA

## 9.4 Subcomunicacion

Puntos clave:

- abrir gestion nueva independiente
- no reemplaza editar madre ni sumar usuarios
- relacion canonica `child_of`
- externo respondedor no habilitado en `v0.2`

## 9.5 Documentos

Puntos clave:

- separar alta de documento nuevo vs nueva version
- aplicar visibilidad externa contextual
- relacion con respuesta formal via versiones incluidas

## 9.6 Chat

Puntos clave:

- separar `internal` y `shared`
- validar actor/esquema por escenario
- no mezclar chat con respuesta formal

---

## 10. Lectura vs mutacion en backend

## 10.1 Casos de lectura

Caracteristicas:

- prioridad en filtros de visibilidad
- bajo efecto colateral de dominio
- posible composicion de datos de multiples apps
- auditoria de lectura opcional segun politica

## 10.2 Casos de mutacion

Caracteristicas:

- autorizacion estricta por accion
- validacion de invariantes de dominio
- validacion de workflow cuando aplica
- persistencia transaccional de cambios
- auditoria explicita recomendada

## 10.3 Implicancia tecnica

No tratar lectura y mutacion como operaciones equivalentes en arquitectura de servicios.

## 11. Riesgos y anti-patrones

## 11.1 Riesgos

- logica de negocio en views/serializers
- servicios gigantes con demasiadas responsabilidades
- duplicacion de reglas entre apps
- auditoria implicita no controlada
- mezclar visibilidad con mutacion
- confundir crear documento con versionar documento

## 11.2 Anti-patrones a evitar

- mega servicio unico por app con todas las operaciones mezcladas
- usar signals como reemplazo de servicios principales
- repartir validaciones de estado en varios lugares sin fuente unica
- delegar reglas de autorizacion a frontend

---

## 12. Propuesta principal y granularidad recomendada

## 12.1 Propuesta principal

Un servicio por caso de uso principal, con apoyo de:

- autorizadores reutilizables
- validador de transicion central
- registrador de auditoria explicito

## 12.2 Lo que no conviene

- mega-servicio unico por app con decenas de ramas
- fragmentacion extrema en micro-servicios internos sin necesidad (`v0.2`)

## 12.3 Granularidad sugerida `v0.2`

Nivel medio:

- suficiente para ownership y pruebas
- sin sobrecarga arquitectonica innecesaria

---

## 13. Orden sugerido de diseno/implementacion de servicios

Orden alineado con `05`, `08`, `09` y `10`:

1. CU-01, CU-02 (creacion de comunicacion)
2. CU-04, CU-05 (participantes y asignaciones)
3. CU-06, CU-07, CU-08 (estado/cierre/reapertura)
4. CU-13, CU-14, CU-18 (documentos y visibilidad)
5. CU-09 (respuesta formal)
6. CU-15, CU-16 (chat)
7. CU-10, CU-20 (subcomunicaciones y relaciones)
8. CU-11, CU-12 (expedientes)
9. CU-17 y CU-19 (detalle e historial robusto)
10. endurecimiento de permisos y validaciones finas de borde

Este orden sigue la progresion: nucleo operativo, resolucion formal, colaboracion, contexto y trazabilidad avanzada.

---

## 14. Cierre y recomendacion general

## 14.1 Recomendacion general de arquitectura de servicios

Adoptar una arquitectura por casos de uso owner, con autorizacion reusable central y validacion de workflow en capa logica, manteniendo `communications` como centro del dominio.

## 14.2 Servicios a definir primero

- crear comunicacion externa e interna
- asignar y quitar participantes
- cambiar estado
- subir documento y version
- emitir respuesta formal

## 14.3 Que no conviene sofisticar de mas en `v0.2`

- motor persistente completo de transiciones
- jerarquias complejas de servicios por accion menor
- automatismos extensivos de eventos
- politicas ultra-finas de permisos fuera de casos nucleo

## 14.4 Simplificaciones de etapa que siguen vigentes

- editor y responsable equivalentes en implementacion
- `child_of` como relacion canonica
- externo respondedor sin subcomunicacion general habilitada
- cierre administrativo final de E2 reservado a FREBA
- visibilidad documental externa por regla funcional contextual

Con este marco, el backend queda listo para pasar de diseno a implementacion con riesgo controlado y sin arbitrariedad funcional.

