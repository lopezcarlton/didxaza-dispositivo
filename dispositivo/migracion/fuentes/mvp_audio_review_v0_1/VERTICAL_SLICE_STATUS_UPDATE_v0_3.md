# Actualización de estado de la vertical slice — v0.3 acústica

Esta actualización no modifica `v0.2.15.3 CLOSED_PASS`.

## Cambios

- FB-079 pasa de `PROBABLE_TRANSCRIPTION_CORRECTION` a `ACOUSTICALLY_SUPPORTED_TRANSCRIPTION_CORRECTION`.
- FB-076 pasa a `ACOUSTICALLY_SUPPORTED_ORTHOGRAPHIC_CANDIDATE`.
- FB-062 retira la interpretación errónea `zee = venir` y conserva `zee = maíz/elote + nda'` como hipótesis acústicamente compatible, no validada.
- FB-019 y FB-099 quedan identificados como problemas semántico-gramaticales que el audio no puede resolver por sí solo.

## Seguridad

Ningún estado activa:

- `AUTO_CORRECT`;
- `ORTHOGRAPHICALLY_VALIDATED`;
- `NATIVE_SPEAKER_VALIDATED`;
- generación libre.

La siguiente transición depende de la revisión estructurada con Vicente.
