
# Levantamiento inicial de requerimientos y definiciones de dominio

## Sistema de gestión de comunicaciones FREBA — v0.1

Documento de trabajo para dejar asentadas las definiciones relevadas hasta el momento sobre el diseño del sistema. Este documento refleja acuerdos conceptuales actuales, decisiones preliminares de modelado y temas pendientes de definición.

---

## 1. Contexto y problemática actual

Actualmente FREBA recibe comunicaciones institucionales a través de dos casillas de correo electrónico. Por esos medios ingresan distintos tipos de comunicaciones, por ejemplo:

- notas
- consultas formales
- consultas informales
- pedidos
- intercambios con distintas carátulas y formatos
- comunicaciones remitidas por distintos tipos de asociados

**Los emisores externos pueden ser, entre otros:**

- cooperativas
- distribuidoras
- organismos
- otras organizaciones asociadas a FREBA

### Problemas actuales detectados

El flujo actual se gestiona principalmente por correo electrónico y presenta los siguientes problemas:

- no hay un proceso definido y uniforme
- no hay trazabilidad clara
- no queda registro formal de quién respondió
- no queda registro completo del tratamiento interno
- no hay una administración ordenada de responsables y participantes
- no existe una visión integral del historial de una gestión
- se dificulta la colaboración interna
- se dificulta el seguimiento del estado de una comunicación
- no existe una estructura clara para responder, organizar y contextualizar comunicaciones relacionadas


---

## 2. Objetivo general del sistema

El objetivo es diseñar un sistema que permita a FREBA administrar, ordenar, registrar y dar seguimiento a las comunicaciones que mantiene con sus asociados y a su flujo interno de tratamiento.

El sistema debe servir principalmente para:

- organizar comunicaciones entrantes y salientes
- dar trazabilidad al proceso
- permitir trabajo colaborativo interno
- estructurar la gestión a partir de tipos de comunicación
- asociar comunicaciones a expedientes cuando corresponda
- permitir respuestas formales
- relacionar comunicaciones entre sí
- y eventualmente exponer parte del proceso a usuarios externos, según el caso

### Enfoque general

El sistema está pensado principalmente para ordenar el trabajo de FREBA. Los usuarios externos participan, pero el control y la administración global del dominio se concentra en FREBA.


---

## 3. Visión conceptual del dominio

### 3.1 Entidad central del dominio

La entidad principal del sistema es la **Comunicación**.

El sistema no está centrado en expedientes como objeto principal. El expediente aparece como un elemento de organización y agrupación, mientras que la comunicación es la unidad operativa central.

### 3.2 Qué es una Comunicación

Una comunicación representa un intercambio formal gestionable entre:

- FREBA y una organización asociada
- o FREBA y otras partes involucradas
- y eventualmente puede relacionarse con otras comunicaciones

Una comunicación:

- tiene tipo
- tiene datos comunes
- puede tener datos particulares según su tipo
- puede tener adjuntos
- tiene un workflow de estados
- tiene usuarios asignados con distintos roles sobre la comunicación
- puede tener una respuesta formal
- puede vincularse con otras comunicaciones
- y puede asociarse a uno o más expedientes


---

## 4. Actores del sistema

### 4.1 Organizaciones

El sistema contempla organizaciones como entidades del dominio. Ejemplos:

- FREBA
- cooperativas
- distribuidoras
- organismos
- otras organizaciones relacionadas

### 4.2 Usuarios

Los usuarios actúan dentro del sistema representando a una organización, aunque puede existir la posibilidad de que representen a mas de una organizacioón.

**Regla importante:**

El emisor real de una comunicación no es solo una persona ni solo una organización, sino:

**usuario concreto + organización a la que representa**.

Esto aplica tanto para usuarios de FREBA como para usuarios externos.

### 4.3 Usuarios internos y externos

**Usuarios internos:**

- Son usuarios pertenecientes a FREBA.

**Usuarios externos:**

- Son usuarios pertenecientes a organizaciones asociadas u otras organizaciones externas.(Cooperativas,distribuidoras, organismos publicos, etc).

