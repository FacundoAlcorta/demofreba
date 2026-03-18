# Decisiones y supuestos

## Sistema de gestión de comunicaciones FREBA

Documento de trabajo para dejar explícitas las decisiones ya tomadas, los supuestos funcionales adoptados para avanzar en el diseño y las restricciones que deben respetarse durante el análisis, modelado e implementación.

Este archivo es especialmente importante para evitar que futuros agentes, diseñadores o desarrolladores:

- inventen reglas no acordadas
- mezclen decisiones firmes con supuestos temporales
- congelen como verdad definitiva algo que todavía puede cambiar
- o contradigan el dominio ya relevado

---

## 1. Objetivo del documento

Este archivo busca distinguir claramente entre:

- **decisiones firmes**
- **supuestos operativos**
- **restricciones**
- **pendientes reales**
- **riesgos de diseño**

La idea es que funcione como documento de control para todo el diseño posterior.

---

## 2. Cómo leer este documento

### 2.1 Decisión firme
Es una definición ya aceptada como base del dominio y que debe respetarse en el diseño actual.

### 2.2 Supuesto operativo
Es una definición provisional adoptada para poder seguir avanzando, aunque negocio todavía no la haya confirmado en forma definitiva.

### 2.3 Restricción
Es algo que no debe hacerse o no debe asumirse.

### 2.4 Pendiente
Es una cuestión todavía abierta que puede requerir revisión futura.

---

## 3. Decisiones firmes de dominio

## 3.1 La entidad principal del sistema es la Comunicación

### Decisión
El sistema está centrado en la **Comunicación**.

### Implicancia
- el expediente no es la entidad principal
- el documento no es la entidad principal
- la lógica central del sistema debe construirse alrededor de la comunicación

---

## 3.2 El expediente es un agrupador administrativo

### Decisión
El expediente cumple una función de agrupación y contexto, no de conducción del flujo principal.

### Implicancia
- una comunicación puede existir sin expediente
- el expediente no gobierna el ciclo de vida de la comunicación
- la gestión sigue ocurriendo sobre la comunicación

---

## 3.3 Toda comunicación pertenece a un tipo de comunicación

### Decisión
El tipo de comunicación es obligatorio y central.

### Implicancia
El tipo define, al menos:

- formulario
- atributos particulares
- workflow
- bandeja inicial
- quién puede iniciarla
- reglas generales de visibilidad

---

## 3.4 La comunicación tiene datos comunes y datos particulares por tipo

### Decisión
Toda comunicación tiene una base común, pero además puede tener atributos específicos según el tipo.

### Implicancia
El diseño debe contemplar una base común y una especialización estructural por tipo.

---

## 3.5 Los atributos particulares por tipo se modelarán con tablas específicas

### Decisión
Se evita, en principio, un modelo basado en estructuras genéricas descontroladas.

### Implicancia
Se prefiere:

- tabla base común
- tablas particulares por tipo

### Restricción asociada
No asumir un `JSONField` como solución por defecto del dominio.

---

## 3.6 No existe derivación como concepto fuerte del dominio

### Decisión
No se modelará la “derivación” como entidad o mecanismo principal.

### Implicancia
Cuando hace falta colaboración sobre la misma gestión:
- se agregan usuarios a la misma comunicación

Cuando hace falta abrir una nueva gestión:
- se crea una nueva comunicación relacionada

---

## 3.7 Las subcomunicaciones son comunicaciones independientes

### Decisión
Una comunicación hija no es una continuación embebida dentro de la misma comunicación, sino una nueva comunicación formal relacionada.

### Implicancia
- tiene su propio tipo
- tiene su propio workflow
- tiene sus propios participantes
- mantiene vínculo contextual con la madre
- no hereda automáticamente todos sus datos

---

## 3.8 La respuesta formal es única

### Decisión
Cada comunicación puede tener una única respuesta formal.

### Implicancia
- no hay múltiples respuestas finales sobre la misma comunicación
- la respuesta es una pieza formal y final del caso

---

## 3.9 La respuesta formal no es una comunicación independiente

### Decisión
La respuesta formal pertenece a la comunicación.

### Implicancia
- no tiene workflow propio
- no tiene estado propio
- forma parte del historial de la comunicación

---

## 3.10 La respuesta formal queda congelada

### Decisión
Una vez emitida, la respuesta formal no se edita ni se anula.

### Implicancia
Debe modelarse como una pieza cerrada y trazable.

---

