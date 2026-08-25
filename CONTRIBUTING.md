# Cómo se escribe en este repositorio

Este repo es la cara pública del proyecto y **la única referencia externa que cita el informe**.
Lo lee gente que no participó del trabajo. Cuatro reglas, todas verificables con
`python3 herramientas/verificar.py`:

1. **Autocontenido hacia afuera.** No se referencia ningún documento de trabajo interno del
   equipo (bitácoras, registros de decisión, fichas de corrección, identificadores de
   hallazgos, rutas de una máquina). Sólo se cita: este repo, los cinco repos públicos de
   código, el informe y la bibliografía. Para un lector externo, cualquier otra cosa es un
   enlace muerto.
2. **Ninguna cifra sin fuente enlazada.** Cada número de resultado enlaza a la página de
   `results/` (o `finetuning/`) de `e-ovrt_experimental-setup` de donde sale, con `n` y
   material. Este repo muestra cifras; no las produce.
3. **Sin binarios pesados.** Sí: figuras PNG/SVG, capturas de la consola, el PDF del informe.
   No: videos, documentos de trabajo `.docx`, datasets, pesos de modelos, corridas.
4. **El vocabulario es el del informe.** CR-01 / CR-02, DBE / EBE, `media.detection.v1`,
   `bus.envelope.v1`, `bench_v3`, limitaciones L1–L8, E-DIR / E-IND / E-HYB,
   `gdino-tiny-560`. Sin sinónimos internos.

Marco de lectura para todo lo que muestre resultados: **los números son el dato de una
combinación bajo un protocolo, no un aprobado/fallado**. Un NO-GO pre-registrado es un
resultado y se muestra como tal.

Excepción única al guardián: `PUBLICAR.md` (checklist interno de publicación, se borra al
publicar). Una línea puntual se exime con el marcador `<!-- verificar:permitir -->` al final.
