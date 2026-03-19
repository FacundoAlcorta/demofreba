# Matriz de permisos y transiciones

## Sistema de gestión de comunicaciones FREBA

Documento de trabajo para definir, de forma operativa, qué puede ver y hacer cada actor del sistema según:

- su organización
- su asignación a la comunicación
- su rol sobre esa comunicación
- el escenario funcional
- y el estado general del caso

Este documento complementa:

- `00_requerimientos_base_v0_2.md`
- `01_glosario_dominio.md`
- `02_escenarios_y_permisos.md`
- `03_modelo_conceptual.md`
- `04_decisiones_y_supuestos.md`
- `06_modelo_relacional_preliminar.md`

---

## 1. Objetivo del documento

Este archivo busca responder:

- quién puede ver una comunicación
- quién puede editarla
- quién puede cambiar estado
- quién puede responder formalmente
- quién puede cargar documentos
- quién puede usar chats
- quién puede asignar usuarios
- quién puede asociar expedientes
- qué transiciones de estado conviene habilitar por escenario

No define todavía código ni permissions classes concretas, pero sí la lógica funcional que luego debe implementar el backend.

---

## 2. Principios generales de permisos

## 2.1 Los permisos no dependen solo del tipo de usuario

Los permisos dependen de la combinación de:

- organización del usuario
- asignación a la comunicación
- rol sobre la comunicación
- escenario operativo
- estado actual de la comunicación

---

## 2.2 Ver no es lo mismo que operar

Debe distinguirse siempre entre:

- visibilidad
- edición
- participación conversacional
- gestión documental
- cambio de estado
- respuesta formal
- administración de participantes
- administración de expediente

---

## 2.3 La exposición externa es restringida

Los externos nunca deben ver por defecto:

- expediente
- historial interno completo
- asignaciones internas de FREBA
- chat interno
- documentos internos no expuestos

---

## 2.4 Editor y Responsable

En `v0.2`, **Editor** y **Responsable** se consideran equivalentes en permisos y operaciones de implementación.

Mientras negocio no defina diferencias reales, esta matriz los trata igual.

---

## 2.5 Observador

El rol de **Observador** es de seguimiento limitado.  
No debe confundirse con rol operativo pleno.

---

## 3. Escenarios considerados

La matriz se organiza sobre estos escenarios:

### E1. Externo que crea una comunicación y espera respuesta
Usuario externo iniciador.

### E2. Externo que recibe una comunicación de FREBA y debe responder
Usuario externo respondedor.

### I1. Usuario interno FREBA que crea una comunicación
Usuario interno creador.

### I2. Usuario interno FREBA que trabaja activamente sobre una comunicación
Usuario interno operativo.

### I3. Usuario interno FREBA con seguimiento limitado
Usuario interno observador o consulta.

---

## 4. Acciones funcionales relevantes

Para esta matriz, las acciones se agrupan en:

### 4.1 Visibilidad
- ver comunicación
- ver participantes
- ver historial
- ver expediente
- ver relaciones con otras comunicaciones

### 4.2 Edición
- editar datos de comunicación
- cerrar comunicación
- reabrir comunicación

### 4.3 Workflow
- cambiar estado

### 4.4 Respuesta formal
- crear respuesta formal
- ver respuesta formal

### 4.5 Documentos
- ver documentos propios
- ver documentos visibles
- subir documentos
- subir nueva versión
- seleccionar documentos para respuesta

### 4.6 Chat
- usar chat interno
- usar chat compartido

### 4.7 Participantes
- agregar usuarios
- quitar usuarios

### 4.8 Subcomunicaciones
- crear subcomunicación
- ver subcomunicaciones relacionadas

### 4.9 Expedientes
- asociar expediente
- mover de expediente
- ver expediente

---

## 5. Matriz principal de permisos por escenario

## 5.1 E1 — Externo que crea y espera respuesta

