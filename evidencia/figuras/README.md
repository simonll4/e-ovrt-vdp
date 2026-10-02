# Figuras

Las figuras de la documentación, dibujadas para leerse en GitHub. Llevan los mismos datos
y la misma semántica que las del informe —A, C y E son sus Figuras 4.5, 4.6 y 4.3—, pero
no su diseño de impresión: el texto explicativo va en el pie de figura de cada página, no
dentro de la imagen.

| Figura | Qué muestra | Dónde se usa | Archivos |
|---|---|---|---|
| A | los tres servicios, la consola, los dos canales de datos y el orden de arranque | [`plataforma/02`](../../plataforma/02-arquitectura.md) · [inicio](../../README.md) | [claro](fig-a-vista-de-procesos.svg) · [oscuro](fig-a-vista-de-procesos-oscuro.svg) · [PNG](fig-a-vista-de-procesos.png) |
| B | F1 de episodios por escena y por sujeto en cuatro densidades, y la ganancia del sujeto con su intervalo de confianza | [`resultados/` §4](../../resultados/README.md#4-el-costo-del-tiempo-real-densidad-de-evidencia) | [claro](fig-b-calidad-vs-densidad.svg) · [oscuro](fig-b-calidad-vs-densidad-oscuro.svg) · [PNG](fig-b-calidad-vs-densidad.png) |
| C | un fotograma con la alerta confirmada, con cuatro llamadas | [`plataforma/03`](../../plataforma/03-flujo-de-una-alerta.md) | [anotada](fig-c-alerta-confirmada-anotada.png) · [original](fig-c-alerta-confirmada.png) · [cuadro completo](fig-c-alerta-confirmada-completa.png) |
| E | la máquina de cinco estados del patrón y un episodio en el tiempo | [`plataforma/03`](../../plataforma/03-flujo-de-una-alerta.md) | [claro](fig-e-maquina-de-estados.svg) · [oscuro](fig-e-maquina-de-estados-oscuro.svg) · [PNG](fig-e-maquina-de-estados.png) |
| F | la frontera de juzgabilidad: escala, iluminación y oclusión | [`resultados/` §5](../../resultados/README.md#5-obra-real-no-guionada-13-clips-de-internet) | [claro](fig-f-frontera-juzgabilidad.svg) · [oscuro](fig-f-frontera-juzgabilidad-oscuro.svg) · [PNG](fig-f-frontera-juzgabilidad.png) |

## De dónde sale cada una

- **A y E** se dibujan desde la especificación de la arquitectura y desde el contrato de
  eventos de patrón del plano de control.
- **B** lee los `metrics.json` de las ocho campañas del eje de densidad en
  `results/clip_bench/`. El script **falla** si un F1 no coincide con el índice publicado,
  o si una ganancia transcrita no coincide con la resta de los F1 medidos.
- **C** parte del fotograma que dibujó el renderizador de `defensa/` de
  `e-ovrt_experimental-setup` sobre el clip `a_p1_c04` del rodaje propio, y le agrega las
  llamadas sin modificar el original.
- **F** lleva sus datos embebidos en el script, porque su fuente son tablas de análisis
  que no tienen un `metrics.json` propio.

## El sistema visual

Todo lo común vive en [`scripts/estilo.py`](scripts/estilo.py): tocarlo cambia todas las
figuras a la vez.

- **Dos temas.** Cada figura se dibuja en claro y en oscuro con los colores de superficie
  de GitHub, y se publica con `<picture>`: GitHub muestra la que corresponde al tema del
  lector. El SVG va transparente; el PNG, con fondo blanco, para usarlo fuera de GitHub.
- **Paleta de obra.** Grafito para el texto, azul acero para la escena y la plataforma,
  naranja de alta visibilidad para el sujeto y la alerta, y el verde lima del chaleco como
  rampa de un solo tono para magnitudes. El par escena–sujeto está validado para
  daltonismo y contraste en los dos temas.
- **Una firma.** Las franjas de seguridad aparecen sólo como cinta angosta para marcar la
  alerta o lo que corre en vivo; nunca como relleno sobre datos.
- **Tipografía.** Lato para el texto y Ubuntu Mono para los identificadores. El SVG
  convierte el texto en trazos, así que se ve igual aunque el lector no tenga las fuentes.

## Tres advertencias de lectura

1. **La distribución está en línea continua** con la cadena: no es un proceso por lotes.
2. **El orden de arranque es control → distribución → medios.** El control queda suscripto
   a las detecciones antes de que los medios emitan, y la distribución necesita la
   identificación de la corrida de control. A las alertas no las protege el orden sino el
   publicador, que espera la suscripción del distribuidor.
3. **La máquina de estados tiene cinco estados y reabre a candidato**, no vuelve a inactivo.

## Regenerar

```bash
cd evidencia/figuras/scripts
python3 fig_a_vista_de_procesos.py
python3 fig_b_calidad_vs_densidad.py
python3 fig_c_alerta_anotada.py
python3 fig_e_maquina_de_estados.py
python3 fig_f_frontera_juzgabilidad.py
```

Requiere `matplotlib` (y `PyYAML` para la B) y las fuentes Lato y Ubuntu Mono; sin ellas,
matplotlib cae a DejaVu y las figuras cambian de aspecto pero no de contenido. La B
necesita además el repositorio `e-ovrt_experimental-setup` clonado como hermano, o
`EOVRT_RESULTS` apuntando a su carpeta `results/`. Cada script escribe la versión clara
(SVG y PNG) y la oscura (SVG); los SVG son estables entre corridas si el dibujo no cambia.
