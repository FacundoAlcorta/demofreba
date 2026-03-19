# Glosario de dominio

## Sistema de gestión de comunicaciones FREBA

Documento de referencia para unificar el significado de los conceptos principales del dominio.  
Las definiciones aquí incluidas deben usarse como base común para análisis funcional, diseño técnico, modelado de datos y desarrollo.

---

## 1. Conceptos centrales

### Comunicación
Entidad principal del sistema.  
Representa un intercambio formal gestionable dentro del ecosistema FREBA.

Una comunicación puede:

- ser iniciada por FREBA o por un usuario externo autorizado
- tener un tipo de comunicación
- tener datos comunes y datos particulares
- tener usuarios asignados
- tener documentos adjuntos
- atravesar un workflow de estados
- tener una respuesta formal
- relacionarse con otras comunicaciones
- asociarse a un expediente

La comunicación es la unidad operativa principal del sistema.

---

### Tipo de comunicación
Configuración funcional que define el comportamiento general de una comunicación.

Un tipo de comunicación puede definir:

- nombre
- formulario de creación
- atributos particulares
- quién puede iniciarla
- bandeja inicial
- workflow aplicable
- reglas de visibilidad
- comportamientos operativos futuros

No es solo una categoría descriptiva, sino una pieza central de parametrización del dominio.

---

### Respuesta formal
Respuesta oficial y final asociada a una comunicación.

Características principales:

- cada comunicación puede tener una única respuesta formal
- la respuesta no es una comunicación independiente
- no tiene workflow propio
- no tiene estado propio
- forma parte del historial de la comunicación
- puede ser emitida por FREBA o por un externo, según el caso y el rol
- una vez emitida, queda congelada y no se edita

La respuesta formal representa el cierre o contestación oficial de una comunicación.

---

### Comunicación hija / subcomunicación
Comunicación nueva creada a partir de otra comunicación existente, con el objetivo de abrir una gestión formal separada pero contextualizada.

Características:

- es independiente de la comunicación origen
- tiene su propio tipo
- tiene su propio workflow
- tiene sus propios participantes
- no hereda automáticamente todos los datos de la madre
- queda vinculada para preservar contexto

Se utiliza cuando no alcanza con seguir trabajando dentro de la misma comunicación y hace falta abrir una nueva gestión relacionada.

---

### Expediente
Entidad de agrupación administrativa que permite organizar comunicaciones relacionadas dentro de un contexto común.

Características actuales:

- no es la entidad principal del sistema
- agrupa comunicaciones
- tiene identificador, carátula, asunto y fecha
- no tiene estado propio en esta etapa
- no tiene responsables propios en esta etapa
- es visible solo para FREBA

Su función principal es dar contexto, orden y agrupación.

---

## 2. Actores y estructura organizacional

### Organización
Entidad institucional que representa a una parte participante dentro del sistema.

Ejemplos:

- FREBA
- cooperativa
- distribuidora
- organismo público
- otra organización asociada o relacionada

Toda comunicación tiene una organización emisora y, según el caso, una organización destino.

---

### Usuario
Persona que accede al sistema y actúa representando a una organización.

Un usuario:

- puede pertenecer a FREBA o a una organización externa
- puede crear o participar en comunicaciones según permisos
- actúa siempre en nombre de una organización
- eventualmente puede representar más de una organización, si el modelo final lo permite

---

### Usuario interno
Usuario perteneciente a FREBA.

Se caracteriza por tener acceso al entorno interno de gestión, incluyendo:

- expedientes
- historial interno
- chat interno
- trabajo colaborativo interno
- administración global del caso, según rol

---

### Usuario externo
Usuario perteneciente a una organización distinta de FREBA.

Su acceso es controlado y limitado a lo que corresponda según:

- su organización
- la comunicación en la que participa
- el escenario de uso
- y su rol sobre la comunicación

No tiene acceso al contexto interno completo de FREBA.

---

### Emisor real
Concepto que indica que quien emite una comunicación no es solo una persona ni solo una organización, sino:

**usuario concreto + organización a la que representa**

Este principio debe respetarse en auditoría, trazabilidad, historial y permisos.

---

## 3. Participación sobre la comunicación

### Asignación
Vínculo entre un usuario y una comunicación que habilita su participación dentro de ella.

La asignación determina:

- si el usuario participa de la comunicación
- con qué rol participa
- qué puede hacer
- qué nivel de operación activa y visibilidad operativa tiene

En escenarios externos, puede existir visibilidad general básica a nivel organización según escenario, aunque la operación activa siga dependiendo de la asignación.

