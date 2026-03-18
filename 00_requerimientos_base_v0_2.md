# Levantamiento inicial de requerimientos y definiciones de dominio

## Sistema de gestión de comunicaciones FREBA — v0.2

Documento de trabajo para dejar asentadas las definiciones relevadas hasta el momento sobre el diseño del sistema.  
Esta versión consolida y depura la `v0.1`, incorporando además las definiciones y supuestos operativos ya acordados para volver el modelo más consistente y utilizable como base de diseño.

---

## 1. Contexto y problemática actual

Actualmente FREBA recibe comunicaciones institucionales a través de dos casillas de correo electrónico.  
Por esos medios ingresan distintos tipos de comunicaciones, por ejemplo:

- notas
- consultas formales
- consultas informales
- pedidos
- intercambios con distintas carátulas y formatos
- comunicaciones remitidas por distintos tipos de asociados

### Los emisores externos pueden ser, entre otros

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

El sistema está pensado principalmente para ordenar el trabajo de FREBA.  
Los usuarios externos participan, pero el control y la administración global del dominio se concentra en FREBA.

---

## 3. Visión conceptual del dominio

### 3.1 Entidad central del dominio

La entidad principal del sistema es la **Comunicación**.

El sistema no está centrado en expedientes como objeto principal.  
El expediente aparece como un elemento de organización y agrupación, mientras que la comunicación es la unidad operativa central.

### 3.2 Qué es una Comunicación

Una comunicación representa un intercambio formal gestionable entre:

- FREBA y una organización asociada
- FREBA y otras partes involucradas
- o distintas partes vinculadas al ecosistema de FREBA, siempre dentro de una gestión administrada por FREBA

Una comunicación:

- tiene tipo
- tiene datos comunes
- puede tener datos particulares según su tipo
- puede tener adjuntos
- tiene un workflow de estados
- tiene usuarios asignados con distintos roles sobre la comunicación
- puede tener una respuesta formal
- puede vincularse con otras comunicaciones
- y puede asociarse a expedientes

### 3.3 Principio rector del dominio

El sistema debe modelar la **gestión de comunicaciones**, no solo su almacenamiento.  
Es decir, no solo importa qué comunicación existe, sino también:

- quién la inicia
- quién la recibe
- quién trabaja sobre ella
- qué estado tiene
- qué respuesta formal se emite
- y qué relación guarda con otras comunicaciones y con expedientes

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

Los usuarios actúan dentro del sistema representando a una organización, aunque puede existir la posibilidad de que un mismo usuario represente a más de una organización.

### Regla importante

El emisor real de una comunicación no es solo una persona ni solo una organización, sino:

**usuario concreto + organización a la que representa**.

Esto aplica tanto para usuarios de FREBA como para usuarios externos.

### 4.3 Usuarios internos y externos

#### Usuarios internos

- Son usuarios pertenecientes a FREBA.

#### Usuarios externos

- Son usuarios pertenecientes a organizaciones asociadas u otras organizaciones externas.
- Ejemplos: cooperativas, distribuidoras, organismos públicos, etc.

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

Los usuarios externos no ven todo el sistema.  
Solo pueden ver aquello que les corresponde según:

- su organización
- la comunicación concreta
- el escenario de participación
- y su rol efectivo sobre esa comunicación

### 5.3 El sistema debe ser colaborativo

Una misma comunicación puede tener varios usuarios asignados trabajando sobre ella.

### 5.4 El sistema debe ser trazable

Debe quedar registro de:

- quién creó
- quién editó
- quién respondió
- quién participó
- qué ocurrió durante el ciclo de vida de la comunicación
- qué documentos se cargaron y sus versiones
- qué relaciones existen con otras comunicaciones
- qué expediente/s la contienen

### 5.5 El sistema debe ser evolutivo

Aunque esta versión define reglas operativas iniciales, el modelo debe quedar preparado para evolucionar en el futuro en temas como:

- diferencias más finas de roles
- notificaciones automáticas
- reglas de transición
- bandejas más sofisticadas
- mayor riqueza de expedientes
- y mayor precisión en visibilidad externa

---

## 6. Tipo de comunicación

### 6.1 Concepto

Toda comunicación pertenece a un tipo de comunicación.

El tipo de comunicación no es solo una etiqueta descriptiva.  
Es una pieza central de configuración funcional.

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

