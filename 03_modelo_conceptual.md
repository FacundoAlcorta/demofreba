# Modelo conceptual

## Sistema de gestión de comunicaciones FREBA

Documento de trabajo para describir el modelo conceptual del sistema, identificando las entidades principales del dominio, sus relaciones y sus responsabilidades funcionales.

Este documento no define todavía la implementación técnica ni el modelo relacional final.  
Su objetivo es servir como puente entre el levantamiento funcional y el futuro diseño de base de datos y arquitectura.

---

## 1. Objetivo del documento

Este archivo busca responder preguntas como:

- qué entidades existen en el dominio
- cuál es la entidad central
- cómo se relacionan entre sí
- qué representa cada una
- qué responsabilidad funcional tiene cada objeto
- qué cosas pertenecen a una comunicación y cuáles no
- qué objetos son configurables y cuáles son operativos

---

## 2. Principio general del modelo

El modelo está centrado en la **Comunicación** como entidad principal del dominio.

Todo lo demás existe para:

- configurarla
- contextualizarla
- permitir operarla
- dejar trazabilidad
- agruparla
- o enriquecer su gestión

El sistema no está centrado en el expediente ni en el documento como objeto principal.  
El objeto principal es la comunicación.

---

## 3. Vista general del dominio

A nivel conceptual, el dominio puede organizarse en seis grupos principales:

### 3.1 Estructura organizacional
- Organización
- Usuario

### 3.2 Configuración funcional
- Tipo de Comunicación
- Workflow
- Estado
- Bandeja

### 3.3 Operación principal
- Comunicación
- Asignación de Usuario a Comunicación
- Rol sobre Comunicación
- Respuesta Formal

### 3.4 Soporte documental y conversacional
- Documento
- Versión de Documento
- Mensaje / Chat

### 3.5 Contexto y agrupación
- Relación entre Comunicaciones
- Expediente
- Asociación Comunicación–Expediente

### 3.6 Trazabilidad
- Historial / Evento de Comunicación

---

## 4. Entidades conceptuales del dominio

## 4.1 Organización

### Definición
Entidad institucional que representa a una parte participante dentro del sistema.

### Ejemplos
- FREBA
- cooperativa
- distribuidora
- organismo público
- otra organización vinculada

### Responsabilidad conceptual
La organización sirve para:

- identificar a qué entidad representa un usuario
- determinar el origen o destino institucional de una comunicación
- delimitar visibilidad externa
- acotar permisos de colaboración externa

### Observaciones
- una comunicación puede tener organización emisora y organización destino
- los usuarios externos solo pueden operar dentro de su propia organización
- FREBA es una organización especial porque administra el dominio completo

---

## 4.2 Usuario

### Definición
Persona que accede al sistema y opera en nombre de una organización.

### Responsabilidad conceptual
El usuario sirve para:

- crear comunicaciones
- participar en comunicaciones
- responder
- cargar documentos
- interactuar en chats
- quedar trazado en el historial

### Reglas relevantes
- el usuario actúa siempre representando a una organización
- eventualmente un mismo usuario podría representar más de una organización
- la autoridad de un usuario no depende solo de quién es, sino también de:
  - su organización
  - su asignación a la comunicación
  - su rol sobre esa comunicación
  - el escenario operativo

---

## 4.3 Tipo de Comunicación

### Definición
Entidad de configuración que define el comportamiento general de una comunicación.

### Responsabilidad conceptual
Determina, entre otras cosas:

- nombre del tipo
- formulario de creación
- atributos particulares
- quién puede iniciarla
- bandeja inicial
- workflow aplicable
- reglas de visibilidad
- otras restricciones operativas

### Naturaleza
Es una entidad **configurable**, no una entidad operativa.

### Relación con la comunicación
Toda comunicación pertenece a un tipo de comunicación.

---

## 4.4 Workflow

### Definición
Conjunto de estados y transiciones posibles asociados a un tipo de comunicación.

### Responsabilidad conceptual
Define el ciclo de vida esperado de una comunicación.

### Naturaleza
Es una entidad **configurable**.

### Relación con el tipo
Un tipo de comunicación tiene asociado un workflow.

### Observaciones
- puede existir un workflow por defecto
- cada tipo puede tener un workflow propio
- en el futuro podría enriquecerse con reglas por transición

---

## 4.5 Estado

