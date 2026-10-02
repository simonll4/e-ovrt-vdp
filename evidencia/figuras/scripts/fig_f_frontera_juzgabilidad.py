#!/usr/bin/env python3
"""FIG-F — Frontera de juzgabilidad: escala × iluminación × oclusión.

Qué muestra: dónde el material de obra real deja de ser evaluable por la plataforma,
y por qué la respuesta NO se reduce a "sujetos chicos". Dos paneles:

  Panel A — mapa de calor: asociación de chaleco a cada `person` detectado, por clip y
  por banda de altura del sujeto, sobre las detecciones crudas de la campaña del lote
  de internet. Cruza los dos primeros ejes: la asociación crece con la escala, pero de
  noche colapsa a casi cualquier tamaño. Al costado, la referencia del rodaje propio.
  Una celda sin medir se dibuja vacía, nunca como cero.

  Panel B — F1 de CR-02 a Nivel A contra la altura mediana del sujeto, un punto por
  clip. Aparece el tercer eje: el clip de sujetos MÁS grandes rinde F1 0,084 porque
  es una cuadrilla apiñada con 58,5 % de personas solapadas. Tres de los cuatro clips
  son del piloto de 12 s (anotados, con Nivel A medido, pero fuera del banco temporal);
  `v06_c01` es del banco.

Las cifras van embebidas porque su fuente son tablas de análisis verificadas —no hay
`metrics.json` con la asociación por banda—. El Nivel A por clip está publicado en
`results/bench_nivel_a/index.md`.

Uso:
    python3 fig_f_frontera_juzgabilidad.py  (requiere matplotlib; ver README del directorio)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from estilo import ANCHO_IN, MONO, coma, generar, rampa  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import to_rgb  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

SALIDA = Path(__file__).resolve().parents[1] / "fig-f-frontera-juzgabilidad"

# --- Panel A ---------------------------------------------------------------------
# Asociación de `vest` a cada detección `person` (proxy: centro del vest dentro del
# torso). `None` es dato ausente: el tramo ≥320 px de v10 no se midió.
BANDAS = ["<80", "80–120", "120–160", "160–220", "220–320", "≥320"]
ASOCIACION = [
    ("v06", "diurno", [0.0, 10.8, 16.8, 57.0, 73.2, 41.4]),
    ("v10", "diurno", [0.0, 9.1, 14.1, 51.9, 62.9, None]),
    ("v04", "nocturno", [0.0, 0.0, 6.1, 8.7, 13.2, 55.1]),
]
# Régimen donde el rodaje validó la plataforma: mediana de altura 716–839 px y
# asociación 96–100 % (mismo modelo y clases, campaña T1).
RODAJE_ASOCIACION = (96, 100)
RODAJE_ALTURA = "716–839 px"

# --- Panel B ---------------------------------------------------------------------
# (clip, altura mediana px, F1 CR-02, del piloto de 12 s, nota, posición de la nota)
CLIPS = [
    ("video15_clip01", 173, 0.381, True, "el mejor: 0 % de estados\nno observables", (14, -2)),
    ("video16_clip10", 178, 0.080, True, None, None),
    ("v06_c01", 211, 0.002, False, None, None),
    ("video02_clip07", 370, 0.084, True, "los sujetos más grandes,\npero 58,5 % de personas\nsolapadas", (-14, 40)),
]
DESTACADO = "video02_clip07"


def luminancia(color) -> float:
    r, g, b = to_rgb(color)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def celda(ax, x, y, valor, t, tema, *, ancho=1.0, alto=1.0, texto=None):
    cmap = rampa(tema)
    if valor is None:
        ax.add_patch(FancyBboxPatch((x + 0.04, y + 0.04), ancho - 0.08, alto - 0.08,
                                    boxstyle="round,pad=0,rounding_size=0.08", facecolor="none",
                                    edgecolor=t["grilla"], linewidth=1.2, zorder=2))
        ax.text(x + ancho / 2, y + alto / 2, "sin medir", ha="center", va="center", fontsize=9,
                color=t["tinta_3"], zorder=3)
        return
    color = cmap(min(valor, 100) / 100)
    ax.add_patch(FancyBboxPatch((x + 0.04, y + 0.04), ancho - 0.08, alto - 0.08,
                                boxstyle="round,pad=0,rounding_size=0.08", facecolor=color,
                                edgecolor="none", zorder=2))
    claro = luminancia(color) > 0.5
    ax.text(x + ancho / 2, y + alto / 2, texto or f"{coma(valor, 1)} %", ha="center", va="center",
            fontsize=10, color="#1f2328" if claro else "#ffffff", zorder=3)


def dibujar(t, tema):
    fig = plt.figure(figsize=(ANCHO_IN, 4.6))

    # ---------------- Panel A ----------------
    ax = fig.add_axes([0.085, 0.20, 0.47, 0.60])
    ax.set_xlim(0, len(BANDAS) + 1.65)
    ax.set_ylim(0, len(ASOCIACION))
    ax.axis("off")
    for fila, (clip, momento, valores) in enumerate(ASOCIACION):
        y = len(ASOCIACION) - 1 - fila
        for col, valor in enumerate(valores):
            celda(ax, col, y, valor, t, tema)
        ax.text(-0.15, y + 0.62, clip, ha="right", va="center", fontsize=10.5, family=MONO, color=t["tinta"])
        ax.text(-0.15, y + 0.32, momento, ha="right", va="center", fontsize=9.5,
                color=t["tinta"] if momento == "nocturno" else t["tinta_2"],
                fontweight="bold" if momento == "nocturno" else "normal")
    for col, banda in enumerate(BANDAS):
        ax.text(col + 0.5, -0.18, banda, ha="center", va="top", fontsize=9.5, color=t["tinta_2"])
    ax.text(len(BANDAS) / 2, -0.62, "altura del sujeto (px, a 1080p)", ha="center", va="top", fontsize=10,
            color=t["tinta_2"])
    # Referencia del rodaje propio, separada: otro material, otra escala.
    x_ref, ancho_ref = len(BANDAS) + 0.35, 1.3
    celda(ax, x_ref, 0, sum(RODAJE_ASOCIACION) / 2, t, tema, ancho=ancho_ref, alto=len(ASOCIACION),
          texto=f"{RODAJE_ASOCIACION[0]}–{RODAJE_ASOCIACION[1]} %")
    ax.text(x_ref + ancho_ref / 2, -0.18, "rodaje\npropio", ha="center", va="top", fontsize=9.5,
            color=t["tinta_2"], linespacing=1.2)
    ax.text(x_ref + ancho_ref / 2, len(ASOCIACION) + 0.12, RODAJE_ALTURA, ha="center", va="bottom",
            fontsize=9, color=t["tinta_3"])
    fig.text(0.015, 0.93, "A · chaleco asociado a la persona detectada", fontsize=11.5, fontweight="bold",
             color=t["tinta"], va="center")

    # ---------------- Panel B ----------------
    bx = fig.add_axes([0.665, 0.20, 0.32, 0.60])
    bx.set_xlim(140, 400)
    bx.set_ylim(-0.02, 0.45)
    bx.set_xticks([160, 220, 280, 340, 400])
    bx.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4])
    bx.set_yticklabels(["0", "0,1", "0,2", "0,3", "0,4"])
    bx.grid(axis="y", color=t["grilla"], linewidth=1.0)
    for lado in ("top", "right", "left"):
        bx.spines[lado].set_visible(False)
    bx.spines["bottom"].set_color(t["grilla"])
    bx.tick_params(length=0, pad=6)
    bx.set_xlabel("altura mediana del sujeto (px)", fontsize=10, color=t["tinta_2"], labelpad=8)
    bx.set_ylabel("F1 de CR-02 (Nivel A)", fontsize=10, color=t["tinta_2"], labelpad=8)
    for clip, altura, f1, piloto, nota, desplazamiento in CLIPS:
        destacado = clip == DESTACADO
        color = t["sujeto"] if destacado else t["tinta_2"]
        bx.plot(altura, f1, "o", markersize=10 if destacado else 9,
                markerfacecolor="none" if piloto else color, markeredgecolor=color,
                markeredgewidth=2.0, zorder=3)
        # Los dos clips pegados al borde izquierdo llevan el rótulo hacia la derecha:
        # centrado, se monta sobre los números del eje.
        # El destacado lo lleva debajo: arriba le llega la línea guía de su nota.
        a_la_derecha = altura < 200
        if destacado:
            xy_rotulo, ha_rotulo, va_rotulo = (0, -12), "center", "top"
        else:
            xy_rotulo, ha_rotulo, va_rotulo = ((8, 9), "left", "baseline") if a_la_derecha else ((0, 11), "center", "baseline")
        bx.annotate(clip, (altura, f1), xytext=xy_rotulo, textcoords="offset points", ha=ha_rotulo, va=va_rotulo,
                    fontsize=9, family=MONO, color=t["tinta"])
        if nota:
            bx.annotate(nota, (altura, f1), xytext=desplazamiento, textcoords="offset points",
                        ha="right" if destacado else "left", va="top" if not destacado else "bottom",
                        fontsize=9.5, color=t["tinta"] if destacado else t["tinta_2"], linespacing=1.25,
                        arrowprops=dict(arrowstyle="-", color=t["tinta_3"], lw=1.0, shrinkA=2, shrinkB=7)
                        if destacado else None)
    bx.legend(
        handles=[
            Line2D([], [], marker="o", linestyle="none", markersize=8, markerfacecolor="none",
                   markeredgecolor=t["tinta_2"], markeredgewidth=2.0, label="piloto de 12 s"),
            Line2D([], [], marker="o", linestyle="none", markersize=8, color=t["tinta_2"], label="banco temporal"),
        ],
        loc="upper right", fontsize=9.5, labelcolor=t["tinta_2"], handletextpad=0.3, borderaxespad=0.2,
    )
    fig.text(0.60, 0.93, "B · la escala sola no ordena el resultado", fontsize=11.5, fontweight="bold",
             color=t["tinta"], va="center")
    return fig


if __name__ == "__main__":
    raise SystemExit(generar(dibujar, SALIDA))
