# Los cinco repositorios de código

Son repos independientes que se clonan **como hermanos en una misma carpeta**: varias
configuraciones usan rutas relativas entre ellos (`../e-ovrt_datasets/...`).

## Fichas
### e-ovrt_media-plane — plano de medios
- https://github.com/simonll4/e-ovrt_media-plane
- Servicio de inferencia open-vocabulary (FastAPI, HTTP/WS). Ingesta de carpeta de imágenes,
  video, RTSP y OAK-D; el modelo se carga una vez (`EOVRT_MODEL_REF`); una corrida activa a la
  vez; publica `media.detection.v1` por archivo o por bus.
- Correr: `python3.12 -m venv .venv && source .venv/bin/activate && pip install -e ".[gpu,dev]"` ·
  `make download-models` · `EOVRT_MODEL_REF=mock make serve` (`:8080`).
- Tests: `make test`.
### e-ovrt_control-plane — plano de control
- https://github.com/Pandulc/e-ovrt_control-plane
- Motor de patrones CR-01 / CR-02 sobre `media.detection.v1`: identidad por sujeto,
  estrategias de evidencia (E-IND, E-DIR, fusiones), persistencia temporal, alertas
  confirmadas al bus `:5558`; evaluador de alertas contra referencia temporal.
- Correr: `python3.11 -m venv .venv && .venv/bin/pip install -e ".[dev]"` ·
  `.venv/bin/eovrt-control serve --port 8081`; `.venv/bin/eovrt-control replay --config <cfg>`
  para el camino offline.
- Tests: `python3 -m pytest tests/ -q --ignore=tests/labs`.
### e-ovrt_alert-distribution — distribución de alertas
- https://github.com/simonll4/e-ovrt_alert-distribution
- Consumidor de alertas confirmadas; política de notificación; entrega MQTT QoS 1 con
  registro idempotente. Servicio HTTP `:8082` (`eovrt-distribute serve`) y CLI `replay`/`live`.
  Python 3.11.
- Correr: `python3.11 -m venv .venv && .venv/bin/pip install -e ".[service]"` ·
  `.venv/bin/eovrt-distribute serve --host 127.0.0.1 --port 8082`.
- Tests: `.venv/bin/python -m pytest -q`.
### e-ovrt_experimental-setup — experimentos, resultados y consola
- https://github.com/simonll4/e-ovrt_experimental-setup
- `prompts/` (prompt sets, incluido el congelado para el rodaje y el bench), `experiments/`
  (manifiestos), **`results/` (los cuatro índices de cifras del proyecto)**, `webconsole/`
  (React + FastAPI BFF, `:8090`), `infra/platform/` (compose integral de 13 servicios),
  `finetuning/` (recetas Slurm/Apptainer y manifiestos de la jornada de fine-tuning),
  `defensa/` (renderer de videos).
- Correr la consola: `cd webconsole && make install && make serve` (requiere el plano de
  medios arriba).
- Tests: `.venv/bin/python -m pytest tests/` · `finetuning/tests/` ·
  `cd webconsole/backend && ../../.venv/bin/python -m pytest` · `cd webconsole/frontend && npm test`.
### e-ovrt_datasets — datos
- https://github.com/Pandulc/e-ovrt_datasets
- Descarga, validación y conversión (COCO/YOLO/ODVG) a la vista canónica `canonical_v2`
  (`person`, `helmet`, `vest`, `bare_head`); construcción y verificación byte a byte del
  banco `bench_v3`; registro de licencias y procedencia. Las imágenes crudas no se versionan.
- Correr: `pip install -r requirements.txt` ·
  `python3 datasets/scripts/convert/convert_datasets.py --datasets construction_site_safety
  chv ppe_siabar shel5k --views canonical_v2`.
- Tests: `python3 -m pytest datasets/tests/ -q`.

## Versiones citadas en el informe
Se completa al congelar (tag `informe-2026` en cada repo). Hasta entonces, la rama de trabajo
es la rama por defecto en GitHub en `e-ovrt_media-plane` y `e-ovrt_experimental-setup` (los
enlaces `blob/HEAD/` resuelven a ella); en `e-ovrt_datasets` y `e-ovrt_control-plane` los
enlaces de este repositorio apuntan a la rama de trabajo por nombre.

| Repositorio | Rama de trabajo | Tag | Commit | Fecha |
|---|---|---|---|---|
| e-ovrt_media-plane | `feature/inference-service` | `informe-2026` | *(al congelar)* | |
| e-ovrt_control-plane | `feature/control-service` | `informe-2026` | | |
| e-ovrt_alert-distribution | `main` | `informe-2026` | | |
| e-ovrt_experimental-setup | `feature/webconsole-adopcion-front-design` | `informe-2026` | | |
| e-ovrt_datasets | `feature/datasets-v2-setup` | `informe-2026` | | |
