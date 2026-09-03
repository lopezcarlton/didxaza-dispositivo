# ESTADO ACTUAL DEL DISPOSITIVO LINGÜÍSTICO

**Proyecto:** Voces de las Nubes  
**Fecha de corte:** 2026-08-31  
**Estado:** snapshot técnico / no canónico

## 1. Función de este documento

Este archivo registra el trabajo desarrollado en paralelo sobre las herramientas lingüísticas internas del proyecto.

No sustituye `METODOLOGIA.md`, `CORPUS.md`, `TEORIA.md`, `PEDAGOGIA.md`, `VALIDACION.md` ni las fuentes lingüísticas del Sistema de Conocimiento.

Su propósito es permitir que el trabajo técnico pueda conservarse, retomarse y auditarse sin convertir sus hipótesis en reglas canónicas.

## 2. Arquitectura general

El dispositivo se organiza alrededor de un núcleo lingüístico compartido consumido por cuatro funciones:

- `ANALYZER_ENGINE`;
- `CORRECTOR_ENGINE`;
- `TUTOR_ENGINE`;
- `GENERATOR_ENGINE`.

El principio arquitectónico es que las cuatro funciones deben consultar las mismas representaciones de evidencia, alcance dialectal, morfología, ortografía y estado de validación.

## 3. Núcleo lingüístico de Juchitán

El trabajo paralelo produjo `JUCHITAN_LINGUISTIC_CORE`, cuya versión de referencia al cierre de esta etapa es **v0.27**.

Estado:

- `EXPERIMENTAL_CORE`;
- orientado específicamente al Didxazá de Juchitán;
- no activa autocorrección por sí mismo;
- reúne reglas y observaciones con procedencia;
- está diseñado para servir a los cuatro componentes.

Entre los dominios ya representados se encuentran:

- orden de constituyentes;
- morfología verbal;
- aspecto;
- persona;
- pronombres dependientes;
- posesión;
- estados y adjetivos;
- negación e interrogación;
- espacio y relaciones semánticas;
- tono, fonación y tipos vocálicos;
- referencia y correferencia;
- discurso narrativo;
- inferencia;
- perspectiva y conocimiento de personajes;
- género y procedencia de evidencia.

La existencia de una regla en el núcleo significa que ha sido registrada para análisis o prueba; no significa automáticamente que sea productiva, normativa o suficientemente validada para generación.

## 4. Analyzer

Objetivo:

> producir análisis estructurados y trazables sin ocultar ambigüedad ni convertir inferencias en hechos.

Capacidades buscadas o trabajadas:

- recuperación de evidencia;
- análisis morfológico;
- reconocimiento de persona y aspecto;
- segmentación y límites;
- análisis múltiple cuando existe ambigüedad;
- persistencia de contexto discursivo;
- referencia entre oraciones;
- clasificación de procedencia y fuerza de evidencia.

Regla vigente:

`NO_ENCONTRADO` significa ausencia de evidencia suficiente recuperada, no error lingüístico.

## 5. Corrector

Objetivo:

> revisar escritura y normalización de manera conservadora, documentada y sensible a variedad.

Principios consolidados en el trabajo paralelo:

- conservar `didxaza_original`;
- crear por separado cualquier `didxaza_normalizado`;
- no inventar formas;
- no tratar una forma de otra comunidad como corrección universal;
- separar ortografía, tono, fonación, morfología y dialectología;
- no añadir tono visible automáticamente sólo porque exista información tonal interna;
- distinguir forma no encontrada de forma incorrecta;
- hacer visible la incertidumbre.

El corrector debe poder abstenerse cuando la evidencia sea insuficiente o exista variación real.

## 6. Tutor

Objetivo:

> explicar el Didxazá mediante capas de evidencia y análisis, no mediante una respuesta opaca.

Una explicación puede distinguir:

- forma;
- segmentación;
- traducción literal;
- traducción natural;
- estructura;
- referencia o antecedente;
- función dentro del discurso;
- inferencias necesarias;
- procedencia;
- nivel de seguridad.

El Tutor depende del mismo núcleo que Analyzer y Corrector. No debe presentar como regla una interpretación que el núcleo conserva sólo como hipótesis.

## 7. Generator

Objetivo:

> ayudar a producir material pedagógico y estímulos de elicitación compatibles con la lógica documentada del Didxazá sin generar una falsa autoridad lingüística.

Principios vigentes:

