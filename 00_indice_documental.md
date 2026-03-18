# Índice documental

## Sistema de gestión de comunicaciones FREBA

Este directorio contiene la documentación base del proyecto, organizada para servir como fuente de verdad funcional y de diseño durante el análisis, modelado e implementación del sistema.

La intención de esta estructura es:

- mantener alineado el dominio
- evitar contradicciones entre documentos
- facilitar el trabajo con agentes
- permitir una evolución ordenada del diseño hacia la implementación

---

## 1. Documento base vigente

### `00_requerimientos_base_v0_2.md`

Es el documento principal del proyecto en esta etapa.

Contiene:

- contexto y problemática actual
- objetivo general del sistema
- visión conceptual del dominio
- actores
- principios funcionales
- definición de comunicación
- tipos de comunicación
- workflows y estados
- respuesta formal
- subcomunicaciones
- expedientes
- visibilidad externa
- reglas de negocio
- supuestos operativos
- pendientes y riesgos

### Regla de uso
Este archivo debe tomarse como la **fuente principal de verdad funcional vigente**.

---

## 2. Documentos derivados de apoyo

### `01_glosario_dominio.md`
Define los conceptos principales del dominio con lenguaje unificado.

Sirve para:

- evitar ambigüedades
- usar siempre los mismos términos
- alinear análisis, diseño y desarrollo

---

### `02_escenarios_y_permisos.md`
Describe los principales escenarios operativos del sistema y qué puede hacer cada actor en cada caso.

Sirve para:

- aterrizar permisos
- entender visibilidad
- distinguir comportamiento interno y externo
- preparar diseño de backend y frontend

---

### `03_modelo_conceptual.md`
Describe las entidades principales del dominio, sus relaciones y sus responsabilidades funcionales.

Sirve para:

- pasar del análisis funcional al diseño estructural
- preparar el futuro modelo relacional
- alinear arquitectura con dominio

---

### `04_decisiones_y_supuestos.md`
Separa con claridad:

- decisiones firmes
- supuestos operativos
- restricciones
- pendientes
- riesgos

Sirve para:

- evitar que se confundan hipótesis con definiciones cerradas
- controlar el alcance del diseño
- evitar invenciones por parte de agentes o desarrolladores

---

### `05_plan_implementacion.md`
Propone un plan de implementación incremental para Django + Django REST Framework.

Sirve para:

- ordenar el desarrollo
- dividir por fases
- identificar dependencias
- evitar perder contexto del dominio

---

### `06_modelo_relacional_preliminar.md`
Traduce el modelo conceptual a una propuesta relacional inicial para backend.

Sirve para:

- definir tablas y relaciones preliminares
- explicitar cardinalidades y restricciones conceptuales
- alinear modelado de datos con el dominio

---

### `07_matriz_permisos_y_transiciones.md`
Detalla permisos por escenario y criterios de transiciones de estado.

Sirve para:

- volver operables las reglas de acceso
- alinear visibilidad, acciones y chat por actor
- orientar validaciones funcionales de backend

---

## 3. Carpeta `agents`

Contiene agentes especializados para trabajar sobre el proyecto con responsabilidades acotadas.

### `agents/domain-analyst.md`
Agente orientado a:

- revisar consistencia del dominio
- detectar ambigüedades
- bajar reglas de negocio
- cuidar alineación entre documentos

No implementa código salvo pedido explícito.

---

### `agents/implementation-planner.md`
Agente orientado a:

- ordenar el trabajo técnico
- dividir implementación en fases
- identificar dependencias
- mantener una secuencia coherente de construcción

No redefine dominio.

---

## 4. Carpeta `archive`

Contiene versiones anteriores o material histórico que ya no es la referencia principal.

### `archive/levantamiento_inicial_requerimientos_freba_v0_1.md`
Versión anterior del levantamiento inicial.

### Regla de uso
Los archivos de `archive/` sirven como referencia histórica, pero **no deben tomarse como fuente principal vigente** si contradicen a la versión actual.

---

## 5. Orden recomendado de lectura

Para entender el proyecto desde cero, se recomienda este orden:

1. `00_requerimientos_base_v0_2.md`
2. `01_glosario_dominio.md`
3. `02_escenarios_y_permisos.md`
4. `03_modelo_conceptual.md`
5. `04_decisiones_y_supuestos.md`
6. `06_modelo_relacional_preliminar.md`
7. `07_matriz_permisos_y_transiciones.md`
8. `05_plan_implementacion.md`

Si se va a trabajar con agentes, luego continuar con:

9. `agents/domain-analyst.md`
10. `agents/implementation-planner.md`

---

## 6. Reglas de mantenimiento documental

### 6.1 Documento base
Si cambia una definición importante del dominio, primero debe actualizarse:

- `00_requerimientos_base_v0_2.md`

y luego revisar impacto en los demás documentos.

### 6.2 Consistencia
Cuando se actualice un concepto central, conviene revisar al menos:

- glosario
- escenarios y permisos
- modelo conceptual
- decisiones y supuestos
- modelo relacional preliminar
- matriz de permisos y transiciones
- plan de implementación

### 6.3 Supuestos
Todo lo que todavía no esté definido por negocio debe marcarse explícitamente como:

- supuesto operativo
- pendiente
- recomendación
- o alternativa

### 6.4 Archivo histórico
Las versiones viejas no deben borrarse si todavía aportan contexto, pero deben permanecer en `archive/`.

---

## 7. Propósito general de esta estructura

Esta documentación existe para que el proyecto pueda avanzar con:

- claridad conceptual
- coherencia funcional
- menor margen de interpretación errónea
- mejor comunicación entre análisis, diseño e implementación

La meta no es solo documentar, sino usar estos archivos como base real de trabajo para construir la aplicación sin perder el contexto del dominio.

---
