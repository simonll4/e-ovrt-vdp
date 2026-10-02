"""Sistema visual de las figuras de la documentación de E-OVRT-VDP.

Las figuras se leen en GitHub, no en papel: van al ancho de lectura de la página
(~880 px), en modo claro y en modo oscuro, y su texto explicativo vive en el
markdown, no horneado en la imagen. Este módulo fija lo que comparten todas:

  · Dos temas, `claro` y `oscuro`, con los colores de superficie de GitHub. Cada
    figura se dibuja una vez por tema y se publica con <picture>; el SVG sale con
    fondo transparente para fundirse con la página.
  · Paleta "de obra": grafito para el texto, azul acero para la granularidad de
    escena y la plataforma, naranja de alta visibilidad para el sujeto y la alerta.
    El par (escena, sujeto) se validó con el validador de seis chequeos en los dos
    temas contra su superficie real: claro #2f6fb3/#e35f1b sobre #ffffff, oscuro
    #4a8bd6/#e8692a sobre #0d1117 — todos PASS, peor ΔE CVD 22,2 (protan).
  · Una firma propia: las franjas de seguridad. Se usan SÓLO como cinta angosta para
    marcar "alerta" o "en vivo" — nunca como relleno sobre datos, que es ruido.
  · Lato para el texto y Ubuntu Mono para identificadores (`CR-01`, `:8081`,
    `confirm_after_ms`). El SVG convierte el texto a trazos: se ve igual en cualquier
    navegador aunque no tenga las fuentes.

Tamaños: con figuras de 10 pulgadas de ancho, 10 pt ≈ 12 px en pantalla. Ningún texto
baja de 9,5 pt.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle  # noqa: E402

ANCHO_IN = 10.0
SANS = "Lato"
MONO = "Ubuntu Mono"

# La negrita de Ubuntu Mono declara peso 400 en sus metadatos, así que matplotlib nunca
# la elige por `fontweight`: se carga por ruta. Sin ella, cae a DejaVu Sans Mono Bold.
_MONO_BOLD = Path("/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf")


def mono_negrita(tam: float) -> font_manager.FontProperties:
    if _MONO_BOLD.exists():
        return font_manager.FontProperties(fname=str(_MONO_BOLD), size=tam)
    return font_manager.FontProperties(family="DejaVu Sans Mono", weight="bold", size=tam)

TEMAS: dict[str, dict[str, str]] = {
    "claro": {
        "fondo": "#ffffff",        # superficie de la página de GitHub (anillo de marcas)
        "tinta": "#1f2328",
        "tinta_2": "#59636e",
        "tinta_3": "#818b98",
        "grilla": "#d1d9e0",
        "caja": "#f6f8fa",
        "borde": "#d1d9e0",
        "escena": "#2f6fb3",
        "escena_suave": "#eaf1fa",
        "sujeto": "#e35f1b",
        "sujeto_suave": "#fdeee6",
        "insignia_texto": "#ffffff",
    },
    "oscuro": {
        "fondo": "#0d1117",
        "tinta": "#e6edf3",
        "tinta_2": "#9198a1",
        "tinta_3": "#6e7681",
        "grilla": "#30363d",
        "caja": "#161b22",
        "borde": "#30363d",
        "escena": "#4a8bd6",
        "escena_suave": "#132338",
        "sujeto": "#e8692a",
        "sujeto_suave": "#2e1a10",
        "insignia_texto": "#0d1117",
    },
}

# Rampa secuencial de un solo tono —el verde lima del chaleco— para magnitudes. La
# luminosidad es monótona: del tono cercano a la superficie (≈0) al más intenso.
RAMPA_CHALECO = {
    "claro": ["#f4f7e6", "#dfeaa8", "#bdd45a", "#8aac1f", "#5a7a0c"],
    "oscuro": ["#1a2111", "#2f4314", "#4f7019", "#7fa428", "#b9d65a"],
}


def rampa(tema: str) -> LinearSegmentedColormap:
    return LinearSegmentedColormap.from_list(f"chaleco_{tema}", RAMPA_CHALECO[tema])


def coma(valor: float, decimales: int = 3) -> str:
    """Formato con coma decimal, como en el informe."""
    return f"{valor:.{decimales}f}".replace(".", ",")


def con_signo(valor: float, decimales: int = 3) -> str:
    return ("+" if valor >= 0 else "−") + coma(abs(valor), decimales)


def aplicar_estilo(t: dict[str, str]) -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": [SANS, "DejaVu Sans"],
            "font.size": 10.5,
            "text.color": t["tinta"],
            "axes.labelcolor": t["tinta_2"],
            "axes.edgecolor": t["grilla"],
            "axes.linewidth": 1.0,
            "axes.facecolor": "none",
            "axes.grid": False,
            "axes.axisbelow": True,
            "grid.color": t["grilla"],
            "grid.linewidth": 1.0,
            "grid.linestyle": "-",  # nunca punteada
            "xtick.color": t["tinta_2"],
            "ytick.color": t["tinta_2"],
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "legend.frameon": False,
            "figure.facecolor": "none",
            "savefig.facecolor": "none",
            "svg.hashsalt": "e-ovrt-vdp",  # identificadores estables: el SVG no cambia si el dibujo no cambia
            "svg.fonttype": "path",
        }
    )


def lienzo(alto_in: float, *, xlim=(0, 100), ylim=(0, 60)):
    """Figura de diagrama: ejes invisibles en coordenadas de 0 a 100 de ancho."""
    fig, ax = plt.subplots(figsize=(ANCHO_IN, alto_in))
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    return fig, ax


def caja(ax, x, y, ancho, alto, *, relleno, borde, grosor=1.2, radio=1.4, z=2):
    patch = FancyBboxPatch(
        (x, y), ancho, alto,
        boxstyle=f"round,pad=0,rounding_size={radio}",
        linewidth=grosor, edgecolor=borde, facecolor=relleno, zorder=z,
    )
    ax.add_patch(patch)
    return patch


def franjas(ax, x, y, ancho, alto, *, color, fondo, paso=1.6, z=3):
    """Cinta de franjas de seguridad a 45°, recortada al rectángulo.

    Es la firma visual del proyecto y marca sólo dos cosas: la alerta y lo que
    corre en vivo. Siempre angosta; nunca encima de datos.
    """
    base = Rectangle((x, y), ancho, alto, facecolor=fondo, edgecolor="none", zorder=z)
    ax.add_patch(base)
    k = x - alto
    while k < x + ancho:
        franja = Polygon(
            [(k, y), (k + paso / 2, y), (k + paso / 2 + alto, y + alto), (k + alto, y + alto)],
            closed=True, facecolor=color, edgecolor="none", zorder=z + 0.1,
        )
        # El recorte va DESPUÉS de add_patch: si se asigna antes, add_patch lo pisa con
        # el rectángulo de los ejes y las franjas se derraman fuera de la cinta.
        ax.add_patch(franja)
        franja.set_clip_path(base)
        k += paso
    return base


def insignia(ax, x, y, numero, t, *, radio=1.55, color=None, z=8, tam=11):
    """Círculo numerado (orden de arranque, llamadas)."""
    ax.add_patch(Circle((x, y), radio, facecolor=color or t["tinta"], edgecolor=t["fondo"],
                        linewidth=2.0, zorder=z))
    ax.text(x, y - 0.05, str(numero), ha="center", va="center", fontsize=tam,
            fontweight="bold", color=t["insignia_texto"], zorder=z + 0.1)


def guardar(fig, base: Path, tema: str) -> list[Path]:
    """Claro: `base.svg` y `base.png`. Oscuro: `base-oscuro.svg`.

    El SVG va transparente para fundirse con la página. El PNG (respaldo y uso fuera
    de GitHub) lleva fondo blanco: un PNG transparente se lee mal fuera de la página.
    """
    salidas = []
    if tema == "claro":
        svg = base.with_suffix(".svg")
        fig.savefig(svg, transparent=True, bbox_inches="tight", pad_inches=0.08, metadata={"Date": None})
        png = base.with_suffix(".png")
        fig.savefig(png, dpi=200, facecolor="#ffffff", bbox_inches="tight", pad_inches=0.08)
        salidas += [svg, png]
    else:
        svg = base.with_name(base.name + "-oscuro.svg")
        fig.savefig(svg, transparent=True, bbox_inches="tight", pad_inches=0.08, metadata={"Date": None})
        salidas.append(svg)
    plt.close(fig)
    return salidas


def generar(dibujar, base: Path) -> int:
    """Dibuja la figura en los dos temas y escribe sus archivos."""
    for tema, t in TEMAS.items():
        aplicar_estilo(t)
        fig = dibujar(t, tema)
        for ruta in guardar(fig, base, tema):
            print(f"escrito: {ruta}")
    return 0
