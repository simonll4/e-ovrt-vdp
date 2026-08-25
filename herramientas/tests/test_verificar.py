from pathlib import Path

import json
import pytest

from herramientas import verificar


def _repo(tmp_path: Path, archivos: dict[str, str]) -> Path:
    for rel, contenido in archivos.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(contenido, encoding="utf-8")
    return tmp_path


def test_archivos_md_excluye_publicar_y_git(tmp_path):
    raiz = _repo(tmp_path, {
        "README.md": "# hola\n",
        "PUBLICAR.md": "operacion/128\n",
        ".git/x.md": "operacion/1\n",
        "plataforma/01.md": "texto\n",
    })
    nombres = [p.relative_to(raiz).as_posix() for p in verificar.archivos_md(raiz)]
    assert nombres == ["README.md", "plataforma/01.md"]


@pytest.mark.parametrize("linea", [
    "ver ../docs/informe/x.md",
    "según docs/operacion/128",
    "consta en operacion/97 §1",
    "nucleo/14 lo describe",
    "decidido en ADR-011",
    "hallazgo F-96.4",
    "decisión D-113.1",
    "ficha AJ-4.02",
    "redline R-13",
    "PODA-03",
    "tarea T-FT-016",
    "[[PENDIENTE: url]]",
    "[[FIGURA B]]",
    "[[CIFRA]]",
    "en /home/simonll4/projects/x",
    "escala AF-3",
    "ítem E3-22",
    "decisión D-P3-6",
    "según doc 71",
])
def test_detecta_cada_patron_prohibido(tmp_path, linea):
    raiz = _repo(tmp_path, {"a.md": f"ok\n{linea}\n"})
    v = verificar.revisar_patrones(raiz)
    assert len(v) == 1
    assert v[0]["archivo"] == "a.md"
    assert v[0]["linea"] == 2
    assert v[0]["texto"] == linea


@pytest.mark.parametrize("linea", [
    "la carpeta docs/ de e-ovrt_experimental-setup",
    "condición CR-01 y CR-02",
    "campaña D1 y estrato B",
    "limitación L1",
    "prompt E-DIR y E-IND",
    "Figura E",
    "contrato media.detection.v1",
    "§17.3.8.2 del informe",
])
def test_no_marca_vocabulario_legitimo(tmp_path, linea):
    raiz = _repo(tmp_path, {"a.md": linea + "\n"})
    assert verificar.revisar_patrones(raiz) == []


def test_marcador_permitir_exime_la_linea(tmp_path):
    raiz = _repo(tmp_path, {"a.md": "ver operacion/128 <!-- verificar:permitir -->\n"})
    assert verificar.revisar_patrones(raiz) == []


def test_publicar_md_esta_exento(tmp_path):
    raiz = _repo(tmp_path, {"PUBLICAR.md": "operacion/128 y /home/x\n"})
    assert verificar.revisar_patrones(raiz) == []


def test_enlace_relativo_existente_pasa(tmp_path):
    raiz = _repo(tmp_path, {
        "README.md": "ver [la guía](plataforma/01.md) y [ancla](plataforma/01.md#seccion) y [carpeta](evidencia/)\n",
        "plataforma/01.md": "# x\n",
        "evidencia/.gitkeep": "",
    })
    assert verificar.revisar_enlaces(raiz) == []


def test_enlace_relativo_roto_falla(tmp_path):
    raiz = _repo(tmp_path, {"README.md": "ver [x](no/existe.md)\n"})
    v = verificar.revisar_enlaces(raiz)
    assert len(v) == 1 and v[0]["linea"] == 1 and "no/existe.md" in v[0]["regla"]


def test_enlaces_externos_mailto_y_anclas_se_ignoran(tmp_path):
    raiz = _repo(tmp_path, {
        "README.md": "[a](https://github.com/x) [b](http://x) [c](mailto:x@y) [d](#local)\n",
    })
    assert verificar.revisar_enlaces(raiz) == []