---

## 5. Principios funcionales del sistema

### 5.1 FREBA administra el dominio

FREBA administra integralmente la operación del sistema:

- configuración de tipos de comunicación
- asociación a expedientes
- asignaciones internas
- visibilidad global
- trabajo colaborativo
- respuesta formal
- trazabilidad
- historial

### 5.2 El mundo externo participa de forma controlada

Los usuarios externos no ven todo el sistema. Solo pueden ver aquello que les corresponde según su organización y las comunicaciones en las que intervienen.

### 5.3 El sistema debe ser colaborativo

Una misma comunicación puede tener varios usuarios asignados trabajando sobre ella.

### 5.4 El sistema debe ser trazable

Debe quedar registro de:

- quién creó
- quién editó
- quién respondió
- quién participó
- y qué ocurrió durante el ciclo de vida de la comunicación


---

## 6. Tipo de comunicación

### 6.1 Concepto

Toda comunicación pertenece a un tipo de comunicación.

El tipo de comunicación no es solo una etiqueta descriptiva. Es una pieza central de configuración funcional.

### 6.2 Qué define un tipo de comunicación

Cada tipo de comunicación puede definir:

- su nombre
- su formulario de creación
- sus atributos particulares
- quién puede iniciarla
- la bandeja inicial
- su workflow de estados
- reglas de visibilidad
- fechas o comportamientos asociados
- y otras reglas operativas futuras

### 6.3 Restricción de creación por tipo

No todos los usuarios pueden crear cualquier tipo de comunicación. La posibilidad de iniciar una comunicación depende del tipo configurado y del perfil/contexto del usuario.


---

## 7. Comunicación: estructura funcional

### 7.1 Datos comunes a todas las comunicaciones

Toda comunicación tiene un conjunto de datos comunes, entre ellos:

- título
- descripción libre
- fecha
- adjuntos / documentos
- usuario creador
- organización emisora
- organización destino
- usuarios asignados
- datos de edición
- estado actual
- tipo de comunicación
- historial asociado

### 7.2 Datos particulares por tipo

Además de los datos comunes, cada tipo de comunicación puede tener atributos propios.

**Decisión preliminar de modelado**

Los atributos variables por tipo se modelarán mediante:

- una tabla base de comunicación con datos comunes
- y tablas específicas por tipo de comunicación con sus atributos particulares

**Motivo de esta decisión**

Se busca:

- evitar un diseño genérico excesivo
- evitar JSONField o estructuras poco gobernables
- mantener tipado fuerte
- facilitar validaciones
- facilitar formularios claros por tipo
- tener consultas más previsibles
- y mantener un diseño relacional ordenado
- poder definir el workflow particulares y reglas de negocio sobre cada tipo en particular

---

## 8. Creación de comunicaciones

### 8.1 Creación por usuarios externos

Cuando una comunicación es creada por un asociado externo:

- la crea un usuario concreto
- actuando en nombre de su organización
- con los atributos definidos para ese tipo
- con posibilidad de adjuntar documentación
- y con la bandeja inicial definida por configuración del tipo de comunicación

### 8.2 Creación por usuarios FREBA

Cuando una comunicación es creada por FREBA:

- la crea un usuario interno
- actuando en nombre de FREBA
- debe elegir la organización destino
- debe poder elegir uno o más usuarios destino pertenecientes a esa organización
- y puede iniciar comunicaciones salientes hacia asociados

### 8.3 Destino de las comunicaciones

**Desde FREBA hacia afuera:**

- Una comunicación creada por FREBA tiene:
	- una organización destino
	- y una lista de uno o más usuarios destino de esa organización

**Desde afuera hacia FREBA:**

- Una comunicación creada por un asociado ingresa según la configuración del tipo y va a la bandeja definida para su atención


---

## 9. Bandejas y asignación de usuarios

### 9.1 Concepto actual de bandeja

Actualmente, el concepto de bandeja se entiende como una lista de usuarios.

No se definió aún como área, cola abstracta o rol lógico. Por el momento, la bandeja se interpreta como conjunto de usuarios asociados a la recepción/trabajo inicial de un tipo de comunicación.

