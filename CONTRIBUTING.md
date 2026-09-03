# Contribuir a didxaza-dispositivo

## Alcance

Este repositorio es una implementación técnica derivada de `lopezcarlton/vocesdelasnubes`. No constituye autoridad lingüística, pedagógica, metodológica ni comunitaria.

Antes de hacer cambios técnicos, leer al menos:

- `REENTRY_TECNICO.md`;
- `KNOWLEDGE_SOURCE_PIN.md`;
- `dispositivo/migracion/CURRENT_EXECUTABLE_STATE_v1.md`;
- `dispositivo/KNOWLEDGE_CONSUMPTION_CONTRACT_v1.md`.

## Límite de conocimiento

Los cambios en este repositorio pueden modificar código, pruebas, adaptadores, empaquetado, reproducibilidad y documentación técnica. No deben convertir una hipótesis, un resultado de ejecución o un artefacto histórico en nueva autoridad de conocimiento.

Cuando un cambio técnico dependa de conocimiento nuevo o revisado:

1. resolver primero la fuente correspondiente en `lopezcarlton/vocesdelasnubes`;
2. registrar el commit exacto de conocimiento utilizado;
3. conservar provenance suficiente para reconstruir la decisión;
4. mantener `UNRESOLVED` cuando la evidencia no autorice una conclusión.

Un `PASS` técnico no equivale a validación lingüística.

## Artefactos históricos y reproducibilidad

No reescribir, reformatear, normalizar, renombrar ni regenerar silenciosamente artefactos históricos cuya identidad se use para reproducibilidad.

En particular:

- respetar `.gitattributes` y los hashes/manifiestos existentes;
- no sustituir payloads exactos por versiones “equivalentes” sin verificar identidad y genealogía;
- preservar los prompts de `dispositivo/prompts/historicos/` como material histórico en cuarentena;
- separar explícitamente una adaptación técnica nueva del artefacto histórico que adapta.

Si una recuperación exacta es imposible, documentar la diferencia en vez de ocultarla.

## COR001

La política vigente del repositorio es:

```text
COR001 = ANALYSIS_TARGET_ONLY
COR001 != GOLD_STANDARD
COR001 != BENCHMARK
COR001 != REGRESSION_AUTHORITY
COR001 != RULE_DISCOVERY_SOURCE
```

COR001 puede usarse para observar el comportamiento del dispositivo y revelar huecos o abstenciones. No puede usarse para decidir que una regla es correcta ni para optimizar el sistema contra sus respuestas.

## Flujo de cambios

Para cambios no triviales:

1. trabajar en una rama separada de `main`;
2. mantener el diff lo más pequeño y verificable posible;
3. ejecutar las pruebas pertinentes y el workflow de reproducibilidad;
4. no integrar un PR con CI rojo;
5. actualizar documentos de estado sólo después de verificar el comportamiento real;
6. distinguir claramente entre corrección técnica, recuperación histórica y cambio de conocimiento.

`CODEOWNERS` declara propiedad/revisión esperada, pero la protección efectiva de `main` depende de branch protection o rulesets de GitHub.

## Archivos locales

`.gitignore` sólo excluye cachés, entornos, secretos locales, metadatos de editor/SO y directorios de trabajo locales. No se deben añadir patrones generales para ignorar CSV, JSON/JSONL, SQLite, ZIP, Markdown u otros formatos que forman parte del estado técnico o histórico del repositorio.

## Licencias y materiales de terceros

Este repositorio no contiene todavía una licencia global que autorice asumir términos uniformes para todo el árbol. Hay artefactos derivados o relacionados con fuentes de terceros cuyos derechos deben auditarse antes de adoptar una licencia general.

No incorporar material de terceros suponiendo que su presencia previa implica permiso de redistribución o relicenciamiento. Todo nuevo material de terceros debe conservar su provenance y los términos aplicables cuando se conozcan.

Esta sección es una regla de contribución técnica; no constituye por sí misma una licencia ni una determinación jurídica sobre los materiales existentes.
