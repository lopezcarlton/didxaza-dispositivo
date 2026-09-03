# THIRD_PARTY_ATTRIBUTION_v1 — atribución y cautelas de redistribución

**Estado:** `PARTIAL_THIRD_PARTY_NOTICE / TECHNICAL_GOVERNANCE / NON_LEGAL_DETERMINATION`  
**Fecha:** 2026-09-03  
**Alcance:** fuentes externas ya identificadas dentro del estado técnico materializado

Este archivo no es una licencia del repositorio. Registra atribuciones y avisos que deben conservarse mientras se decide una arquitectura de licenciamiento compatible con el origen mixto de los artefactos.

```text
THIRD_PARTY_NOTICE != REPOSITORY_LICENSE
PUBLIC_ACCESS != OPEN_LICENSE
SOURCE_LICENSE != WHOLE_REPOSITORY_LICENSE
PER_RECORD_ATTRIBUTION != OPTIONAL_METADATA
```

## 1. Dictionaria — Didxazá–Spanish–English Dictionary

**Fuente:** *Didxazá–Spanish–English Dictionary*  
**Compilers:** Gabriela Pérez Báez, Terrence Kaufman, Christian Brendel  
**With:** Rosaura López Cartas, Javier López Cartas, Rosalino Gallegos Luis, Víctor Cata  
**Sitio:** `https://dictionaria.clld.org/contributions/didxazageneral`

El sitio Dictionaria declara en su pie de página que Dictionaria, editado por Martin Haspelmath y Barbara Stiebels, está bajo `Creative Commons Attribution 4.0 International License`.

La atribución no debe reducirse a una sola cita bibliográfica. La introducción del diccionario explica que incorpora conocimiento aportado por más de veinte hablantes y que usa códigos para acreditarlos. También declara tres fuentes publicadas digitalizadas con atribución correspondiente:

```text
EJG = Eustaquio Jiménez Girón / Jiménez Girón 1979
ND  = Jiménez Jiménez & Vicente Marcial Cerqueda / 2000
VP  = Velma Pickett / Pickett et al. 2001
```

Por ello, para los artefactos locales derivados de Dictionaria:

- conservar las columnas/campos de atribución existentes;
- conservar códigos de contributor/source cuando estén presentes;
- no borrar `Attribution`, `attribution_entry`, `attribution_sense` u otros equivalentes al producir derivados;
- no presentar datos con código `[VP]`, `[ND]`, `[EJG]` u otro código como si fueran creación original del repositorio;
- registrar transformaciones técnicas que separen copia/export de datos y estructura derivada.

Artefactos locales directamente asociados:

```text
dispositivo/runtime/v0_2_15_3/DICTIONARIA_entries_v0_2_15_2.csv
dispositivo/runtime/v0_2_15_3/DICTIONARIA_senses_v0_2_15_2.csv
dispositivo/runtime/v0_2_15_3/DICTIONARIA_examples_v0_2_15_2.csv
dispositivo/analyzer/DIC_VERB_2385_v0_1.csv
```

La SQLite v2.20 usa explícitamente `BIB054_DICTIONARIA` en varias tablas. Ver `SQLITE_RIGHTS_SOURCE_MAP_v1.json`.

**Tratamiento técnico vigente:** `CC_BY_4_0_NOTICE_VERIFIED / PER_RECORD_ATTRIBUTION_MUST_BE_PRESERVED / WHOLE_REPO_LICENSE_NOT_INFERRED`.

## 2. Pickett, Black y Marcial Cerqueda — Gramática popular del zapoteco del Istmo

**Fuente:** Velma B. Pickett, Cheryl Black y Vicente Marcial Cerqueda, *Gramática popular del zapoteco del Istmo*.  
**Edición:** segunda edición electrónica, 2001  
**Editores:** Centro de Investigación y Desarrollo Binnizá A.C.; Instituto Lingüístico de Verano A.C.  
**Fuente oficial de referencia:** `https://mexico.sil.org/resources/archives/35304`

El registro oficial de SIL confirma título, responsables, edición y editores. El front matter de la segunda edición electrónica contiene aviso `D.R.` para Centro de Investigación y Desarrollo Binnizá A.C. e Instituto Lingüístico de Verano A.C. No se ha verificado una licencia abierta aplicable a esta obra.

`BIB004_GRAMATICA_POPULAR` aparece de forma verificable en:

```text
documentary_alignment_v0210 = 131 filas
person_possession_exact_v0214 = 100 filas
```

