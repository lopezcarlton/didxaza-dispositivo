# Fuentes controladas del dispositivo

Esta carpeta contiene **contratos técnicos**, no una segunda autoridad documental.
La identidad y el estatus de las fuentes pertenecen a `lopezcarlton/vocesdelasnubes`.

## Biyubi

Fuente canónica:

`lopezcarlton/vocesdelasnubes/conocimiento/fuentes/SRC-BIYUBI-DICCIONARIO-DIDXAZA-ESPANOL.md`

El snapshot registrado de Biyubi es una copia controlada y no se publica en este
repositorio. Para que el Analyzer la consulte, montar el XLSX exacto mediante:

```bash
export DIDXAZA_BIYUBI_XLSX=/ruta/al/diccionario-biyubi.xlsx
python dispositivo/analyzer/analyzer_v0_35_migrated_adapter.py \
  --surface "texto didxazá"
```

También puede suministrarse explícitamente:

```bash
python dispositivo/analyzer/analyzer_v0_35_migrated_adapter.py \
  --biyubi-xlsx /ruta/al/diccionario-biyubi.xlsx \
  --require-biyubi \
  --surface "texto didxazá"
```

El loader exige el SHA-256 y el conteo de 23,601 filas con datos registrados en
`BIYUBI_SOURCE_CONTRACT_v1.json`. Si el archivo no coincide, falla en lugar de
sustituir silenciosamente la fuente.

Reglas de uso:

```text
BIYUBI = SECONDARY_SURFACE_EVIDENCE
BIYUBI != ORTHOGRAPHIC_AUTHORITY
BIYUBI_ATTESTATION != CORRECTNESS_LICENSE
BIYUBI_ABSENCE != INCORRECTNESS
NEAR_MATCH = false
STRIP_TONE = false
PDLMA_TO_SURFACE_FOR_EXACT = false
```

Los resultados distinguen `BIYUBI_EXACT_ENTRY` de
`BIYUBI_EXACT_TOKEN_ATTESTATION`.
