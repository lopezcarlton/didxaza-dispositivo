# RIGHTS_PROVENANCE_AUDIT_v1 — primera pasada DT-004

**Estado:** `PARTIAL_RIGHTS_AUDIT / TECHNICAL_GOVERNANCE / NON_LEGAL_DETERMINATION`  
**Fecha de verificación:** 2026-09-03  
**Decisión vigente:** `BLANKET_LICENSE_STATUS = BLOCKED_PENDING_RIGHTS_AUDIT`

## 1. Propósito

Esta auditoría existe para evitar que la ausencia de `LICENSE` se resuelva asignando una licencia uniforme a un árbol que mezcla código del proyecto, artefactos históricos, datos derivados y materiales con términos externos distintos.

No determina por sí sola qué usos permite la ley ni sustituye asesoría jurídica. Registra evidencia técnica y documental suficiente para no confundir:

```text
PUBLICLY_AVAILABLE != OPEN_LICENSED
SOURCE_LICENSE != AUTOMATIC_LICENSE_FOR_EVERY_LOCAL_DERIVATIVE
TECHNICAL_REPRODUCIBILITY != REDISTRIBUTION_PERMISSION
UNKNOWN_RIGHTS != PROVEN_PERMISSION
UNKNOWN_RIGHTS != PROVEN_PROHIBITION
```

El inventario machine-readable asociado es `RIGHTS_PROVENANCE_INVENTORY_v1.json`.

## 2. Dictionaria — Didxazá–Spanish–English Dictionary

Fuente pública verificada:

`https://dictionaria.clld.org/contributions/didxazageneral`

Las páginas de la contribución y de entradas individuales muestran el aviso:

`Creative Commons Attribution 4.0 International License`.

Artefactos locales de alta relación con esa fuente:

- `runtime/v0_2_15_3/DICTIONARIA_entries_v0_2_15_2.csv`;
- `runtime/v0_2_15_3/DICTIONARIA_senses_v0_2_15_2.csv`;
- `runtime/v0_2_15_3/DICTIONARIA_examples_v0_2_15_2.csv`;
- `analyzer/DIC_VERB_2385_v0_1.csv`.

Los tres CSV `DICTIONARIA_*` son inputs exactos preservados por el release. `DIC_VERB_2385_v0_1.csv` contiene 2,385 verbos y campos que corresponden al contenido léxico/morfológico del diccionario general.

**Estado provisional:** `OPEN_LICENSE_NOTICE_VERIFIED_CC_BY_4_0 / LOCAL_ATTRIBUTION_CHAIN_REQUIRED`.

Antes de declarar estos archivos cubiertos correctamente por una licencia local hay que registrar de manera explícita la atribución, la fuente/export exacto y, para derivados, qué transformaciones se aplicaron.

## 3. Bueno Holle 2019

Fuente:

Juan José Bueno Holle, *Information structure in Isthmus Zapotec narrative and conversation*, Language Science Press, 2019.

Fuente pública verificada:

`https://langsci-press.org/catalog/book/219`

La editorial declara `Creative Commons Attribution 4.0 International License`. Esto coincide con el provenance ya preservado internamente en:

`migracion/fuentes/BH2019_SOURCE_PROVENANCE_v0_36_1.json`

que contiene:

```text
license_reported_in_source = CC BY 4.0
source_id = BH2019_BOOK
```

Artefactos locales asociados incluyen la matriz BIB065, el provenance y el reading state.

**Estado provisional:** `SOURCE_LICENSE_VERIFIED_CC_BY_4_0 / LOCAL_DERIVATIVE_AUTHORSHIP_SEPARATION_REQUIRED`.

La licencia de la obra fuente no significa que cada fila o comentario añadido por el proyecto tenga automáticamente el mismo origen autoral. Para una licencia limpia conviene separar metadatos/análisis del proyecto de expresión copiada o adaptada de la fuente y conservar atribución suficiente.

## 4. Pickett — Vocabulario zapoteco del Istmo

Fuente interna identificada en el dataset:

`source_id = BIB003_PICKETT_VOCABULARIO`

El archivo local:

`runtime/v0_2_15_3/PICKETT_LEXICON_BACKFILL_v0_1.csv`

