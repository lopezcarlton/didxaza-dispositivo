# RIGHTS_PROVENANCE_AUDIT_v1 — DT-004

**Estado:** `PARTIAL_RIGHTS_AUDIT / TABLE_LEVEL_SQLITE_PROVENANCE_PARTIALLY_VERIFIED / TECHNICAL_GOVERNANCE / NON_LEGAL_DETERMINATION`  
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
SOURCE_ID_SIMILARITY != SOURCE_ID_IDENTITY
TABLE_PROVENANCE != COPYRIGHT_SCOPE_DETERMINATION
```

Artefactos asociados:

- `RIGHTS_PROVENANCE_INVENTORY_v1.json`;
- `SQLITE_RIGHTS_SOURCE_MAP_v1.json`;
- `audit_runtime_rights_sources.py`;
- workflow `rights-provenance-audit`.

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

La auditoría read-only de la SQLite v2.20 verifica además el uso explícito de:

`source_id = BIB054_DICTIONARIA`.

Conteos exactos materializados:

```text
verb_lexeme_class_v023   = 2,385 / 2,385 filas BIB054_DICTIONARIA
bound_entry_v024         = 6,600 / 6,600 filas BIB054_DICTIONARIA
causative_inventory_v025 =   869 /   869 filas BIB054_DICTIONARIA
derivation_inventory_v025= 1,064 / 1,064 filas BIB054_DICTIONARIA
surface_attestation_v029 =84,188 /84,188 filas BIB054_DICTIONARIA
```

`surface_attestation_v029` se divide por provenance estructural en:

```text
EXAMPLE_NGRAM = 75,176
HEADWORD      =  9,012
```

**Estado provisional:** `OPEN_LICENSE_NOTICE_VERIFIED_CC_BY_4_0 / LOCAL_ATTRIBUTION_CHAIN_REQUIRED`.

El próximo paso no es “aplicar CC BY 4.0 al repositorio”. Es materializar atribución suficiente para los exports locales y documentar las transformaciones que producen tablas derivadas.

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

Fuentes públicas verificadas:

- `https://mexico.sil.org/resources/archives/35335`
- `https://www.lulu.com/shop/velma-pickett/vocabulario-zapoteco-del-istmo/paperback/product-21584671.html`

La ficha de SIL identifica la quinta edición electrónica, a Velma Pickett como compiladora y al Instituto Lingüístico de Verano como editor, y ofrece el PDF; en esa ficha no aparece una licencia abierta específica para la obra. La página editorial actual de Lulu para el título muestra `All Rights Reserved - Standard Copyright License`.

### 4.1 BIB003_PICKETT_VOCABULARIO

El archivo local:

`runtime/v0_2_15_3/PICKETT_LEXICON_BACKFILL_v0_1.csv`

preserva 2,534 registros estructurados. Entre sus campos están `headword_raw_2007`, `gloss_es`, `entry_line_raw_2007`, páginas, edición extraída y reconciliación hacia la edición objetivo.

La SQLite confirma:

```text
pickett_lexical_record_v0211 = 2,534 filas
source_id                    = BIB003_PICKETT_VOCABULARIO
source_edition_extracted     = 2007_FIFTH_ELECTRONIC
```

Además:

```text
cross_source_exact_surface_v0212 = 1,118 filas
source_ids_json = [BIB003_PICKETT_VOCABULARIO, BIB054_DICTIONARIA]
```

### 4.2 BIB055_PICKETT_VOCABULARIO

`DOCUMENTARY_ALIGNMENT_REGISTRY_v0_2_15_2.csv` usa una segunda ID para frases del Apéndice V. La auditoría SQLite confirma:

```text
documentary_alignment_v0210 = 147 filas totales
BIB004_GRAMATICA_POPULAR    = 131
BIB055_PICKETT_VOCABULARIO  = 16
BIB055 source_location      = Apéndice V, pp.123–124+
```

No se ha demostrado que `BIB003_PICKETT_VOCABULARIO` y `BIB055_PICKETT_VOCABULARIO` sean identificadores intercambiables. Pueden corresponder a dos registros bibliográficos, dos funciones de ingestion, dos ediciones o una duplicación histórica. La similitud del nombre no autoriza fusionarlos.

```text
BIB003 != BIB055 until genealogy is verified
```

**Estado provisional de la familia Pickett:** `NO_OPEN_LICENSE_VERIFIED / HIGH_PRIORITY_RIGHTS_REVIEW_REQUIRED`.

Esto no prueba que ningún uso del dataset local sea ilegal ni decide excepciones aplicables. Sí impide asumir que la disponibilidad pública del PDF autoriza relicenciar el backfill o las frases documentales bajo una licencia abierta global.

Antes de una distribución abierta del repositorio como paquete licenciado deben resolverse al menos una de estas rutas:

- localizar términos o permiso aplicables a la edición concreta utilizada;
- obtener permiso adecuado;
- definir una estrategia de exclusión/distribución separada para el dataset;
- sustituirlo por una fuente con términos compatibles, preservando genealogía y reproducibilidad histórica por un mecanismo apropiado.

No eliminar ni modificar archivos históricos sólo para simplificar el problema de licencia.

## 5. SQLite v2.20 — provenance de tabla verificado

La SQLite auditada es exactamente:

```text
BASE_CORRECTOR_DIDXAZA_SURFACE_SEMANTICS_v2_20.sqlite
SHA256 = 2379773426baf4e3eace87c61ec17f7a1e1b9164421e56cf736d35eb64a5ebed
integrity_check = ok
tables = 85
```

