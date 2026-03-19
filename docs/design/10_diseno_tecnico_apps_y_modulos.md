# Diseno Tecnico de Apps y Modulos Django (v0.2)

## Sistema de gestion de comunicaciones FREBA

## 1. Objetivo y alcance

Este documento propone una arquitectura modular de apps Django para backend FREBA, alineada con:

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

El objetivo es definir:

- que apps crear
- que responsabilidad tiene cada una
- donde viven modelos y casos de uso
- como mantener bajo acoplamiento
- que modulo es nucleo y cual es soporte

Fuera de alcance:

- codigo Python
- estructura completa de archivos con implementacion
- details de serializers/views/permissions classes

---

## 2. Principios de modularizacion

## 2.1 Separar configuracion de operacion

- configuracion: tipo, workflow, estados, bandejas
- operacion: comunicacion, asignaciones, respuesta, documentos, chats, expediente, eventos

## 2.2 Comunicacion como centro del dominio

La app de comunicaciones gobierna el caso operativo principal.  
Expediente no debe transformarse en modulo central.

## 2.3 Permisos no son dominio nuevo

La logica reusable de autorizacion conviene centralizarla, pero sin crear una app de permisos que reemplace el dominio.

## 2.4 Evitar mega-app

No conviene meter todo en `communications`.  
Documentos, chats, expediente y auditoria tienen responsabilidades distintas.

## 2.5 Evitar ciclos de dependencia

La direccion de dependencias debe ser clara y estable.  
Cada app debe tener un borde funcional simple.

## 2.6 Mantener enfoque pragmatico `v0.2`

Arquitectura modular suficiente para escalar, sin sobreingenieria enterprise temprana.

---

## 3. Propuesta principal recomendada de apps

## 3.1 Lista de apps

- `organizations`
- `accounts` (o `users`)
- `communication_config`
- `communications`
- `documents`
- `chats`
- `expedients`
- `audit`
- `permissions_support`

## 3.2 Resumen rapido por app

| App | Tipo | Rol principal |
|---|---|---|
| `organizations` | Soporte base | Organizaciones institucionales |
| `accounts` | Soporte base | Usuarios y pertenencia a organizaciones |
| `communication_config` | Configuracion | Tipos, workflows, estados, bandejas |
| `communications` | Nucleo dominio | Caso principal, asignaciones, respuesta formal, relaciones |
| `documents` | Nucleo dominio | Documento logico + versiones |
| `chats` | Nucleo dominio | Mensajes internos/compartidos |
| `expedients` | Nucleo dominio secundario | Agrupacion administrativa |
| `audit` | Soporte operativo | Eventos/historial |
| `permissions_support` | Soporte tecnico | Contexto y autorizacion reusable |

---

## 4. Detalle por app (proposito, alcance y dependencias)

## 4.1 `organizations`

### Proposito
Mantener la entidad institucional participante.

### Por que conviene separarla
Evita acoplar identidad organizacional al modulo operativo de comunicaciones.

### Modelos que viven aqui

- `Organization`

### Servicios/casos de uso esperables

- resolucion de organizacion institucional
- validaciones de estado activo de organizacion

### Que no conviene meter aqui

- logica de workflow
- logica de mensajes/documentos
- reglas de permisos por accion

### Dependencias aceptables

- sin dependencias fuertes al resto del dominio

### Dependencias peligrosas a evitar

- depender de `communications` para resolver datos basicos de organizacion

---

## 4.2 `accounts`

### Proposito
Gestionar usuarios y su representacion organizacional.

### Por que conviene separarla
El dominio necesita distinguir actor, usuario y organizacion representada.

### Modelos que viven aqui

- `User` (custom o extendido)
- `UserOrganizationMembership`

### Servicios/casos de uso esperables

- seleccion de organizacion activa de sesion
- resolucion de membresia valida del usuario

### Que no conviene meter aqui

- reglas de estado de comunicacion
- logica de respuesta formal

### Dependencias aceptables

- depende de `organizations`

### Dependencias peligrosas a evitar

- depender de `communications` para autenticacion o perfiles

---

## 4.3 `communication_config`

### Proposito
Centralizar configuracion de tipos y ciclo de vida.

