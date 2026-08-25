#!/usr/bin/env python3
"""FIG-F — Frontera de juzgabilidad: escala × iluminación × oclusión (§17.5).

Qué muestra: dónde el material deja de ser evaluable por la plataforma, y por qué la
respuesta NO se reduce a "sujetos chicos". Dos paneles que comparten lenguaje de color:

  Panel A — asociación de chaleco a cada `person` detectado, por banda de altura del
  sujeto. Cruza los dos primeros ejes: la asociación crece con la escala (eje 1) pero
  de noche colapsa a cualquier tamaño (eje 2). Es la medición sobre las detecciones
  crudas de la campaña I1 del lote de internet.

  Panel B — F1 de CR-02 contra altura mediana del sujeto, un punto por clip con GT
  humano y Nivel A medido. Aquí aparece el tercer eje: el clip de sujetos MÁS grandes
  del conjunto rinde F1 0,084 porque es una cuadrilla apiñada con 58,5 % de personas
  solapadas. La escala sola no ordena el resultado.

Las cifras van embebidas porque su fuente son tablas de documentos operativos
verificados —no hay `metrics.json` con la asociación por banda—; cada bloque declara
su documento de origen y la nota al pie de la figura lo repite.

Uso:
    python3 fig_f_frontera_juzgabilidad.py  (requiere matplotlib; ver README del directorio)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from estilo import (  # noqa: E402  — fija el backend Agg antes de importar pyplot
    ANCHO_COLUMNA_IN,
    AQUA,
    AZUL,
    BANDA,
    NARANJA,
    SUPERFICIE,
    TINTA,
    TINTA_2,
    TINTA_3,
    aplicar_estilo,
    guardar,
    limpiar_ejes,
    nota_al_pie,
)
import matplotlib.pyplot as plt  # noqa: E402

SALIDA = Path(__file__).resolve().parents[1] / "fig-f-frontera-juzgabilidad"

# --- Panel A -------------------------------------------------------------------
# Asociación de `vest` a cada detección `person` (proxy: centro del vest dentro del
# torso), sobre las detecciones crudas de la campaña I1. El "—" del original es dato
# ausente, no cero: se corta la serie, nunca se dibuja como 0.
BANDAS = ["<80", "80–120", "120–160", "160–220", "220–320", "≥320"]
CENTROS = [1, 2, 3, 4, 5, 6]

ASOCIACION = {
    "v06 · diurno": {
        "valores": [0.0, 10.8, 16.8, 57.0, 73.2, 41.4],
        "color": AZUL,
        "marcador": "o",
        "etiqueta_offset": (7, -6),
    },
    "v10 · diurno": {
        "valores": [0.0, 9.1, 14.1, 51.9, 62.9, None],
        "color": AQUA,  # contraste 2,74: exige la etiqueta directa que se dibuja abajo
        "marcador": "^",
        "etiqueta_offset": (-30, 26),  # arriba-izquierda: a la derecha se monta sobre la curva de v06
    },
    "v04 · nocturno": {
        "valores": [0.0, 0.0, 6.1, 8.7, 13.2, 55.1],
        "color": NARANJA,
        "marcador": "s",
        "etiqueta_offset": (7, 6),
    },
}

# Régimen donde el rodaje validó la plataforma: mediana de altura 716–839 px y
# asociación 96–100 % (mismo modelo y clases, campaña T1).
RODAJE_ASOCIACION = (96, 100)

# --- Panel B -------------------------------------------------------------------
# Los clips con GT humano y Nivel A medido. `oclusion` sólo está medida donde la
# fuente la reporta; `None` = no medida, y así se declara.
CLIPS = [
    # (etiqueta, altura mediana px, F1 CR-02, oclusión medida, nota, desplazamiento
    #  de la nota en puntos). Las notas se ubican a mano: con cuatro puntos y dos de
    #  ellos casi superpuestos en x, un desplazamiento uniforme produce choques.
    ("video15_clip01", 173, 0.381, None, "mejor del conjunto:\n0 % no observable para el humano", (14, -4)),
    ("video16_clip10", 178, 0.080, None, None, None),
    ("v06_c01", 211, 0.002, None, None, None),
    ("video02_clip07", 370, 0.084, 58.5, "sujetos MÁS grandes del conjunto,\npero 58,5 % de personas solapadas", (-8, -6)),
]


def main() -> int:
    aplicar_estilo()
    # Paneles apilados, no lado a lado: en el ancho de columna del informe (16 cm) dos
    # paneles dejan a las etiquetas de banda del panel A montadas unas sobre otras.
    fig, (ax_a, ax_b) = plt.subplots(
        2, 1, figsize=(ANCHO_COLUMNA_IN, 5.6), gridspec_kw={"height_ratios": [1.25, 1]}
    )

    # ---------------- Panel A: escala × iluminación ----------------
    ax_a.axhspan(RODAJE_ASOCIACION[0], RODAJE_ASOCIACION[1] + 4, color=BANDA, zorder=0, lw=0)
    ax_a.text(
        6.42,
        RODAJE_ASOCIACION[0] + 2,
        "régimen donde el rodaje validó la plataforma (96–100 %)",
        ha="right",
        va="center",
        fontsize=6.8,
        color=TINTA_3,
    )

    for etiqueta, cfg in ASOCIACION.items():
        xs = [c for c, v in zip(CENTROS, cfg["valores"]) if v is not None]
        ys = [v for v in cfg["valores"] if v is not None]
        ax_a.plot(
            xs,
            ys,
            color=cfg["color"],
            marker=cfg["marcador"],
            markersize=5,
            markeredgecolor=SUPERFICIE,
            markeredgewidth=1.2,
            label=etiqueta,
            zorder=3,
        )
        # Etiqueta directa para cada serie (obligatoria por la regla de relieve del
        # slot aqua, y aplicada a las tres para que el panel se lea sin la leyenda).
        ax_a.annotate(
            etiqueta.replace(" · ", "\n"),
            xy=(xs[-1], ys[-1]),
            xytext=cfg["etiqueta_offset"],
            textcoords="offset points",
            fontsize=6.8,
            color=cfg["color"],
            va="center",
            linespacing=1.3,
        )

    ax_a.set_xticks(CENTROS)
    ax_a.set_xticklabels(BANDAS, fontsize=7.5)
    ax_a.set_xlim(0.6, 6.9)
    ax_a.set_ylim(0, 105)
    ax_a.set_yticks([0, 25, 50, 75, 100])
    ax_a.set_yticklabels(["0", "25", "50", "75", "100 %"])
    ax_a.set_xlabel("altura del sujeto (px a 1080p)", fontsize=8)
    ax_a.set_ylabel("chaleco asociado al sujeto detectado", fontsize=8)
    ax_a.grid(axis="x", visible=False)
    limpiar_ejes(ax_a)
    ax_a.set_title("A · escala e iluminación", loc="left", fontsize=8.5, pad=7, color=TINTA)

    # ---------------- Panel B: el tercer eje ----------------
    for etiqueta, altura, f1, oclusion, nota, desplazamiento in CLIPS:
        destacado = oclusion is not None
        color = NARANJA if destacado else AZUL
        ax_b.scatter(
            [altura],
            [f1],
            s=68 if destacado else 46,
            color=color,
            edgecolor=SUPERFICIE,
            linewidth=1.4,
            zorder=3,
        )
        ax_b.annotate(
            etiqueta,
            xy=(altura, f1),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center",
            fontsize=7,
            color=TINTA_2,
        )
        if nota:
            dx, dy = desplazamiento
            ax_b.annotate(
                nota,
                xy=(altura, f1),
                xytext=(dx, dy),
                textcoords="offset points",
                ha="left" if dx > 0 else "right",
                va="center" if dy == 0 else "top",
                fontsize=6.8,
                color=color if destacado else TINTA_3,
                linespacing=1.4,
            )

    ax_b.set_xlim(140, 470)
    ax_b.set_ylim(-0.02, 0.52)
    ax_b.set_xticks([160, 220, 280, 340, 400])
    ax_b.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
    ax_b.set_yticklabels(["0", "0,1", "0,2", "0,3", "0,4", "0,5"])
    ax_b.set_xlabel("altura mediana del sujeto (px)", fontsize=8)
    ax_b.set_ylabel("F1 de CR-02 sobre el clip", fontsize=8)
    ax_b.grid(axis="x", visible=False)
    limpiar_ejes(ax_b)
    ax_b.set_title("B · la escala sola no ordena", loc="left", fontsize=8.5, pad=7, color=TINTA)

    fig.subplots_adjust(hspace=0.45)

    nota_al_pie(
        fig,
        [
            "Panel A: asociación de chaleco por banda de altura sobre las detecciones crudas de la campaña I1 "
            "(clips v06 y v10 diurnos, v04 nocturno); el tramo ≥320 px de v10 no fue medido y por eso la serie se corta.",
            "Panel B: los cuatro clips con referencia humana y Nivel A medido. El de sujetos más grandes rinde F1 0,084 "
            "por oclusión mutua, no por escala.",
            "La frontera tiene al menos tres ejes —escala, iluminación y oclusión— y ninguno de los tres, por sí solo, "
            "predice si el material es evaluable.",
        ],
        y=-0.10,
        tam=6.8,
    )

    salidas = guardar(fig, str(SALIDA))
    for ruta in salidas:
        print(f"escrito: {ruta}")
    print("fuentes: detecciones crudas de la campaña I1 (panel A) · clips con GT humano y Nivel A medido (panel B)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