### Definición
Situación actual de una comunicación dentro de un workflow.

### Responsabilidad conceptual
Permite conocer en qué etapa del tratamiento se encuentra una comunicación.

### Relación con la comunicación
Cada comunicación tiene un único estado actual.

### Relación con workflow
Los estados válidos dependen del workflow aplicable a esa comunicación.

### Observaciones
- el estado pertenece a la comunicación
- no hay estados distintos para interno y externo en esta etapa
- los estados son visibles para quienes pueden ver la comunicación

---

## 4.6 Bandeja

### Definición
Agrupación inicial de usuarios a la que ingresa una comunicación según su tipo.

### Responsabilidad conceptual
Definir la recepción inicial y el primer ámbito de trabajo sobre una comunicación entrante.

### Naturaleza
En esta etapa se entiende como una **lista de usuarios**, no necesariamente como área formal ni cola avanzada.

### Observaciones
- se usa especialmente cuando una comunicación entra desde un externo hacia FREBA
- cuando la comunicación la crea FREBA, la bandeja efectiva se reemplaza por la selección manual de usuarios destino

---

## 4.7 Comunicación

### Definición
Entidad principal del sistema.  
Representa un intercambio formal gestionable.

### Responsabilidad conceptual
La comunicación concentra:

- el contenido principal del caso
- su tipo
- su estado
- sus participantes
- sus documentos
- su respuesta formal
- sus relaciones con otras comunicaciones
- su pertenencia a expediente
- su historial operativo

### Componentes conceptuales
Una comunicación posee:

- datos comunes
- datos particulares según tipo
- organización emisora
- organización destino
- estado actual
- usuarios asignados
- documentos
- chat
- respuesta formal opcional
- relaciones con otras comunicaciones
- asociación a expediente

### Reglas relevantes
- es la unidad operativa central del sistema
- puede ser iniciada por FREBA o por un externo
- no tiene borrador en esta etapa
- al crearse, se envía
- puede cerrarse con o sin respuesta
- si ya tiene respuesta formal final, la continuidad del tema se resuelve con una nueva comunicación relacionada

---

## 4.8 Datos particulares por tipo de comunicación

### Definición
Conjunto de atributos específicos que existen solo para determinados tipos de comunicación.

### Responsabilidad conceptual
Permitir que tipos distintos de comunicación tengan estructuras de datos distintas sin perder orden relacional.

### Naturaleza
Se prevé modelarlos en subestructuras específicas por tipo.

### Relación con la comunicación
Una comunicación tiene siempre una base común y, eventualmente, una extensión de datos particulares según el tipo al que pertenece.

### Observaciones
- esta pieza no necesariamente debe leerse como una entidad visible para el usuario final
- conceptualmente representa la especialización estructural de la comunicación

---

## 4.9 Asignación de Usuario a Comunicación

### Definición
Relación entre un usuario y una comunicación que formaliza su participación en ella.

### Responsabilidad conceptual
Permite determinar:

- qué usuarios participan en una comunicación
- con qué rol participan
- qué pueden hacer
- qué alcance operativo y de visibilidad tienen dentro de la comunicación

### Naturaleza
Es una entidad relacional-operativa.

### Relación con la comunicación
Una comunicación puede tener múltiples usuarios asignados.

### Relación con usuario
Un usuario puede estar asignado a múltiples comunicaciones.

### Observaciones
La asignación es una de las piezas más importantes del modelo, porque conecta:

- permisos
- visibilidad
- colaboración
- trazabilidad
- define principalmente la **operación activa** sobre la comunicación
- para usuarios externos puede existir visibilidad organizacional básica (existencia y datos generales) según escenario, aun cuando la operación activa requiera asignación

---

## 4.10 Rol sobre Comunicación

### Definición
Clasificación funcional del nivel de intervención que un usuario tiene dentro de una comunicación.

### Ejemplos actuales
- observador
- editor
- responsable

### Responsabilidad conceptual
Define el alcance operativo del usuario sobre la comunicación.

### Observaciones
- en esta etapa, editor y responsable se consideran equivalentes
- el rol no debe pensarse aislado del escenario
- a futuro podría enriquecerse o separarse mejor

---

## 4.11 Respuesta Formal

### Definición
Respuesta oficial y final asociada a una comunicación.

### Responsabilidad conceptual
Representa la contestación formal del caso tratado en esa comunicación.