La auditoría se ejecuta mediante `audit_runtime_rights_sources.py` en `mode=ro`. El selector sólo considera tokens completos de nombres de columnas de provenance (`source`, `provenance`, `attribution`, `origin`, `license`) y excluye tokens de contenido como `text`, `raw`, `surface`, `gloss`, `definition`, `example`, `translation`, `payload` y `original`.

Durante el desarrollo del auditor se detectó y corrigió un falso positivo: la primera versión buscaba `origin` como subcadena y podía confundir `didxaza_original` con provenance. Esa salida no se usa como evidencia. La versión vigente usa `WHOLE_IDENTIFIER_TOKEN_MATCH` y emite `content_fields_emitted = false`.

Evidencia vigente:

```text
workflow = rights-provenance-audit
run_id   = 33818497839
head_sha = 8080eeff8a062db392f3237db8a99cd52abaa7dd
status   = success
```

El mapa compacto derivado está en:

`SQLITE_RIGHTS_SOURCE_MAP_v1.json`.

Además de Dictionaria y Pickett, quedaron identificados:

```text
person_possession_exact_v0214 = 100 filas BIB004_GRAMATICA_POPULAR
morphology_rule_registry_v023 =  11 filas BIB059_PBK2016
```

Esto reduce el estado de la SQLite desde “origen mixto sin mapear” a:

`TABLE_LEVEL_PROVENANCE_PARTIALLY_MAPPED / FIELD_AND_OUTPUT_REVIEW_STILL_REQUIRED`.

No permite aún decidir una licencia del binario completo.

## 6. Hueco verificado en `source_profile`

La tabla `source_profile` contiene seis IDs:

```text
BIB004_GRAMATICA_POPULAR
BIB015_ALFABETO_POPULAR_1956
BIB054_DICTIONARIA
BIB056_CUADERNO_2015
BIB063_CARDONA
BIB084_DEANDA2022
```

Sin embargo otras tablas usan de forma verificable:

```text
BIB003_PICKETT_VOCABULARIO
BIB055_PICKETT_VOCABULARIO
BIB059_PBK2016
```

sin que esas tres IDs tengan fila en `source_profile`.

**Estado:** `PROVENANCE_PROFILE_COVERAGE_GAP`.

Esto no autoriza añadir filas directamente a la SQLite histórica. La SQLite v2.20 se mantiene byte-exacta. Si se decide cubrir ese hueco, debe hacerse en una capa derivada nueva, un registry externo o una futura versión explícita, no mutando el release histórico.

## 7. Otras fuentes cuyo estado de derechos todavía falta verificar

La auditoría de tabla hace visibles frentes que DT-004 aún no ha investigado externamente:

- `BIB004_GRAMATICA_POPULAR` — 131 filas en `documentary_alignment_v0210` y 100 en `person_possession_exact_v0214`;
- `BIB059_PBK2016` — 11 reglas en `morphology_rule_registry_v023`;
- fuentes nombradas dentro de `bound_rule_registry_v024`, incluyendo GP, Xneza, Cuaderno y combinaciones de ellas.

Su presencia en la SQLite no equivale a un estado jurídico conocido.

## 8. Código y documentación del proyecto

El repositorio contiene mucho código y documentación técnica aparentemente producidos dentro del proyecto, pero también migraciones históricas, informes, matrices y documentos que pueden incorporar expresión derivada de fuentes externas.

**Estado provisional:** `AUTHORSHIP_INVENTORY_INCOMPLETE`.

No es necesario bloquear desarrollo interno por esto. Sí conviene evitar una declaración tipo “todo el repositorio es MIT/Apache/CC…” antes de separar:

1. código original del proyecto;
2. documentación/metadatos originales;
3. datos con licencia externa abierta y requisitos de atribución;
4. datos con derechos todavía no resueltos;
5. artefactos mixtos derivados.

## 9. Gate para una licencia futura

No crear un `LICENSE` global hasta que existan respuestas trazables para:

```text
DICTIONARIA_ATTRIBUTION_CHAIN = resolved
PICKETT_BIB003_DISTRIBUTION_STATUS = resolved_or_separated
PICKETT_BIB055_GENEALOGY_AND_DISTRIBUTION_STATUS = resolved_or_separated
BIB004_RIGHTS_STATUS = verified
BIB059_RIGHTS_STATUS = verified
MIXED_SQLITE_RIGHTS_MAP = sufficiently_resolved_or_separated
PROJECT_AUTHORED_SCOPE = inventoried
THIRD_PARTY_NOTICES = materialized_where_required
```

La salida final puede ser una licencia global, licencias por subárbol/archivo, archivos `NOTICE`, exclusiones de distribución o una estrategia mixta. El inventario no prejuzga cuál será la correcta.

## 10. Próxima pasada DT-004

Prioridad técnica siguiente:

1. materializar atribución concreta de Dictionaria;
2. resolver genealogía `BIB003` vs `BIB055` sin colapsar IDs por inferencia;
3. verificar derechos externos de `BIB004_GRAMATICA_POPULAR` y `BIB059_PBK2016`;
4. decidir una representación no destructiva para el hueco de `source_profile`;
5. auditar por separado SQLite v2.19 y outputs de replay;
6. separar scope de código/documentación puramente del proyecto;
7. sólo entonces proponer una arquitectura de licencias.
