# Verificación: las suites de los cinco repos

Corridas el **2026-08-25** en el workspace de desarrollo, con los comandos exactos de abajo.
No son cifras copiadas de una foto anterior.

| Repo / módulo | Comando | Resultado |
|---|---|---|
| e-ovrt_datasets | `python3 -m pytest datasets/tests/ -q` (corrió con el `python3` del sistema; no hizo falta el venv de respaldo) | `431 passed in 1.19s` |
| e-ovrt_media-plane | `.venv/bin/python -m pytest -q` | `665 passed, 5 skipped, 2 warnings in 32.89s` |
| e-ovrt_control-plane | `.venv/bin/python -m pytest tests/ -q --ignore=tests/labs` | `312 passed, 2 warnings in 5.76s` |
| e-ovrt_alert-distribution | `.venv/bin/python -m pytest -q` (la integración MQTT real queda deseleccionada por defecto) | `133 passed, 1 deselected, 1 warning in 3.52s` |
| e-ovrt_experimental-setup — runner | `.venv/bin/python -m pytest tests/ -q` | `88 passed in 0.91s` |
| e-ovrt_experimental-setup — fine-tuning | `.venv/bin/python -m pytest finetuning/tests/ -q` | `46 passed in 0.89s` |
| webconsole — backend (BFF) | `cd webconsole/backend && ../../.venv/bin/python -m pytest -q` | `1 failed, 667 passed in 74.62s` |
| webconsole — frontend | `cd webconsole/frontend && npm test` | `Test Files  55 passed (55)` / `Tests  387 passed (387)` |
| **Total** | | **2.729 tests pasados** |

La única falla del día está en el BFF: `tests/test_stream_proxy.py::test_ws_preview_reenvia_binario`,
con `concurrent.futures._base.CancelledError` en el cierre del proxy de streaming. No se reintentó
ni se maquilló; queda anotada tal como salió. Los 5 casos saltados en media-plane y el 1 deseleccionado
en alert-distribution (la integración MQTT real, que exige un broker vivo) tampoco entran en el total
de pasados.

Además, este repo se verifica con `python3 herramientas/verificar.py` (reglas de contenido) y
`python -m pytest herramientas/tests -q` (38 tests del guardián).
