#!/usr/bin/env python3
"""FIG-C — Fotograma con la alerta confirmada, con llamadas (Figura 4.6 del informe).

Parte del fotograma que dibujó el renderizador de `defensa/` de
`e-ovrt_experimental-setup` sobre el clip `a_p1_c04` del rodaje propio
(`fig-c-alerta-confirmada.png`, que no se modifica) y le agrega cuatro llamadas
numeradas; la explicación de cada una va en el pie de figura del markdown:

  1. el aviso de la alerta confirmada (CR-01, severidad alta, t = 7,3 s);
  2. la persona: la condición se evalúa sobre ella;
  3. el casco sobre la mesa: está en cuadro pero no asociado al sujeto, y no
     suprime la condición;
  4. la línea de tiempo: de la primera evidencia a la ALERTA.

Es una foto: sale una sola versión (PNG), igual para el modo claro y el oscuro.

Uso:
    python3 fig_c_alerta_anotada.py  (requiere matplotlib; ver README del directorio)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from estilo import TEMAS, aplicar_estilo, insignia  # noqa: E402
import matplotlib.image as mpimg  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.patheffects as pe  # noqa: E402

FIGURAS = Path(__file__).resolve().parents[1]
ENTRADA = FIGURAS / "fig-c-alerta-confirmada.png"
SALIDA = FIGURAS / "fig-c-alerta-confirmada-anotada.png"

# (número, posición de la insignia, punto señalado) en píxeles del fotograma.
LLAMADAS = [
    (1, (680, 46), (604, 46)),
    (2, (965, 150), (1225, 150)),
    (3, (1640, 250), (1372, 330)),
    (4, (600, 870), (466, 960)),
]


def main() -> int:
    t = TEMAS["claro"]
    aplicar_estilo(t)
    imagen = mpimg.imread(ENTRADA)
    alto, ancho = imagen.shape[:2]
    fig = plt.figure(figsize=(ancho / 100, alto / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(imagen)
    ax.set_xlim(0, ancho)
    ax.set_ylim(alto, 0)
    ax.axis("off")
    contorno = [pe.Stroke(linewidth=6.5, foreground="#1f2328"), pe.Normal()]
    for numero, (bx, by), (px, py) in LLAMADAS:
        ax.plot([bx, px], [by, py], color="#ffffff", linewidth=3.2, solid_capstyle="round", zorder=5,
                path_effects=contorno)
        ax.plot(px, py, "o", markersize=9, color="#ffffff", markeredgecolor="#1f2328", markeredgewidth=2.2, zorder=6)
        insignia(ax, bx, by, numero, t, radio=26, color=t["sujeto"], tam=26)
    fig.savefig(SALIDA, dpi=100)
    plt.close(fig)
    print(f"escrito: {SALIDA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