## 3.11 Si un tema continúa después de una respuesta final, se crea una nueva comunicación

### Decisión
No se debe continuar operativamente sobre la misma comunicación como flujo normal una vez que ya tuvo respuesta formal final.

### Implicancia
La continuidad del caso debe resolverse con una nueva comunicación relacionada.

---

## 3.12 La lógica principal de permisos depende de la asignación y del rol sobre la comunicación

### Decisión
Los permisos no deben depender solo de si un usuario es interno o externo.

### Implicancia
La pieza central para permisos es:

- la comunicación
- la asignación del usuario a esa comunicación
- el rol dentro de esa comunicación
- el escenario operativo

---

## 3.13 Los usuarios actúan en nombre de una organización

### Decisión
El emisor real siempre debe entenderse como:

**usuario concreto + organización representada**

### Implicancia
Esto debe reflejarse en:
- auditoría
- trazabilidad
- vistas
- permisos
- historial

---

## 3.14 Los externos no ven expedientes

### Decisión
Los expedientes son visibles solo para FREBA.

### Implicancia
Toda la lógica de expediente queda dentro del mundo interno.

---

## 3.15 El estado de una comunicación es único y visible para quienes tienen acceso a ella

### Decisión
No habrá, por ahora, estados distintos para interno y externo.

### Implicancia
El estado debe ser único a nivel de comunicación.

---

## 3.16 Los documentos se versionan

### Decisión
Los documentos no se reemplazan destruyendo el anterior.

### Implicancia
- cada nueva carga genera versión
- la última versión es la vigente
- las anteriores se conservan

---

## 3.17 Debe existir trazabilidad

### Decisión
La trazabilidad es obligatoria como principio del sistema.

### Implicancia
El sistema debe poder reconstruir:
- quién hizo qué
- cuándo
- sobre qué comunicación
- con qué documentos
- con qué cambio de estado
- con qué respuesta
- con qué relaciones

---

## 4. Supuestos operativos adoptados para poder avanzar

## 4.1 No hay borradores de comunicación en v0.2

### Supuesto
En esta etapa, una comunicación se envía al momento de crearse.

### Motivo
Simplificar el diseño inicial y evitar complejidad temprana.

### Posible revisión futura
Más adelante podría incorporarse un concepto formal de borrador o publicación diferida.

---

## 4.2 No hay borradores de respuesta formal en v0.2

### Supuesto
La respuesta formal se crea y se emite en el mismo acto.

### Motivo
Simplificar el modelo y mantener la respuesta como pieza final cerrada.

---

## 4.3 Editor y Responsable tienen el mismo alcance funcional

### Supuesto
Mientras negocio no defina diferencias concretas, ambos roles se consideran equivalentes.

### Motivo
Permitir avanzar sin bloquear el diseño por una diferencia aún no acordada.

### Posible revisión futura
Más adelante podrían diferenciarse por:
- ownership
- aprobación
- decisión final
- seguimiento principal

---

## 4.4 La bandeja se interpreta como lista de usuarios

### Supuesto
No se modela todavía como área, cola compleja o entidad avanzada.

### Motivo
Resolver el ingreso inicial sin sobreingeniería temprana.

### Posible revisión futura
Podría evolucionar a:
- área
- cola lógica
- grupo operativo
- entidad configurable con reglas

---

## 4.5 Rol inicial de usuarios de bandeja: Editor

### Supuesto
Los usuarios que reciben inicialmente una comunicación desde bandeja quedan con capacidad operativa equivalente a editor.

### Motivo
Permitir trabajo colaborativo desde el inicio.

### Riesgo
Podría dar demasiado poder distribuido si la bandeja es muy amplia.

---

## 4.6 Operación inicial con un expediente principal por comunicación

### Supuesto
Aunque el diseño pueda soportar múltiples expedientes, la operación inicial se simplifica usando uno principal por comunicación.

### Motivo
Simplificar UX y reducir ambigüedad.

### Posible revisión futura
Habilitar realmente múltiples expedientes cuando negocio lo valide.

---

## 4.7 Chat separado en dos ámbitos

### Supuesto
Se modelarán dos chats o dos espacios conversacionales diferenciados:

- chat interno FREBA
- chat compartido con externos

### Motivo
Separar claramente trabajo interno de intercambio con contraparte.

---

## 4.8 Los mensajes de chat no admiten adjuntos propios

### Supuesto
Los adjuntos se manejan siempre como documentos de la comunicación, no como adjuntos del mensaje.