| Acción | Permitido | Observaciones |
|---|---|---|
| Ver comunicación | Sí | Puede ver la comunicación que originó o las que incumban a su organización según reglas |
| Ver estado actual | Sí | Siempre visible para seguimiento |
| Ver respuesta formal | Sí | Cuando exista |
| Ver documentos propios | Sí | Los que su organización cargó |
| Ver documentos internos FREBA | No | No se exponen |
| Ver documentos finales de respuesta | Sí | Solo los incluidos en la respuesta |
| Editar comunicación luego del envío | No | No como flujo normal |
| Cambiar estado | No | El tratamiento queda del lado de FREBA |
| Crear respuesta formal | No | No responde esa misma comunicación en este escenario |
| Usar chat compartido | Sí | Mientras la comunicación esté abierta y el tipo/flujo lo permita |
| Usar chat interno | No | Nunca |
| Agregar usuarios | No | No administra participantes en este escenario |
| Quitar usuarios | No | No administra participantes |
| Ver participantes internos FREBA | No | No corresponde |
| Ver historial interno | No | No corresponde |
| Ver expediente | No | Nunca |
| Crear subcomunicación / réplica por continuidad post-respuesta final | Sí | Para continuar el tema luego de respuesta formal final; normalmente con la comunicación ya cerrada o finalizada |

---

## 5.2 E2 — Externo que recibe y debe responder

| Acción | Permitido | Observaciones |
|---|---|---|
| Ver comunicación | Sí | Es destinatario de la gestión |
| Ver estado actual | Sí | Visible |
| Ver respuesta formal | Sí | Si ya fue emitida |
| Ver documentos del envío inicial | Sí | Los expuestos por FREBA al enviarla |
| Ver documentos de su propia organización | Sí | Puede consultar los que cargó su organización |
| Ver documentos internos FREBA no expuestos | No | No corresponde |
| Subir documentos | Sí | Para construir la respuesta |
| Subir nueva versión documental | Sí | Sobre documentos de trabajo que le correspondan |
| Editar datos habilitados | Sí | Según el tipo y el flujo |
| Cambiar estado | Sí | Solo dentro de estados operativos del escenario de respuesta |
| Cerrar comunicación (cierre administrativo final) | No en `v0.2` | Reservado a FREBA |
| Crear respuesta formal | Sí | Cuando le corresponda responder |
| Usar chat compartido | Sí | Canal operativo con FREBA |
| Usar chat interno | No | Nunca |
| Agregar usuarios de su organización | Sí | Solo de su misma organización |
| Quitar usuarios de su organización | Sí | Solo de su misma organización |
| Ver participantes de su propia organización | Sí | Solo participantes de su misma organización |
| Ver participantes internos FREBA | No | No corresponde |
| Ver participantes de otras organizaciones externas | No | No corresponde |
| Agregar usuarios de otra organización | No | Nunca |
| Ver expediente | No | Nunca |
| Ver historial interno completo | No | Nunca |
| Crear subcomunicación | No habilitado en `v0.2` (pendiente de definición de negocio) | No se habilita como regla general en esta versión |
| Ver referencia contextual básica | Sí | Puede ver lo necesario para entender su comunicación, no todo el contexto interno |

---

## 5.3 I1 — Usuario interno FREBA que crea una comunicación

| Acción | Permitido | Observaciones |
|---|---|---|
| Crear comunicación | Sí | Según tipo habilitado |
| Definir organización destino | Sí | Cuando corresponda |
| Seleccionar usuarios destino | Sí | Especialmente en salientes a externos |
| Adjuntar documentos iniciales | Sí | Sí |
| Editar antes/después de envío mientras esté abierta | Sí | Según reglas de la comunicación |
| Ver historial completo | Sí | Interno |
| Usar chat interno | Sí | Sí |
| Usar chat compartido | Sí | Si el escenario lo requiere |
| Agregar usuarios | Sí | Según rol operativo |
| Asociar expediente | Sí | Si tiene rol editor/responsable sobre la comunicación |
| Crear subcomunicación | Sí | Como usuario interno operativo con asignación activa |
| Emitir respuesta formal | Sí | Si su rol operativo y el workflow lo habilitan |

---

## 5.4 I2 — Usuario interno FREBA operativo