No todos los usuarios pueden crear cualquier tipo de comunicación.  
La posibilidad de iniciar una comunicación depende del tipo configurado y del perfil/contexto del usuario.

### 6.4 Supuesto operativo adoptado

En esta etapa, el tipo de comunicación es la principal pieza de parametrización del comportamiento general de la comunicación.  
No se pretende aún una configuración infinita ni completamente abierta desde interfaz.

---

## 7. Comunicación: estructura funcional

### 7.1 Datos comunes a todas las comunicaciones

Toda comunicación tiene un conjunto de datos comunes, entre ellos:

- título
- descripción libre
- fecha de creación
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

### Decisión preliminar de modelado

Los atributos variables por tipo se modelarán mediante:

- una tabla base de comunicación con datos comunes
- y tablas específicas por tipo de comunicación con sus atributos particulares

### Motivo de esta decisión

Se busca:

- evitar un diseño genérico excesivo
- evitar `JSONField` o estructuras poco gobernables
- mantener tipado fuerte
- facilitar validaciones
- facilitar formularios claros por tipo
- tener consultas más previsibles
- mantener un diseño relacional ordenado
- poder definir workflow y reglas particulares sobre cada tipo

### 7.3 Alcance de la edición

Mientras la comunicación esté abierta, sus datos editables podrán modificarse según rol y escenario.  
Si la comunicación está cerrada, la modificación requerirá reapertura cuando esa reapertura esté permitida.

---

## 8. Creación y envío de comunicaciones

### 8.1 Regla general

En `v0.2`, una comunicación **no tiene borrador**.  
Cuando se crea, se considera **enviada** y toma el estado inicial definido por su tipo de comunicación.

### 8.2 Creación por usuarios externos

Cuando una comunicación es creada por un asociado externo:

- la crea un usuario concreto
- actuando en nombre de su organización
- con los atributos definidos para ese tipo
- con posibilidad de adjuntar documentación
- y con la bandeja inicial definida por configuración del tipo de comunicación

### 8.3 Creación por usuarios FREBA

Cuando una comunicación es creada por FREBA:

- la crea un usuario interno
- actuando en nombre de FREBA
- debe elegir la organización destino
- debe poder elegir uno o más usuarios destino pertenecientes a esa organización
- y puede iniciar comunicaciones salientes hacia asociados

### 8.4 Destino de las comunicaciones

#### Desde FREBA hacia afuera

- Una comunicación creada por FREBA tiene:
  - una organización destino
  - y una lista de uno o más usuarios destino de esa organización

#### Desde afuera hacia FREBA

- Una comunicación creada por un asociado ingresa según la configuración del tipo
- y va a la bandeja definida para su atención

### 8.5 Visibilidad inmediata

En `v0.2`, una comunicación creada por FREBA hacia un externo queda visible para la organización destino apenas se envía.

### 8.6 Ajustes posteriores a un envío

En `v0.2`, no existe una instancia formal de borrador posterior al envío.  
Si FREBA necesita corregir una comunicación aún abierta luego de haberla enviado, podrá:

- quitar temporalmente asignaciones externas
- realizar los ajustes necesarios
- y volver a asignar a los usuarios externos

Esta solución se toma como regla operativa inicial, aunque más adelante podría reemplazarse por un modelo más explícito de emisión/publicación.

---

## 9. Bandejas y asignación de usuarios

### 9.1 Concepto actual de bandeja

Actualmente, el concepto de bandeja se entiende como una lista de usuarios.

No se definió aún como:

- área
- cola abstracta
- rol lógico
- o entidad operativa más compleja

Por el momento, la bandeja se interpreta como conjunto de usuarios asociados a la recepción/trabajo inicial de un tipo de comunicación.

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

### 9.4 Regla de bandeja según origen

- Si la comunicación la crea un externo: se usa la bandeja inicial configurada por el tipo.
- Si la comunicación la crea FREBA: la “bandeja” efectiva son los usuarios destino seleccionados por quien la crea.

### 9.5 Rol inicial de usuarios de bandeja

En `v0.2`, cuando una comunicación entra a una bandeja, los usuarios iniciales quedan asignados con rol operativo equivalente a **Editor**.

---

## 10. Asignación y colaboración sobre una comunicación

### 10.1 Múltiples usuarios por comunicación

Una comunicación puede tener múltiples usuarios asignados.

### 10.2 Sentido de la asignación múltiple