### Motivo
Mantener el modelo documental más limpio.

---

## 4.9 El historial completo es principalmente interno

### Supuesto
El historial completo operativo y de auditoría será visible para FREBA, no para externos.

### Motivo
Proteger el trabajo interno y simplificar la exposición externa.

---

## 4.10 El externo ve solo documentos acotados

### Supuesto
El externo no ve todos los documentos de trabajo interno.

### Ve:
- los documentos que él mismo cargó
- los documentos del envío inicial visibles para él
- los documentos finales incluidos en la respuesta

### No ve:
- documentos intermedios internos de FREBA

---

## 4.11 Externo en escenario de respuesta puede operar activamente

### Supuesto
Cuando FREBA envía una comunicación a un externo para que responda, ese externo puede:

- editar datos habilitados
- subir documentos
- usar chat compartido
- agregar usuarios de su organización
- mover ciertos estados
- emitir la respuesta formal

### Motivo
Reflejar el caso real donde el externo necesita trabajar para construir la respuesta.

---

## 4.12 Externo que inicia y espera respuesta tiene permisos limitados

### Supuesto
Cuando el externo es iniciador y no respondedor, queda mucho más acotado.

### Puede:
- crear
- ver estado
- ver respuesta
- participar del chat compartido cuando corresponda

### No puede:
- seguir operando activamente la comunicación como flujo normal
- administrar usuarios
- ver trabajo interno

---

## 4.13 Reapertura solo antes de respuesta final

### Supuesto
Una comunicación cerrada puede reabrirse si aún no existe respuesta formal emitida.

### Motivo
Mantener coherencia con la idea de que la respuesta final cierra conceptualmente la gestión.

---

## 4.14 El ajuste de una comunicación ya enviada se resuelve quitando y reponiendo asignación externa

### Supuesto
Si FREBA necesita corregir una comunicación ya enviada, puede quitar la asignación al externo, editar y volver a asignar.

### Motivo
Resolver operativamente el problema sin introducir todavía un modelo formal de publicación diferida.

### Riesgo
Es una solución funcional viable, pero conceptualmente imperfecta.  
Podría reemplazarse en el futuro por una lógica de “emitida / visible / publicada”.

---

## 4.15 Se admite recursividad entre comunicaciones

### Supuesto
Una hija puede generar nuevas hijas a nivel de modelo.

### Motivo
No limitar artificialmente el dominio.

### Criterio de UX inicial
La interfaz puede mostrar prioritariamente padre e hijas directas para no complejizar la navegación.

---

## 5. Restricciones de diseño

## 5.1 No inventar dominio no validado

### Restricción
No deben agregarse conceptos de negocio que no estén en los documentos base o en supuestos expresamente marcados.

Ejemplos:
- firmas digitales obligatorias
- circuitos de aprobación no definidos
- múltiples respuestas formales
- expedientes con estados si todavía no fueron acordados

---

## 5.2 No convertir supuestos en verdades absolutas

### Restricción
Todo lo que en este documento esté marcado como supuesto debe tratarse como provisional.

---

## 5.3 No mezclar chat con respuesta formal

### Restricción
La respuesta formal y el chat cumplen funciones distintas.

- el chat = intercambio operativo no formal
- la respuesta formal = contestación oficial y final

---

## 5.4 No modelar al expediente como centro del sistema

### Restricción
El expediente no debe dominar el diseño general ni absorber la identidad de la comunicación.

---

## 5.5 No asumir visibilidad total para externos

### Restricción
Los externos no deben ver por defecto todo lo que ocurre dentro de una comunicación.

La visibilidad externa siempre debe ser acotada y contextual.

---

## 5.6 No asumir que todos los roles ya están cerrados

### Restricción
La diferencia entre observador, editor y responsable todavía puede refinarse.

---

## 5.7 No asumir que todas las transiciones son libres

### Restricción
Aunque hoy haya reglas generales, más adelante puede definirse una matriz de transiciones más estricta por tipo, rol o escenario.

---

## 6. Pendientes reales

## 6.1 Diferencia fina entre Editor y Responsable

### Estado actual
No definida.

### Impacto
Afecta:
- permisos finos
- ownership
- métricas
- UX
- responsabilidades operativas

---

## 6.2 Matriz de transiciones por estado

### Estado actual
No definida en detalle.

### Impacto
Afecta:
- backend
- motor de permisos
- workflow real
- validaciones

---

## 6.3 Casos reales por tipo de comunicación

