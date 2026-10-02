# Verificación: las suites de los cinco repositorios

Corridas el **2026-10-02** en el entorno de desarrollo, una después de la otra, con los
comandos exactos de abajo y sobre el commit de `main` que indica la tabla. Lo que se informa
es la última línea de cada suite, tal como salió: no se reintentó nada ni se descontó ninguna
falla.

| Repositorio o módulo | Commit | Comando | Resultado |
|---|---|---|---|
| e-ovrt_datasets | `9a9fb842` | `python3 -m pytest datasets/tests/ -q` | `431 passed in 1.70s` |
| e-ovrt_media-plane | `7fabbc9` | `.venv/bin/python -m pytest -q` | `665 passed, 5 skipped, 2 warnings in 41.47s` |
| e-ovrt_control-plane | `a0f9f89` | `.venv/bin/python -m pytest tests/ -q --ignore=tests/labs` | `312 passed, 2 warnings in 6.68s` |
| e-ovrt_alert-distribution | `eccd202` | `.venv/bin/python -m pytest -q` | `133 passed, 1 deselected, 1 warning in 4.06s` |
| e-ovrt_experimental-setup · runner | `a74bb57` | `.venv/bin/python -m pytest tests/ -q` | `88 passed in 1.34s` |
| e-ovrt_experimental-setup · fine-tuning | `a74bb57` | `.venv/bin/python -m pytest finetuning/tests/ -q` | `46 passed in 1.45s` |
| webconsole · backend (BFF) | `a74bb57` | `cd webconsole/backend && ../../.venv/bin/python -m pytest -q` | `1 failed, 932 passed in 183.22s` |
| webconsole · frontend | `a74bb57` | `cd webconsole/frontend && npm test` | `Test Files 76 passed (76)` · `Tests 541 passed (541)` |
| **Total** | | | **3.148 pruebas pasadas · 1 fallida** |

## La falla, tal como salió

`tests/test_experiment_history.py::test_missing_alert_file_is_not_zero_alerts`, en el BFF:
`assert 502 == 404`. La prueba borra el archivo de alertas consolidado de un experimento
histórico y espera un 404; el BFF, ante ese faltante, consulta las alertas en vivo al plano de
control, y sin ese servicio levantado responde 502. Se reprodujo igual al correrla sola, así que
no es intermitente. Queda anotada como salió.

La falla que registró la corrida anterior (2026-08-25, en el proxy de streaming del BFF) no se
repitió. Los 5 casos saltados de media-plane y el caso deseleccionado de alert-distribution —la
integración MQTT real, que exige un broker vivo— no entran en el total de pasadas.

## Este repositorio

Las reglas de contenido de este repositorio se verifican con
`python3 herramientas/verificar.py` (cero violaciones) y su guardián tiene sus propias pruebas:
`python3 -m pytest herramientas/tests -q`. Las reglas están en
[`CONTRIBUTING.md`](../CONTRIBUTING.md).