Cuando una comunicación tiene varios usuarios asignados, significa que todos ellos, según su rol, pueden participar en su tratamiento.

La participación puede incluir:

- leer
- estar al tanto
- actualizar atributos
- cargar o modificar documentos
- asignar nuevos usuarios
- colaborar en la resolución
- responder formalmente
- cambiar el estado

### 10.3 Transparencia organizacional externa

A nivel externo, las comunicaciones pertenecientes a una organización son visibles en términos generales para esa organización, pero no todos los usuarios externos necesariamente tendrán el mismo nivel de acceso operativo.

En `v0.2` se adopta esta regla:

- cualquier usuario de la misma organización puede ver la existencia y datos generales de comunicaciones que involucren a su organización, según el escenario
- solo los usuarios explícitamente asignados podrán operar activamente sobre ellas
- el acceso al chat, a la respuesta y a acciones operativas depende del rol y la asignación concreta

### 10.4 Incorporación de nuevos usuarios externos

Cuando un externo deba responder una comunicación enviada por FREBA, podrá agregar otros usuarios de su misma organización.

En `v0.2`, esta incorporación queda limitada a usuarios de la misma organización y no permite asignar usuarios de otras organizaciones.

### 10.5 Regla operativa de asignación externa adoptada

Como supuesto funcional viable para esta versión:

- un externo solo puede agregar usuarios de su misma organización
- esos usuarios no adquieren más alcance que el que el flujo y el rol les permitan
- FREBA sigue siendo la autoridad de administración global del caso

---

## 11. Roles sobre la comunicación

### 11.1 Roles identificados conceptualmente

Dentro de una comunicación pueden existir roles tales como:

- observador
- editor
- responsable

### 11.2 Regla operativa para v0.2

Dado que negocio aún no definió diferencias concretas entre **Editor** y **Responsable**, en `v0.2` ambos roles se consideran funcionalmente equivalentes en permisos.

### 11.3 Alcance actual de los roles

#### Observador

En principio, su función es de seguimiento limitado.  
Por defecto:

- puede ver lo que le corresponde según visibilidad de la comunicación
- no puede ver el chat interno
- no puede ver documentos internos de trabajo
- no puede gestionar asignaciones
- no puede responder formalmente
- no puede cambiar el estado

**Aclaración importante:**  
El acceso a chat compartido externo no se define solo por el nombre del rol, sino también por el escenario de participación de la comunicación.

#### Editor / Responsable

En `v0.2`, ambos pueden:

- cambiar el estado
- responder formalmente
- agregar o quitar usuarios
- asociar o desasociar expedientes
- crear subcomunicaciones
- cargar y versionar documentos
- usar chat según ámbito
- editar la comunicación mientras esté abierta

### 11.4 Principio importante

La lógica principal de permisos debe basarse en:

- la asignación del usuario a la comunicación
- el rol que posee sobre esa comunicación
- y el contexto operativo de la comunicación

No en una diferencia rígida entre “interno” y “externo”.

---

## 12. Workflow y estados

### 12.1 Workflow por tipo de comunicación

Cada tipo de comunicación debe poder tener su propio workflow.

### 12.2 Workflow por defecto

Además, debe existir un workflow por defecto, básico, inicialmente pensado con cuatro estados.

### 12.3 Configurabilidad

La idea es que los estados no queden hardcodeados.  
Deben poder configurarse para que, si en el futuro cambian, se modifique la configuración del tipo de comunicación y no la lógica base del sistema.

### 12.4 Estado único y visible para todos

El estado de una comunicación es único y visible para todos los usuarios que participan de ella.

No se prevé, por ahora, tener estados distintos para vista interna y externa.

### 12.5 Automatismos futuros

Por el momento, los cambios de estado no dispararán automatismos obligatorios, pero el sistema debe quedar diseñado para que en el futuro las transiciones puedan disparar:

- notificaciones
- asignaciones
- vencimientos
- u otros comportamientos automáticos

### 12.6 Cambios de estado por externos

En `v0.2`, un externo con rol operativo habilitado podrá cambiar el estado de una comunicación cuando esté participando activamente en el escenario de respuesta.

Como criterio funcional inicial:

- podrá mover la comunicación en estados de trabajo vinculados a la elaboración de la respuesta
- podrá dejarla en un estado equivalente a “respondida”
- el cierre administrativo definitivo podrá quedar a cargo del flujo previsto para cada tipo

Esta regla podrá refinarse más adelante por transición puntual.