| Acción | Permitido | Observaciones |
|---|---|---|
| Ver comunicación | Sí | Completa |
| Ver historial completo | Sí | Completo |
| Ver participantes | Sí | Completo |
| Ver documentos y versiones | Sí | Completo |
| Ver expediente | Sí | Si la comunicación está asociada |
| Editar datos de comunicación abierta | Sí | Sí |
| Cambiar estado | Sí | Según transición válida |
| Cerrar comunicación | Sí | Según flujo |
| Reabrir comunicación sin respuesta final | Sí | Permitido |
| Reabrir comunicación con respuesta final | No, como flujo normal | Se recomienda nueva hija |
| Crear respuesta formal | Sí | Sí |
| Usar chat interno | Sí | Sí |
| Usar chat compartido | Sí | Si el escenario lo requiere |
| Subir documentos | Sí | Sí |
| Versionar documentos | Sí | Sí |
| Agregar usuarios | Sí | Sí |
| Quitar usuarios | Sí | Sí |
| Crear subcomunicación | Sí | Sí |
| Asociar expediente | Sí | Sí |
| Cambiar de expediente | Sí | Sí |

---

## 5.5 I3 — Usuario interno FREBA con seguimiento limitado

| Acción | Permitido | Observaciones |
|---|---|---|
| Ver comunicación | Sí | Según asignación/rol |
| Ver estado | Sí | Sí |
| Ver historial | Sí | Si es interno con acceso a la comunicación |
| Ver documentos | Sí | Sí |
| Ver expediente | Sí | Si tiene acceso a la comunicación |
| Editar | No | El escenario I3 es de seguimiento limitado |
| Cambiar estado | No | El escenario I3 es de seguimiento limitado |
| Crear respuesta formal | No | Si no tiene rol operativo |
| Usar chat interno | No | El escenario I3 no opera chat interno |
| Usar chat compartido | No | El escenario I3 no opera chat compartido |
| Agregar usuarios | No | El escenario I3 no administra participantes |
| Crear subcomunicación | No | El escenario I3 no abre nuevas gestiones |

---

## 6. Matriz resumida por rol sobre comunicación

## 6.1 Observador

| Acción | Permitido | Observaciones |
|---|---|---|
| Ver comunicación | Sí | Según escenario y visibilidad |
| Ver estado | Sí | Sí |
| Ver respuesta formal | Sí | Si existe |
| Editar comunicación | No | No |
| Cambiar estado | No | No |
| Crear respuesta formal | No | No |
| Subir documentos | No | No como regla general |
| Versionar documentos | No | No |
| Agregar usuarios | No | No |
| Quitar usuarios | No | No |
| Usar chat interno | No | Nunca |
| Usar chat compartido | No en `v0.2` | El rol observador no opera intercambio compartido |
| Ver expediente | Sí para internos con acceso / No para externos | Regla fija por tipo de actor |

---

## 6.2 Editor

| Acción | Permitido | Observaciones |
|---|---|---|
| Ver comunicación | Sí | Sí |
| Editar comunicación abierta | Sí | Sí |
| Cambiar estado | Sí | Según transición permitida |
| Crear respuesta formal | Sí | Sí |
| Subir documentos | Sí | Sí |
| Versionar documentos | Sí | Sí |
| Agregar usuarios | Sí | Con restricciones por organización si es externo |
| Quitar usuarios | Sí | Con restricciones por organización si es externo |
| Usar chat interno | Sí para internos | No para externos |
| Usar chat compartido | Sí | Si el escenario lo requiere |
| Asociar expediente | Sí para internos | No para externos |
| Crear subcomunicación | Sí para internos / No habilitado en `v0.2` para externos en E2 | Para externo respondedor queda pendiente de definición de negocio para una versión futura |

---

## 6.3 Responsable

En `v0.2`, tiene el mismo alcance que Editor, incluyendo implementación operativa.

La separación conceptual se mantiene para permitir evolución futura, pero no cambia esta matriz.

---

## 7. Reglas de visibilidad

## 7.1 Visibilidad externa mínima

Un externo nunca ve:

- expediente
- historial interno detallado
- chat interno
- asignaciones internas completas de FREBA
- participantes de otras organizaciones externas
- documentos internos no expuestos

---

## 7.2 Visibilidad externa permitida

Un externo puede ver, según escenario:

- datos generales de la comunicación
- estado actual
- participantes de su propia organización
- documentos que cargó su organización
- documentos del envío inicial visibles para él
- respuesta formal
- documentos incluidos en la respuesta
- chat compartido, cuando corresponda

---

## 7.3 Visibilidad interna FREBA

Un usuario interno con acceso operativo puede ver:

- comunicación completa
- historial completo
- documentos y versiones
- asignaciones
- expediente
- subcomunicaciones
- chat interno
- chat compartido

---

## 8. Reglas de chat

