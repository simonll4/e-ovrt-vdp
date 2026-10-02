# Los cinco repositorios de código

Son repositorios independientes que se clonan **como hermanos dentro de una misma carpeta**:
varias configuraciones usan rutas relativas entre ellos (`../e-ovrt_datasets/...`). Todos
tienen el trabajo integrado en `main`, que es su rama por defecto.

```bash
mkdir e-ovrt && cd e-ovrt
for r in simonll4/e-ovrt_media-plane Pandulc/e-ovrt_control-plane \
         simonll4/e-ovrt_alert-distribution simonll4/e-ovrt_experimental-setup \
         Pandulc/e-ovrt_datasets; do
  git clone "https://github.com/$r.git"
done
```

| Repositorio | Plano o rol | Python | Puerto |
|---|---|---|---|
| [e-ovrt_media-plane](#e-ovrt_media-plane--plano-de-medios) | plano de medios | 3.12 | `:8080` |
| [e-ovrt_control-plane](#e-ovrt_control-plane--plano-de-control) | plano de control | 3.11 o superior | `:8081` |
| [e-ovrt_alert-distribution](#e-ovrt_alert-distribution--distribución-de-alertas) | distribución de alertas | 3.11 | `:8082` |
| [e-ovrt_experimental-setup](#e-ovrt_experimental-setup--experimentos-resultados-y-consola) | experimentos, resultados y consola | 3.11 | `:8090` |
| [e-ovrt_datasets](#e-ovrt_datasets--datos) | datos y bancos | 3.x | — |

Cómo se comprobó que todas las suites corren, con el resultado de cada una:
[`evidencia/verificacion.md`](../evidencia/verificacion.md).

## e-ovrt_media-plane — plano de medios

<https://github.com/simonll4/e-ovrt_media-plane>

Servicio de inferencia open-vocabulary (FastAPI, HTTP y WebSocket). Ingiere carpetas de
imágenes, video, RTSP y OAK-D; carga el modelo una sola vez (`EOVRT_MODEL_REF`); mantiene una
corrida activa a la vez y publica `media.detection.v1` por archivo o por bus.

```bash
python3.12 -m venv .venv && source .venv/bin/activate && pip install -e ".[gpu,dev]"
make download-models
EOVRT_MODEL_REF=mock make serve      # :8080, sin GPU
make test
```

## e-ovrt_control-plane — plano de control

<https://github.com/Pandulc/e-ovrt_control-plane>

Motor de patrones CR-01 / CR-02 sobre `media.detection.v1`: identidad por sujeto,
estrategias de evidencia (E-IND, E-DIR y sus fusiones), persistencia temporal y alertas
confirmadas al bus `:5558`. Incluye el evaluador de alertas contra la referencia temporal.

```bash
python3.11 -m venv .venv && .venv/bin/pip install -e ".[dev]"
.venv/bin/eovrt-control serve --port 8081          # servicio
.venv/bin/eovrt-control replay --config <cfg>      # camino offline
python3 -m pytest tests/ -q --ignore=tests/labs
```

## e-ovrt_alert-distribution — distribución de alertas

<https://github.com/simonll4/e-ovrt_alert-distribution>

Consume las alertas confirmadas, aplica la política de notificación y las entrega por MQTT
QoS 1 con un registro idempotente. Es un servicio HTTP (`eovrt-distribute serve`) y conserva
la CLI `replay` / `live`.

```bash
python3.11 -m venv .venv && .venv/bin/pip install -e ".[service]"
.venv/bin/eovrt-distribute serve --host 127.0.0.1 --port 8082
.venv/bin/python -m pytest -q
```

## e-ovrt_experimental-setup — experimentos, resultados y consola

<https://github.com/simonll4/e-ovrt_experimental-setup>

- `prompts/`: los conjuntos de prompts, incluido el congelado para el rodaje y el banco.
- `experiments/`: los manifiestos de experimento.
- **`results/`: los cuatro índices de cifras del proyecto.**
- `webconsole/`: la consola web (React + FastAPI BFF, `:8090`).
- `infra/platform/`: el `docker compose` integral de 13 servicios.
- `finetuning/`: recetas Slurm/Apptainer y manifiestos de la jornada de ajuste fino.
- `defensa/`: el renderizador de los videos.

```bash
python3.11 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
cd webconsole && make install && make serve        # requiere el plano de medios arriba
```

Pruebas: `.venv/bin/python -m pytest tests/` · `.venv/bin/python -m pytest finetuning/tests/` ·
`cd webconsole/backend && ../../.venv/bin/python -m pytest` · `cd webconsole/frontend && npm test`.

## e-ovrt_datasets — datos

<https://github.com/Pandulc/e-ovrt_datasets>

Descarga, validación y conversión (COCO, YOLO y ODVG) a la vista canónica `canonical_v2`
(`person`, `helmet`, `vest`, `bare_head`); construcción y verificación byte a byte del banco
`bench_v3`; registro de licencias y procedencia. Las imágenes crudas no se versionan.

```bash
pip install -r requirements.txt
python3 datasets/scripts/convert/convert_datasets.py \
    --datasets construction_site_safety chv ppe_siabar shel5k --views canonical_v2
python3 -m pytest datasets/tests/ -q
```

## Versiones citadas en el informe

Se completa al congelar, con el tag `informe-2026` en cada repositorio. Hasta entonces, los
enlaces `blob/HEAD/` de este repositorio resuelven a `main`.

| Repositorio | Rama | Tag | Commit | Fecha |
|---|---|---|---|---|
| e-ovrt_media-plane | `main` | `informe-2026` | *(al congelar)* | |
| e-ovrt_control-plane | `main` | `informe-2026` | | |
| e-ovrt_alert-distribution | `main` | `informe-2026` | | |
| e-ovrt_experimental-setup | `main` | `informe-2026` | | |
| e-ovrt_datasets | `main` | `informe-2026` | | |