### Características
- cada comunicación puede tener una única respuesta formal
- no es una comunicación nueva
- no tiene workflow propio
- no tiene estado propio
- puede tener texto y documentos
- una vez emitida, queda congelada

### Relación con la comunicación
La respuesta formal pertenece a una única comunicación.

### Observaciones
- puede ser emitida por FREBA o por un externo, según el escenario
- forma parte del historial de la comunicación

---

## 4.12 Documento

### Definición
Objeto documental asociado a una comunicación.

### Responsabilidad conceptual
Representar archivos y piezas documentales que acompañan o forman parte del tratamiento del caso.

### Uso conceptual
Un documento puede intervenir en:

- la creación de una comunicación
- el trabajo posterior sobre esa comunicación
- la construcción de la respuesta formal

### Observaciones
- los documentos pertenecen a la comunicación
- su exposición a externos depende del contexto y de reglas de visibilidad

---

## 4.13 Versión de Documento

### Definición
Registro de una iteración o actualización de un documento lógico.

### Responsabilidad conceptual
Permitir mantener trazabilidad documental sin perder la última versión vigente.

### Relación con documento
Un documento puede tener múltiples versiones.

### Observaciones
- la última versión es la vigente
- las versiones anteriores se conservan
- esta entidad es clave para el trabajo colaborativo documental

---

## 4.14 Mensaje / Chat de Comunicación

### Definición
Mensaje cronológico asociado a una comunicación para intercambio operativo no formal.

### Responsabilidad conceptual
Permitir colaboración conversacional sin reemplazar la formalidad de la respuesta.

### Ámbitos conceptuales
Existen dos ámbitos:

- chat interno FREBA
- chat compartido con externos

### Observaciones
- los mensajes pertenecen a una comunicación
- el acceso al mensaje depende del ámbito y del rol
- no admiten adjuntos propios en esta etapa
- no se borran

---

## 4.15 Relación entre Comunicaciones

### Definición
Vínculo que conecta dos comunicaciones para expresar contexto, continuidad o dependencia funcional.

### Relación principal actual
- padre / hija

### Responsabilidad conceptual
Permitir que una comunicación pueda originar otra sin mezclar sus ciclos de vida.

### Observaciones
- la hija es independiente de la madre
- no hereda automáticamente todos sus datos
- permite abrir una gestión nueva pero contextualizada
- es clave para resolver continuidad después de una respuesta final

---

## 4.16 Expediente

### Definición
Entidad de agrupación administrativa que reúne comunicaciones bajo un contexto común.

### Responsabilidad conceptual
Aportar organización, agrupación y referencia administrativa.

### Características actuales
- tiene identificador
- tiene carátula
- tiene asunto
- tiene fecha
- no tiene estado propio en esta etapa
- no tiene responsables propios en esta etapa
- es visible solo para FREBA

### Observaciones
- no gobierna la vida de la comunicación
- su función es contextual y agrupadora
- la gestión sigue ocurriendo sobre las comunicaciones

---

## 4.17 Asociación Comunicación–Expediente

### Definición
Relación entre una comunicación y un expediente.

### Responsabilidad conceptual
Permitir que una comunicación quede agrupada dentro de un expediente.

### Regla operativa actual
- a nivel de modelo podría soportarse asociación múltiple
- a nivel funcional inicial se trabajará con un expediente principal por comunicación

### Observaciones
- si una madre tiene expediente, las hijas se asocian al mismo
- si la madre se asocia después, esa asociación se propaga a las hijas

---

## 4.18 Historial / Evento de Comunicación

### Definición
Registro de hechos relevantes ocurridos sobre una comunicación.

### Responsabilidad conceptual
Dar trazabilidad al ciclo de vida y permitir reconstruir qué pasó, cuándo y por quién.

### Ejemplos de eventos
- creación
- edición
- cambio de estado
- asignación de usuarios
- respuesta emitida
- carga documental
- nueva versión documental
- asociación a expediente
- creación de subcomunicación

### Observaciones
- el historial completo es principalmente interno para FREBA
- externamente se expone solo una parte muy acotada de la evolución del caso

---

## 5. Relaciones conceptuales principales

## 5.1 Organización ↔ Usuario
- una organización puede tener muchos usuarios
- un usuario representa al menos una organización

---