preserva 2,534 registros estructurados. Entre sus campos están `headword_raw_2007`, `gloss_es`, `entry_line_raw_2007`, páginas, edición extraída y reconciliación hacia la edición objetivo.

Fuentes públicas verificadas:

- `https://mexico.sil.org/resources/archives/35335`
- `https://www.lulu.com/shop/velma-pickett/vocabulario-zapoteco-del-istmo/paperback/product-21584671.html`

La ficha de SIL identifica la quinta edición electrónica, a Velma Pickett como compiladora y al Instituto Lingüístico de Verano como editor, y ofrece el PDF; en esa ficha no aparece una licencia abierta específica para la obra. La página editorial actual de Lulu para el título muestra `All Rights Reserved - Standard Copyright License`.

**Estado provisional:** `NO_OPEN_LICENSE_VERIFIED / HIGH_PRIORITY_RIGHTS_REVIEW_REQUIRED`.

Esto no prueba que ningún uso del dataset local sea ilegal ni decide excepciones aplicables. Sí impide asumir que la disponibilidad pública del PDF autoriza relicenciar el backfill bajo una licencia abierta global.

Antes de una distribución abierta del repositorio como paquete licenciado deben resolverse al menos una de estas rutas:

- localizar términos o permiso aplicables a la edición concreta utilizada;
- obtener permiso adecuado;
- definir una estrategia de exclusión/distribución separada para el dataset;
- sustituirlo por una fuente con términos compatibles, preservando genealogía y reproducibilidad histórica por un mecanismo apropiado.

No eliminar ni modificar el archivo histórico sólo para simplificar el problema de licencia.

## 5. SQLite y outputs de origen mixto

Las SQLite v2.19/v2.20 y varios outputs del runtime combinan estado técnico del proyecto con capas derivadas de distintas fuentes.

**Estado provisional:** `MIXED_ORIGIN / TABLE_FIELD_AND_OUTPUT_COMPOSITION_AUDIT_REQUIRED`.

Antes de decidir una licencia para esos binarios hay que mapear, como mínimo:

- tablas/campos que reproducen datos de Dictionaria;
- tablas/campos que incorporan Pickett u otras fuentes documentales;
- contenido puramente estructural o generado por el proyecto;
- outputs que puedan reproducir texto, glosas o ejemplos procedentes de una fuente externa.

La identidad byte-exacta y la reproducibilidad del replay deben conservarse durante esta auditoría; no son evidencia de derechos.

## 6. Código y documentación del proyecto

El repositorio contiene mucho código y documentación técnica aparentemente producidos dentro del proyecto, pero también migraciones históricas, informes, matrices y documentos que pueden incorporar expresión derivada de fuentes externas.

**Estado provisional:** `AUTHORSHIP_INVENTORY_INCOMPLETE`.

No es necesario bloquear desarrollo interno por esto. Sí conviene evitar una declaración tipo “todo el repositorio es MIT/Apache/CC…” antes de separar:

1. código original del proyecto;
2. documentación/metadatos originales;
3. datos con licencia externa abierta y requisitos de atribución;
4. datos con derechos todavía no resueltos;
5. artefactos mixtos derivados.

## 7. Gate para una licencia futura

No crear un `LICENSE` global hasta que existan respuestas trazables para:

```text
DICTIONARIA_ATTRIBUTION_CHAIN = resolved
PICKETT_DISTRIBUTION_STATUS = resolved_or_separated
MIXED_SQLITE_RIGHTS_MAP = resolved_or_separated
PROJECT_AUTHORED_SCOPE = inventoried
THIRD_PARTY_NOTICES = materialized_where_required
```

La salida final puede ser una licencia global, licencias por subárbol/archivo, archivos `NOTICE`, exclusiones de distribución o una estrategia mixta. El inventario no prejuzga cuál será la correcta.

## 8. Próxima pasada DT-004

Prioridad técnica siguiente:

1. mapear Dictionaria a atribución concreta;
2. profundizar Pickett por edición/permiso;
3. inventariar tablas/campos de las SQLite de origen mixto;
4. separar scope de código/documentación puramente del proyecto;
5. sólo entonces proponer una arquitectura de licencias.