---

## 13. Ciclo de vida: edición, cierre y reapertura

### 13.1 Edición

Una comunicación puede editarse mientras esté abierta.

### 13.2 Reapertura

Si una comunicación está cerrada y todavía no tiene respuesta formal emitida, un usuario con rol habilitado podrá reabrirla.

### 13.3 Regla de continuidad luego de respuesta final

Si una comunicación ya tiene una **respuesta formal emitida**, no se continuará el intercambio sobre la misma como flujo normal.

La continuidad del tema se resolverá mediante una **nueva comunicación relacionada (hija / réplica)**.

### 13.4 Cierre y respuesta

El cierre de una comunicación **no obliga** necesariamente a cargar una respuesta.

Puede existir una comunicación:

- cerrada sin respuesta
- o cerrada con respuesta formal asociada

### 13.5 Regla operativa recomendada

Aunque el sistema pueda permitir reapertura sin respuesta final, una vez que ya hubo una respuesta formal, la práctica funcional recomendada será abrir una nueva comunicación relacionada en lugar de reabrir la original.

---

## 14. Respuesta formal de una comunicación

### 14.1 Concepto

Cada comunicación puede tener una única respuesta formal.

La respuesta:

- no tiene workflow propio
- no tiene estado propio
- está asociada a una comunicación con estado
- forma parte del historial de esa comunicación
- puede ser generada por un usuario habilitado según su rol

### 14.2 Naturaleza de la respuesta

La respuesta se entiende como la respuesta formal y final a una comunicación.

No se la considera una nueva comunicación independiente, sino un elemento formal asociado a la comunicación existente.

### 14.3 Quién puede responder

Puede responder:

- un usuario de FREBA
- o un usuario externo

siempre que tenga rol operativo habilitado sobre esa comunicación.

### 14.4 Casos de uso esperados

- **Caso 1:** Un asociado crea una comunicación hacia FREBA y luego espera una respuesta formal de FREBA.
- **Caso 2:** FREBA crea una comunicación hacia un asociado y luego espera una respuesta formal del asociado destinatario.

### 14.5 Contenido de la respuesta

La respuesta puede incluir:

- texto de respuesta
- archivos adjuntos propios de la respuesta
- selección de documentos ya existentes en la comunicación, normalmente en su última versión

### 14.6 Emisión y congelamiento

En `v0.2`:

- la respuesta no tiene borrador
- cuando se crea, se emite
- una vez emitida, no puede editarse
- una vez emitida, no puede anularse
- una vez emitida, queda congelada como respuesta formal de esa comunicación

### 14.7 Visibilidad de la respuesta

La respuesta es visible para todos los usuarios con acceso a la comunicación.

---

## 15. Escenarios externos

### 15.1 Escenario A: el externo crea una comunicación y espera respuesta

En este escenario:

- el externo crea la comunicación
- queda a la espera de tratamiento por parte de FREBA
- no sigue cargando documentación luego de su envío inicial
- no administra usuarios
- puede consultar el estado
- puede ver la respuesta cuando exista
- puede utilizar el chat compartido en la medida en que esté habilitado para la comunicación abierta
- no ve el trabajo interno de FREBA

### 15.2 Escenario B: FREBA crea una comunicación y el externo debe responder

En este escenario:

- FREBA envía la comunicación al externo
- el externo debe poder trabajar activamente sobre ella para construir la respuesta
- puede subir documentos
- puede actualizar datos de la comunicación
- puede usar el chat compartido
- puede agregar usuarios de su misma organización
- puede mover la comunicación dentro de los estados operativos habilitados
- y finalmente puede emitir la respuesta formal

### 15.3 Restricción organizacional externa

Los usuarios externos solo pueden actuar dentro de comunicaciones vinculadas a su propia organización.  
Nunca pueden asignar ni involucrar usuarios de otras organizaciones externas.

### 15.4 Regla sobre réplica posterior a una respuesta

Cuando un externo haya recibido una respuesta final y necesite continuar con el tema, lo hará mediante una nueva comunicación relacionada vinculada a la original.

---

## 16. Chat y colaboración conversacional

### 16.1 Necesidad funcional

La comunicación debe permitir organización colaborativa mediante mensajes cronológicos.

### 16.2 Dos ámbitos de chat

En `v0.2` se adopta como mejor opción funcional separar el chat en dos ámbitos:

- **chat interno FREBA**
- **chat compartido con la contraparte externa**

