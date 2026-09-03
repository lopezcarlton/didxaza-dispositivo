# RIGHTS_PROVENANCE_AUDIT_v2 — DT-004 checkpoint

**Estado:** `PARTIAL_RIGHTS_AUDIT / THIRD_PARTY_NOTICE_MATERIALIZED / SOURCE_IDENTITIES_ADVANCED / NON_LEGAL_DETERMINATION`  
**Fecha:** 2026-09-03  
**Reemplaza para planificación actual:** `RIGHTS_PROVENANCE_AUDIT_v1.md`  
**Licencia global:** `BLOCKED_PENDING_RIGHTS_AND_DISTRIBUTION_ARCHITECTURE`

## 1. Qué cambió desde v1

DT-004 ya no está en una fase de inventario inicial. Desde v1 se materializó:

- auditor read-only de provenance para SQLite v2.20;
- mapa tabla → source ID → número de filas;
- conteos exactos para campos de provenance de baja cardinalidad;
- `THIRD_PARTY_ATTRIBUTION_v1.md`;
- suplemento no destructivo para source IDs usados por v2.20 pero ausentes de `source_profile`;
- verificación externa de identidad/derechos de `BIB004_GRAMATICA_POPULAR`;
- triangulación de identidad y aviso de copyright de `BIB059_PBK2016`.

No se modificó la SQLite histórica ni se añadió `LICENSE`.

## 2. Dictionaria / BIB054

La fuente externa es *Didxazá–Spanish–English Dictionary*, compilado por Gabriela Pérez Báez, Terrence Kaufman y Christian Brendel, con Rosaura López Cartas, Javier López Cartas, Rosalino Gallegos Luis y Víctor Cata.

Dictionaria declara un aviso `Creative Commons Attribution 4.0 International License` en el sitio. La introducción del diccionario exige conservar una atribución más granular: los registros acreditan a hablantes mediante códigos y también identifican datos procedentes de tres fuentes publicadas, incluido `VP = Velma Pickett / Pickett et al. 2001`.

Por ello:

```text
DICTIONARIA_SITE_LICENSE = CC_BY_4_0_NOTICE_VERIFIED
PER_RECORD_ATTRIBUTION = MUST_BE_PRESERVED
WHOLE_REPOSITORY_LICENSE = NOT_INFERRED
```

El NOTICE concreto está en `THIRD_PARTY_ATTRIBUTION_v1.md`.

La SQLite v2.20 confirma, entre otras:

```text
verb_lexeme_class_v023    2,385 filas BIB054_DICTIONARIA
bound_entry_v024          6,600 filas BIB054_DICTIONARIA
causative_inventory_v025    869 filas BIB054_DICTIONARIA
derivation_inventory_v025 1,064 filas BIB054_DICTIONARIA
surface_attestation_v029 84,188 filas BIB054_DICTIONARIA
```

## 3. Gramática Popular / BIB004

Identidad verificada:

Velma B. Pickett, Cheryl Black y Vicente Marcial Cerqueda. *Gramática popular del zapoteco del Istmo*. Segunda edición electrónica, 2001. Centro de Investigación y Desarrollo Binnizá A.C.; Instituto Lingüístico de Verano A.C.

El registro oficial de SIL confirma título, responsables, edición, fecha y editor. El front matter de la edición electrónica contiene aviso `D.R.` para Centro de Investigación y Desarrollo Binnizá A.C. e Instituto Lingüístico de Verano A.C. No se localizó una licencia abierta aplicable a la obra.

En v2.20:

```text
documentary_alignment_v0210  131 filas BIB004_GRAMATICA_POPULAR
person_possession_exact_v0214 100 filas BIB004_GRAMATICA_POPULAR
```

Estado:

`D_R_RIGHTS_NOTICE_OBSERVED / NO_OPEN_LICENSE_VERIFIED / DISTRIBUTION_REVIEW_REQUIRED`.

## 4. Pérez Báez & Kaufman 2016 / BIB059

La identidad se considera **triangulada**, no inferida sólo desde la sigla.

Fuente:

