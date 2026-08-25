#!/usr/bin/env python3
"""FIG-A — Vista de procesos de la plataforma experimental (§17.4.1).

Es la respuesta gráfica al "cómo está hecho": complementa a la Figura 4.1 (vista
lógica) mostrando la disposición efectiva de procesos del prototipo. Su especificación
caja por caja y flecha por flecha está en el informe (§17.4.1), actualizada para
reflejar al módulo de distribución como servicio HTTP de la plataforma.

Dos cosas que la figura enseña y que no son decoración:

  · **El orden de arranque es el inverso del flujo de datos.** Los datos van
    medios → control → distribución, pero el orquestador levanta primero la
    distribución, después el control y por último los medios: en PUB/SUB el
    consumidor que no está suscripto pierde lo publicado antes de suscribirse. Es
    una regla de corrección, no un detalle de implementación.
  · **No hay flecha del bus a la interfaz de inspección.** Esa ausencia comunica una
    frontera de diseño: la consola es cliente de las interfaces de servicio, nunca
    consumidora del bus. Verificado en el código: el cliente HTTP del módulo de
    distribución vive en la ruta del runner (`experiment/distribution_http.py`), no
    en la de inspección.

Y una que corrige a la especificación original: el módulo de distribución va en
**línea continua** —es un servicio HTTP más, disparado por el orquestador igual
que los otros dos—, no punteada como "capacidad no implementada".

Criterio de dibujo: en el ancho de columna del informe el detalle largo NO entra
dentro de la figura. Las flechas llevan el rótulo mínimo que las identifica ("bus",
"canal de alertas") y lo que viaja por ellas se explica en la nota al pie.

Uso:
    python3 fig_a_vista_de_procesos.py  (requiere matplotlib; ver README del directorio)
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

SALIDA = Path(__file__).resolve().parents[1] / "fig-a-vista-de-procesos"

# Tres roles, tres tratamientos. El color agrupa por rol, nunca por importancia.
ROLES = {
    "servicio": {"relleno": "#eef4fc", "borde": AZUL},
    "consola": {"relleno": "#f3f2ef", "borde": TINTA_2},
    "repositorio": {"relleno": "#fcf0ea", "borde": NARANJA},
}

# Geometría. Canal libre a la izquierda (x≈3) para el retorno de consolidación, y
# huecos de 8,5 unidades entre servicios para que los rótulos de las flechas de datos
# tengan lugar propio en vez de caer sobre el texto de las cajas.
FILA_SERVICIOS_Y, ALTO_SERVICIO = 26.0, 16.0
CAJAS = [
    (
        7.5, 55.0, 37.0, 12.0, "consola",
        "Orquestador experimental",
        "manifiesto de experimento\ndispara los tres servicios\nconsolida artefactos y reporta",
    ),
    (
        60.0, 55.0, 38.0, 12.0, "consola",
        "Interfaz de inspección",
        "cliente de las interfaces de servicio\nde los planos de medios y de control",
    ),
    (
        7.5, FILA_SERVICIOS_Y, 26.0, ALTO_SERVICIO, "servicio",
        "Servicio de medios",
        "ingesta · control de ritmo\nnormalización · inferencia OVD\npostproceso · publicación\nmodelo cargado al arranque",
    ),
    (
        42.0, FILA_SERVICIOS_Y, 26.0, ALTO_SERVICIO, "servicio",
        "Servicio de control",
        "consumo de eventos\nmotor de patrones\nalertas internas · persistencia\nmétricas",
    ),
    (
        76.5, FILA_SERVICIOS_Y, 23.5, ALTO_SERVICIO, "servicio",
        "Módulo de distribución",
        "política de entrega\nledger de idempotencia\npublicación MQTT\nregistros",
    ),
    (
        18.0, 3.0, 50.0, 10.0, "repositorio",
        "Repositorio de corrida",
        "archivos de sólo adición, uno por plano",
    ),
]


def dibujar_caja(ax, x, y, ancho, alto, rol, titulo, cuerpo) -> None:
    estilo = ROLES[rol]
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            ancho,
            alto,
            boxstyle="round,pad=0,rounding_size=1.2",
            linewidth=1.1,
            edgecolor=estilo["borde"],
            facecolor=estilo["relleno"],
            zorder=2,
        )
    )
    ax.text(
        x + ancho / 2, y + alto - 2.4, titulo,
        ha="center", va="center", fontsize=7.2, fontweight="bold", color=TINTA, zorder=3,
    )
    ax.text(
        x + ancho / 2, y + (alto - 4.2) / 2, cuerpo,
        ha="center", va="center", fontsize=5.8, color=TINTA_2, linespacing=1.55, zorder=3,
    )


def flecha(ax, origen, destino, color, *, ancho=1.1, rad=0.0):
    ax.add_patch(
        FancyArrowPatch(
            origen, destino,
            arrowstyle="-|>", mutation_scale=9, linewidth=ancho, color=color,
            connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0, zorder=4,
        )
    )


def rotulo(ax, x, y, texto, color=TINTA_2, tam=6.0, ha="center", va="center", peso="normal", rot=0):
    ax.text(
        x, y, texto, ha=ha, va=va, fontsize=tam, color=color, fontweight=peso,
        linespacing=1.4, rotation=rot, zorder=6,
        bbox=dict(boxstyle="round,pad=0.18", facecolor=SUPERFICIE, edgecolor="none"),
    )


def main() -> int:
    aplicar_estilo()
    fig, ax = plt.subplots(figsize=(ANCHO_COLUMNA_IN, 4.3))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 68)
    ax.axis("off")
    # El lienzo del diagrama ocupa toda la figura: con los márgenes por defecto queda
    # una franja vacía de ~14 % entre el dibujo y la nota al pie.
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    for x, y, ancho, alto, rol, titulo, cuerpo in CAJAS:
        dibujar_caja(ax, x, y, ancho, alto, rol, titulo, cuerpo)

    y_flujo = FILA_SERVICIOS_Y + 5.0

    # --- Flujo de datos: medios → control → distribución ---
    flecha(ax, (33.5, y_flujo), (42.0, y_flujo), TINTA, ancho=1.5)
    rotulo(ax, 37.7, y_flujo + 3.4, "bus", TINTA, 6.2, peso="bold")
    flecha(ax, (68.0, y_flujo), (76.5, y_flujo), TINTA, ancho=1.5)
    rotulo(ax, 72.2, y_flujo + 3.6, "canal", TINTA, 6.2, peso="bold")

    # --- Persistencia: al repositorio, y antes que la publicación al bus ---
    flecha(ax, (20.5, FILA_SERVICIOS_Y), (28.0, 13.0), TINTA, ancho=1.3)
    rotulo(ax, 20.0, 19.0, "persiste antes\nde publicar", TINTA, 5.9)
    flecha(ax, (55.0, FILA_SERVICIOS_Y), (52.0, 13.0), TINTA, ancho=1.3)
    rotulo(ax, 58.5, 19.5, "persiste", TINTA, 5.9)

    # --- Arranque: el orden es el INVERSO del flujo de datos ---
    flecha(ax, (13.0, 55.0), (15.0, FILA_SERVICIOS_Y + ALTO_SERVICIO), AZUL)
    rotulo(ax, 11.0, 48.0, "③", AZUL, 8.5, peso="bold")
    flecha(ax, (28.0, 55.0), (50.0, FILA_SERVICIOS_Y + ALTO_SERVICIO), AZUL, rad=-0.10)
    rotulo(ax, 36.0, 47.0, "②", AZUL, 8.5, peso="bold")
    flecha(ax, (41.0, 55.0), (84.0, FILA_SERVICIOS_Y + ALTO_SERVICIO), AZUL, rad=-0.14)
    rotulo(ax, 61.0, 45.4, "①", AZUL, 8.5, peso="bold")

    # --- Inspección: lectura por las interfaces de servicio, nunca por el bus ---
    flecha(ax, (64.0, 55.0), (25.0, FILA_SERVICIOS_Y + ALTO_SERVICIO), TINTA_3, ancho=0.9, rad=0.13)
    flecha(ax, (75.0, 55.0), (60.0, FILA_SERVICIOS_Y + ALTO_SERVICIO), TINTA_3, ancho=0.9, rad=0.10)

    # --- Consolidación: el repositorio vuelve al orquestador por el canal izquierdo ---
    flecha(ax, (18.0, 8.0), (3.0, 8.0), TINTA_3, ancho=0.9)
    flecha(ax, (3.0, 8.0), (3.0, 55.5), TINTA_3, ancho=0.9)
    rotulo(ax, 3.0, 33.0, "consolidación y reporte", TINTA_3, 5.9, rot=90)

    # --- Leyenda de tipos de flecha ---
    leyenda_y, leyenda_x = 19.0, 74.0
    for desplazamiento, color, grosor, texto in (
        (0.0, TINTA, 1.5, "flujo de datos"),
        (-4.0, AZUL, 1.1, "arranque de servicio"),
        (-8.0, TINTA_3, 0.9, "lectura y consolidación"),
    ):
        ax.plot(
            [leyenda_x, leyenda_x + 5], [leyenda_y + desplazamiento] * 2,
            color=color, lw=grosor, clip_on=False, zorder=5,
        )
        ax.text(
            leyenda_x + 6.2, leyenda_y + desplazamiento, texto,
            fontsize=5.9, color=TINTA_2, va="center", zorder=5,
        )

    nota_al_pie(
        fig,
        [
            "Por el bus viaja el evento de percepción y el ciclo de vida de la corrida; por el canal de alertas, "
            "las alertas ya confirmadas por el motor de patrones.",
            "①②③ marcan el orden de arranque, que es el INVERSO del flujo de datos: cada consumidor queda suscripto "
            "antes de que su productor empiece a emitir, porque en PUB/SUB lo publicado antes de la suscripción se "
            "pierde. Es una regla de corrección, no un detalle de implementación.",
            "Los tres módulos se ejecutan como servicios independientes gobernados por configuración y pueden "
            "disponerse en un mismo host o en hosts distintos sin modificar su lógica. No existe flecha del bus a la "
            "interfaz de inspección: esa ausencia es una frontera de diseño, no una omisión del dibujo.",
        ],
        y=-0.03,
    )

    salidas = guardar(fig, str(SALIDA))
    for ruta in salidas:
        print(f"escrito: {ruta}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