### 16.3 Chat interno FREBA

Está destinado a usuarios internos de FREBA con rol operativo sobre la comunicación.

Sirve para:

- coordinar trabajo interno
- dejar comentarios de análisis
- pedir intervención
- ordenar tareas y contexto

### 16.4 Chat compartido

Está destinado a la interacción entre FREBA y la contraparte externa cuando el escenario lo requiera.

Puede usarse para:

- aclaraciones
- pedidos de información
- seguimiento
- intercambio operativo no formal

### 16.5 Reglas del chat

En `v0.2`:

- el chat es cronológico
- no se puede borrar
- no admite adjuntos propios
- los adjuntos se gestionan como documentos de la comunicación
- el acceso al chat depende del rol y del ámbito
- un observador no accede al chat interno
- un externo solo accede al chat compartido cuando corresponde a su escenario y asignación

---

## 17. Documentos y adjuntos

### 17.1 Concepto general

Los documentos forman parte de la comunicación y deben poder gestionarse a lo largo de su ciclo de vida.

### 17.2 Momentos de carga

Los documentos pueden adjuntarse:

- al crear una comunicación
- mientras la comunicación esté abierta
- y seleccionarse luego como parte de una respuesta

### 17.3 Versionado

Los documentos no se reemplazan destruyendo versiones anteriores.

En `v0.2`:

- cada nueva carga genera una nueva versión
- la última versión es la vigente
- deben mantenerse almacenadas las versiones anteriores
- el historial de versiones debe poder consultarse internamente

### 17.4 Metadatos mínimos del documento

Cada documento debería registrar, como mínimo:

- nombre lógico
- nombre de archivo
- fecha de carga
- versión
- tipo documental o extensión
- usuario que lo cargó
- comunicación a la que pertenece

### 17.5 Visibilidad documental

Aunque el documento pertenezca a una comunicación, no toda versión documental será visible automáticamente a externos.

En `v0.2` se adopta esta regla funcional:

- los documentos de trabajo interno de FREBA no se exponen automáticamente al externo
- el externo ve los documentos que él mismo cargó
- el externo ve los documentos finales expuestos en la respuesta
- en comunicaciones enviadas por FREBA hacia el externo, el externo verá también los adjuntos que formen parte del envío inicial

### 17.6 Documentos de respuesta

La respuesta puede incluir:

- documentos seleccionados de la comunicación, normalmente en su última versión
- y, si el flujo lo permite, nuevos documentos cargados por quien responde antes de emitirla

---

## 18. Relación entre comunicaciones

### 18.1 Concepto general

El sistema debe permitir crear una comunicación a partir de otra comunicación ya existente.

### 18.2 Sentido funcional

La finalidad no es “derivar” una comunicación, sino relacionar comunicaciones independientes dentro de un contexto mayor.

### 18.3 Aclaración importante: no existe derivación como concepto fuerte

Se descarta, por ahora, el concepto de derivación como entidad o acción principal del dominio.

En lugar de eso:

- una comunicación puede sumar nuevos usuarios asignados para colaborar
- y cuando se necesita abrir otra gestión formal, se crea una nueva comunicación relacionada

### 18.4 Comunicación hija / subcomunicación

Una comunicación hija:

- es independiente
- tiene su propio tipo
- tiene su propio workflow
- tiene sus propios participantes
- no hereda datos obligatoriamente
- pero queda relacionada con la comunicación origen para dar contexto

### 18.5 Regla de continuidad posterior a respuesta final

Si un tema continúa luego de una respuesta final, la continuidad se resuelve mediante una nueva comunicación relacionada, no reabriendo la original como flujo normal.

### 18.6 Ejemplo de uso

Llega una comunicación “A” a FREBA.  
FREBA detecta que necesita consultar a otras organizaciones asociadas o a otras personas para poder responderla.

Entonces se crean nuevas comunicaciones relacionadas con “A”, de modo que:

- desde “A” se pueda ver el contexto general
- y desde las subcomunicaciones también se pueda entender que forman parte de un caso mayor

### 18.7 Resumen de hijas

La comunicación madre debe poder mostrar un resumen de sus hijas, incluyendo al menos:

- listado de comunicaciones hijas
- vínculo con la madre
- estado
- acceso contextual

### 18.8 Propagación de expediente