**Tratamiento técnico vigente:** `D_R_RIGHTS_NOTICE_OBSERVED / NO_OPEN_LICENSE_VERIFIED / REDISTRIBUTION_AND_RELICENSING_REVIEW_REQUIRED`.

No eliminar ejemplos/registros históricos para simplificar licenciamiento. Si un release distribuible necesita separar material, hacerlo mediante una estrategia explícita de packaging o exclusión, preservando genealogía en el repositorio de investigación conforme a los derechos aplicables.

## 3. Pérez Báez & Kaufman 2016 — Verb Classes in Juchitán Zapotec

**Fuente:** Gabriela Pérez Báez & Terrence Kaufman. 2016. “Verb Classes in Juchitán Zapotec.” *Anthropological Linguistics* 58(3):217–257.  
**DOI:** `10.1353/anl.2016.0030`  
**Repositorio bibliográfico:** `https://repository.si.edu/handle/10088/32808`

La identidad interna está triangulada por:

- `source_id = BIB059_PBK2016` en `morphology_rule_registry_v023`;
- `PBK2016_REGLAS_MORF_VERB_v0_1.csv` registrado como source snapshot dentro de la SQLite;
- once reglas `PBK-VERB-*` / `PBK-DER-*` en `didxaza_runtime_v0_2_3_morphology_i.py`, con referencias a pp. 4–38;
- la bibliografía de Dictionaria, que identifica Pérez Báez & Kaufman 2016 sobre clasificación verbal de Juchitán;
- los metadatos bibliográficos externos, que identifican el artículo, volumen, páginas y DOI.

La publicación reporta `© 2016, Indiana University Anthropological Linguistics. All rights reserved.` La disponibilidad del PDF en un repositorio institucional no se interpreta como licencia abierta.

En la SQLite v2.20:

```text
morphology_rule_registry_v023 = 11 filas BIB059_PBK2016
```

**Tratamiento técnico vigente:** `IDENTITY_TRIANGULATED / ALL_RIGHTS_RESERVED_NOTICE_OBSERVED / DERIVED_RULE_RELICENSING_REVIEW_REQUIRED`.

Este estado no decide por sí mismo si una regla abstracta, hecho lingüístico o transformación concreta está protegida por copyright. Únicamente impide tratar el conjunto derivado como material abierto por defecto sin análisis adicional.

## 4. Pickett — Vocabulario zapoteco del Istmo

El frente del *Vocabulario* sigue separado de la Gramática y del artículo PBK2016. La SQLite conserva dos IDs históricas distintas:

```text
BIB003_PICKETT_VOCABULARIO = lexical backfill, 2,534 filas
BIB055_PICKETT_VOCABULARIO = Appendix V documentary alignment, 16 filas
```

No fusionar esas IDs sólo por similitud de título. Ver `RIGHTS_PROVENANCE_AUDIT_v1.md` y `SQLITE_RIGHTS_SOURCE_MAP_v1.json`.

**Tratamiento técnico vigente:** `NO_OPEN_LICENSE_VERIFIED / SOURCE_ID_GENEALOGY_PENDING / RIGHTS_REVIEW_REQUIRED`.

## 5. Bueno Holle 2019

**Fuente:** Juan José Bueno Holle. 2019. *Information structure in Isthmus Zapotec narrative and conversation*. Language Science Press.  
**Fuente editorial:** `https://langsci-press.org/catalog/book/219`  
**Licencia reportada:** `CC BY 4.0`.

La misma licencia está registrada en `BH2019_SOURCE_PROVENANCE_v0_36_1.json`.

**Tratamiento técnico vigente:** `SOURCE_CC_BY_4_0_VERIFIED / ATTRIBUTION_REQUIRED / PROJECT_ANALYSIS_AUTHORSHIP_SEPARATE`.

## 6. Reglas para derivados y empaquetado

Hasta completar DT-004:

```text
DO_NOT_ADD_BLANKET_LICENSE
DO_NOT_DROP_ATTRIBUTION_COLUMNS
DO_NOT_COLLAPSE_SOURCE_IDS_BY_SIMILAR_TITLE
DO_NOT_TREAT_REPOSITORY_AVAILABILITY_AS_LICENSE
DO_NOT_MUTATE_HISTORICAL_RELEASES_TO_FIX_NOTICE_GAPS
```

Una futura distribución podrá necesitar `NOTICE`, licencias por subárbol, archivos excluidos del paquete distribuible o una combinación. Este documento sólo materializa el mínimo de atribución/provenance ya verificado.
