"""Estilo compartido de las figuras de datos del informe (FIG-B, FIG-F).

Un solo lugar define paleta, tipografía y cromo para que las figuras del informe se
lean como un sistema y no como piezas sueltas. La paleta es la instancia validada del
método de visualización: los slots se verificaron con el validador de seis chequeos
(banda de luminosidad, piso de croma, separación CVD, piso de visión normal, contraste)
en modo claro sobre superficie #fcfcfb, que es el caso del informe impreso.

  slot 1 azul    #2a78d6
  slot 2 naranja #eb6834
  slot 3 aqua    #1baf7a   <- contraste 2,74 < 3:1 sobre la superficie: por regla de
                              relieve, toda serie con este color va SIEMPRE con
                              etiqueta directa visible, nunca identificada por color solo.

Verificado: par (1,2) todos los chequeos PASS; terna (1,3,2) PASS en `--pairs all`
(peor par CVD ΔE 9,2 deutan; visión normal 24,0) con la advertencia de contraste de
aqua atendida por etiquetado directo.

Reglas de cromo aplicadas (evitan los anti-patrones conocidos): marcas finas, grilla
y ejes en hairline sólido —nunca punteados—, sin número sobre cada punto (se etiqueta
selectivamente el extremo), leyenda presente siempre que haya 2+ series, y sin doble
eje y en ninguna figura.
"""

from __future__ import annotations

import textwrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Paleta categórica validada (modo claro).
AZUL = "#2a78d6"      # slot 1
NARANJA = "#eb6834"   # slot 2
AQUA = "#1baf7a"      # slot 3 — exige etiqueta directa (relief rule)

SUPERFICIE = "#fcfcfb"
TINTA = "#0b0b0b"        # texto primario
TINTA_2 = "#52514e"      # texto secundario
TINTA_3 = "#8a8985"      # texto atenuado / notas
GRILLA = "#e4e3df"       # hairline, un tono sobre la superficie
BANDA = "#f0eeea"        # relleno de regiones anotadas

# Ancho de columna del informe: 16 cm.
ANCHO_COLUMNA_IN = 6.3


def aplicar_estilo() -> None:
    """Estilo base: sans para todo, cromo recesivo, sin marcos superfluos."""
    plt.rcParams.update(
        {
            "figure.facecolor": SUPERFICIE,
            "axes.facecolor": SUPERFICIE,
            "savefig.facecolor": SUPERFICIE,
            "font.family": "sans-serif",
            "font.sans-serif": ["DejaVu Sans"],
            "font.size": 9,
            "axes.titlesize": 10,
            "axes.titleweight": "bold",
            "axes.titlecolor": TINTA,
            "axes.labelsize": 9,
            "axes.labelcolor": TINTA_2,
            "axes.edgecolor": GRILLA,
            "axes.linewidth": 0.8,
            "axes.grid": True,
            "axes.axisbelow": True,
            "grid.color": GRILLA,
            "grid.linewidth": 0.8,
            "grid.linestyle": "-",  # nunca punteada
            "xtick.color": TINTA_2,
            "ytick.color": TINTA_2,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "xtick.direction": "out",
            "ytick.direction": "out",
            "legend.frameon": False,
            "legend.fontsize": 8.5,
            "legend.labelcolor": TINTA_2,
            "lines.linewidth": 2.0,
            "lines.markersize": 6.5,
            "figure.dpi": 300,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.06,
        }
    )


def limpiar_ejes(ax) -> None:
    """Quita el marco superior/derecho: menos cromo, más dato."""
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(GRILLA)
    ax.tick_params(length=3, width=0.8)


def nota_al_pie(fig, parrafos, *, y=-0.05, tam=6.4, ancho_max=112) -> None:
    """Nota de procedencia al pie, con el texto CORTADO al ancho de la figura.

    Sin este corte, `savefig(bbox_inches="tight")` expande el lienzo hasta abarcar la
    línea más larga: una nota de 200 caracteres produjo un PNG de 4.083 px de ancho
    para una figura de 6,3 pulgadas (1.890 px). Insertado a 16 cm en el documento, eso
    achica TODA la figura a la mitad y deja los ejes ilegibles. El ancho por defecto
    (112 caracteres) entra en la columna del informe a este tamaño de letra.

    `parrafos` es una lista: cada elemento se corta por separado y conserva su
    condición de renglón propio.
    """
    lineas = []
    for parrafo in parrafos:
        lineas.extend(textwrap.wrap(parrafo, width=ancho_max) or [""])
    fig.text(
        0.0,
        y,
        "\n".join(lineas),
        fontsize=tam,
        color=TINTA_3,
        linespacing=1.5,
        va="top",
    )


def guardar(fig, destino_sin_extension) -> list[str]:
    """Emite PNG (para insertar en el `.docx`) y SVG (fuente vectorial)."""
    salidas = []
    for ext in ("png", "svg"):
        ruta = f"{destino_sin_extension}.{ext}"
        fig.savefig(ruta)
        salidas.append(ruta)
    plt.close(fig)
    return salidas