Si la comunicación madre está asociada a un expediente, sus hijas quedarán asociadas automáticamente al mismo expediente.  
Si la madre se asocia a un expediente con posterioridad, esa asociación se propagará a las hijas.

### 18.9 Profundidad de relación

Como supuesto operativo viable, el modelo podrá soportar relaciones recursivas entre comunicaciones, aunque la interfaz inicial puede priorizar la visualización de padre e hijas directas para no complejizar la UX.

---

## 19. Expedientes

### 19.1 Rol del expediente en el sistema

El expediente es un elemento de agrupación y organización administrativa, no la entidad principal del dominio.

### 19.2 Características del expediente

Por el momento, un expediente tiene:

- identificador
- carátula
- asunto
- fecha
- y posiblemente otros atributos a definir más adelante

### 19.3 Visibilidad

Los expedientes son visibles solo para usuarios de FREBA.  
Los usuarios externos no ven expedientes.

### 19.4 Creación del expediente

En `v0.2`, cualquier usuario interno de FREBA puede crear un expediente.

### 19.5 Asociación entre comunicación y expediente

A nivel de diseño, el modelo podrá soportar asociación múltiple entre comunicación y expediente.

Sin embargo, en `v0.2`, por simplicidad funcional y de UX, se adopta como regla operativa trabajar con **un único expediente principal por comunicación**.

### 19.6 Asociación y movimiento

Solo un usuario con rol **Editor** o **Responsable** sobre una comunicación puede:

- asociarla a un expediente
- desasociarla
- moverla de un expediente a otro

### 19.7 Expediente sin estado

Por el momento, el expediente no tiene estado propio.  
Cumple una función de agrupación y contexto administrativo.

### 19.8 Expediente sin responsables propios

En `v0.2`, el expediente no tiene participantes ni responsables propios.  
La gestión sigue ocurriendo sobre las comunicaciones que contiene.

---

## 20. Visibilidad para usuarios externos

### 20.1 Alcance general

Un usuario externo solo puede ver comunicaciones que incumban a su organización.

### 20.2 Qué comunicaciones externas son visibles

Un usuario externo puede ver comunicaciones que:

- su organización originó
- fueron creadas por FREBA y tienen a su organización como destino
- o en las que fue asignado según las reglas del sistema

### 20.3 Qué no ve el externo

El mundo externo no ve:

- expedientes
- estructura interna de organización de FREBA
- historial interno detallado
- asignaciones internas de FREBA
- documentos internos de trabajo
- chat interno FREBA

### 20.4 Qué sí ve el externo

Según el escenario y su nivel de participación, el externo puede ver:

- los datos generales de la comunicación
- el estado actual
- los documentos que cargó
- los adjuntos visibles del envío inicial
- la respuesta formal emitida
- los documentos finales incluidos en esa respuesta
- el chat compartido, cuando corresponda

---

## 21. Historial y trazabilidad

### 21.1 Necesidad funcional

El sistema debe conservar historial y trazabilidad suficiente para reconstruir el ciclo de vida de una comunicación.

### 21.2 Elementos esperables del historial

Como mínimo, el historial debería poder reflejar:

- creación
- edición
- cambios relevantes
- respuesta formal
- asignación de usuarios
- relación con otras comunicaciones
- asociación a expediente
- participación general en la gestión
- carga de documentos y versiones

### 21.3 Historial visible y no visible

En `v0.2` se adopta esta regla:

- el historial completo operativo y de auditoría es interno para FREBA
- el externo no ve ese historial completo
- el externo solo ve el estado actual y la respuesta formal emitida, además de la información general que le corresponda

---

## 22. Escenarios operativos resumidos

### 22.1 Externo que crea y espera respuesta

Puede:

- crear la comunicación
- cargar adjuntos iniciales
- ver estado
- ver la respuesta final
- participar del chat compartido cuando corresponda

No puede:

- seguir modificando libremente la comunicación como flujo normal
- ver trabajo interno de FREBA
- ver historial interno
- administrar usuarios de la comunicación

### 22.2 Externo que recibe y debe responder

Puede:

- ver la comunicación
- trabajar activamente sobre ella
- subir documentos
- actualizar datos editables
- usar chat compartido
- agregar usuarios de su misma organización
- mover estados operativos habilitados
- emitir la respuesta formal

### 22.3 Usuario interno FREBA

Puede, según rol operativo:

- crear comunicaciones
- asignar usuarios
- trabajar internamente
- usar chat interno y chat compartido
- versionar documentos
- responder
- asociar expedientes
- crear subcomunicaciones