### 9.2 Funcionamiento esperado

Cuando una comunicación entra a una bandeja:

- todos los usuarios de esa bandeja quedan asociados a la comunicación
- la intención es permitir trabajo colaborativo
- no necesariamente se asigna desde el inicio a una sola persona

### 9.3 Caso típico previsto

De forma general, muchas comunicaciones recaerán inicialmente en Mesa de Entrada, y luego desde allí se podrán:

- asignar usuarios internos
- organizar el tratamiento
- iniciar nuevas comunicaciones relacionadas
- construir una solución
- y finalmente generar una respuesta formal


---

## 10. Asignación y colaboración sobre una comunicación

### 10.1 Múltiples usuarios por comunicación

Una comunicación puede tener múltiples usuarios asignados.

### 10.2 Sentido de la asignación múltiple

Cuando una comunicación tiene varios usuarios asignados, significa que todos ellos, según su rol, pueden participar en su tratamiento.

La participación puede incluir, según rol:

- leer
- estar al tanto
- actualizar atributos
- cargar o modificar documentos
- asignar nuevos usuarios
- colaborar en la resolución
- responder formalmente

### 10.3 Colaboración interna

Se prevé que una comunicación permita organización colaborativa mediante:

- notas
- chat
- comentarios o mecanismos de intercambio sobre la comunicación
- archivos adjuntos

Este punto está definido conceptualmente, aunque todavía no está cerrado el modelo exacto.


---

## 11. Roles sobre la comunicación

### 11.1 Roles identificados conceptualmente

Dentro de una comunicación pueden existir roles tales como:

- observador
- responsable
- colaborador
- editor

### 11.2 Definición todavía pendiente

Aún no está cerrada la definición exacta de:

- qué puede hacer cada rol
- qué puede ver cada rol
- qué permisos concretos tiene cada uno
- qué operaciones habilita cada rol

### 11.3 Principio importante ya definido

Un usuario asignado a una comunicación tiene el mismo alcance funcional según su rol, sin importar si pertenece a FREBA o a una organización externa.

**Ejemplo:**

Si un usuario de FREBA y un usuario externo están asignados a una misma comunicación y ambos tienen rol de editor, ambos pueden ver lo mismo y hacer lo mismo sobre esa comunicación.

**Conclusión preliminar:**

La lógica principal de permisos debe basarse en:

- la asignación del usuario a la comunicación
- y el rol que posee sobre esa comunicación

No en una diferencia rígida entre “interno” y “externo”, aunque podrían existir restricciones contextuales adicionales a definir más adelante si el negocio las necesitara.


---

## 12. Workflow y estados

### 12.1 Workflow por tipo de comunicación

Cada tipo de comunicación debe poder tener su propio workflow.

### 12.2 Workflow por defecto

Además, debe existir un workflow por defecto, básico, inicialmente pensado con cuatro estados.

### 12.3 Configurabilidad

La idea es que los estados no queden hardcodeados. Deben poder configurarse para que, si en el futuro cambian, se modifique la configuración del tipo de comunicación y no la lógica base del sistema.

### 12.4 Estado único y visible para todos

El estado de una comunicación es único y visible para todos los usuarios que participan de ella.

No se prevé, por ahora, tener estados distintos para vista interna y externa.

### 12.5 Automatismos futuros

Por el momento, los cambios de estado no dispararán automatismos obligatorios, pero el sistema debe quedar diseñado para que en el futuro las transiciones puedan disparar:

- notificaciones
- asignaciones
- vencimientos
- u otros comportamientos automáticos


---

## 13. Respuesta formal de una comunicación

### 13.1 Concepto

Cada comunicación puede tener una única respuesta formal.

La respuesta:

- no tiene workflow propio
- no tiene estado propio
- está asociada a una comunicación con estado
- forma parte del historial de esa comunicación
- puede ser generada por un usuario habilitado según su rol

### 13.2 Naturaleza de la respuesta

La respuesta se entiende como la respuesta formal y final a una comunicación.

