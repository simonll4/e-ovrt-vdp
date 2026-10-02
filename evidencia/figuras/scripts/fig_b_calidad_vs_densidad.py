#!/usr/bin/env python3
"""FIG-B — La ganancia de la identidad por sujeto sobrevive al tiempo real.

Qué muestra: para cada densidad de evidencia —30 fps del banco y las tres cadencias
que el camino en vivo sostuvo—, el F1 de episodios con granularidad de escena y de
sujeto (izquierda), y la ganancia del sujeto con su intervalo de confianza
(derecha). La lectura que la figura existe para fijar: **la ganancia excluye el cero
en las cuatro densidades**.

Fuentes:
  · F1 por campaña: los `metrics.json` de las ocho campañas del eje de densidad, leídos
    del artefacto —nunca transcritos— más el `stride` de cada `campaign.yaml`. Se
    verifican contra el índice publicado (`results/clip_bench/index.md`, eje de
    densidad); si divergen, el script falla.
  · Intervalos de la ganancia: bootstrap pareado por clip, publicado en
    `results/clip_bench/index.md` ("Lo que dicen estas filas"). No hay un artefacto
    legible por máquina con esos intervalos, así que van transcritos acá; el punto
    central de cada uno se verifica contra la resta de los F1 medidos.

Reglas de lectura (van en el pie de figura del markdown): se grafica F1 de episodios,
nunca el SDR, que no es comparable entre cadencias; los clips negativos no entran a
F1 (su métrica son los falsos positivos: 0 de 4 en las ocho campañas).

Uso:
    python3 fig_b_calidad_vs_densidad.py  (requiere matplotlib y PyYAML; ver README del directorio)
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from estilo import ANCHO_IN, coma, con_signo, franjas, generar  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

# Repo hermano `e-ovrt_experimental-setup` clonado al lado por defecto; EOVRT_RESULTS
# sobrescribe la ubicación de su carpeta `results/` (ver README del directorio).
_DEFAULT_RESULTS = Path(__file__).resolve().parents[4] / "e-ovrt_experimental-setup" / "results"
RESULTS = Path(os.environ.get("EOVRT_RESULTS", str(_DEFAULT_RESULTS)))
CLIP_BENCH = RESULTS / "clip_bench"
SALIDA = Path(__file__).resolve().parents[1] / "fig-b-calidad-vs-densidad"

FPS_NOMINAL = 30.0

# Filas de arriba hacia abajo: de la densidad del banco a la peor cadencia en vivo.
# (rótulo, descripción, campaña de escena, campaña de sujeto, en vivo)
FILAS = [
    ("30 fps", "referencia DBE · stride 1",
     "t1_gdinotiny560_v2short_scene", "g1_gdinotiny560_v2short_subject", False),
    ("4,29 fps", "techo en vivo · stride 7",
     "r1_gdinotiny560_v2short_scene_s7", "r2_gdinotiny560_v2short_subject_s7", True),
    ("2,00 fps", "lo que corrió el rodaje · stride 15",
     "r3_gdinotiny560_v2short_scene_s15", "r4_gdinotiny560_v2short_subject_s15", True),
    ("1,15 fps", "peor caso en vivo · stride 26",
     "r5_gdinotiny560_v2short_scene_s26", "r6_gdinotiny560_v2short_subject_s26", True),
]

# Verificación contra el índice publicado (F1 micro de episodios positivos), por fila.
ESPERADO_INDICE = [(0.789, 0.930), (0.794, 0.866), (0.738, 0.875), (0.646, 0.742)]

# Ganancia sujeto − escena e IC 95 % (bootstrap pareado por clip), transcritos de
# results/clip_bench/index.md. El punto se verifica contra los F1 medidos.
GANANCIA_IC = [(0.141, 0.032, 0.258), (0.072, 0.013, 0.145), (0.137, 0.032, 0.258), (0.096, 0.011, 0.202)]


def leer_campana(nombre: str) -> tuple[float, float]:
    """Devuelve (fps efectivos, F1 micro) leídos del artefacto de la campaña."""
    directorio = CLIP_BENCH / nombre
    metrics = json.loads((directorio / "metrics.json").read_text(encoding="utf-8"))
    campana = yaml.safe_load((directorio / "campaign.yaml").read_text(encoding="utf-8"))
    stride = int(campana.get("stride", 1))
    return FPS_NOMINAL / stride, float(metrics["positives"]["f1_micro"])


def leer_y_verificar() -> list[tuple[float, float]]:
    datos = []
    for (rotulo, _, escena, sujeto, _), esperado, (ganancia, *_ic) in zip(FILAS, ESPERADO_INDICE, GANANCIA_IC):
        _, f1_escena = leer_campana(escena)
        _, f1_sujeto = leer_campana(sujeto)
        medido = (round(f1_escena, 3), round(f1_sujeto, 3))
        if medido != esperado:
            raise SystemExit(f"FIG-B: a {rotulo} se midió {medido} pero el índice publica {esperado}. "
                             "La figura no puede contradecir la fuente citable.")
        if round(medido[1] - medido[0], 3) != ganancia:
            raise SystemExit(f"FIG-B: a {rotulo} la ganancia medida es {medido[1] - medido[0]:.3f} y la "
                             f"transcrita {ganancia}. Revisar el índice antes de dibujar.")
        datos.append((f1_escena, f1_sujeto))
    return datos


DATOS: list[tuple[float, float]] = []


def dibujar(t, tema):
    fig = plt.figure(figsize=(ANCHO_IN, 4.5))
    y_filas = [4, 3, 2, 1]
    ylim = (0.45, 4.65)
    abajo, alto = 0.13, 0.70

    # --- Rótulos de fila ---
    for y, (rotulo, desc, *_rest) in zip(y_filas, FILAS):
        yf = abajo + (y - ylim[0]) / (ylim[1] - ylim[0]) * alto
        fig.text(0.0, yf + 0.025, rotulo, fontsize=12, fontweight="bold", color=t["tinta"], va="center")
        fig.text(0.0, yf - 0.035, desc, fontsize=9.5, color=t["tinta_2"], va="center")

    # --- Cinta de las cadencias en vivo ---
    # Sus ejes van en pulgadas (escala 1:1) para que las franjas salgan a 45° en pantalla.
    ancho_cinta_in, alto_in = 0.12, alto * 4.5
    cinta = fig.add_axes([0.236, abajo, ancho_cinta_in / ANCHO_IN, alto])
    cinta.set_xlim(0, ancho_cinta_in)
    cinta.set_ylim(0, alto_in)
    cinta.axis("off")
    a_pulgadas = lambda y: (y - ylim[0]) / (ylim[1] - ylim[0]) * alto_in  # noqa: E731
    y_ini, y_fin = a_pulgadas(0.6), a_pulgadas(3.4)
    franjas(cinta, 0, y_ini, ancho_cinta_in, y_fin - y_ini, color=t["sujeto"], fondo=t["fondo"], paso=0.11)
    fig.text(0.258, abajo + (y_ini + y_fin) / 2 / alto_in * alto, "cadencias en vivo", rotation=90,
             fontsize=9.5, color=t["tinta_2"], ha="center", va="center")

    # --- Panel izquierdo: escena y sujeto unidos por su brecha ---
    ax = fig.add_axes([0.28, abajo, 0.385, alto])
    ax.set_xlim(0.60, 1.00)
    ax.set_ylim(*ylim)
    ax.set_xticks([0.6, 0.7, 0.8, 0.9, 1.0])
    ax.set_xticklabels(["0,6", "0,7", "0,8", "0,9", "1,0"])
    ax.set_yticks([])
    ax.grid(axis="x", color=t["grilla"], linewidth=1.0)
    for lado in ("top", "right", "left"):
        ax.spines[lado].set_visible(False)
    ax.spines["bottom"].set_color(t["grilla"])
    ax.tick_params(axis="x", length=0, pad=6)
    for y, (f1_escena, f1_sujeto) in zip(y_filas, DATOS):
        ax.plot([f1_escena, f1_sujeto], [y, y], color=t["tinta_3"], linewidth=2.6, solid_capstyle="round", zorder=2)
        ax.plot(f1_escena, y, "o", markersize=11, color=t["escena"], markeredgecolor=t["fondo"],
                markeredgewidth=2.0, zorder=3)
        ax.plot(f1_sujeto, y, "s", markersize=10, color=t["sujeto"], markeredgecolor=t["fondo"],
                markeredgewidth=2.0, zorder=3)
    # Valores sólo en la fila de referencia: el resto está en la tabla de resultados.
    f1_escena, f1_sujeto = DATOS[0]
    ax.text(f1_escena - 0.012, 4, coma(f1_escena), ha="right", va="center", fontsize=10, color=t["tinta_2"])
    ax.text(f1_sujeto + 0.012, 4, coma(f1_sujeto), ha="left", va="center", fontsize=10, color=t["tinta_2"])
    ax.text(0.0, 1.10, "F1 de episodios", transform=ax.transAxes, fontsize=11, fontweight="bold",
            color=t["tinta"], va="center")
    ax.legend(
        handles=[
            Line2D([], [], marker="o", linestyle="none", markersize=9, color=t["escena"], label="escena"),
            Line2D([], [], marker="s", linestyle="none", markersize=8.5, color=t["sujeto"], label="sujeto"),
        ],
        loc="center left", bbox_to_anchor=(0.36, 1.10), ncol=2, fontsize=10, labelcolor=t["tinta_2"],
        handletextpad=0.3, columnspacing=1.2, borderaxespad=0,
    )

    # --- Panel derecho: la ganancia y su intervalo; la línea del cero es la lectura ---
    bx = fig.add_axes([0.715, abajo, 0.115, alto])
    bx.set_xlim(-0.04, 0.30)
    bx.set_ylim(*ylim)
    bx.set_xticks([0.0, 0.1, 0.2, 0.3])
    bx.set_xticklabels(["0", "0,1", "0,2", "0,3"])
    bx.set_yticks([])
    for lado in ("top", "right", "left"):
        bx.spines[lado].set_visible(False)
    bx.spines["bottom"].set_color(t["grilla"])
    bx.tick_params(axis="x", length=0, pad=6)
    bx.axvline(0.0, color=t["tinta_2"], linewidth=1.3, zorder=1)
    for y, (ganancia, inferior, superior) in zip(y_filas, GANANCIA_IC):
        bx.plot([inferior, superior], [y, y], color=t["sujeto"], linewidth=2.6, solid_capstyle="round", zorder=2)
        bx.plot(ganancia, y, "D", markersize=7.5, color=t["sujeto"], markeredgecolor=t["fondo"],
                markeredgewidth=1.8, zorder=3)
        bx.text(1.08, y + 0.13, con_signo(ganancia), transform=bx.get_yaxis_transform(), fontsize=11,
                fontweight="bold", color=t["tinta"], va="center", ha="left")
        bx.text(1.08, y - 0.2, f"[{con_signo(inferior)}; {con_signo(superior)}]", transform=bx.get_yaxis_transform(),
                fontsize=9.5, color=t["tinta_2"], va="center", ha="left")
    bx.text(0.0, 1.10, "ganancia del sujeto (IC 95 %)", transform=bx.transAxes, fontsize=11,
            fontweight="bold", color=t["tinta"], va="center")
    return fig


if __name__ == "__main__":
    DATOS.extend(leer_y_verificar())
    for (rotulo, *_rest), (e, s) in zip(FILAS, DATOS):
        print(f"{rotulo}: escena {e:.3f} · sujeto {s:.3f} · ganancia {s - e:+.3f}")
    print("verificado contra results/clip_bench/index.md (eje de densidad y ganancias)")
    raise SystemExit(generar(dibujar, SALIDA))