---

## 23. Modelo conceptual preliminar

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
- Versión de Documento
- Chat / Mensaje de comunicación
- Relación entre Comunicaciones
- Expediente
- Asociación Comunicación–Expediente

---

## 24. Reglas de negocio ya bastante firmes

- La unidad central del sistema es la comunicación.
- Toda comunicación pertenece a un tipo de comunicación.
- Todo usuario actúa en nombre de una organización.
- Una comunicación puede ser iniciada por FREBA o por un usuario externo autorizado.
- No todos los usuarios pueden iniciar cualquier tipo de comunicación.
- Toda comunicación tiene atributos comunes.
- Cada tipo de comunicación puede tener atributos particulares propios.
- Los atributos particulares por tipo se modelarán, preliminarmente, en tablas específicas por tipo.
- Cada tipo de comunicación define su formulario, su workflow, su bandeja inicial y reglas de visibilidad.
- Una comunicación no tiene borrador en `v0.2`; al crearse, se envía.
- Una comunicación puede tener múltiples usuarios asignados.
- Los usuarios asignados participan colaborativamente según el rol que tengan sobre la comunicación.
- En `v0.2`, Editor y Responsable tienen el mismo alcance funcional.
- La lógica principal de permisos depende de la asignación, el rol y el contexto operativo.
- El estado de una comunicación es único y visible para todos sus participantes con acceso.
- Cada tipo de comunicación usa un workflow configurable.
- Debe existir un workflow por defecto, básico.
- Cada comunicación puede tener una única respuesta formal.
- La respuesta formal no es una nueva comunicación independiente.
- La respuesta puede ser emitida tanto por FREBA como por un asociado, según rol.
- La respuesta forma parte del historial de la comunicación.
- La respuesta no se edita ni anula una vez emitida.
- No se usará, por ahora, el concepto de derivación como entidad central.
- La colaboración se resuelve mediante asignación de usuarios sobre la misma comunicación.
- Cuando se necesite abrir una gestión formal separada, se crea una nueva comunicación relacionada.
- Las comunicaciones relacionadas son independientes, aunque vinculadas.
- Si una comunicación ya tuvo respuesta final y el tema continúa, se crea una nueva hija / réplica.
- Una comunicación puede asociarse a expedientes.
- En `v0.2`, funcionalmente se trabajará con un expediente principal por comunicación.
- Un expediente es un agrupador administrativo visible solo para FREBA.
- Los usuarios externos solo ven las comunicaciones que les incumban según su organización, asignación y escenario.
- El sistema debe quedar preparado para que, a futuro, los cambios de estado disparen notificaciones u otras acciones automáticas.

---

## 25. Supuestos funcionales adoptados para resolver grises de v0.2

### 25.1 Editor y Responsable

Hasta que negocio defina una diferencia real, ambos roles se consideran equivalentes en permisos.

### 25.2 Reapertura con respuesta final

Si una comunicación ya tiene respuesta formal emitida, no se reabre como flujo normal.  
La continuidad se resuelve mediante una nueva comunicación relacionada.

### 25.3 Chat separado

Se adoptan dos chats:

- uno interno para FREBA
- uno compartido con externos

### 25.4 Visibilidad documental externa

El externo no ve todos los documentos intermedios de trabajo.  
Ve solo:

- los documentos que él mismo cargó
- los adjuntos visibles del envío inicial
- y los documentos finales incluidos en la respuesta

### 25.5 Expediente principal único en la operación

Aunque el diseño soporte asociación múltiple, en `v0.2` la operación se simplifica usando un único expediente principal por comunicación.

### 25.6 Transparencia organizacional externa

La organización externa puede tener visibilidad general sobre comunicaciones que le incumban, pero la operación activa queda limitada a usuarios asignados y según rol.

### 25.7 Externo con posibilidad de respuesta

Cuando FREBA envía una comunicación a un externo para responder, ese externo puede trabajar activamente sobre ella, incluyendo documentos, datos, chat, estado y respuesta, siempre dentro del alcance de su organización.

### 25.8 Profundidad de subcomunicaciones

A nivel de modelo se admite relación recursiva entre comunicaciones, aunque la primera experiencia de uso puede limitar la exposición visual a relaciones directas para simplificar.

---

## 26. Pendientes, dudas abiertas y definiciones no cerradas

