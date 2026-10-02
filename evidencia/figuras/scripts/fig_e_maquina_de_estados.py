#!/usr/bin/env python3
"""FIG-E — Máquina de estados del motor de patrones (Figura 4.3 del informe).

Versión para la documentación. Los CINCO estados reales del motor y sus
transiciones, leídos del contrato de `pattern_events` del plano de control
(`_advance_hit`, `_advance_clear` y el barrido de expiración).

Lo que la figura tiene que dejar dicho es la tesis del plano de control:
**detección no es alerta.** La alerta se emite al entrar a `confirmed`, cuando la
condición se sostuvo `confirm_after_ms`; un transitorio no llega y resuelve sin
alertar. Detalles del comportamiento real que el dibujo respeta:

  · Desde `inactive` se puede saltar directo a `confirmed` si la condición ya se
    cumple con el primer evento (igual al reabrir desde `resolved`; eso lo dice el
    pie de figura).
  · `sustained` es el régimen: la evidencia que sigue llegando lo mantiene sin un
    cambio de estado nuevo, así que un episodio largo no multiplica alertas.
  · A `resolved` se llega por despeje sostenido o por ausencia del sujeto por encima
    del tiempo de expiración, y la reapertura vuelve a `candidate`, nunca a `inactive`.

Debajo, una franja de tiempo esquemática (sin escala) ancla la máquina a un episodio.
Las ventanas son las del conjunto de patrones vigente `cr01_cr02_v2`: CR-01 4.000 ms,
CR-02 7.000 ms.

Uso:
    python3 fig_e_maquina_de_estados.py  (requiere matplotlib; ver README del directorio)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from estilo import MONO, caja, franjas, generar, lienzo, mono_negrita  # noqa: E402
from matplotlib.patches import FancyArrowPatch  # noqa: E402

SALIDA = Path(__file__).resolve().parents[1] / "fig-e-maquina-de-estados"

Y_FILA, ALTO, ANCHO = 33.0, 10.0, 15.0
Y_MEDIO = Y_FILA + ALTO / 2
# (clave, x, y, subtítulo)
ESTADOS = {
    "inactive": (2.0, Y_FILA, "sin episodio"),
    "candidate": (27.0, Y_FILA, "evidencia acumulando"),
    "confirmed": (53.5, Y_FILA, "se emite la ALERTA"),
    "sustained": (79.5, Y_FILA, "episodio en régimen"),
    "resolved": (53.5, 12.5, "episodio cerrado"),
}


def flecha(ax, origen, destino, color, *, ancho=1.4, rad=0.0, cabeza=10, z=4):
    ax.add_patch(FancyArrowPatch(
        origen, destino, arrowstyle="-|>", mutation_scale=cabeza, linewidth=ancho, color=color,
        connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0, zorder=z,
    ))


def texto(ax, x, y, s, t, *, color=None, tam=9.5, peso="normal", familia=None, ha="center", fondo=False):
    ax.text(
        x, y, s, ha=ha, va="center", fontsize=tam, color=color or t["tinta_2"], fontweight=peso,
        family=familia, linespacing=1.3, zorder=7,
        bbox=dict(boxstyle="round,pad=0.2", facecolor=t["fondo"], edgecolor="none") if fondo else None,
    )


def dibujar(t, tema):
    fig, ax = lienzo(5.8, ylim=(0, 58))

    for clave, (x, y, sub) in ESTADOS.items():
        alerta = clave == "confirmed"
        neutro = clave in ("inactive", "resolved")
        caja(ax, x, y, ANCHO, ALTO,
             relleno=t["sujeto_suave"] if alerta else (t["caja"] if neutro else t["escena_suave"]),
             borde=t["sujeto"] if alerta else (t["tinta_3"] if neutro else t["escena"]),
             grosor=2.0 if alerta else 1.5, radio=1.6)
        if alerta:
            franjas(ax, x + 1.6, y + ALTO - 1.25, ANCHO - 3.2, 0.7, color=t["sujeto"], fondo=t["sujeto_suave"], paso=1.0)
        ax.text(x + ANCHO / 2, y + 5.6, clave, ha="center", va="center", fontproperties=mono_negrita(13),
                color=t["tinta"], zorder=5)
        ax.text(x + ANCHO / 2, y + 2.5, sub, ha="center", va="center", fontsize=9.5,
                fontweight="bold" if alerta else "normal", color=t["tinta"] if alerta else t["tinta_2"], zorder=5)

    # --- Cadena principal ---
    flecha(ax, (17.0, Y_MEDIO), (27.0, Y_MEDIO), t["tinta_2"])
    texto(ax, 22.0, Y_MEDIO + 2.6, "primera\nevidencia", t)
    flecha(ax, (42.0, Y_MEDIO), (53.5, Y_MEDIO), t["sujeto"], ancho=2.6, cabeza=13)
    texto(ax, 47.75, Y_MEDIO + 2.1, "se sostiene", t, color=t["tinta"], peso="bold")
    texto(ax, 47.75, Y_MEDIO - 2.1, "confirm_after_ms", t, color=t["tinta"], tam=9, familia=MONO)
    flecha(ax, (68.5, Y_MEDIO), (79.5, Y_MEDIO), t["tinta_2"])
    texto(ax, 74.0, Y_MEDIO + 2.6, "evidencia\nposterior", t)

    # --- Atajo: la condición ya se cumple con el primer evento ---
    flecha(ax, (9.5, Y_FILA + ALTO), (58.5, Y_FILA + ALTO), t["tinta_3"], ancho=1.2, rad=-0.22)
    texto(ax, 33.0, 52.4, "si la condición ya se cumple con el primer evento, salta a confirmed", t, tam=9.5)

    # --- Régimen: la evidencia que sigue llegando no cambia de estado ---
    flecha(ax, (83.5, Y_FILA + ALTO), (90.5, Y_FILA + ALTO), t["tinta_3"], ancho=1.2, rad=-1.4, cabeza=9)
    texto(ax, 87.0, 51.2, "evidencia sostenida:\nsin alertas nuevas", t)

    # --- Cierre del episodio ---
    xr, yr = ESTADOS["resolved"][0], ESTADOS["resolved"][1]
    flecha(ax, (37.0, Y_FILA), (xr, yr + 6.5), t["tinta_2"])                       # transitorio
    flecha(ax, (61.0, Y_FILA), (61.0, yr + ALTO), t["tinta_2"])                    # confirmed → resolved
    flecha(ax, (87.0, Y_FILA), (xr + ANCHO, yr + 6.0), t["tinta_2"])               # sustained → resolved
    texto(ax, 49.4, 27.2, "transitorio:\nresuelve\nsin alerta", t, ha="left", color=t["tinta"])
    texto(ax, 78.0, 22.6, "despeje sostenido, o ausencia\ndel sujeto más allá del\ntiempo de expiración", t, ha="left")

    # --- Reapertura: vuelve a candidate, nunca a inactive ---
    flecha(ax, (xr, yr + 2.5), (31.0, Y_FILA), t["tinta_3"], ancho=1.2)
    texto(ax, 30.0, 20.0, "evidencia nueva:\notro episodio", t, ha="right")

    # --- Franja de tiempo esquemática: un episodio ---
    y0, h = 3.0, 3.2
    ax.text(2.0, 11.4, "un episodio en el tiempo (esquema, sin escala)", fontsize=9.5,
            color=t["tinta_3"], va="center", zorder=5)
    ax.plot([2.0, 14.0], [y0 + h / 2] * 2, color=t["tinta_3"], linewidth=1.2, zorder=4)
    caja(ax, 14.0, y0, 22.0, h, relleno=t["escena_suave"], borde=t["escena"], grosor=1.2, radio=0.6)
    texto(ax, 25.0, y0 + h / 2, "candidate", t, familia=MONO, color=t["tinta"])
    caja(ax, 36.6, y0, 45.4, h, relleno=t["sujeto_suave"], borde=t["sujeto"], grosor=1.2, radio=0.6)
    texto(ax, 59.3, y0 + h / 2, "sustained · sin alertas nuevas", t, color=t["tinta"])
    franjas(ax, 35.7, y0 - 0.7, 0.9, h + 1.4, color=t["sujeto"], fondo=t["fondo"], paso=0.7)
    texto(ax, 36.15, y0 + h + 2.1, "ALERTA", t, color=t["tinta"], peso="bold")
    ax.plot([82.0, 93.0], [y0 + h / 2] * 2, color=t["tinta_3"], linewidth=1.2, zorder=4)
    texto(ax, 87.5, y0 + h + 1.6, "resolved", t, familia=MONO)
    flecha(ax, (93.0, y0 + h / 2), (98.5, y0 + h / 2), t["tinta_3"], ancho=1.2, cabeza=9)
    texto(ax, 96.0, y0 - 1.4, "tiempo", t, tam=9)
    # La ventana de confirmación, como cota entre la primera evidencia y la alerta.
    ax.plot([14.0, 14.0], [y0 - 0.4, y0 + h + 1.2], color=t["tinta_2"], linewidth=1.2, zorder=5)
    texto(ax, 14.0, y0 + h + 2.1, "1.ª evidencia", t, color=t["tinta"])
    ax.annotate("", xy=(14.2, y0 - 1.8), xytext=(35.3, y0 - 1.8),
                arrowprops=dict(arrowstyle="<|-|>", color=t["tinta_2"], lw=1.0, shrinkA=0, shrinkB=0,
                                mutation_scale=7), zorder=5)
    texto(ax, 24.8, y0 - 3.6, "confirm_after_ms: CR-01 4.000 · CR-02 7.000", t, tam=9, familia=MONO)
    return fig


if __name__ == "__main__":
    raise SystemExit(generar(dibujar, SALIDA))