- el español funciona como puente semántico, no como plantilla estructural;
- situación, función comunicativa y objetivo lingüístico/pedagógico deben distinguirse;
- una estructura española objetivo no equivale a un patrón productivo del Didxazá;
- la forma final en Didxazá requiere hablante y evidencia;
- el generador debe reciclar recursos ya documentados sin forzar repeticiones artificiales;
- naturalidad y cobertura se evalúan longitudinalmente, no sólo dentro de una escena.

El trabajo paralelo ya ha producido un andamiaje conservador de generación, pero **no se considera un generador autónomo confiable de Didxazá**.

## 8. Cambio metodológico de agosto: impacto en el dispositivo

La incorporación de Bueno Holle (2019) obliga a representar de manera más explícita la procedencia de los datos.

El dispositivo deberá poder distinguir, como mínimo:

- `SPONTANEOUS`;
- `ELICITED_NONLINGUISTIC`;
- `SPEAKER_JUDGMENT`;
- `TRANSLATION_REFORMULATION`;
- `DOCUMENTARY`.

También deberá separar:

- superficie ortográfica;
- información fonológica o tonal interna;
- grabación primaria;
- transcripción;
- segmentación;
- traducción;
- análisis prosódico;
- análisis gramatical/pragmático.

Consecuencias por componente:

### Analyzer

Debe interpretar una forma según su procedencia y contexto, y no tratar todas las observaciones como evidencia equivalente.

### Corrector

No debe declarar imposible una construcción únicamente porque sea rara en el corpus espontáneo ni inferir ausencia de tono por ausencia de marca gráfica superficial.

### Tutor

Puede explicar diferencias de organización informativa y discurso cuando la evidencia esté documentada, distinguiendo forma, contexto y análisis.

### Generator

Además de escenas pedagógicamente diseñadas, podrá apoyarse en patrones y estrategias descubiertos mediante habla natural y elicitación no lingüística. Los futuros estímulos deberán poder representar contexto previo, contraste, saliencia o información compartida cuando esos factores sean relevantes.

## 9. Relación con COR001 y COR002

### COR001

No se utiliza como fuente para inventar reglas ni como gold standard del dispositivo.

Puede analizarse para observar qué reconoce el sistema, dónde se abstiene y qué huecos documentales revela.

### COR002

El dispositivo debe servir a COR002 en dos direcciones:

1. recuperar conocimiento que ayude a preparar mejores escenas y estímulos;
2. analizar posteriormente el material producido por hablantes para identificar estructuras, recurrencias, variantes y vacíos.

La generación y el análisis no sustituyen la validación con hablantes.

## 10. Artefactos todavía fuera del repositorio

Al cierre de agosto, parte importante de la implementación permanece fuera de este repositorio en paquetes de trabajo, bases locales, scripts, inventarios y documentos de migración.

Entre ellos se encuentran distintas versiones de:

- bases de datos lingüísticas;
- runtimes de análisis;
- pruebas y benchmarks;
- inventarios de verbos y construcciones;
- tablas de paradigmas;
- colas de validación;
- matrices de preparación para generación;
- paquetes de migración y auditoría.

**No se declara aquí que esos archivos hayan sido migrados.**

La siguiente migración técnica deberá hacerse de manera selectiva, conservando sólo artefactos reproducibles y útiles. Este snapshot permite empezar esa migración sin que la ausencia temporal de los ejecutables vuelva invisible el trabajo realizado.

## 11. Regla de promoción al Sistema de Conocimiento

Un resultado del dispositivo sólo puede convertirse en conocimiento canónico cuando:

1. existe evidencia identificable;
2. se distingue dato de interpretación;
3. se verifica su alcance;
4. se resuelven o registran contradicciones;
5. se valida por la autoridad pertinente cuando sea necesario;
6. se adopta mediante las reglas de actualización del repositorio.

Hasta entonces permanece en esta capa como resultado experimental.

## 12. Próxima etapa

El objetivo inmediato no es ampliar indefinidamente la infraestructura.

La prioridad es utilizar el dispositivo sobre evidencia nueva:

- literatura lingüística adicional;
- corpus oral independiente;
- elicitación no lingüística;
- producciones de hablantes;
- COR002 cuando existan traducciones o grabaciones.

La utilidad del dispositivo se medirá por su capacidad para mejorar análisis, revisión, aprendizaje y producción de corpus sin ocultar incertidumbre ni sustituir autoridad lingüística humana.
