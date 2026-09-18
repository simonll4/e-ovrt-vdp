# Material de video: qué se usó y qué se publica

**No se publica ningún video en este repositorio.** El material de obra propia no se
redistribuye; el de internet se referencia a su origen. Los clips se conservan en una
carpeta de evidencia con acceso autorizado: ver [`mapa-de-artefactos.md`](mapa-de-artefactos.md) §4.

## Rodaje propio (34 clips, no publicados)

- Obra real, bloque guionado con hardware real (cámara OAK-D Pro PoE y RTSP), grabado y
  recortado desde la consola. Referencia temporal humana anotada en CVAT en dos pasadas;
  34 clips, 34 episodios evaluables. Sus métricas están en
  [`results/clip_bench/`](https://github.com/simonll4/e-ovrt_experimental-setup/blob/HEAD/results/clip_bench/index.md).
  Los fotogramas que aparecen en las figuras (C) provienen de este rodaje.

## Lote de internet (13 clips, referenciados por URL)

- Obra real **no guionada**, diurna en su mayoría (tres clips nocturnos: uno positivo,
  `v04_c01`, y dos negativos, `v04_c02` y `v04_c03`), un clip largo de "soak"
  (0,1027 h, `v06_c01`) para el control de falsos positivos. Cada clip se recortó de un
  video público; acá va su origen. Los términos de uso son los del canal; no se
  redistribuye el material.

| Clip | Escenario | Fuente | Video de origen | Términos |
|---|---|---|---|---|
| `v01_c01` | P5 | YouTube @HospitalConstruction | *(sin URL registrada)* | uso evaluativo interno, sin redistribución (a confirmar con la URL) |
| `v01_c02` | P1 | YouTube @HospitalConstruction | *(sin URL registrada)* | uso evaluativo interno, sin redistribución (a confirmar con la URL) |
| `v02_c01` | P5 | YouTube @HospitalConstruction | *(sin URL registrada)* | uso evaluativo interno, sin redistribución (a confirmar con la URL) |
| `v03_c01` | P5 | YouTube @HospitalConstruction | *(sin URL registrada)* | uso evaluativo interno, sin redistribución (a confirmar con la URL) |
| `v03_c02` | P5 | YouTube @HospitalConstruction | *(sin URL registrada)* | uso evaluativo interno, sin redistribución (a confirmar con la URL) |
| `v04_c01` | P1 | YouTube @HospitalConstruction | *(sin URL registrada)* | uso evaluativo interno, sin redistribución (a confirmar con la URL) |
| `v04_c02` | P5 | YouTube @HospitalConstruction | *(sin URL registrada)* | uso evaluativo interno, sin redistribución (a confirmar con la URL) |
| `v04_c03` | P5 | YouTube @HospitalConstruction | *(sin URL registrada)* | uso evaluativo interno, sin redistribución (a confirmar con la URL) |
| `v05_c01` | P5 | YouTube @HospitalConstruction | *(sin URL registrada)* | uso evaluativo interno, sin redistribución (a confirmar con la URL) |
| `v06_c01` | P5 | YouTube @HospitalConstruction | *(sin URL registrada)* | uso evaluativo interno, sin redistribución (a confirmar con la URL) |
| `v07_c01` | P5 | YouTube @HospitalConstruction | *(sin URL registrada)* | uso evaluativo interno, sin redistribución (a confirmar con la URL) |
| `v09_c01` | P5 | YouTube @HospitalConstruction | *(sin URL registrada)* | uso evaluativo interno, sin redistribución (a confirmar con la URL) |
| `v10_c01` | P5 | YouTube @HospitalConstruction | *(sin URL registrada)* | uso evaluativo interno, sin redistribución (a confirmar con la URL) |

- El escenario es el guion previsto para el clip: **P5** = cumplimiento total
  (negativo), **P1** = una infracción registrada.
- `v08_c01` se relevó pero quedó **excluido del banco con causa** y no se publica.

## Cómo se anotó la referencia

- Nivel B: episodios (inicio/fin) de CR-01 y CR-02 por clip; bordes adjudicados por
  oclusión en 6 clips (L3); sin doble anotación (L2). Una revisión ciega posterior del
  lote de internet cambió 5 de 7 declaraciones de episodio: donde el estado no era
  observable, la anotación pasó a "desconocido". Ese resultado está en
  [`results/clip_bench/`](https://github.com/simonll4/e-ovrt_experimental-setup/blob/HEAD/results/clip_bench/index.md).
