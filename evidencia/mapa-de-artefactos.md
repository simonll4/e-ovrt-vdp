# Mapa de artefactos: dónde está cada cosa que el informe identifica

El informe describe los materiales por lo que son, sin nombres de archivo ni rutas. Esta
página es el puente: para cada material del anexo de reproducibilidad (Anexo E) dice qué
archivo es, en qué repositorio vive y cómo se comprueba. Los enlaces apuntan a la rama de
trabajo vigente de cada repositorio; al congelar (tag `informe-2026`) se reemplazan por el tag.

## 1. Materiales congelados y su huella

Dos huellas SHA-256 identifican los dos bancos sobre los que se sostienen todas las
comparaciones. Un tercero que descargue el archivo y obtenga la misma huella evalúa el
mismo contenido que el informe.

| Material | Archivo | Huella SHA-256 |
|---|---|---|
| Banco de imágenes `bench_v3` (6.477 imágenes, 3 fuentes) | [`bench_v3.json`](https://github.com/Pandulc/e-ovrt_datasets/blob/main/datasets/processed/coco/bench/curated/bench_v3.json) | `4557024ecc4ee497ab1fad01d6819206395c10fd794010ed8c1d9198b19a4462` |
| Manifiesto del banco temporal (47 clips) | [`manifest.yaml`](https://github.com/Pandulc/e-ovrt_datasets/blob/main/datasets/processed/clip_bench/manifest.yaml) | `3f14f50a53c0d6c57b429378544dcfb6ed87fc942640db302c53ba1470001a75` |

Las huellas de los estratos del banco de imágenes viajan dentro de su
[manifiesto de composición](https://github.com/Pandulc/e-ovrt_datasets/blob/main/datasets/processed/coco/bench/curated/bench_v3_manifest.json)
(`source_sha256` por fuente); las del banco temporal, en
[`clip_bench.sha256`](https://github.com/Pandulc/e-ovrt_datasets/blob/main/datasets/processed/clip_bench/clip_bench.sha256).
Los conjuntos de prompts se identifican por el contenido de su archivo en
[`prompts/`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/HEAD/prompts).

## 2. Cada material del Anexo E, y dónde está

| Material (Anexo E, Tabla E.1) | Qué archivo es | Dónde vive | Cómo se comprueba |
|---|---|---|---|
| Banco de imágenes | `bench_v3.json` (COCO), su manifiesto de composición y la ficha de procedencia por fuente | [`e-ovrt_datasets` · `datasets/processed/coco/bench/curated/`](https://github.com/Pandulc/e-ovrt_datasets/tree/main/datasets/processed/coco/bench/curated) · [ficha `bench_v3`](https://github.com/Pandulc/e-ovrt_datasets/blob/main/datasets/registry/bench_v3.md) | Huella de la tabla anterior; el generador del banco reproduce los estratos byte a byte ([`build_bench_v3.py`](https://github.com/Pandulc/e-ovrt_datasets/blob/main/datasets/scripts/curate/build_bench_v3.py)) |
| Vocabulario (conjuntos de prompts) | `cr01_cr02_v2_short.yaml` (el congelado del rodaje y del banco), `eind_v1.yaml`, `edir_v1.yaml` | [`e-ovrt_experimental-setup` · `prompts/`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/HEAD/prompts) | El contenido del archivo, no su nombre, es lo que identifica la corrida |
| Banco temporal | `manifest.yaml`, la referencia temporal humana por clip (`gt/`) y las anotaciones exportadas (`annotations/`) | [`e-ovrt_datasets` · `datasets/processed/clip_bench/`](https://github.com/Pandulc/e-ovrt_datasets/tree/main/datasets/processed/clip_bench) | Huella de la tabla anterior; los videos no se publican (ver §4) |
| Configuración efectiva de un experimento | Manifiesto de la corrida: fuente, perfil del modelo, vocabulario, conjunto de patrones, instrumentación | [`e-ovrt_experimental-setup` · `experiments/`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/HEAD/experiments) · patrones en [`e-ovrt_control-plane` · `configs/patterns/`](https://github.com/Pandulc/e-ovrt_control-plane/tree/main/configs/patterns) | Parámetros solicitados contra parámetros aplicados, que la corrida conserva |
| Corrida de medios, de control y de distribución | Detecciones por unidad visual, eventos y alertas del patrón, registro de notificaciones: los artefactos primarios de cada corrida | Carpetas de corrida, que git ignora: están en la carpeta de evidencia con acceso autorizado (§4). Sus métricas y resúmenes, en `results/` | Relectura de las detecciones conservadas con la misma configuración; correspondencia alerta–intento–resultado |
| Resultados derivados | Métricas por clip, resúmenes por condición, escenario y estrato, con la campaña y la huella del banco al pie | [`e-ovrt_experimental-setup` · `results/`](https://github.com/simonll4/e-ovrt_experimental-setup/blob/HEAD/results/index.md): [imágenes](https://github.com/simonll4/e-ovrt_experimental-setup/blob/HEAD/results/bench_imagenes/index.md) · [estado por persona](https://github.com/simonll4/e-ovrt_experimental-setup/blob/HEAD/results/bench_nivel_a/index.md) · [alertas por episodio](https://github.com/simonll4/e-ovrt_experimental-setup/blob/HEAD/results/clip_bench/index.md) · [tiempo real](https://github.com/simonll4/e-ovrt_experimental-setup/blob/HEAD/results/realtime/index.md) | Coincidencia de numeradores, denominadores y reglas de agregación; cada tabla enlaza su artefacto (`metrics.json`, `campaign.yaml`) |
| Rama de ajuste fino | Manifiestos de los tramos, criterios pre-registrados y veredictos | [`e-ovrt_experimental-setup` · `finetuning/manifests/`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/HEAD/finetuning/manifests) | Los pesos no se publican; los veredictos remiten a su evaluación en `results/` |
| Empaquetado de la plataforma | Composición de los trece servicios y su documentación operativa | [`e-ovrt_experimental-setup` · `infra/platform/`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/HEAD/infra/platform) | `docker compose config` valida la composición; la construcción y el arranque integral están previstos antes de la presentación final |
| Procedencia y licencias de los datos | Registro de licencias y de descargas por fuente | [`e-ovrt_datasets` · `datasets/registry/`](https://github.com/Pandulc/e-ovrt_datasets/tree/main/datasets/registry) | Lo que el Anexo F declara por fuente |

## 3. Cómo se reproduce cada cosa

El Anexo E del informe describe la secuencia por material sin comandos. Los comandos
concretos están en el `README` de cada repositorio: construir el banco de imágenes y
verificar sus estratos, en `e-ovrt_datasets`; evaluar una corrida contra el banco, en
`e-ovrt_media-plane`; releer detecciones y evaluar alertas contra la referencia temporal,
en `e-ovrt_control-plane`; lanzar una corrida de punta a punta, en la consola de
`e-ovrt_experimental-setup`. Ver [`repositorios/`](../repositorios/README.md).

## 4. Material con acceso autorizado

No se publica ningún video ni imagen original (ver [`material-de-video.md`](material-de-video.md)).
Los clips del rodaje propio, los recortes del lote de obra real, las carpetas de corrida con
sus artefactos primarios y los pesos de la rama de ajuste fino se conservan en una **carpeta
de evidencia con acceso autorizado**. El enlace a esa carpeta se publica en esta sección al
cierre de la entrega; el acceso se solicita a los autores (datos de contacto en
[`CITATION.cff`](../CITATION.cff)).