### Por que conviene separarla
Permite evolucion de configuracion sin tocar objetos operativos de casos.

### Modelos que viven aqui

- `Workflow`
- `WorkflowState`
- `CommunicationType`
- `Inbox`
- `InboxUser`

### Servicios/casos de uso esperables

- resolucion de workflow por tipo
- resolucion de estado inicial
- consulta de capacidades base de tipo

### Que no conviene meter aqui

- cambios de estado de casos concretos
- logica de asignacion operativa por comunicacion

### Dependencias aceptables

- depende de `accounts` para `InboxUser`

### Dependencias peligrosas a evitar

- depender de `communications` para definicion de catalogos

---

## 4.4 `communications`

### Proposito
Nucleo operativo del sistema.

### Por que conviene separarla
Concentra la entidad central del dominio y sus invariantes principales.

### Modelos que viven aqui

- `Communication`
- subtablas por tipo (`Communication<Tipo>Data`)
- `CommunicationAssignment`
- `FormalResponse`
- `FormalResponseDocument`
- `CommunicationRelation`

### Servicios/casos de uso esperables

- crear comunicacion
- editar comunicacion abierta
- asignar/quitar participantes
- cambiar estado
- cerrar/reabrir
- emitir respuesta formal
- crear subcomunicacion relacionada

### Que no conviene meter aqui

- almacenamiento de archivos/versiones (eso vive en `documents`)
- publicacion de mensajes (eso vive en `chats`)
- agrupacion administrativa de expediente (eso vive en `expedients`)
- infraestructura de auditoria tecnica

### Dependencias aceptables

- `organizations`
- `accounts`
- `communication_config`

### Dependencias peligrosas a evitar

- depender fuertemente de `audit` para ejecutar reglas de negocio
- depender de `permissions_support` como fuente de dominio (solo usarlo para autorizacion)

---

## 4.5 `documents`

### Proposito
Gestionar documento logico y versionado documental.

### Por que conviene separarla
Permite evolucion de ciclo documental sin inflar `communications`.

### Modelos que viven aqui

- `Document`
- `DocumentVersion`

### Servicios/casos de uso esperables

- subir documento
- subir nueva version
- resolver version vigente
- filtrar documentos visibles por contexto/escenario

### Que no conviene meter aqui

- emision de respuesta formal
- reglas de estado de comunicacion

### Dependencias aceptables

- `communications` (owner del caso)
- `accounts`
- `organizations`

### Dependencias peligrosas a evitar

- conocer reglas completas de permisos de todo el sistema
- decidir escenarios por cuenta propia

---

## 4.6 `chats`

### Proposito
Gestionar intercambio conversacional interno/compartido.

### Por que conviene separarla
El chat tiene reglas de alcance distintas a documentos y respuesta formal.

### Modelos que viven aqui

- `CommunicationMessage`

### Servicios/casos de uso esperables

- publicar mensaje interno
- publicar mensaje compartido
- listar mensajes filtrando por scope y permisos

### Que no conviene meter aqui

- respuesta formal
- adjuntos documentales como logica principal

### Dependencias aceptables

- `communications`
- `accounts`
- `organizations`

### Dependencias peligrosas a evitar

- acoplarse al historial de `audit` como requisito para publicar

---

## 4.7 `expedients`

### Proposito
Resolver agrupacion administrativa secundaria.

### Por que conviene separarla
Mantiene expediente desacoplado del nucleo de caso.

### Modelos que viven aqui

- `Expedient`
- `CommunicationExpedient`

### Servicios/casos de uso esperables

- crear expediente
- asociar comunicacion a expediente
- mover comunicacion entre expedientes
- resolver expediente principal operativo

### Que no conviene meter aqui

- logica de estado/flujo de comunicacion
- logica de permisos principal por escenario

### Dependencias aceptables

- `communications`
- `accounts` (quien asocia)

### Dependencias peligrosas a evitar

- que `communications` dependa de comportamiento complejo de expediente para operar su flujo principal

---

## 4.8 `audit`

### Proposito
Registrar trazabilidad y eventos relevantes.

### Por que conviene separarla
Evita que la auditoria gobierne el dominio.

### Modelos que viven aqui

- `CommunicationEvent`