Una comunicación puede tener múltiples usuarios asignados.

---

### Rol sobre comunicación
Función que define el alcance operativo de un usuario dentro de una comunicación.

En esta etapa, los roles identificados son:

- observador
- editor
- responsable

La lógica de permisos se apoya en el rol sobre la comunicación, no solo en si el usuario es interno o externo.

---

### Observador
Rol de seguimiento limitado dentro de una comunicación.

En `v0.2`:

- puede ver lo que le corresponda según su visibilidad
- no puede gestionar la comunicación
- no puede responder formalmente
- no puede cambiar estado
- no puede administrar usuarios
- no ve el chat interno
- no usa chat compartido como rol observador puro

Su alcance exacto puede variar según escenario, pero su lógica general es de consulta y seguimiento.

---

### Editor
Rol operativo de trabajo activo sobre una comunicación.

En esta etapa, el editor puede:

- editar la comunicación mientras esté abierta
- cambiar estado
- usar chat según ámbito
- cargar documentos
- agregar o quitar usuarios
- asociar expedientes
- crear subcomunicaciones
- emitir respuesta formal

En `v0.2`, editor y responsable se consideran equivalentes en permisos y operaciones de implementación.

---

### Responsable
Rol operativo de trabajo activo sobre una comunicación.

En términos funcionales actuales, tiene el mismo alcance que editor.  
Se mantiene como concepto separado porque negocio podría definir más adelante diferencias entre ambos.

En `v0.2`, backend puede tratarlos igual para autorización y operaciones núcleo.

---

## 4. Flujo y estados

### Workflow
Conjunto ordenado de estados y posibles transiciones aplicables a una comunicación.

Cada tipo de comunicación puede tener su propio workflow.  
Además, existe la idea de un workflow por defecto para tipos básicos o genéricos.

---

### Estado
Situación actual de una comunicación dentro de su workflow.

Características:

- cada comunicación tiene un único estado actual
- el estado pertenece a la comunicación
- el estado es visible para quienes tienen acceso a la comunicación
- los estados deben ser configurables y no hardcodeados

---

### Estado inicial
Primer estado que toma una comunicación al ser creada y enviada.

Depende del tipo de comunicación y de su workflow asociado.

---

### Cierre
Acción o situación por la cual una comunicación deja de estar abierta para trabajo normal.

En esta etapa:

- una comunicación puede cerrarse con o sin respuesta formal
- una comunicación cerrada puede reabrirse si no tiene respuesta final emitida
- si ya tiene respuesta formal final, la continuidad del tema debe resolverse con una nueva comunicación relacionada

---

### Reapertura
Acción mediante la cual una comunicación cerrada vuelve a estado operativo.

En esta etapa solo se contempla como válida cuando todavía no existe respuesta formal emitida.

---

## 5. Documentos y contenido

### Documento
Archivo o pieza documental asociada a una comunicación.

Puede formar parte de:

- la creación de una comunicación
- el trabajo interno o externo sobre la comunicación
- la respuesta formal

Los documentos son parte central del tratamiento del caso.

---

### Versión de documento
Registro de una actualización o nueva carga sobre un mismo documento lógico.

En esta etapa:

- cada nueva carga genera una nueva versión
- la última versión es la vigente
- las versiones anteriores se conservan
- el historial de versiones forma parte de la trazabilidad documental

---

### Documento vigente
Última versión disponible de un documento.

Es la versión que debe considerarse actual para trabajo operativo y para exposición cuando quede incluida en la respuesta formal.

---

### Adjunto inicial
Documento incorporado al momento de crear una comunicación.

Puede venir cargado por FREBA o por un externo, según quién la inicie.

---

### Documento de respuesta
Documento que forma parte de la respuesta formal de una comunicación.

Puede ser:

- un documento ya cargado en la comunicación y seleccionado al responder
- o un documento nuevo agregado antes de emitir la respuesta, según el flujo habilitado

---

## 6. Comunicación conversacional y colaboración

### Chat
Espacio cronológico de mensajes vinculado a una comunicación.

Se utiliza para intercambio operativo no formal y colaboración.

En esta etapa:

- no reemplaza la respuesta formal
- no admite borrado
- no gestiona adjuntos propios
- se separa por ámbitos de visibilidad

---

### Chat interno
Canal de conversación reservado para usuarios internos de FREBA.

Sirve para:

- coordinar tareas
- analizar el caso
- dejar comentarios internos
- ordenar el trabajo colaborativo interno