### 26.1 Diferencia real entre Editor y Responsable

En `v0.2` se unifican, pero negocio aún no definió una diferencia conceptual y operativa entre ambos.

### 26.2 Casos reales por tipo de comunicación

Todavía faltan ejemplos concretos y validados de tipos reales de comunicación.  
Eso permitirá revisar formularios, atributos particulares, workflows y permisos.

### 26.3 Matriz fina de permisos por transición

Aunque ya hay reglas generales, todavía falta definir con mayor precisión qué transiciones puntuales puede ejecutar cada rol según el tipo de comunicación.

### 26.4 Automatismos futuros

Todavía no está definido:

- qué eventos dispararán notificaciones
- a quiénes
- por qué canal
- bajo qué condiciones

### 26.5 Modelo detallado de bandeja

Actualmente se entiende como lista de usuarios.  
Todavía no se definió si más adelante será:

- una entidad propia
- una agrupación por área
- una cola lógica más rica
- o una mezcla de usuarios y reglas

### 26.6 Reglas finas de visibilidad organizacional externa

Aunque ya se fijó una base, todavía puede requerirse un ajuste más fino sobre:

- qué ve exactamente cualquier usuario de una organización
- qué ve solo un usuario asignado
- qué acciones quedan habilitadas según escenario
- y cómo se refinan los permisos de chat compartido

### 26.7 Reglas de transición más estrictas para externos

En esta versión se definió un criterio operativo general, pero todavía falta definir con precisión si ciertos estados finales o administrativos quedarán reservados exclusivamente a FREBA.

---

## 27. Riesgos de diseño a tener presentes

### 27.1 Sobreconfiguración

Existe riesgo de volver demasiado complejo el sistema si se intenta parametrizar todo desde el inicio.

### 27.2 Explosión de tablas por tipo

La decisión de tener tablas específicas por tipo es sana, pero requiere disciplina para evitar proliferación desordenada de estructuras y lógica dispersa.

### 27.3 Ambigüedad entre colaboración y subcomunicación

Debe quedar muy claro cuándo se trabaja sobre la misma comunicación y cuándo se crea una nueva relacionada.

### 27.4 Complejidad de permisos

El sistema puede volverse muy difícil de mantener si los roles, visibilidades y acciones no se formalizan pronto en matrices y reglas claras.

### 27.5 Complejidad futura de expedientes múltiples

Aunque a nivel diseño pueda soportarse, permitir múltiples expedientes por comunicación puede generar complejidad funcional y de experiencia de usuario.

---

## 28. Próximos pasos recomendados

### 28.1 Cerrar glosario del dominio

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

### 28.2 Armar matriz de escenarios y permisos

Cruzar al menos estos escenarios:

- externo que crea y espera respuesta
- externo que recibe y debe responder
- usuario FREBA que crea
- usuario FREBA que trabaja internamente
- usuario FREBA que solo observa

Y para cada uno definir:

- qué ve
- qué puede editar
- si usa chat interno o compartido
- si ve documentos
- si puede subir documentos
- si puede cambiar estado
- si puede responder
- si puede agregar usuarios

### 28.3 Definir 3 casos de uso reales

Tomar 3 tipos reales de comunicación y describir:

- quién la inicia
- qué campos tiene
- quién la recibe
- cómo se trabaja
- cómo se responde
- si requiere expediente
- si puede generar subcomunicaciones

### 28.4 Bajar modelo conceptual inicial

Construir un modelo más formal de entidades y relaciones.

### 28.5 Recién después pasar a diseño técnico

Una vez consolidadas estas reglas, pasar a:

- decisiones de arquitectura
- diseño de modelo de datos
- diseño de agentes para Claude Code
- plan de implementación incremental

---

## 29. Síntesis final

Hasta este punto, el sistema puede entenderse como una plataforma de gestión de comunicaciones institucionales de FREBA, centrada en comunicaciones tipadas, configurables, colaborativas y trazables, con capacidad de respuesta formal, relación entre comunicaciones y asociación a expediente.

El foco principal del sistema no es simplemente recibir mensajes, sino permitir que FREBA:

- organice
- distribuya
- trabaje
- contextualice
- responda
- y registre adecuadamente sus comunicaciones con asociados

La versión `v0.2` deja cerradas muchas de las decisiones operativas mínimas para comenzar una etapa de diseño más formal, aun cuando todavía quedan definiciones finas de negocio por validar más adelante.