### Servicios/casos de uso esperables

- registrar eventos relevantes
- consulta de historial por comunicacion
- registro de auditoria como side-effect no bloqueante de los casos de uso owner en `v0.2`

### Que no conviene meter aqui

- decisiones de negocio de autorizacion
- validacion de workflow

### Dependencias aceptables

- depende de varias apps para observar eventos

### Dependencias peligrosas a evitar

- que el resto de apps dependa de `audit` para poder funcionar
- que una operacion principal falle solo por falla de persistencia en `audit`

---

## 4.9 `permissions_support`

### Proposito
Centralizar logica reusable de autorizacion y contexto.

### Por que conviene separarla
Evita duplicacion de reglas en views/serializers/servicios dispersos.

### Modelos que viven aqui

- ninguno obligatorio en `v0.2`

### Servicios/casos de uso esperables

- resolver contexto de autorizacion (actor, organizacion activa, escenario, asignacion, rol, estado)
- evaluar reglas `can_*` reutilizables
- encapsular matrices de decision por accion

### Que no conviene meter aqui

- dominio nuevo
- ownership de comunicaciones/documentos/chats

### Dependencias aceptables

- puede leer `communications`, `accounts`, `organizations`, `documents`, `chats`, `expedients`

### Dependencias peligrosas a evitar

- que las apps de dominio dependan circularmente de implementaciones internas de `permissions_support`

---

## 5. Nucleo vs configuracion vs soporte

## 5.1 Clasificacion recomendada

### Nucleo de dominio

- `communications`
- `documents`
- `chats`
- `expedients` (nucleo secundario/contextual)

### Configuracion

- `communication_config`

### Soporte tecnico/operativo

- `organizations`
- `accounts`
- `audit`
- `permissions_support`

## 5.2 Imprescindibles desde el inicio

- `organizations`
- `accounts`
- `communication_config`
- `communications`
- `permissions_support` (al menos minimo)

## 5.3 Apps que pueden arrancar minimas

- `chats` (modelo + reglas base por scope)
- `expedients` (modelo + asociacion principal)
- `audit` (eventos minimos al principio)

## 5.4 Apps que pueden existir sin muchas tablas

- `permissions_support` (principalmente servicios/reglas)

---

## 6. Relaciones y dependencias entre apps

## 6.1 Dependencias aceptables (direccion principal)

- `accounts` -> `organizations`
- `communication_config` -> `accounts` (solo para `InboxUser`)
- `communications` -> `accounts`, `organizations`, `communication_config`
- `documents` -> `communications`, `accounts`, `organizations`
- `chats` -> `communications`, `accounts`, `organizations`
- `expedients` -> `communications`, `accounts`
- `audit` -> observa multiples apps (sin gobernarlas)
- `permissions_support` -> consulta multiples apps para decidir autorizacion

## 6.2 Dependencias a evitar

- `communication_config` dependiendo de `communications`
- `documents` decidiendo estados/workflow
- `chats` implementando reglas de respuesta formal
- `communications` acoplado fuerte a `audit`
- `expedients` forzando flujo principal de `communications`
- ciclos `communications` <-> `permissions_support`

## 6.3 Como reducir acoplamiento

- interfaces de servicio claras por app
- contrato de entrada/salida por caso de uso
- un unico punto de autorizacion reusable
- reglas de dominio en servicios del modulo owner

---

## 7. Ubicacion de servicios y casos de uso

Ubicacion recomendada por operacion:

- crear comunicacion -> `communications`
- asignar participantes -> `communications`
- cambiar estado -> `communications` (con apoyo de `communication_config` y `permissions_support`)
- emitir respuesta formal -> `communications` (usa `documents` para versiones incluidas)
- crear subcomunicacion -> `communications`
- asociar/mover expediente -> `expedients`
- subir documento -> `documents`
- subir nueva version -> `documents`
- publicar mensaje interno -> `chats`
- publicar mensaje compartido -> `chats`

Criterio general:

- cada app implementa su propia logica de dominio
- la app `permissions_support` decide autorizacion reusable
- los endpoints solo orquestan, no concentran negocio
- auditoria como side-effect: no debe gobernar ni bloquear el resultado de la operacion principal en `v0.2`