### Estado actual
Faltan ejemplos concretos validados.

### Impacto
Es clave para:
- revisar formularios
- validar atributos particulares
- validar workflows
- medir si el modelo cubre bien la realidad

---

## 6.4 Modelo futuro de bandeja

### Estado actual
Solo se entiende como lista de usuarios.

### Impacto
Puede influir en:
- asignación automática
- métricas
- ownership inicial
- organización operativa

---

## 6.5 Visibilidad organizacional externa fina

### Estado actual
Está definida en términos generales, pero falta granularidad.

### Impacto
Afecta:
- permisos
- UX
- APIs
- seguridad funcional

---

## 6.6 Estados finales reservados a FREBA

### Estado actual
No completamente definido.

### Impacto
Hay que revisar si ciertos estados finales o administrativos deberían ser solo internos.

---

## 6.7 Profundidad y visualización de árboles de subcomunicaciones

### Estado actual
El modelo admite recursividad, pero no está completamente definido cómo se mostrará ni hasta qué nivel se operará cómodamente.

---

## 6.8 Creación de subcomunicación por externo respondedor

### Estado actual
No está cerrada como regla general en `v0.2`; requiere definición de negocio por escenario y tipo de comunicación.

### Impacto
Afecta la matriz de permisos, la UX y las validaciones de backend sobre continuidad del caso y colaboración externa.

---

## 7. Riesgos principales

## 7.1 Sobreconfiguración temprana

### Riesgo
Intentar parametrizar absolutamente todo desde el inicio puede volver inmanejable el sistema.

### Recomendación
Mantener configurables solo las piezas realmente necesarias en esta etapa.

---

## 7.2 Permisos demasiado complejos

### Riesgo
Mezclar organización, rol, asignación, escenario, visibilidad documental y chats puede generar una matriz demasiado difícil de mantener.

### Recomendación
Separar claramente:
- permisos por rol
- permisos por escenario
- visibilidad de contenido

---

## 7.3 Explosión de tablas por tipo

### Riesgo
La estrategia de tablas particulares por tipo puede volverse caótica si no se gobierna bien.

### Recomendación
Usar ese enfoque con disciplina y solo para tipos que realmente lo justifiquen.

---

## 7.4 Confusión entre colaboración y nueva gestión

### Riesgo
Si no queda clara la diferencia entre sumar usuarios y crear una subcomunicación, la operación puede volverse inconsistente.

### Recomendación
Mantener la regla:
- sumar usuarios = misma comunicación
- abrir gestión nueva = nueva comunicación relacionada

---

## 7.5 Exposición externa mal controlada

### Riesgo
Si no se modela bien qué ve el externo, pueden filtrarse documentos o datos internos.

### Recomendación
Tratar toda visibilidad externa como exposición explícita, no implícita.

---

## 8. Criterios para diseño e implementación

## 8.1 Qué debe respetar cualquier diseño futuro

Todo diseño futuro debe respetar al menos estas bases:

- la comunicación es el centro
- la respuesta formal es única y final
- el expediente es secundario
- la asignación es clave para permisos
- los documentos se versionan
- la visibilidad externa es restringida
- la continuidad post-respuesta va por nueva comunicación relacionada

---

## 8.2 Qué puede cambiar más adelante sin romper el modelo

Podrían cambiar sin invalidar el modelo general:

- diferencia entre editor y responsable
- lógica de bandeja
- detalle de transiciones
- riqueza del expediente
- notificaciones automáticas
- profundidad operativa de subcomunicaciones
- refinamiento de exposición externa

---

## 8.3 Qué no debería cambiar sin revisar el diseño completo

Si cambia alguna de estas cosas, probablemente haya que revisar el diseño de fondo:

- que la entidad central deje de ser comunicación
- que la respuesta formal deje de ser única
- que el expediente pase a ser el objeto principal
- que las subcomunicaciones dejen de ser independientes
- que los externos tengan visibilidad total del trabajo interno

---

## 9. Uso recomendado de este documento

Este archivo debe usarse para:

- alinear agentes de diseño y desarrollo
- revisar si una propuesta respeta lo acordado
- marcar qué es decisión y qué es supuesto
- evitar invenciones de dominio
- detectar cuándo una implementación contradice la base funcional

Debe leerse junto con:

- `00_requerimientos_base_v0_2.md`
- `01_glosario_dominio.md`
- `02_escenarios_y_permisos.md`
- `03_modelo_conceptual.md`
- `05_plan_implementacion.md`

---