## 8.1 Chat interno

| Actor | Acceso |
|---|---|
| Interno FREBA operativo | Sí |
| Interno FREBA seguimiento | No |
| Externo iniciador | No |
| Externo respondedor | No |

### Regla
El chat interno es exclusivamente de FREBA.

---

## 8.2 Chat compartido

| Actor | Acceso |
|---|---|
| Interno FREBA operativo | Sí |
| Externo iniciador | Sí, cuando el flujo lo permita |
| Externo respondedor | Sí |
| Observador puro sin participación compartida | No en `v0.2` |

### Regla
El chat compartido existe para intercambio operativo entre FREBA y la contraparte externa.

---

## 9. Reglas documentales

## 9.1 Visibilidad documental por actor

| Tipo de documento | Interno FREBA | Externo iniciador | Externo respondedor |
|---|---|---|---|
| Documento cargado por su propia organización | Sí | Sí | Sí |
| Documento del envío inicial expuesto al externo | Sí | Sí, si FREBA lo expuso | Sí, si FREBA lo expuso |
| Documento interno de trabajo FREBA | Sí | No | No |
| Documento cargado por otra organización externa | Sí | No | No |
| Documento incluido en respuesta formal | Sí | Sí | Sí |

### Regla operativa de visibilidad documental externa (`v0.2`)

- el externo ve documentos cargados por su propia organización
- ve adjuntos expuestos en el envío inicial
- ve documentos incluidos en la respuesta formal
- no ve documentos internos de trabajo de FREBA
- cualquier ayuda técnica de implementación (por ejemplo flags de exposición) no reemplaza esta regla funcional

---

## 9.2 Acciones documentales por actor

| Acción | Interno FREBA operativo | Externo iniciador | Externo respondedor |
|---|---|---|---|
| Subir documento | Sí | Solo al crear | Sí |
| Versionar documento | Sí | No | Sí |
| Ver historial completo de versiones | Sí | No | No en `v0.2` |
| Seleccionar documento para respuesta | Sí | No | Sí, si le toca responder |

---

## 10. Reglas de participantes

## 10.1 Alta de participantes

| Actor | Puede agregar usuarios | Restricción |
|---|---|---|
| Interno FREBA operativo | Sí | Según rol operativo |
| Externo iniciador | No | No administra participantes |
| Externo respondedor | Sí | Solo usuarios de su misma organización |

---

## 10.2 Baja de participantes

| Actor | Puede quitar usuarios | Restricción |
|---|---|---|
| Interno FREBA operativo | Sí | Sí |
| Externo iniciador | No | No |
| Externo respondedor | Sí | Solo dentro de su organización y según flujo |

---

## 11. Reglas de respuesta formal

## 11.1 Quién puede crearla

| Escenario | Actor habilitado |
|---|---|
| Externo crea y espera respuesta | FREBA |
| FREBA crea y espera respuesta | Externo destinatario |
| Comunicación interna gestionada por FREBA | FREBA, si el flujo lo requiere |

---

## 11.2 Restricciones

- solo una respuesta formal por comunicación
- una vez emitida, no se edita
- una vez emitida, no se anula
- la respuesta no reemplaza al chat
- la respuesta no es una subcomunicación

---

## 12. Reglas de subcomunicaciones

## 12.1 Quién puede crearlas

| Actor | Permitido | Observaciones |
|---|---|---|
| Interno FREBA operativo | Sí | Sí |
| Externo iniciador | Sí, como réplica posterior | Por continuidad luego de respuesta formal final; normalmente sobre comunicación ya cerrada o finalizada y propia |
| Externo respondedor | No habilitado en `v0.2` (pendiente de definición de negocio) | No se habilita como regla general en esta versión |

---

## 12.2 Criterio de uso

Se crea subcomunicación cuando:

- hace falta abrir una gestión formal separada
- hay otro destinatario o subcaso
- no alcanza con sumar usuarios a la misma comunicación

No se crea subcomunicación cuando:

- solo hace falta sumar colaboración sobre la misma comunicación

---

## 13. Reglas de expediente

## 13.1 Visibilidad

| Actor | Ver expediente |
|---|---|
| Interno FREBA con acceso | Sí |
| Externo | No |

---

## 13.2 Asociación

| Actor | Asociar / mover expediente |
|---|---|
| Interno FREBA editor/responsable | Sí |
| Externo | No |

