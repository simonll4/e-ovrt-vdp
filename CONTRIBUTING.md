# Cómo se escribe en este repositorio

Este repo es la cara pública del proyecto y **la única referencia externa que cita el informe**.
Lo lee gente que no participó del trabajo. Cinco reglas; las cuatro primeras se verifican
con `python3 herramientas/verificar.py`:

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
5. **Lo que el informe declara sin redistribución no se redistribuye por ningún canal**: ni
   en este repositorio ni en la carpeta de evidencia con acceso autorizado. Hoy son los 13
   clips del lote de internet y las imágenes de CHV y de la copia de MOCS (Anexo F). Quien
   abra un canal nuevo replica la exclusión ahí: citar la fuente no es permiso para
   redistribuir.

Marco de lectura para todo lo que muestre resultados: **los números son el dato de una
combinación bajo un protocolo, no un aprobado/fallado**. Un NO-GO pre-registrado es un
resultado y se muestra como tal.

Una línea puntual se exime del guardián con el marcador `<!-- verificar:permitir -->` al
final.