## 5.2 Tipo de Comunicación ↔ Workflow
- un tipo de comunicación tiene asociado un workflow

---

## 5.3 Workflow ↔ Estado
- un workflow contiene estados posibles y sus transiciones

---

## 5.4 Tipo de Comunicación ↔ Comunicación
- toda comunicación pertenece a un tipo de comunicación

---

## 5.5 Comunicación ↔ Estado
- toda comunicación tiene un estado actual

---

## 5.6 Comunicación ↔ Usuario
- la operación activa del usuario sobre la comunicación se formaliza por **asignación**
- en escenario externo puede existir visibilidad general básica por organización, según reglas de escenario y visibilidad

---

## 5.7 Comunicación ↔ Asignación
- una comunicación tiene muchas asignaciones de usuarios

---

## 5.8 Asignación ↔ Rol sobre Comunicación
- cada asignación incluye el rol con el que participa ese usuario en esa comunicación

---

## 5.9 Comunicación ↔ Respuesta Formal
- una comunicación puede tener cero o una respuesta formal

---

## 5.10 Comunicación ↔ Documento
- una comunicación puede tener muchos documentos

---

## 5.11 Documento ↔ Versión de Documento
- un documento puede tener muchas versiones

---

## 5.12 Comunicación ↔ Mensaje / Chat
- una comunicación puede tener muchos mensajes
- los mensajes pertenecen a un ámbito de visibilidad determinado

---

## 5.13 Comunicación ↔ Comunicación
- una comunicación puede relacionarse con otra como madre o hija

---

## 5.14 Comunicación ↔ Expediente
- una comunicación puede asociarse a un expediente principal en la operación inicial
- el modelo puede quedar preparado para múltiples asociaciones futuras

---

## 5.15 Comunicación ↔ Historial / Evento
- una comunicación tiene muchos eventos de historial

---

## 6. Separación conceptual entre entidades configurables y operativas

## 6.1 Entidades configurables
Son las que definen comportamiento general del sistema y no representan casos concretos de trabajo.

Incluyen:

- Tipo de Comunicación
- Workflow
- Estado (como catálogo/configuración del workflow)
- Bandeja

---

## 6.2 Entidades operativas
Son las que representan casos reales o trabajo concreto dentro del sistema.

Incluyen:

- Comunicación
- Asignación
- Respuesta Formal
- Documento
- Versión de Documento
- Mensaje / Chat
- Relación entre Comunicaciones
- Expediente
- Asociación Comunicación–Expediente
- Historial / Evento

---

## 7. Decisiones conceptuales ya bastante firmes

- la entidad principal del dominio es la comunicación
- el expediente es un agrupador, no el centro del modelo
- la respuesta formal no es una comunicación independiente
- una comunicación puede tener una única respuesta formal
- la continuidad de un tema posterior a respuesta final se resuelve con una nueva comunicación relacionada
- las subcomunicaciones son independientes aunque contextualizadas
- los documentos pertenecen a la comunicación y se versionan
- la participación de un usuario se formaliza mediante asignación
- la visibilidad externa es limitada y depende del escenario
- el modelo distingue entre configuración del comportamiento y operación real

---

## 8. Zonas conceptuales todavía abiertas

### 8.1 Diferencia fina entre Editor y Responsable
Hoy se consideran equivalentes, pero a futuro podrían separarse más.

### 8.2 Bandeja como entidad rica o simple
Hoy se modela como lista de usuarios, pero podría crecer conceptualmente.

### 8.3 Profundidad de relaciones entre comunicaciones
El modelo admite recursividad, pero todavía no está definido cuánto se mostrará o gestionará operativamente.

### 8.4 Modelo definitivo de visibilidad organizacional externa
Está claro en términos generales, pero podría necesitar más granularidad.

### 8.5 Expediente múltiple
El diseño puede prepararse para soportarlo, pero la operación inicial será simple.

---

## 9. Uso recomendado de este documento

Este archivo debe usarse como base para:

- pasar a un modelo relacional preliminar
- diseñar entidades backend
- discutir arquitectura
- validar cobertura de casos de uso
- alinear agentes de diseño y modelado

Debe leerse junto con:

- `00_requerimientos_base_v0_2.md`
- `01_glosario_dominio.md`
- `02_escenarios_y_permisos.md`
- `04_decisiones_y_supuestos.md`
- `05_plan_implementacion.md`

---