---

## 8. Ubicacion de la logica de permisos

## 8.1 Recomendacion principal

### En `permissions_support`

- resolvedor de escenario/contexto
- reglas reutilizables `can_*`
- politicas comunes de visibilidad vs accion

### Cerca de dominio (`communications` y apps owner)

- validaciones de invariantes de accion concreta
- chequeos de estado/transicion en servicios de negocio

### En endpoints

- validacion final y traduccion de errores
- nunca usar endpoint/serializer como fuente principal de autorizacion

## 8.2 Que no conviene

- permisos duplicados en serializers, views y servicios al mismo tiempo
- logica de autorizacion copiada por endpoint
- reglas de escenario hardcodeadas en frontend

---

## 9. Riesgos y anti-patrones de modularizacion

## 9.1 Riesgos principales

- mega app `communications` con todo adentro
- `documents` conociendo demasiada logica de permisos globales
- `audit` convertido en dependencia obligatoria del dominio
- `expedients` creciendo mas que `communications`
- reglas de negocio repartidas entre apps sin criterio
- logica de permisos duplicada en varias capas

## 9.2 Anti-patrones concretos

- acoplar almacenamiento documental a respuesta formal en la misma capa sin limites
- resolver workflow fuera de `communications` sin contrato unico
- permitir dependencias circulares entre apps de dominio
- usar signals como reemplazo de servicios de negocio para todo

---

## 10. Propuesta principal y alternativa mas simple

## 10.1 Propuesta principal recomendada

Usar 9 apps:

- `organizations`
- `accounts`
- `communication_config`
- `communications`
- `documents`
- `chats`
- `expedients`
- `audit`
- `permissions_support`

Es la opcion recomendada para este proyecto porque balancea:

- claridad de ownership
- mantenibilidad
- bajo acoplamiento
- crecimiento controlado

## 10.2 Alternativa mas simple/minimalista

Opcion de arranque mas compacta:

- `core_identity` (`organizations` + `accounts`)
- `communication_core` (`communication_config` + `communications`)
- `collaboration` (`documents` + `chats`)
- `context` (`expedients` + `audit`)
- `permissions_support`

Ventaja:

- menos apps iniciales

Costo:

- ownership mas difuso
- mayor riesgo de mezcla interna de responsabilidades

Conclusion:

Para FREBA `v0.2`, conviene la propuesta principal de 9 apps.

---

## 11. Orden sugerido de construccion de apps (alineado con `05`)

1. `organizations`
2. `accounts`
3. `communication_config`
4. `communications` (base + asignaciones + estado)
5. `permissions_support` (minimo para acciones nucleo)
6. `documents`
7. consolidar respuesta formal en `communications` usando `documents`
8. `chats`
9. `communications` (relaciones/subcomunicaciones)
10. `expedients`
11. `audit`
12. endurecimiento transversal de permisos y validaciones finas

Este orden respeta el criterio: primero nucleo operativo, luego colaboracion/contexto, luego robustez.

---

## 12. Cierre y recomendaciones de congelamiento inicial

## 12.1 Recomendacion general de arquitectura modular

Adoptar la propuesta principal de 9 apps con ownership claro y permisos centralizados como soporte reusable.

## 12.2 Que conviene congelar desde el inicio

- nombres base de apps y responsabilidades
- `communications` como modulo central de casos
- separacion `documents` / `chats` / `expedients`
- `permissions_support` como modulo de autorizacion reusable
- direccion de dependencias sin ciclos

## 12.3 Que no conviene sofisticar todavia en `v0.2`

- arquitectura hiperplugable de permisos
- motor configurable completo de transiciones persistentes
- expansion de expediente a logicas complejas multi-contexto
- explosion de apps accesorias sin valor inmediato

## 12.4 Simplificaciones explicitas de etapa

- `editor` y `responsible` equivalentes en implementacion
- `child_of` como relacion canonica
- externo respondedor sin subcomunicacion habilitada en `v0.2`
- cierre administrativo final de E2 del lado FREBA
- validacion de transiciones en capa logica (sin motor persistente completo)

Con este marco, la estructura modular queda lista para iniciar implementacion backend con bajo riesgo de retrabajo.
