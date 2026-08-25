#!/usr/bin/env python3
"""FIG-B — Curva de calidad contra densidad de evidencia (§17.5).

Qué muestra: cuánta calidad de detección de episodios sobrevive cuando la cadencia de
inferencia baja de la densidad del banco (30 fps, stride 1) a la que el camino live
puede sostener (1,16-4,42 fps, medidos en el rodaje). Es la figura del **costo del tiempo real**.

Fuente: los `metrics.json` de las ocho campañas del eje de densidad, leídos del
artefacto —nunca transcritos de una tabla intermedia— más el `stride` de cada
`campaign.yaml`. Las cifras resultantes se verifican contra el índice publicado
(`results/clip_bench/index.md` §Eje de densidad); si divergen, el script falla.

Dos reglas de lectura que la figura respeta y que su nota al pie debe repetir:
  · Se grafica F1 de episodios, NUNCA el SDR: el SDR no es comparable entre cadencias
    (su subida al bajar la densidad es, en la práctica, artefacto del instrumento de
    medición y no una mejora real).
  · Los clips negativos no entran a P/R/F1; su métrica son los FP (0/4 en las ocho
    campañas), y eso se dice en la nota, no se dibuja.

Uso:
    python3 fig_b_calidad_vs_densidad.py  (requiere matplotlib; ver README del directorio)
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from estilo import (  # noqa: E402  — fija el backend Agg antes de importar pyplot
    ANCHO_COLUMNA_IN,
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

# Repo hermano `e-ovrt_experimental-setup` clonado al lado por defecto; EOVRT_RESULTS
# sobrescribe la ubicación de su carpeta `results/` (ver README del directorio).
_DEFAULT_RESULTS = Path(__file__).resolve().parents[4] / "e-ovrt_experimental-setup" / "results"
RESULTS = Path(os.environ.get("EOVRT_RESULTS", str(_DEFAULT_RESULTS)))
CLIP_BENCH = RESULTS / "clip_bench"
SALIDA = Path(__file__).resolve().parents[1] / "fig-b-calidad-vs-densidad"

FPS_NOMINAL = 30.0

# (campaign_dir, ancla que representa) por granularidad. El orden es de menor a mayor
# densidad para que la serie se dibuje en el sentido del eje.
SERIES = {
    "escena": {
        "color": AZUL,
        "marcador": "o",
        "campanas": [
            ("r5_gdinotiny560_v2short_scene_s26", "peor caso live"),
            ("r3_gdinotiny560_v2short_scene_s15", "rodaje"),
            ("r1_gdinotiny560_v2short_scene_s7", "techo live"),
            ("t1_gdinotiny560_v2short_scene", "referencia DBE"),
        ],
    },
    "sujeto": {
        "color": NARANJA,
        "marcador": "s",
        "campanas": [
            ("r6_gdinotiny560_v2short_subject_s26", "peor caso live"),
            ("r4_gdinotiny560_v2short_subject_s15", "rodaje"),
            ("r2_gdinotiny560_v2short_subject_s7", "techo live"),
            ("g1_gdinotiny560_v2short_subject", "referencia DBE"),
        ],
    },
}

# Verificación contra el índice publicado (F1 micro de episodios positivos).
ESPERADO_INDICE = {
    "escena": [0.646, 0.738, 0.794, 0.789],
    "sujeto": [0.742, 0.875, 0.866, 0.930],
}

# Banda de cadencia que el camino live sostuvo con hardware real, medida en el rodaje.
LIVE_MIN, LIVE_MAX = 1.16, 4.42


def leer_campana(nombre: str) -> tuple[float, float]:
    """Devuelve (fps efectivos, F1 micro) leídos del artefacto de la campaña."""
    directorio = CLIP_BENCH / nombre
    metrics = json.loads((directorio / "metrics.json").read_text(encoding="utf-8"))
    campana = yaml.safe_load((directorio / "campaign.yaml").read_text(encoding="utf-8"))
    stride = int(campana.get("stride", 1))
    return FPS_NOMINAL / stride, float(metrics["positives"]["f1_micro"])


def main() -> int:
    datos = {}
    for granularidad, cfg in SERIES.items():
        puntos = [leer_campana(nombre) for nombre, _ in cfg["campanas"]]
        datos[granularidad] = puntos
        medidos = [round(f1, 3) for _, f1 in puntos]
        if medidos != ESPERADO_INDICE[granularidad]:
            raise SystemExit(
                f"FIG-B: {granularidad} midió {medidos} pero el índice publica "
                f"{ESPERADO_INDICE[granularidad]}. Regenerar el índice o revisar la campaña "
                "antes de dibujar: la figura no puede contradecir la fuente citable."
            )

    aplicar_estilo()
    fig, ax = plt.subplots(figsize=(ANCHO_COLUMNA_IN, 3.5))

    # Región donde vive el camino live, anotada como banda (no como línea punteada).
    ax.axvspan(LIVE_MIN, LIVE_MAX, color=BANDA, zorder=0, lw=0)
    ax.text(
        (LIVE_MIN * LIVE_MAX) ** 0.5,
        0.075,
        "cadencia sostenible\nen vivo (1,16–4,42 fps)",
        ha="center",
        va="bottom",
        fontsize=7.5,
        color=TINTA_3,
        linespacing=1.35,
    )

    for granularidad, cfg in SERIES.items():
        xs = [p[0] for p in datos[granularidad]]
        ys = [p[1] for p in datos[granularidad]]
        ax.plot(
            xs,
            ys,
            color=cfg["color"],
            marker=cfg["marcador"],
            label=f"granularidad de {granularidad}",
            markeredgecolor=SUPERFICIE,  # anillo de 2px sobre marcas superpuestas
            markeredgewidth=1.4,
            clip_on=False,
            zorder=3,
        )
        # Etiqueta directa en el extremo de referencia (selectiva, no en cada punto).
        ax.annotate(
            f"{granularidad}\n{ys[-1]:.3f}".replace(".", ","),
            xy=(xs[-1], ys[-1]),
            xytext=(9, 0),
            textcoords="offset points",
            va="center",
            ha="left",
            fontsize=8,
            color=TINTA_2,
            linespacing=1.3,
        )
        # Y el valor en el techo del camino live: es el punto decisión-relevante.
        idx_techo = 2
        ax.annotate(
            f"{ys[idx_techo]:.3f}".replace(".", ","),
            xy=(xs[idx_techo], ys[idx_techo]),
            xytext=(0, -13 if granularidad == "escena" else 9),
            textcoords="offset points",
            ha="center",
            fontsize=8,
            color=cfg["color"],
            fontweight="bold",
        )

    ax.set_xscale("log")
    ax.set_xlim(1.0, 42)
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("F1 de episodios (micro)")
    ax.set_xlabel(
        "densidad de evidencia (fotogramas inferidos por segundo, escala logarítmica)",
        labelpad=10,
    )

    # Valor y ancla en la MISMA etiqueta de tick. En dos bloques separados el rótulo del
    # eje queda en el medio y las anclas se leen como si fueran otro eje.
    ticks = [1.15, 2.0, 4.29, 30.0]
    # Anclas en dos líneas: a 1,15 y 2,00 fps los ticks quedan cerca en escala
    # logarítmica y una etiqueta de una línea se solapa con la vecina.
    anclas = ["peor caso\nlive (×26)", "rodaje\n(×15)", "techo\nlive (×7)", "referencia\nDBE (×1)"]
    ax.set_xticks(ticks)
    ax.set_xticklabels(
        [
            f"{t:.2f}".replace('.', ',') + f"\n{ancla}" if t < 10 else f"{t:.0f}\n{ancla}"
            for t, ancla in zip(ticks, anclas)
        ],
        linespacing=1.6,
    )
    ax.set_xticks([], minor=True)

    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(["0", "0,2", "0,4", "0,6", "0,8", "1,0"])
    ax.grid(axis="x", visible=False)
    limpiar_ejes(ax)

    # Sin título ni subtítulo horneados: el epígrafe ("Figura N — …") lo pone el
    # documento. Duplicarlo dentro de la imagen se lee como descuido de edición.
    # Sí queda la línea de procedencia: es la regla del proyecto — toda figura de
    # resultados carga el identificador que la hace verificable por un tercero.
    ax.legend(loc="lower right", bbox_to_anchor=(1.0, 0.04), handlelength=1.6)

    nota_al_pie(
        fig,
        [
            "Campañas t1/g1 (stride 1) y r1–r6 (strides 7/15/26) sobre el banco de 34 clips del rodaje; modelo "
            "gdino-tiny-560 y prompts cr01_cr02_v2_short en las ocho, variable única el stride.",
            "Los clips negativos no entran a F1 —su métrica son los falsos positivos, 0/4 en las ocho campañas— y no "
            "se grafica el SDR, que no es comparable entre cadencias.",
            "Con 34 episodios evaluables, las diferencias menores a ~0,02 (escena 4,29 vs 30 fps; sujeto 2,00 vs 4,29) "
            "están dentro de la resolución del banco y no se leen como orden.",
        ],
        y=-0.30,
        tam=6.8,
    )

    salidas = guardar(fig, str(SALIDA))
    for granularidad in SERIES:
        pares = ", ".join(
            f"{fps:.2f} fps → F1 {f1:.3f}" for fps, f1 in datos[granularidad]
        )
        print(f"{granularidad}: {pares}")
    print("verificado contra results/clip_bench/index.md §Eje de densidad")
    for ruta in salidas:
        print(f"escrito: {ruta}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
