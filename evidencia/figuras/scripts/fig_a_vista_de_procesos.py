#!/usr/bin/env python3
"""FIG-A — Vista de procesos de la plataforma (Figura 4.5 del informe).

Versión para la documentación: misma semántica que la figura del informe, dibujada
para leerse en GitHub. Lo que la figura tiene que dejar dicho sin ambigüedad:

  · Tres servicios HTTP gobernados por configuración —medios, control,
    distribución—, cada uno con su puerto.
  · Dos canales de datos publicador/suscriptor: detecciones (medios → control) y
    alertas confirmadas (control → distribución), y la salida MQTT QoS 1.
  · La consola es cliente de las interfaces HTTP de servicio: no hay ninguna línea
    entre un bus y la consola, y esa ausencia es una frontera de diseño.
  · El orden de arranque que impone el orquestador es control → distribución →
    medios (Figura 4.5 y Tabla B.7 del informe). Va como insignia SOBRE cada servicio,
    no sobre una flecha: así no se puede leer como orden del flujo de datos. La no
    pérdida de alertas no depende de ese orden sino del publicador, que espera la
    suscripción del distribuidor (lo dice el pie de figura en el markdown).
  · Medios persiste cada evento antes de publicarlo; el repositorio de corrida
    vuelve al orquestador por consolidación.

Uso:
    python3 fig_a_vista_de_procesos.py  (requiere matplotlib; ver README del directorio)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from estilo import MONO, caja, franjas, generar, insignia, lienzo  # noqa: E402
from matplotlib.patches import FancyArrowPatch  # noqa: E402

SALIDA = Path(__file__).resolve().parents[1] / "fig-a-vista-de-procesos"

Y_SERV, ALTO_SERV, ANCHO_SERV = 25.0, 16.0, 19.0
Y_FLUJO = Y_SERV + 8.0
# (clave, x, título, puerto, dos renglones, orden de arranque)
SERVICIOS = [
    ("medios", 11.5, "Medios", ":8080", ("ingesta e inferencia", "open-vocabulary"), 3),
    ("control", 40.5, "Control", ":8081", ("motor de patrones", "identidad por sujeto"), 1),
    ("distribucion", 69.5, "Distribución", ":8082", ("política de entrega", "registro idempotente"), 2),
]
CENTRO = {clave: x + ANCHO_SERV / 2 for clave, x, *_ in SERVICIOS}


def flecha(ax, origen, destino, color, *, ancho=1.2, cabeza=10, z=4):
    ax.add_patch(FancyArrowPatch(
        origen, destino, arrowstyle="-|>", mutation_scale=cabeza, linewidth=ancho,
        color=color, shrinkA=0, shrinkB=0, zorder=z, capstyle="round", joinstyle="round",
    ))


def linea(ax, xs, ys, color, ancho=1.2, z=3):
    ax.plot(xs, ys, color=color, linewidth=ancho, solid_capstyle="round", zorder=z)


def rotulo(ax, x, y, texto, t, *, color=None, tam=10, peso="normal", familia=None, ha="center", fondo=True):
    ax.text(
        x, y, texto, ha=ha, va="center", fontsize=tam, color=color or t["tinta_2"],
        fontweight=peso, family=familia, linespacing=1.25, zorder=7,
        bbox=dict(boxstyle="round,pad=0.22", facecolor=t["fondo"], edgecolor="none") if fondo else None,
    )


def dibujar(t, tema):
    fig, ax = lienzo(6.2, ylim=(0, 62))

    # --- Consola: dos componentes, un solo servicio web ---
    caja(ax, 9.0, 49.0, 82.0, 11.6, relleno=t["caja"], borde=t["borde"], radio=1.6)
    ax.text(10.6, 58.9, "Consola web", fontsize=11, fontweight="bold", color=t["tinta"], va="center", zorder=5)
    ax.text(19.6, 58.9, ":8090", fontsize=10.5, family=MONO, color=t["tinta_2"], va="center", zorder=5)
    for x, titulo, detalle in (
        (11.0, "Orquestador de experimentos", "dispara los tres servicios · consolida y reporta"),
        (51.0, "Interfaz de inspección", "consulta medios y control"),
    ):
        caja(ax, x, 50.3, 38.0, 6.6, relleno=t["fondo"], borde=t["borde"], radio=1.0, z=3)
        ax.text(x + 19.0, 54.9, titulo, ha="center", va="center", fontsize=10.5, fontweight="bold",
                color=t["tinta"], zorder=5)
        ax.text(x + 19.0, 52.2, detalle, ha="center", va="center", fontsize=9.5, color=t["tinta_2"], zorder=5)

    # --- Interfaces HTTP de servicio: un riel con bajadas ortogonales ---
    y_riel = 45.5
    linea(ax, [CENTRO["medios"], CENTRO["distribucion"]], [y_riel, y_riel], t["tinta_3"])
    for x in (30.0, 70.0):  # orquestador e inspección bajan al riel
        linea(ax, [x, x], [50.3, y_riel], t["tinta_3"])
    for clave in CENTRO:
        flecha(ax, (CENTRO[clave], y_riel), (CENTRO[clave], Y_SERV + ALTO_SERV), t["tinta_3"], ancho=1.2, cabeza=9)
    rotulo(ax, 60.0, y_riel, "HTTP de servicio", t, tam=9.5)

    # --- Servicios, con su orden de arranque como insignia ---
    for clave, x, titulo, puerto, renglones, orden in SERVICIOS:
        caja(ax, x, Y_SERV, ANCHO_SERV, ALTO_SERV, relleno=t["escena_suave"], borde=t["escena"], grosor=1.6)
        cx = x + ANCHO_SERV / 2
        ax.text(cx, Y_SERV + 12.6, titulo, ha="center", va="center", fontsize=12.5, fontweight="bold",
                color=t["tinta"], zorder=5)
        ax.text(cx, Y_SERV + 9.4, puerto, ha="center", va="center", fontsize=11, family=MONO,
                color=t["escena"], zorder=5)
        ax.text(cx, Y_SERV + 4.6, "\n".join(renglones), ha="center", va="center", fontsize=9.5,
                color=t["tinta_2"], linespacing=1.35, zorder=5)
        insignia(ax, x + 0.4, Y_SERV + ALTO_SERV - 0.4, orden, t, color=t["tinta"])

    # --- Fuentes de video ---
    caja(ax, 2.4, 27.5, 7.6, 11.0, relleno=t["caja"], borde=t["borde"], radio=1.0)
    ax.text(6.2, 36.6, "fuentes", ha="center", va="center", fontsize=9.5, fontweight="bold", color=t["tinta"], zorder=5)
    ax.text(6.2, 31.6, "OAK-D\nRTSP\nvideo\nimágenes", ha="center", va="center", fontsize=9, color=t["tinta_2"],
            linespacing=1.3, zorder=5)
    flecha(ax, (10.0, Y_FLUJO), (11.5, Y_FLUJO), t["tinta"], ancho=2.0)

    # --- Canal de detecciones: medios → control ---
    flecha(ax, (30.5, Y_FLUJO), (40.5, Y_FLUJO), t["tinta"], ancho=2.4, cabeza=13)
    rotulo(ax, 35.5, Y_FLUJO + 2.6, "ZeroMQ", t, tam=9.5, fondo=False)
    rotulo(ax, 35.5, Y_FLUJO - 2.6, "detecciones", t, color=t["tinta"], tam=9.5, peso="bold", fondo=False)

    # --- Canal de alertas: control → distribución, marcado con la cinta de alerta ---
    flecha(ax, (59.5, Y_FLUJO), (69.5, Y_FLUJO), t["sujeto"], ancho=2.4, cabeza=13)
    franjas(ax, 60.2, Y_FLUJO - 1.25, 7.6, 0.75, color=t["sujeto"], fondo=t["fondo"], paso=1.1)
    rotulo(ax, 64.5, Y_FLUJO + 2.6, ":5558", t, tam=10, familia=MONO, fondo=False)
    rotulo(ax, 64.5, Y_FLUJO - 3.6, "alertas\nconfirmadas", t, color=t["tinta"], tam=9.5, peso="bold", fondo=False)

    # --- Salida MQTT ---
    flecha(ax, (88.5, Y_FLUJO), (91.0, Y_FLUJO), t["sujeto"], ancho=2.4, cabeza=11)
    caja(ax, 91.0, Y_FLUJO - 3.6, 8.4, 7.2, relleno=t["sujeto_suave"], borde=t["sujeto"], grosor=1.4, radio=1.0)
    ax.text(95.2, Y_FLUJO + 1.2, "MQTT", ha="center", va="center", fontsize=10.5, fontweight="bold",
            color=t["tinta"], zorder=5)
    ax.text(95.2, Y_FLUJO - 1.6, "QoS 1", ha="center", va="center", fontsize=9.5, family=MONO,
            color=t["tinta_2"], zorder=5)

    # --- Repositorio de corrida: lo que persiste cada plano ---
    caja(ax, 11.5, 5.0, 48.0, 9.0, relleno=t["caja"], borde=t["tinta_3"], grosor=1.2, radio=1.2)
    ax.text(35.5, 11.0, "Repositorio de corrida", ha="center", va="center", fontsize=11.5, fontweight="bold",
            color=t["tinta"], zorder=5)
    ax.text(35.5, 7.6, "JSONL de sólo adición, uno por plano · fuente de verdad", ha="center", va="center",
            fontsize=9.5, color=t["tinta_2"], zorder=5)
    flecha(ax, (CENTRO["medios"], Y_SERV), (CENTRO["medios"], 14.0), t["tinta"], ancho=1.8)
    rotulo(ax, CENTRO["medios"] + 1.2, 19.5, "persiste antes\nde publicar", t, ha="left", tam=9.5, fondo=False)
    flecha(ax, (CENTRO["control"], Y_SERV), (CENTRO["control"], 14.0), t["tinta"], ancho=1.8)
    rotulo(ax, CENTRO["control"] + 1.2, 19.5, "persiste", t, ha="left", tam=9.5, fondo=False)

    # --- Consolidación: del repositorio al orquestador, por un canal propio ---
    linea(ax, [11.5, 1.0], [9.5, 9.5], t["tinta_3"])
    linea(ax, [1.0, 1.0], [9.5, 53.6], t["tinta_3"])
    flecha(ax, (1.0, 53.6), (9.0, 53.6), t["tinta_3"], ancho=1.2, cabeza=9)
    ax.text(1.0, 20.5, "consolidación", rotation=90, ha="center", va="center", fontsize=9.5,
            color=t["tinta_2"], zorder=7,
            bbox=dict(boxstyle="round,pad=0.25", facecolor=t["fondo"], edgecolor="none"))

    # --- Leyenda ---
    x0, y0 = 66.0, 12.6
    entradas = [
        (t["tinta"], 2.4, "flujo de detecciones"),
        (t["sujeto"], 2.4, "alertas confirmadas"),
        (t["tinta_3"], 1.2, "HTTP y consolidación"),
    ]
    for i, (color, grosor, texto) in enumerate(entradas):
        y = y0 - i * 3.0
        linea(ax, [x0, x0 + 4.5], [y, y], color, ancho=grosor, z=5)
        ax.text(x0 + 6.0, y, texto, va="center", fontsize=9.5, color=t["tinta_2"], zorder=5)
    y = y0 - 3 * 3.0
    for i in range(3):
        insignia(ax, x0 + 0.2 + i * 2.6, y, i + 1, t, radio=1.1, tam=8.5)
    ax.text(x0 + 8.0, y, "orden de arranque", va="center", fontsize=9.5, color=t["tinta_2"], zorder=5)
    return fig


if __name__ == "__main__":
    raise SystemExit(generar(dibujar, SALIDA))