---

## 14. Categorías funcionales de estados

Dado que los nombres definitivos de estados pueden variar según tipo, se adopta esta clasificación funcional preliminar:

- **Inicial**
- **En análisis**
- **En trabajo**
- **Pendiente de respuesta**
- **Respondida**
- **Cerrada**

Esto no reemplaza el workflow real por tipo, pero ayuda a pensar transiciones.

---

## 15. Matriz preliminar de transiciones por escenario

## 15.1 Transiciones sugeridas — Externo iniciador (E1)

| Desde | Hacia | Permitido | Observaciones |
|---|---|---|---|
| Inicial / En análisis / En trabajo | Consulta de estado | Sí | Solo lectura, no transición |
| Cualquiera | Nueva réplica / hija | Sí, tras respuesta formal final | No modifica la original; operativamente suele darse con comunicación cerrada o finalizada |

### Regla
El externo iniciador no opera el workflow principal de tratamiento.

---

## 15.2 Transiciones sugeridas — Externo respondedor (E2)

| Desde | Hacia | Permitido | Observaciones |
|---|---|---|---|
| Inicial | En trabajo | Sí | Si le toca preparar respuesta |
| En trabajo | Pendiente de respuesta | Sí, cuando el estado exista en el workflow del tipo | Si el workflow no incluye ese estado, esta transición no aplica |
| En trabajo / Pendiente de respuesta | Respondida | Sí | Cuando emite respuesta |
| Respondida | Cerrada | No para E2 en `v0.2` | Cierre administrativo reservado a FREBA |

### Regla operativa `v0.2`
En escenario E2, el externo puede llevar la comunicación a estado “Respondida”, pero el cierre administrativo final queda del lado de FREBA.

---

## 15.3 Transiciones sugeridas — Interno FREBA operativo (I2)

| Desde | Hacia | Permitido | Observaciones |
|---|---|---|---|
| Inicial | En análisis | Sí | Sí |
| En análisis | En trabajo | Sí | Sí |
| En trabajo | Pendiente de respuesta | Sí | Sí |
| Pendiente de respuesta | Respondida | Sí | Si emite respuesta |
| Respondida | Cerrada | Sí | Sí |
| Cerrada | Reabierta / En análisis | Sí, solo sin respuesta final | Si no hay respuesta formal emitida |

---

## 16. Reglas de reapertura

## 16.1 Sin respuesta formal emitida
Una comunicación cerrada puede reabrirse por un usuario con rol operativo habilitado.

## 16.2 Con respuesta formal emitida
No se recomienda reabrirla como flujo normal.

### Regla operativa
Si el tema continúa luego de respuesta final:

- no se sigue trabajando sobre la misma comunicación
- se crea una nueva comunicación relacionada

---

## 17. Pendientes a refinar más adelante

### 17.1 Diferencia real entre Editor y Responsable
En `v0.2`, la matriz los trata igual por decisión de implementación.

### 17.2 Transiciones exactas por tipo de comunicación
Esta matriz propone criterios generales, no workflows definitivos por tipo.

### 17.3 Alcance fino del Observador
Puede requerir más precisión cuando existan casos reales.

### 17.4 Permisos exactos de usuarios agregados por externos
En `v0.2` queda acotado, pero podría requerir mayor detalle.

### 17.5 Estados administrativos reservados a FREBA
Conviene validarlo cuando se definan tipos reales.

---

## 18. Recomendaciones para backend

Esta matriz debe transformarse luego en:

- servicios de autorización
- permission classes por endpoint
- validadores de transición de estado
- filtros de visibilidad documental
- filtros de visibilidad de chat
- validaciones por escenario

No conviene implementar estas reglas repartidas de forma arbitraria en serializers y views sin una capa central clara.

---

## 19. Uso recomendado de este documento

Este archivo debe usarse para:

- diseñar permisos de backend
- revisar que la UX respete restricciones reales
- controlar exposición externa
- validar transiciones de estado
- alinear chats, documentos, respuesta y asignaciones

Debe leerse junto con:

- `00_requerimientos_base_v0_2.md`
- `02_escenarios_y_permisos.md`
- `03_modelo_conceptual.md`
- `04_decisiones_y_supuestos.md`
- `06_modelo_relacional_preliminar.md`

---