No se la está considerando como una nueva comunicación independiente, sino como un elemento formal asociado a la comunicación existente.

### 13.3 Quién puede responder

Puede responder:

- un usuario de FREBA
- o un usuario externo
- siempre que tenga el rol adecuado sobre la comunicación

### 13.4 Casos de uso esperados

- **Caso 1:** Un asociado crea una comunicación hacia FREBA y luego espera una respuesta formal de FREBA.
- **Caso 2:** FREBA crea una comunicación hacia un asociado y luego espera una respuesta formal del asociado destinatario.

### 13.5 Contenido de la respuesta

La respuesta puede incluir:

- texto de respuesta
- archivos adjuntos propios de la respuesta(seguramente alguno o todos los archivos de la comunicacion)


---

## 14. Relación entre comunicaciones

### 14.1 Concepto general

El sistema debe permitir crear una comunicación a partir de otra comunicación ya existente.

### 14.2 Sentido funcional

La finalidad no es “derivar” una comunicación, sino relacionar comunicaciones independientes dentro de un contexto mayor.

### 14.3 Aclaración importante: no existe derivación como concepto fuerte

Se descarta, por ahora, el concepto de derivación como entidad o acción principal del dominio.

En lugar de eso:

- una comunicación puede sumar nuevos usuarios asignados para colaborar
- y cuando se necesita abrir otra gestión formal, se crea una nueva comunicación relacionada

### 14.4 Comunicación hija / subcomunicación

Una comunicación hija:

- es independiente
- tiene su propio tipo
- tiene su propio workflow
- tiene sus propios participantes
- no hereda datos obligatoriamente
- pero queda relacionada con la comunicación origen para dar contexto

### 14.5 Ejemplo de uso

Llega una comunicación “A” a FREBA. FREBA detecta que necesita consultar a otras organizaciones asociadas o a otras personas para poder responderla.

Entonces se crean nuevas comunicaciones relacionadas con “A”, de modo que:

- desde “A” se pueda ver el contexto general
- y desde las subcomunicaciones también se pueda entender que forman parte de un caso mayor

### 14.6 Herencia de datos

Las comunicaciones relacionadas no heredan automáticamente los datos de la comunicación origen. Se relacionan, pero siguen siendo entidades independientes.


---

## 15. Expedientes

### 15.1 Rol del expediente en el sistema

El expediente es un elemento de agrupación y organización administrativa, no la entidad principal del dominio.

### 15.2 Características del expediente

Por el momento, un expediente tiene:

- identificador
- carátula
- asunto
- fecha
- y posiblemente otros atributos a definir más adelante

### 15.3 Visibilidad

Los expedientes son visibles solo para usuarios de FREBA.

Los usuarios externos no ven expedientes.

### 15.4 Creación del expediente

La idea actual es que el expediente pueda ser creado manualmente por FREBA.

También se contempla como posibilidad futura que ciertas asociaciones se automaticen, por ejemplo:

- si una comunicación padre está asociada a un expediente
- sus subcomunicaciones podrían vincularse automáticamente a ese expediente

Esto no está cerrado todavía.

### 15.5 Asociación entre comunicación y expediente

Una comunicación:

- puede no estar asociada a ningún expediente
- puede asociarse a un expediente
- y actualmente se contempla también la posibilidad de asociarla a más de un expediente

### 15.6 Cambio de expediente

Una comunicación puede pasar de un expediente a otro, cambiando su asociación.

### 15.7 Comunicaciones informales

Se reconoce que puede haber comunicaciones que no necesiten expediente y permanezcan como intercambios más informales o autónomos.


---

## 16. Visibilidad para usuarios externos

### 16.1 Alcance general

Un usuario externo solo puede ver comunicaciones que incumban a su organización.

### 16.2 Qué comunicaciones externas son visibles

Un usuario externo puede ver comunicaciones que:

- su organización originó
- fueron creadas por FREBA y tienen a su organización como destino
- o en las que fue asignado según las reglas del sistema

### 16.3 Límite de visibilidad

El mundo externo no ve:

- expedientes
- estructura interna de organización de FREBA
- ni información ajena a las comunicaciones que le correspondan


---

## 17. Historial y trazabilidad

### 17.1 Necesidad funcional

El sistema debe conservar historial y trazabilidad suficiente para reconstruir el ciclo de vida de una comunicación.

### 17.2 Elementos esperables del historial

Como mínimo, el historial debería poder reflejar:

- creación
- edición
- cambios relevantes
- respuesta formal
- asignación de usuarios
- relación con otras comunicaciones
- asociación a expediente
- y participación general en la gestión

### 17.3 Respuesta en el historial

La respuesta formal forma parte del historial de la comunicación.


---

## 18. Modelo conceptual preliminar

A nivel conceptual, las piezas principales del dominio serían:

- Organización
- Usuario
- Tipo de Comunicación
- Workflow
- Estado
- Comunicación
- Datos particulares por tipo de comunicación
- Asignación de Usuario a Comunicación
- Rol sobre Comunicación
- Respuesta de Comunicación
- Documento adjunto
- Nota / comentario / chat interno
- Relación entre Comunicaciones
- Expediente
- Asociación Comunicación–Expediente


---

## 19. Reglas de negocio ya bastante firmes

- La unidad central del sistema es la comunicación.
- Toda comunicación pertenece a un tipo de comunicación.
- Todo usuario actúa en nombre de una organización.
- Una comunicación puede ser iniciada por FREBA o por un usuario externo autorizado.
- No todos los usuarios pueden iniciar cualquier tipo de comunicación.
- Toda comunicación tiene atributos comunes.
- Cada tipo de comunicación puede tener atributos particulares propios.
- Los atributos particulares por tipo se modelarán, preliminarmente, en tablas específicas por tipo.
- Cada tipo de comunicación define su formulario, su workflow, su bandeja inicial y reglas de visibilidad.
- Una comunicación puede tener múltiples usuarios asignados.
- Los usuarios asignados participan colaborativamente según el rol que tengan sobre la comunicación.
- Los roles sobre la comunicación aplican conceptualmente igual para usuarios internos y externos.
- La lógica principal de permisos debe depender de la asignación del usuario y su rol sobre la comunicación.
- El estado de una comunicación es único y visible para todos sus participantes.
- Cada tipo de comunicación usa un workflow configurable.
- Debe existir un workflow por defecto, básico.
- Cada comunicación puede tener una única respuesta formal.
- La respuesta formal no es una nueva comunicación independiente.
- La respuesta puede ser emitida tanto por FREBA como por un asociado, según rol.
- La respuesta forma parte del historial de la comunicación.
- No se usará, por ahora, el concepto de derivación como entidad central.
- La colaboración se resuelve mediante asignación de usuarios sobre la misma comunicación.
- Cuando se necesite abrir una gestión formal separada, se crea una nueva comunicación relacionada.
- Las comunicaciones relacionadas son independientes, aunque vinculadas.
- Una comunicación puede asociarse opcionalmente a expedientes.
- Un expediente es un agrupador administrativo visible solo para FREBA.
- Los usuarios externos solo ven las comunicaciones que les incumban según su organización y asignación.
- El sistema debe quedar preparado para que, a futuro, los cambios de estado disparen notificaciones u otras acciones automáticas.


---

## 20. Decisiones de diseño ya tomadas o bastante encaminadas

### 20.1 Decisión: centro del dominio

El sistema estará centrado en comunicaciones, no en expedientes.

### 20.2 Decisión: atributos por tipo

Se prefiere un modelo relacional con:

- tabla base común
- tablas particulares por tipo

### 20.3 Decisión: respuesta formal

La respuesta será:

- única por comunicación
- formal
- final
- asociada a la comunicación
- parte del historial
- sin workflow propio

### 20.4 Decisión: colaboración

Se prioriza colaboración por asignación de usuarios sobre una misma comunicación, en lugar de derivaciones formales.

### 20.5 Decisión: subcomunicaciones

Las subcomunicaciones serán comunicaciones independientes relacionadas con una comunicación origen.

### 20.6 Decisión: visibilidad externa

