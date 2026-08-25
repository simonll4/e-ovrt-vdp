#!/usr/bin/env python3
"""FIG-E — Máquina de estados del motor de patrones (§17.3.8.2).

Los CINCO estados reales del motor y sus transiciones, leídos del contrato de
`pattern_events` en el código del plano de control (`engine/pattern_engine.py`,
métodos `_advance_hit`, `_advance_clear` y el barrido de expiración). El rótulo de
tres estados que circuló antes (`open → confirmed → resolved`) era una simplificación
incorrecta: el destino es el fijado en §17.3.8.2, porque la máquina de estados es
diseño, no implementación.

Lo que la figura tiene que dejar dicho, y es la tesis del plano de control:
**detección no es alerta.** La alerta se emite en la transición de entrada a
`confirmed`, no cuando aparece la primera evidencia; entre una cosa y la otra hay una
condición temporal (`confirm_after_ms`) que un transitorio no alcanza a cumplir — por
eso un transitorio muere en `candidate` y resuelve en silencio.

Tres detalles del comportamiento real que el dibujo respeta y que un diagrama
"de manual" se saltearía:

  · Desde `inactive`/`resolved` se puede saltar **directo a `confirmed`** si la
    condición de confirmación ya se cumple con el primer evento.
  · `sustained` es el estado de régimen: la evidencia que sigue llegando lo mantiene
    ahí sin emitir un cambio de estado nuevo.
  · A `resolved` se llega por **dos caminos distintos**: despeje sostenido de la
    condición, o ausencia del sujeto por encima del tiempo de expiración.

Uso:
    python3 fig_e_maquina_de_estados.py  (requiere matplotlib; ver README del directorio)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from estilo import (  # noqa: E402  — fija el backend Agg antes de importar pyplot
    ANCHO_COLUMNA_IN,
    AZUL,
    NARANJA,
    SUPERFICIE,
    TINTA,
    TINTA_2,
    TINTA_3,
    aplicar_estilo,
    guardar,
    nota_al_pie,
)
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

SALIDA = Path(__file__).resolve().parents[1] / "fig-e-maquina-de-estados"

ALTO_ESTADO = 9.0
ANCHO_ESTADO = 19.0

# (clave, x, y, etiqueta, subtítulo, destacado)
ESTADOS = [
    ("inactive", 2.0, 46.0, "inactive", "sin episodio", False),
    ("candidate", 27.0, 46.0, "candidate", "evidencia acumulando", False),
    ("confirmed", 52.0, 46.0, "confirmed", "se emite la ALERTA", True),
    ("sustained", 77.0, 46.0, "sustained", "episodio en régimen", False),
    ("resolved", 39.5, 11.0, "resolved", "episodio cerrado", False),
]


def dibujar_estado(ax, x, y, etiqueta, subtitulo, destacado) -> None:
    ax.add_patch(
        FancyBboxPatch(
            (x, y), ANCHO_ESTADO, ALTO_ESTADO,
            boxstyle="round,pad=0,rounding_size=2.6",
            linewidth=1.7 if destacado else 1.1,
            edgecolor=NARANJA if destacado else AZUL,
            facecolor="#fcf0ea" if destacado else "#eef4fc",
            zorder=2,
        )
    )
    ax.text(
        x + ANCHO_ESTADO / 2, y + ALTO_ESTADO - 3.4, etiqueta,
        ha="center", va="center", fontsize=8.2, fontweight="bold",
        color=NARANJA if destacado else TINTA, zorder=3, family="DejaVu Sans Mono",
    )
    ax.text(
        x + ANCHO_ESTADO / 2, y + 2.9, subtitulo,
        ha="center", va="center", fontsize=6.0, color=TINTA_2, zorder=3,
    )


def flecha(ax, origen, destino, color=TINTA_2, *, ancho=1.0, rad=0.0):
    ax.add_patch(
        FancyArrowPatch(
            origen, destino,
            arrowstyle="-|>", mutation_scale=9, linewidth=ancho, color=color,
            connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0, zorder=4,
        )
    )


def rotulo(ax, x, y, texto, color=TINTA_2, tam=5.9, peso="normal", ha="center", va="center"):
    ax.text(
        x, y, texto, ha=ha, va=va, fontsize=tam, color=color, fontweight=peso,
        linespacing=1.4, zorder=6,
        bbox=dict(boxstyle="round,pad=0.2", facecolor=SUPERFICIE, edgecolor="none"),
    )


def main() -> int:
    aplicar_estilo()
    fig, ax = plt.subplots(figsize=(ANCHO_COLUMNA_IN, 3.6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 66)
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    for _clave, x, y, etiqueta, subtitulo, destacado in ESTADOS:
        dibujar_estado(ax, x, y, etiqueta, subtitulo, destacado)

    y_medio = 46.0 + ALTO_ESTADO / 2

    # --- Cadena principal ---
    flecha(ax, (21.0, y_medio), (27.0, y_medio), TINTA_2)
    rotulo(ax, 24.0, y_medio + 6.6, "primera\nevidencia")
    flecha(ax, (46.0, y_medio), (52.0, y_medio), NARANJA, ancho=1.6)
    rotulo(ax, 49.0, y_medio + 7.4, "se cumple\nconfirm_after_ms", NARANJA, 6.0, peso="bold")
    flecha(ax, (71.0, y_medio), (77.0, y_medio), TINTA_2)
    rotulo(ax, 74.0, y_medio + 6.6, "evidencia\nposterior")

    # --- Atajo: si la confirmación ya se cumple con el primer evento ---
    flecha(ax, (11.5, 55.0), (61.5, 55.0), TINTA_3, ancho=0.9, rad=-0.28)
    rotulo(ax, 36.5, 62.0, "si la condición ya está confirmada en el primer evento, se salta candidate", TINTA_3, 5.7)

    # --- Régimen: la evidencia que sigue llegando mantiene sustained ---
    ax.add_patch(
        FancyArrowPatch(
            (84.0, 55.0), (92.0, 55.0),
            arrowstyle="-|>", mutation_scale=8, linewidth=0.9, color=TINTA_3,
            connectionstyle="arc3,rad=-1.1", shrinkA=0, shrinkB=0, zorder=4,
        )
    )
    rotulo(ax, 88.0, 62.0, "evidencia sostenida", TINTA_3, 5.7)

    # --- Cierre del episodio: dos caminos distintos hacia resolved ---
    flecha(ax, (34.0, 46.0), (44.0, 20.0), TINTA_2, rad=0.12)
    flecha(ax, (60.0, 46.0), (52.0, 20.0), TINTA_2, rad=-0.10)
    flecha(ax, (84.0, 46.0), (58.5, 17.5), TINTA_2, rad=-0.16)
    rotulo(
        ax, 74.0, 27.0,
        "despeje sostenido de la condición\nO ausencia del sujeto por encima\ndel tiempo de expiración",
        TINTA_2, 5.9,
    )

    # --- Reapertura: evidencia nueva sobre un episodio cerrado ---
    # Va a `candidate`, NO a `inactive`: `inactive` es sólo el estado inicial, y el
    # motor reabre el episodio desde el estado de acumulación (o salta a `confirmed`
    # si la condición ya se cumple, igual que en el arranque).
    flecha(ax, (39.5, 15.5), (31.0, 46.0), TINTA_3, ancho=0.9, rad=0.30)
    rotulo(ax, 22.0, 29.0, "evidencia nueva:\nempieza otro episodio", TINTA_3, 5.9)

    # --- La lectura que la figura existe para dejar fijada ---
    rotulo(
        ax, 60.0, 36.5,
        "un transitorio muere en candidate: no alcanza a cumplir\nla condición temporal y resuelve sin emitir alerta",
        TINTA_3, 5.8,
    )

    nota_al_pie(
        fig,
        [
            "Estados y transiciones del contrato `pattern_events` del plano de control. La alerta se emite en la "
            "transición de entrada a `confirmed`: entre la primera evidencia y la alerta media una condición temporal "
            "(`confirm_after_ms`), y eso es lo que separa una detección de una alerta.",
            "`sustained` es el estado de régimen —la evidencia que sigue llegando lo mantiene ahí sin producir un "
            "cambio de estado nuevo—, de modo que un episodio prolongado no multiplica alertas.",
        ],
        y=-0.02,
        tam=6.4,
    )

    salidas = guardar(fig, str(SALIDA))
    for ruta in salidas:
        print(f"escrito: {ruta}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
