# HOLDOUT_GENERALIZATION_REQUIREMENTS v0.1

## Propósito

Medir generalización real del dispositivo didxazá sin reutilizar material que haya guiado el core.

## Requisitos mínimos

1. El conjunto se define **después** de congelar la versión de `PRODUCTION_KNOWLEDGE` a evaluar.
2. Ninguna frase, traducción, diagnóstico, audio o respuesta del holdout puede usarse para elegir qué reglas, ejemplos o lexemas integrar antes de la medición.
3. Debe contener texto de Juchitán o material explícitamente etiquetado por variedad; no mezclar variedades sin etiqueta.
4. Gold y audio, si existen, permanecen sellados hasta congelar la salida text-only.
5. El español, si existe, es scoring-only.
6. Debe incluir ejemplos con cobertura conocida y ejemplos nuevos, para separar recuperación de conocimiento y generalización estructural.
7. Después de usar una edición del holdout para desarrollo, esa edición deja de ser holdout y pasa a regression/development data.
8. Cada nueva medición de generalización requiere material todavía no utilizado para ajustar el sistema.

## Métricas mínimas

- COMPLETE_INDEPENDENT_ANALYSIS
- PARTIAL por tipo
- ABSTAIN
- REVIEW_CANDIDATE
- VALIDATED_CORRECTION
- falsos positivos de corrección
- provenance válido
- dependencia de audio = 0 para pipeline basal