Los externos tendrán una visión acotada solo a lo que corresponda a su organización y participación.


---

## 21. Pendientes, dudas abiertas y definiciones no cerradas

### 21.1 Permisos concretos por rol

Falta definir con precisión:

- qué puede ver un observador
- qué puede hacer un colaborador
- qué puede hacer un responsable
- qué puede hacer un editor
- si hay otros roles
- y qué acciones exactas habilita cada rol

### 21.2 Matriz de acciones por rol

Falta definir una matriz clara que cruce:

- rol
- acción
- visibilidad
- edición
- respuesta
- gestión de documentos
- reasignación
- cierre
- reapertura

### 21.3 Regla exacta de edición de la comunicación

Hay una ambigüedad pendiente sobre esta definición:

- se mencionó que la comunicación “se pueda editar siempre y cuando esté cerrada”
- y también que un editor puede reabrirla

Esto necesita aclararse porque operativamente parece probable que se haya querido decir:

- que se puede editar mientras no esté cerrada
- y que si está cerrada, un editor puede reabrirla

Debe definirse de forma explícita.

### 21.4 Relación entre cierre y respuesta

Falta cerrar si:

- cerrar obliga a generar respuesta
- cerrar permite generar respuesta
- respuesta y cierre ocurren juntos
- puede cerrarse sin respuesta
- puede responderse sin cerrar

### 21.5 Edición de la respuesta formal

Falta definir:

- si la respuesta puede editarse
- hasta cuándo
- si se versiona
- o si una vez emitida queda bloqueada

### 21.6 Borradores

Falta definir si existen:

- borradores de comunicación
- borradores de respuesta
- y en qué momento una comunicación o respuesta pasa a ser visible para el otro actor

### 21.7 Publicación / emisión hacia destino

Falta definir si una comunicación creada por FREBA:

- queda inmediatamente visible para la organización destino
- o puede permanecer en estado interno antes de emitirse

### 21.8 Notas / chat / comentarios

Se definió la necesidad conceptual de colaboración tipo notas o chat, pero falta definir:

- si serán comentarios internos
- si habrá hilos
- si habrá visibilidad diferenciada
- si también podrá existir colaboración visible para externos
- o si la colaboración será solo interna FREBA

### 21.9 Documentos

Falta definir con mayor precisión:

- tipos de documentos
- si los documentos se versionan
- si pueden reemplazarse
- si pueden anularse
- si hay documentos solo de la comunicación y otros de la respuesta
- y si puede haber documentos ligados al expediente y no solo a la comunicación

### 21.10 Modelo exacto de bandeja

Actualmente la bandeja se entiende como lista de usuarios, pero falta definir si más adelante será:

- una entidad propia
- una cola lógica
- una agrupación por área
- una combinación de usuarios y reglas
- o solo una configuración simple por tipo

### 21.11 Reglas de asignación

Falta definir:

- quién puede asignar usuarios
- quién puede removerlos
- si puede haber usuario principal
- si todos los asignados son equivalentes
- cómo se comportan los roles en asignaciones múltiples

### 21.12 Comunicación y múltiples expedientes

Está contemplado que una comunicación pueda pertenecer a más de un expediente, pero este punto requiere validación adicional porque puede complejizar:

- el contexto
- la trazabilidad
- la interpretación de pertenencia
- y la experiencia de uso

### 21.13 Automatismos futuros

A...existing code...

quién puede removerlos,

si puede haber usuario principal,

si todos los asignados son equivalentes,

cómo se comportan los roles en asignaciones múltiples.

### 21.12 Comunicación y múltiples expedientes

Está contemplado que una comunicación pueda pertenecer a más de un expediente, pero este punto requiere validación adicional porque puede complejizar:

el contexto,

la trazabilidad,

la interpretación de pertenencia,

y la experiencia de uso.

### 21.13 Automatismos futuros

Aunque se prevé que el sistema quede preparado, todavía no está definido:

qué eventos dispararán notificaciones,

a quiénes,

por qué canal,

y bajo qué condiciones.

### 21.14 Casos de uso reales por tipo