def test_enlace_relativo_al_padre_del_archivo(tmp_path):
    raiz = _repo(tmp_path, {
        "plataforma/02.md": "![fig](../evidencia/figuras/fig-a.png)\n",
        "evidencia/figuras/fig-a.png": "png",
    })
    assert verificar.revisar_enlaces(raiz) == []
    assert verificar.revisar_imagenes(raiz) == []


def test_imagen_inexistente_falla(tmp_path):
    raiz = _repo(tmp_path, {"a.md": "![fig](figuras/nada.png)\n"})
    v = verificar.revisar_imagenes(raiz)
    assert len(v) == 1 and v[0]["regla"].startswith("(d)")


RES = "https://github.com/simonll4/e-ovrt_experimental-setup/blob/HEAD/results/clip_bench/index.md"
FT = "https://github.com/simonll4/e-ovrt_experimental-setup/blob/HEAD/finetuning/manifests/x.json"


def test_fila_con_cifra_y_enlace_a_results_pasa(tmp_path):
    raiz = _repo(tmp_path, {"resultados/README.md":
        "| Qué | Cifra | Fuente |\n|---|---|---|\n"
        f"| G1 | F1 **0,930** (n=34) | [clip_bench]({RES}) |\n"
        f"| FT | bare_head 0,0909 | [manifest]({FT}) |\n"})
    assert verificar.revisar_cifras(raiz) == []


def test_fila_con_cifra_sin_enlace_falla(tmp_path):
    raiz = _repo(tmp_path, {"resultados/README.md":
        "| Qué | Cifra |\n|---|---|\n| G1 | F1 0,930 |\n| p95 | 64,534 ms |\n"})
    v = verificar.revisar_cifras(raiz)
    assert [x["linea"] for x in v] == [3, 4]
    assert all(x["regla"].startswith("(c)") for x in v)


def test_encabezado_con_p95_o_n_no_se_marca(tmp_path):
    raiz = _repo(tmp_path, {"resultados/README.md":
        "| Tramo | p95 | n= |\n|---|---|---|\n"
        f"| distribución | 64,534 ms | [x]({RES}) |\n"})
    assert verificar.revisar_cifras(raiz) == []


def test_cifras_solo_aplica_a_resultados(tmp_path):
    raiz = _repo(tmp_path, {"plataforma/02.md": "| a | 0,5 |\n|---|---|\n| b | 0,930 |\n"})
    assert verificar.revisar_cifras(raiz) == []


def test_enlace_a_otro_repo_no_cuenta_como_fuente(tmp_path):
    raiz = _repo(tmp_path, {"resultados/README.md":
        "| a | b |\n|---|---|\n| G1 | 0,930 [x](https://github.com/simonll4/e-ovrt_media-plane) |\n"})
    assert len(verificar.revisar_cifras(raiz)) == 1


def test_revisar_todo_concatena(tmp_path):
    raiz = _repo(tmp_path, {
        "a.md": "operacion/1 y [x](no.md) y ![f](no.png)\n",
        "resultados/README.md": "| a | b |\n|---|---|\n| c | 0,5 |\n",
    })
    reglas = sorted(v["regla"][:3] for v in verificar.revisar_todo(raiz))
    assert reglas == ["(a)", "(b)", "(b)", "(c)", "(d)"]


def test_main_exit_code_y_salida(tmp_path, capsys):
    raiz = _repo(tmp_path, {"a.md": "limpio\n"})
    assert verificar.main(["--raiz", str(raiz)]) == 0
    assert "OK: 0 violaciones" in capsys.readouterr().out
    raiz2 = _repo(tmp_path / "otro", {"a.md": "operacion/1\n"})
    assert verificar.main(["--raiz", str(raiz2)]) == 1
    assert "a.md:1:" in capsys.readouterr().out


def test_main_json(tmp_path, capsys):
    raiz = _repo(tmp_path, {"a.md": "ADR-011\n"})
    assert verificar.main(["--raiz", str(raiz), "--json"]) == 1
    datos = json.loads(capsys.readouterr().out)
    assert datos[0]["archivo"] == "a.md" and datos[0]["linea"] == 1