Los externos no tienen acceso a este ámbito.

---

### Chat compartido
Canal de conversación visible entre FREBA y la contraparte externa, cuando el escenario de la comunicación lo requiera.

Se usa para:

- aclaraciones
- pedidos de información
- seguimiento
- intercambio operativo no formal

No reemplaza la respuesta formal.

---

## 7. Escenarios operativos

### Escenario externo iniciador
Escenario en el que un usuario externo crea una comunicación hacia FREBA y luego queda esperando tratamiento y respuesta.

En este escenario, el externo tiene un rol más acotado:

- crea la comunicación
- carga documentación inicial
- consulta estado
- espera respuesta
- puede participar del chat compartido si corresponde

---

### Escenario externo respondedor
Escenario en el que FREBA crea una comunicación hacia un externo y espera una respuesta de esa organización.

En este escenario, el externo trabaja activamente sobre la comunicación para construir la respuesta.

Puede, según el diseño actual:

- subir documentos
- actualizar datos
- usar chat compartido
- agregar usuarios de su misma organización
- mover ciertos estados
- emitir la respuesta formal

---

### Escenario interno FREBA
Escenario en el que uno o más usuarios internos de FREBA gestionan una comunicación, sea de origen interno o externo.

Incluye:

- análisis
- colaboración interna
- uso de chat interno
- gestión documental
- asignaciones
- subcomunicaciones
- respuesta formal
- asociación a expedientes

---

## 8. Relación entre objetos

### Relación entre comunicaciones
Vínculo que conecta dos comunicaciones dentro de un mismo contexto de trabajo.

En esta etapa, la relación principal es **padre / hija**.

Sirve para:

- preservar contexto
- reconstruir el caso general
- entender comunicaciones que nacen a partir de otras

---

### Comunicación madre
Comunicación origen a partir de la cual se genera una o más comunicaciones hijas.

Debe poder mostrar al menos una referencia clara a sus hijas.

---

### Comunicación hija
Comunicación relacionada nacida desde otra comunicación.

No es una edición ni una derivación de la original, sino una nueva gestión formal vinculada.

---

### Expediente principal
Expediente que actúa como contenedor principal de una comunicación en la operación actual del sistema.

Aunque el diseño pueda soportar múltiples expedientes, en la práctica inicial se propone operar con uno principal por comunicación.

---

## 9. Trazabilidad y visibilidad

### Historial
Registro cronológico de hechos relevantes ocurridos sobre una comunicación.

Puede incluir:

- creación
- edición
- cambios de estado
- asignaciones
- respuesta formal
- carga de documentos
- nuevas versiones
- relación con expedientes
- creación de subcomunicaciones

---

### Trazabilidad
Capacidad del sistema para reconstruir quién hizo qué, cuándo y sobre qué objeto.

Es un principio central del sistema.

---

### Visibilidad
Alcance de acceso que tiene un usuario sobre la información de una comunicación.

La visibilidad depende de:

- organización
- asignación
- rol
- escenario
- tipo de información

No todo lo que existe en una comunicación es necesariamente visible para todos sus participantes.

---

### Visibilidad externa restringida
Principio según el cual los usuarios externos no ven la totalidad de la información gestionada por FREBA.

Por ejemplo, en esta etapa los externos no ven:

- expedientes
- historial interno detallado
- chat interno
- documentos internos de trabajo
- asignaciones internas completas

---

## 10. Conceptos de implementación conceptual

### Documento madre
Archivo principal de definiciones de dominio que actúa como fuente de verdad provisoria del sistema.

En este caso, el levantamiento de requerimientos `v0.2` cumple ese rol.

---

### Supuesto operativo
Definición adoptada provisionalmente para poder seguir diseñando o implementando aunque negocio todavía no la haya confirmado de forma definitiva.

Debe quedar siempre explicitado como supuesto y no como verdad cerrada del negocio.

---

### Regla de negocio
Condición, restricción o comportamiento que el sistema debe respetar por responder a una necesidad del dominio.

Ejemplo:
- una comunicación tiene una única respuesta formal
- los externos no ven expedientes
- una comunicación hija no reemplaza a la madre

---

## 11. Términos a seguir refinando

Los siguientes conceptos ya existen en el dominio, pero todavía requieren definición más precisa en etapas futuras:

- diferencia real entre editor y responsable
- reglas finas de transición por estado
- definición más rica de bandeja
- reglas exactas de visibilidad organizacional externa
- casos reales por tipo de comunicación
- alcance definitivo de expedientes múltiples

---
