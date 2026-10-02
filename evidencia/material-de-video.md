# Material de video: qué se usó y dónde está

El banco temporal reúne **47 clips de dos orígenes**, y la distinción importa para leer los
resultados: el rodaje es material guionado y el lote de internet es obra real no guionada,
así que los dos estratos se reportan siempre por separado, nunca sólo agregados.

Ningún video se publica en este repositorio. Su referencia temporal humana, sus anotaciones
y todas las métricas medidas sobre ellos sí están en GitHub, para los 47 clips.

| Origen | Clips | Dónde está el video |
|---|---|---|
| Rodaje propio | 34 | en la [carpeta de evidencia con acceso autorizado](mapa-de-artefactos.md#4-evidencia-con-acceso-autorizado) |
| Lote de internet (@HospitalConstruction) | 13 | en su fuente original: no se redistribuye |

## Rodaje propio (34 clips)

Obra real, bloque guionado, con hardware real: una cámara OAK-D Pro PoE y una cámara IP
RTSP, grabadas y recortadas desde la consola. Las personas que aparecen en cuadro son los
integrantes del proyecto, actuando según un guion. La referencia temporal humana se anotó
en CVAT en dos pasadas: 34 clips, 34 episodios evaluables. Sus métricas están en
[`results/clip_bench/`](https://github.com/simonll4/e-ovrt_experimental-setup/blob/HEAD/results/clip_bench/index.md),
y los fotogramas de la figura C salen de este rodaje.

Cada clip de la carpeta con acceso autorizado se verifica contra el SHA-256 que el
[manifiesto del banco temporal](https://github.com/Pandulc/e-ovrt_datasets/blob/main/datasets/processed/clip_bench/manifest.yaml)
registra para ese clip; el manifiesto, a su vez, tiene su huella congelada en el
[mapa de artefactos](mapa-de-artefactos.md#1-materiales-congelados-y-su-huella).

## Lote de internet (13 clips)

Obra real **no guionada**, diurna en su mayoría —tres clips nocturnos: uno positivo,
`v04_c01`, y dos negativos, `v04_c02` y `v04_c03`—, con un clip largo de *soak*
(0,1027 h, `v06_c01`) para el control de falsos positivos.

Los 13 clips son recortes de 10 videos que el canal de YouTube
[@HospitalConstruction](https://www.youtube.com/@HospitalConstruction) publicó en su serie
de seguimiento de la construcción de un hospital. Todos están reunidos en la lista de
reproducción [*"Raw" construction videos*](https://www.youtube.com/playlist?list=PLVG3-xIaXtKzAC9JJnZJUY4aBCg0BNPKV),
la misma que cita el informe (Anexo F). Se usaron las subidas de *footage* a velocidad
original, no los *time-lapse* de la serie.

Sobre ese material rige la licencia estándar de YouTube, no Creative Commons, y que un video
sea públicamente visible no acredita autorización para redistribuirlo. Por eso el proyecto
declaró un uso académico y evaluativo, con cita y **sin redistribución**: los clips no están
en este repositorio ni en la carpeta de evidencia, y quien quiera verlos va a la lista de
reproducción. Su ausencia no le quita verificabilidad a ninguna cifra.

| Clip | Escenario | Clip | Escenario |
|---|---|---|---|
| `v01_c01` | P5 | `v04_c03` | P5 |
| `v01_c02` | P1 | `v05_c01` | P5 |
| `v02_c01` | P5 | `v06_c01` | P5 |
| `v03_c01` | P5 | `v07_c01` | P5 |
| `v03_c02` | P5 | `v09_c01` | P5 |
| `v04_c01` | P1 | `v10_c01` | P5 |
| `v04_c02` | P5 | | |

El escenario es el guion previsto para el clip: **P5**, cumplimiento total (negativo);
**P1**, una infracción registrada. `v08_c01` se relevó pero quedó **excluido del banco con
causa**.

## Cómo se anotó la referencia

Nivel B: episodios (inicio y fin) de CR-01 y CR-02 por clip, con bordes adjudicados por
oclusión en 6 clips (limitación L3) y sin doble anotación (limitación L2). Una revisión ciega
posterior del lote de internet encontró que 5 de las 7 declaraciones de episodio eran errores
de anotación por sobre-declarar estados que no resultaban observables, y dejó 2 episodios
evaluables y 11 clips negativos. Ese resultado está en
[`results/clip_bench/`](https://github.com/simonll4/e-ovrt_experimental-setup/blob/HEAD/results/clip_bench/index.md).
