# Verificación: las suites de los cinco repositorios

Corridas el **2026-10-02** en el entorno de desarrollo, una después de la otra, con los
comandos exactos de abajo y sobre el commit que lleva el tag `informe-2026` de cada
repositorio: la versión que cita el informe. Lo que se informa es la última línea de cada
suite, tal como salió.

| Repositorio o módulo | Commit (`informe-2026`) | Comando | Resultado |
|---|---|---|---|
| e-ovrt_datasets | `9a9fb842` | `python3 -m pytest datasets/tests/ -q` | `431 passed in 1.70s` |
| e-ovrt_media-plane | `7fabbc9` | `.venv/bin/python -m pytest -q` | `665 passed, 5 skipped, 2 warnings in 41.47s` |
| e-ovrt_control-plane | `a0f9f89` | `.venv/bin/python -m pytest tests/ -q --ignore=tests/labs` | `312 passed, 2 warnings in 6.68s` |
| e-ovrt_alert-distribution | `eccd202` | `.venv/bin/python -m pytest -q` | `133 passed, 1 deselected, 1 warning in 4.06s` |
| e-ovrt_experimental-setup · runner | `01b0dda` | `.venv/bin/python -m pytest tests/ -q` | `88 passed in 1.56s` |
| e-ovrt_experimental-setup · fine-tuning | `01b0dda` | `.venv/bin/python -m pytest finetuning/tests/ -q` | `46 passed in 1.82s` |
| webconsole · backend (BFF) | `01b0dda` | `cd webconsole/backend && ../../.venv/bin/python -m pytest -q` | `934 passed in 153.96s` |
| webconsole · frontend | `01b0dda` | `cd webconsole/frontend && npm test` | `Test Files 76 passed (76)` · `Tests 541 passed (541)` |
| **Total** | | | **3.150 pruebas pasadas · 0 fallidas** |

Los 5 casos saltados de media-plane y el caso deseleccionado de alert-distribution —la
integración MQTT real, que exige un broker vivo— no entran en el total de pasadas.

## La falla que se arregló antes de congelar

La primera corrida del día dio una falla en el BFF:
`tests/test_experiment_history.py::test_missing_alert_file_is_not_zero_alerts`, con
`assert 502 == 404`. No era un error del BFF sino de la prueba, que dependía del entorno: al
faltar la copia consolidada de las alertas de un experimento histórico, el BFF las consulta
en vivo al plano de control, y la prueba no inyectaba uno falso. Pasaba sólo si había un plano
de control escuchando en `localhost:8081`; si no, la conexión vencía y la respuesta era 502.

El arreglo (`01b0dda`, sólo pruebas) la hace hermética con el plano de control falso que ya
usan las demás, y suma la prueba del otro camino: con el plano de control caído la respuesta
es 502. En los dos casos, nunca una lista vacía de alertas.

La falla que había registrado la corrida del 2026-08-25, en el proxy de streaming del BFF,
no volvió a aparecer.

## Este repositorio

Las reglas de contenido de este repositorio se verifican con
`python3 herramientas/verificar.py` (cero violaciones) y su guardián tiene sus propias pruebas:
`python3 -m pytest herramientas/tests -q`. Las reglas están en
[`CONTRIBUTING.md`](../CONTRIBUTING.md).
