#!/usr/bin/env python3
"""Guardián de las reglas de contenido del repo e-ovrt-vdp.

Reglas (ver CONTRIBUTING.md):
  (a) ningún patrón de referencia interna en los .md;
  (b) todo enlace relativo resuelve a un archivo/carpeta del repo;
  (c) toda fila con cifra en resultados/README.md enlaza a results/ o finetuning/;
  (d) toda imagen referenciada existe.
Uso: python3 herramientas/verificar.py [--raiz DIR] [--json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PATRONES_PROHIBIDOS: list[tuple[str, str]] = [
    (r"\.\./docs/", "ruta al set documental interno"),
    (r"\bdocs/(operacion|nucleo|decisiones|informe|sintesis|specs)\b", "ruta al set documental interno"),
    (r"\boperacion/\d", "referencia a bitácora interna"),
    (r"\bnucleo/\d", "referencia a documento interno de núcleo"),
    (r"\bADR-\d", "referencia a registro de decisión interno"),
    (r"\bF-\d", "identificador interno de hallazgo"),
    (r"\bD-\d", "identificador interno de decisión"),
    (r"\bAJ-\d", "ficha interna de ajuste"),
    (r"\bR-\d\d", "redline interno"),
    (r"\bPODA-", "ficha interna de poda"),
    (r"\bT-FT-", "identificador interno de tarea"),
    (r"\[\[PENDIENTE", "marcador de borrador"),
    (r"\[\[FIGURA", "marcador de borrador"),
    (r"\[\[CIFRA", "marcador de borrador"),
    (r"/home/", "ruta absoluta de una máquina"),
    (r"\bAF-\d", "identificador interno de conclusión"),
    (r"\bE[34]-\d", "identificador interno de corrección"),
    (r"\bD-P\d", "identificador interno de decisión de pase"),
    (r"\b[Dd]ocs? \d{2,3}\b", "referencia a documento interno por número"),
]
_COMPILADOS = [(re.compile(rx), desc) for rx, desc in PATRONES_PROHIBIDOS]

PERMITIR = "<!-- verificar:permitir -->"
EXCLUIR = {"PUBLICAR.md"}


def archivos_md(raiz: Path) -> list[Path]:
    out = []
    for p in sorted(raiz.rglob("*.md")):
        if ".git" in p.relative_to(raiz).parts:
            continue
        if p.name in EXCLUIR:
            continue
        out.append(p)
    return out


def _violacion(raiz: Path, archivo: Path, linea: int, regla: str, texto: str) -> dict:
    return {
        "archivo": archivo.relative_to(raiz).as_posix(),
        "linea": linea,
        "regla": regla,
        "texto": texto.rstrip("\n"),
    }


def revisar_patrones(raiz: Path) -> list[dict]:
    violaciones = []
    for archivo in archivos_md(raiz):
        for n, linea in enumerate(archivo.read_text(encoding="utf-8").splitlines(), start=1):
            if PERMITIR in linea:
                continue
            for rx, desc in _COMPILADOS:
                if rx.search(linea):
                    # una violación por línea: el primer patrón que matchea alcanza para señalarla
                    violaciones.append(_violacion(raiz, archivo, n, f"(a) {desc}: {rx.pattern}", linea))
                    break
    return violaciones


ENLACE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
IMAGEN = re.compile(r"!\[[^\]]*\]\(([^)\s]+)")
_EXTERNO = ("http://", "https://", "mailto:")


def _destinos_relativos(linea: str, rx: re.Pattern) -> list[str]:
    out = []
    for destino in rx.findall(linea):
        if destino.startswith(_EXTERNO) or destino.startswith("#"):
            continue
        out.append(destino.split("#", 1)[0])
    return out


def _revisar_destinos(raiz: Path, rx: re.Pattern, etiqueta: str) -> list[dict]:
    violaciones = []
    for archivo in archivos_md(raiz):
        for n, linea in enumerate(archivo.read_text(encoding="utf-8").splitlines(), start=1):
            for destino in _destinos_relativos(linea, rx):
                if not (archivo.parent / destino).exists():
                    violaciones.append(_violacion(raiz, archivo, n, f"{etiqueta} destino inexistente: {destino}", linea))
    return violaciones


def revisar_enlaces(raiz: Path) -> list[dict]:
    return _revisar_destinos(raiz, ENLACE, "(b)")


def revisar_imagenes(raiz: Path) -> list[dict]:
    return _revisar_destinos(raiz, IMAGEN, "(d)")


CIFRA = re.compile(r"\d+,\d+|\bp95\b|\bn\s*=\s*\d")
ENLACE_FUENTE = re.compile(
    r"https://github\.com/simonll4/e-ovrt_experimental-setup/blob/[^/\s)]+/(results|finetuning)/"
)
ARCHIVO_CIFRAS = Path("resultados/README.md")
_SEPARADOR = re.compile(r"^\|\s*[-:]")


def _es_encabezado(lineas: list[str], i: int) -> bool:
    for siguiente in lineas[i + 1:]:
        if siguiente.strip():
            return bool(_SEPARADOR.match(siguiente))
    return False


def revisar_cifras(raiz: Path) -> list[dict]:
    archivo = raiz / ARCHIVO_CIFRAS
    if not archivo.exists():
        return []
    lineas = archivo.read_text(encoding="utf-8").splitlines()
    violaciones = []
    for i, linea in enumerate(lineas):
        if not linea.lstrip().startswith("|") or _SEPARADOR.match(linea) or _es_encabezado(lineas, i):
            continue
        if CIFRA.search(linea) and not ENLACE_FUENTE.search(linea):
            violaciones.append(_violacion(raiz, archivo, i + 1, "(c) fila con cifra sin enlace a results/ o finetuning/", linea))
    return violaciones


def revisar_todo(raiz: Path) -> list[dict]:
    return revisar_patrones(raiz) + revisar_enlaces(raiz) + revisar_cifras(raiz) + revisar_imagenes(raiz)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--raiz", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--json", action="store_true", help="salida JSON")
    args = parser.parse_args(argv)
    violaciones = revisar_todo(args.raiz.resolve())
    if args.json:
        print(json.dumps(violaciones, ensure_ascii=False, indent=2))
    elif violaciones:
        for v in violaciones:
            print(f"{v['archivo']}:{v['linea']}: {v['regla']} — {v['texto']}")
        print(f"{len(violaciones)} violaciones")
    else:
        print("OK: 0 violaciones")
    return 1 if violaciones else 0


if __name__ == "__main__":
    sys.exit(main())