Todavía faltan ejemplos concretos y validados de tipos de comunicación reales.
Cuando estén disponibles, permitirán:

pulir mejor el modelo,

validar atributos particulares,

y revisar si las decisiones actuales cubren correctamente los escenarios de negocio.

### 21.15 Reglas de subcomunicaciones

Falta definir con más precisión:

cuándo conviene crear una subcomunicación,

cuándo alcanza con asignar usuarios a la comunicación original,

cómo se muestran en interfaz,

si la comunicación madre debe mostrar estados resumidos de sus hijas,

y si algunas asociaciones deben ser automáticas.

### 21.16 Visibilidad fina

Aunque ya está claro que los externos ven solo lo que les corresponde, todavía falta bajar a detalle:

qué ve exactamente cada participante,

qué partes del historial son visibles,

qué acciones quedan visibles para todos,

y qué datos quedan restringidos.


---

## 22. Riesgos de diseño a tener presentes

### 22.1 Sobreconfiguración

Existe riesgo de volver demasiado complejo el sistema si se intenta parametrizar todo desde el inicio.

### 22.2 Explosión de tablas por tipo

La decisión de tener tablas específicas por tipo es sana, pero requiere disciplina para evitar proliferación desordenada de estructuras y lógica dispersa.

### 22.3 Ambigüedad entre colaboración y subcomunicación

Debe quedar muy claro cuándo se trabaja sobre la misma comunicación y cuándo se crea una nueva relacionada.

### 22.4 Complejidad de permisos

El sistema puede volverse muy difícil de mantener si los roles, visibilidades y acciones no se formalizan pronto en una matriz clara.

### 22.5 Complejidad por múltiples expedientes

Permitir que una comunicación esté en varios expedientes puede ser útil, pero también puede generar confusión funcional.


---

## 23. Próximos pasos recomendados

### 23.1 Cerrar glosario del dominio

Definir formalmente conceptos como:

- comunicación
- tipo de comunicación
- respuesta
- expediente
- subcomunicación
- bandeja
- asignación
- rol
- editor
- responsable
- observador
- colaborador

### 23.2 Armar matriz de permisos por rol

Cruzar:

- rol
- acción
- visibilidad
- edición
- respuesta
- cierre
- reapertura
- asignación
- gestión documental

### 23.3 Definir 3 casos de uso reales

Tomar 3 tipos reales de comunicación y describir:

- quién la inicia
- qué campos tiene
- quién la recibe
- cómo se trabaja
- cómo se responde
- si requiere expediente
- si puede generar subcomunicaciones

### 23.4 Bajar modelo conceptual inicial

Construir un modelo más formal de entidades y relaciones.

### 23.5 Recién después pasar a diseño técnico

Una vez consolidadas estas reglas, pasar a:

- decisiones de arquitectura
- diseño de modelo de datos
- diseño de agentes para Claude Code
- plan de implementación incremental

qué campos tiene,

quién la recibe,

cómo se trabaja,

cómo se responde,

si requiere expediente,

si puede generar subcomunicaciones.

23.4 Bajar modelo conceptual inicial

Construir un modelo más formal de entidades y relaciones.

23.5 Recién después pasar a diseño técnico

Una vez consolidadas estas reglas, pasar a:

decisiones de arquitectura,

diseño de modelo de datos,

diseño de agentes para Claude Code,

plan de implementación incremental.


---

## 24. Síntesis final

Hasta este punto, el sistema puede entenderse como una plataforma de gestión de comunicaciones institucionales de FREBA, centrada en comunicaciones tipadas, configurables, colaborativas y trazables, con capacidad de respuesta formal, relación entre comunicaciones y asociación opcional a expedientes.

El foco principal del sistema no es simplemente recibir mensajes, sino permitir que FREBA:

- organice
- distribuya
- trabaje
- contextualice
- responda
- y registre adecuadamente sus comunicaciones con asociados

Lo ya definido alcanza para comenzar una etapa de diseño más formal, aunque todavía quedan decisiones operativas y de permisos que deben cerrarse antes de pasar a implementación.