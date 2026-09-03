# Prompts históricos — cuarentena

**Estado:** `HISTORICAL_QUARANTINE / NOT_ACTIVE_POLICY / NOT_CURRENT_EXECUTION_INSTRUCTIONS`

Esta carpeta conserva prompts recuperados por valor genealógico e histórico. Su presencia no los convierte en instrucciones activas del dispositivo, política vigente, contrato técnico actual ni autoridad de conocimiento.

## Contenido preservado en este checkpoint

| Archivo | Git blob en el checkpoint 2026-09-03 | Clasificación |
|---|---|---|
| `generadordecorpusv7` | `8c14216194b47bb1ae1ab0443009ef6eab60f371` | prompt histórico |
| `verificador de ortografía` | `3f8e251eb20f2d1695b87d7a99687605c0811548` | prompt histórico |

Los nombres sin extensión y los espacios del nombre histórico se conservan deliberadamente. No renombrar, añadir extensiones, reformatear ni normalizar estos archivos sólo para hacerlos más cómodos de usar.

## Regla de uso

```text
HISTORICAL_PROMPT != ACTIVE_PROMPT
HISTORICAL_PROMPT != CURRENT_POLICY
HISTORICAL_PROMPT != KNOWLEDGE_AUTHORITY
HISTORICAL_PROMPT != EXECUTION_CONTRACT
```

No ejecutar estos archivos como si describieran el estado actual del Analyzer, Corrector, Tutor o Generator.

Si una idea o requisito contenido aquí parece útil para trabajo nuevo, debe tratarse como evidencia histórica de diseño: verificarla contra el estado técnico actual y, cuando implique conocimiento lingüístico/pedagógico/metodológico, contra la fuente canónica `lopezcarlton/vocesdelasnubes`. Cualquier adopción nueva debe quedar explícita y trazable; nunca se hereda autoridad por estar escrita en un prompt histórico.

El código actual y los contratos de ejecución se determinan desde los componentes y documentos técnicos vigentes del repositorio, no desde esta carpeta.
