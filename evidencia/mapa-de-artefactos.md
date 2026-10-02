# Mapa de artefactos: dónde está cada cosa que el informe identifica

El informe describe los materiales por lo que son, sin nombres de archivo ni rutas. Esta
página es el puente: para cada material del anexo de reproducibilidad (Anexo E) dice qué
archivo es, en qué repositorio vive y cómo se comprueba. Los enlaces apuntan a `main`, la
rama por defecto de cada repositorio; al congelar (tag `informe-2026`) se reemplazan por el
tag.

## 1. Materiales congelados y su huella

Dos huellas SHA-256 identifican los dos bancos sobre los que se sostienen todas las
comparaciones. Quien descargue el archivo y obtenga la misma huella evalúa el mismo
contenido que el informe.

| Material | Archivo | Huella SHA-256 |
|---|---|---|
| Banco de imágenes `bench_v3` (6.477 imágenes, 3 fuentes) | [`bench_v3.json`](https://github.com/Pandulc/e-ovrt_datasets/blob/main/datasets/processed/coco/bench/curated/bench_v3.json) | `4557024ecc4ee497ab1fad01d6819206395c10fd794010ed8c1d9198b19a4462` |
| Manifiesto del banco temporal (47 clips) | [`manifest.yaml`](https://github.com/Pandulc/e-ovrt_datasets/blob/main/datasets/processed/clip_bench/manifest.yaml) | `3f14f50a53c0d6c57b429378544dcfb6ed87fc942640db302c53ba1470001a75` |

Las huellas de los estratos del banco de imágenes viajan dentro de su
[manifiesto de composición](https://github.com/Pandulc/e-ovrt_datasets/blob/main/datasets/processed/coco/bench/curated/bench_v3_manifest.json)
(`source_sha256` por fuente). El manifiesto del banco temporal registra el SHA-256 de cada
clip de video, y las huellas de su referencia temporal y de sus anotaciones están en
[`clip_bench.sha256`](https://github.com/Pandulc/e-ovrt_datasets/blob/main/datasets/processed/clip_bench/clip_bench.sha256).
Los conjuntos de prompts se identifican por el contenido de su archivo en
[`prompts/`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/HEAD/prompts).

## 2. Cada material del Anexo E, y dónde está

| Material (Anexo E, Tabla E.1) | Qué archivo es | Dónde vive | Cómo se comprueba |
|---|---|---|---|
| Banco de imágenes | `bench_v3.json` (COCO), su manifiesto de composición y la ficha de procedencia por fuente | [`e-ovrt_datasets` · `datasets/processed/coco/bench/curated/`](https://github.com/Pandulc/e-ovrt_datasets/tree/main/datasets/processed/coco/bench/curated) · [ficha `bench_v3`](https://github.com/Pandulc/e-ovrt_datasets/blob/main/datasets/registry/bench_v3.md) | Huella de la §1; el generador del banco reproduce los estratos byte a byte ([`build_bench_v3.py`](https://github.com/Pandulc/e-ovrt_datasets/blob/main/datasets/scripts/curate/build_bench_v3.py)) |
| Vocabulario (conjuntos de prompts) | `cr01_cr02_v2_short.yaml` (el congelado del rodaje y del banco), `eind_v1.yaml`, `edir_v1.yaml` | [`e-ovrt_experimental-setup` · `prompts/`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/HEAD/prompts) | El contenido del archivo, no su nombre, identifica la corrida |
| Banco temporal | `manifest.yaml`, la referencia temporal humana por clip (`gt/`) y las anotaciones exportadas (`annotations/`) | [`e-ovrt_datasets` · `datasets/processed/clip_bench/`](https://github.com/Pandulc/e-ovrt_datasets/tree/main/datasets/processed/clip_bench) | Huella de la §1. Los 34 clips propios están en la carpeta con acceso autorizado (§4); los 13 de internet, en su fuente ([material de video](material-de-video.md)) |
| Configuración efectiva de un experimento | Manifiesto de la corrida: fuente, perfil del modelo, vocabulario, conjunto de patrones, instrumentación | [`e-ovrt_experimental-setup` · `experiments/`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/HEAD/experiments) · patrones en [`e-ovrt_control-plane` · `configs/patterns/`](https://github.com/Pandulc/e-ovrt_control-plane/tree/main/configs/patterns) | Parámetros solicitados contra parámetros aplicados, que la corrida conserva |
| Corrida de medios, de control y de distribución | Detecciones por unidad visual, eventos y alertas del patrón, registro de notificaciones: los artefactos primarios de cada corrida | Las carpetas de corrida, que git ignora, están en la carpeta con acceso autorizado (§4); sus métricas y resúmenes, en `results/` | Relectura de las detecciones conservadas con la misma configuración; correspondencia alerta–intento–resultado |
| Resultados derivados | Métricas por clip y resúmenes por condición, escenario y estrato, con la campaña y la huella del banco al pie | [`e-ovrt_experimental-setup` · `results/`](https://github.com/simonll4/e-ovrt_experimental-setup/blob/HEAD/results/index.md): [imágenes](https://github.com/simonll4/e-ovrt_experimental-setup/blob/HEAD/results/bench_imagenes/index.md) · [estado por persona](https://github.com/simonll4/e-ovrt_experimental-setup/blob/HEAD/results/bench_nivel_a/index.md) · [alertas por episodio](https://github.com/simonll4/e-ovrt_experimental-setup/blob/HEAD/results/clip_bench/index.md) · [tiempo real](https://github.com/simonll4/e-ovrt_experimental-setup/blob/HEAD/results/realtime/index.md) | Coincidencia de numeradores, denominadores y reglas de agregación; cada tabla enlaza su artefacto (`metrics.json`, `campaign.yaml`) |
| Rama de ajuste fino | Manifiestos de los tramos, criterios pre-registrados y veredictos | [`e-ovrt_experimental-setup` · `finetuning/manifests/`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/HEAD/finetuning/manifests) | Los veredictos remiten a su evaluación en `results/`. Los checkpoints no se publican: están en la carpeta con acceso autorizado (§4) |
| Empaquetado de la plataforma | Composición de los trece servicios y su documentación operativa | [`e-ovrt_experimental-setup` · `infra/platform/`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/HEAD/infra/platform) | `docker compose config` valida la composición; la construcción de las imágenes y el arranque integral no están verificados, como declara el informe |
| Procedencia y licencias de los datos | Registro de licencias y de descargas por fuente | [`e-ovrt_datasets` · `datasets/registry/`](https://github.com/Pandulc/e-ovrt_datasets/tree/main/datasets/registry) | Lo que el Anexo F declara por fuente |

## 3. Cómo se reproduce cada cosa

El Anexo E del informe describe la secuencia por material, sin comandos. Los comandos
concretos están en el `README` de cada repositorio:

- construir el banco de imágenes y verificar sus estratos, en `e-ovrt_datasets`;
- evaluar una corrida contra el banco, en `e-ovrt_media-plane`;
- releer detecciones y evaluar alertas contra la referencia temporal, en `e-ovrt_control-plane`;
- lanzar una corrida de punta a punta, en la consola de `e-ovrt_experimental-setup`.

Las fichas, con los comandos de instalación y de pruebas, están en
[`repositorios/`](../repositorios/README.md).

## 4. Evidencia con acceso autorizado

Lo que git no guarda está en una carpeta de Google Drive **con acceso restringido**:

> **[Carpeta de evidencia de E-OVRT-VDP](https://drive.google.com/drive/folders/1LFLf3XXeZoY2zKFLfhfBB1lMT4ux4vHY?usp=sharing)**
> Se abre con una cuenta de Google; quien no tenga acceso lo pide con «Solicitar acceso»
> desde el mismo enlace, y los autores aprueban cada pedido.

La carpeta respalda las cifras, pero no es su fuente: cada cifra se cita desde el informe
(sección y tabla) y desde `results/`. Qué hay y cómo se comprueba cada paquete después de
bajarlo:

| Paquete | Contenido | Archivos | Peso | SHA-256 |
|---|---|---|---|---|
| `1-ver-la-plataforma-funcionando/` | cinco videos renderizados a partir de corridas reales, sueltos para verlos en el navegador | 5 | 105 MB | — |
| `2-banco-de-video-y-su-GT/clips/` | los 34 clips del rodaje propio, sueltos | 34 | 1,00 GB | uno por clip, en el [manifiesto del banco temporal](https://github.com/Pandulc/e-ovrt_datasets/blob/main/datasets/processed/clip_bench/manifest.yaml) |
| `2-banco-de-video-y-su-GT/gt-humano.zip` | la referencia temporal humana completa, anotada en CVAT (también en GitHub) | 261 | 4 MB | `23c11a282bcb08b3147130e9a414ad7af2f405e759e7d13b198da58009e382f6` |
| `3-artefactos-de-resultados/artefactos-de-results.zip` | los artefactos que respaldan cada cifra de los índices de `results/` | 11.503 | 74 MB | `0377695d3c82d66343e0f47c896a7919ef8bced165be6b6181395ceb40685312` |
| `4-fine-tuning/checkpoints.zip` | los checkpoints de los tramos T1 y T2 | 76 | 1,92 GB | `6f9f2b2d22668983aa5ae4ebc613c039ec1dff04871f48ca160eed891041596c` |
| `4-fine-tuning/corridas-y-evaluaciones.zip` | las evaluaciones de cada checkpoint y de su línea de base contra `bench_v3`: la medición de los dos NO-GO | 61 | 8 MB | `3283f2f2f681339700c40ae2a540b2727b3da18fa0219c179ca794cec7f8b00b` |
| `5-datos-de-campana/datos-de-operacion.zip` | los datos crudos de las campañas de medición | 11.323 | 160 MB | `bc342e58733b21282292147e21e0a349b714daba1ec82dd17de1b9aa18212292` |

Para comprobar una descarga alcanza con `sha256sum <archivo>` y comparar el resultado con la
tabla.

**Lo que la carpeta no tiene, y por qué:**

- **Los 13 clips del lote de internet.** El informe declara un uso con cita y sin
  redistribución (Anexo F); se consiguen en la lista de reproducción que cita
  [`material-de-video.md`](material-de-video.md).
- **Imágenes de conjuntos de terceros.** Las evaluaciones del ajuste fino van sin las
  imágenes del banco con las cajas dibujadas: `bench_v3` incluye CHV, cuyas imágenes no se
  redistribuyen (Anexo F), y los veredictos salen de los archivos de evaluación, que sí están.
- **La filmación original del rodaje** y **los pesos preentrenados** de los modelos, que se
  descargan de su fuente original.