Gabriela Pérez Báez & Terrence Kaufman. 2016. “Verb Classes in Juchitán Zapotec.” *Anthropological Linguistics* 58(3):217–257. DOI `10.1353/anl.2016.0030`.

Evidencia convergente:

1. SQLite: `source_id = BIB059_PBK2016` en las 11 filas de `morphology_rule_registry_v023`.
2. SQLite snapshot: `PBK2016_REGLAS_MORF_VERB_v0_1.csv`.
3. Runtime v0.2.3: once reglas `PBK-VERB-*`/`PBK-DER-*`, todas con `BIB059_PBK2016` y páginas 4–38.
4. Dictionaria cita Pérez Báez & Kaufman 2016 sobre clasificación verbal de Juchitán.
5. Metadatos externos coinciden en autores, año, tema, volumen, páginas y DOI.

La publicación reporta copyright 2016 de Indiana University Anthropological Linguistics y `All rights reserved`.

Estado:

`IDENTITY_TRIANGULATED / ALL_RIGHTS_RESERVED_NOTICE_OBSERVED / DERIVED_RULE_RELICENSING_REVIEW_REQUIRED`.

Esto no adjudica si los hechos lingüísticos abstractos son protegibles. Sí impide asumir que la expresión del artículo o una derivación textual concreta pueda abrirse automáticamente.

## 5. Pickett Vocabulary / BIB003 y BIB055

Se mantiene la separación:

```text
BIB003_PICKETT_VOCABULARIO = 2,534 registros lexical backfill
BIB055_PICKETT_VOCABULARIO = 16 alineamientos del Apéndice V
```

`BIB003` tiene edición fuente local verificada `2007_FIFTH_ELECTRONIC`. `BIB055` tiene work family y ubicación verificadas, pero la edición exacta y su genealogía respecto de BIB003 permanecen sin resolver.

No fusionar IDs.

## 6. Hueco source_profile: resuelto documentalmente, no en la SQLite

La tabla histórica `source_profile` no contiene BIB003, BIB055 ni BIB059 aunque las tres IDs son utilizadas por otras tablas.

En vez de modificar la SQLite exacta se creó:

`SOURCE_PROFILE_SUPPLEMENT_v1.json`.

Estado:

```text
HISTORICAL_SOURCE_PROFILE_GAP = preserved
NON_DESTRUCTIVE_SUPPLEMENT = present
HISTORICAL_SQLITE_MUTATED = false
```

El suplemento no es autoridad lingüística; es metadato de gobernanza/provenance.

## 7. Estado de la licencia global

Todavía **no** debe añadirse un `LICENSE` global. La causa ya no es desconocimiento general del árbol, sino frentes concretos:

- tratamiento distribuible de los datos Pickett;
- tratamiento de los alineamientos/ejemplos exactos de Gramática Popular;
- tratamiento de la expresión derivada de PBK2016;
- auditoría de SQLite v2.19;
- auditoría de outputs del replay;
- separación de código/documentación original del proyecto frente a expresión migrada o derivada;
- decisión final entre licencias por subárbol, NOTICE, exclusiones de paquete o estrategia mixta.

## 8. Estado operativo de DT-004

```text
INITIAL_RIGHTS_INVENTORY = DONE
V2_20_TABLE_LEVEL_SOURCE_MAP = DONE
DICTIONARIA_NOTICE = MATERIALIZED
BIB004_IDENTITY_AND_RIGHTS_NOTICE = VERIFIED
BIB059_IDENTITY_TRIANGULATED_AND_RIGHTS_NOTICE = VERIFIED
SOURCE_PROFILE_NON_DESTRUCTIVE_SUPPLEMENT = MATERIALIZED
PICKETT_BIB003_BIB055_GENEALOGY = OPEN
V2_19_RIGHTS_AUDIT = OPEN
REPLAY_OUTPUT_RIGHTS_AUDIT = OPEN
PROJECT_AUTHORED_SCOPE_INVENTORY = OPEN
DISTRIBUTION_ARCHITECTURE = OPEN
BLANKET_LICENSE = BLOCKED
```
