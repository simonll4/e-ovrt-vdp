# Figuras
Las figuras del informe, en PNG a 300 dpi (ancho de diseño 16 cm) y SVG. Cuatro se generan
desde los datos publicados con los scripts de `scripts/`; la C es un fotograma.

| Figura | Archivo | Qué muestra | De dónde sale |
|---|---|---|---|
| A | `fig-a-vista-de-procesos` | los procesos de la plataforma y sus interfaces | especificación de la arquitectura |
| B | `fig-b-calidad-vs-densidad` | F1 de alertas vs densidad de evidencia, escena y sujeto | `results/clip_bench/{t1,g1,r1…r6}/metrics.json`; el script falla si la cifra no coincide; 1,15 fps es el stride 26 sobre 30 fps; 1,16–4,42 fps es la banda medida en vivo |
| C | `fig-c-alerta-confirmada` (+ `-completa`) | fotograma con la alerta confirmada dibujada | fotograma del clip `a_p1_c04` del rodaje propio, con la alerta dibujada por el renderizador de `defensa/` de `e-ovrt_experimental-setup` |
| E | `fig-e-maquina-de-estados` | la máquina de cinco estados del patrón | contrato de eventos de patrón del plano de control |
| F | `fig-f-frontera-juzgabilidad` | asociación de chaleco por banda de altura (A) y Nivel A por clip (B) | campañas del lote de internet |

## Tres advertencias de lectura
1. **La distribución está en línea, continua** con la cadena; no es un proceso por lotes.
2. **El orden de arranque es inverso al flujo de datos**: distribución → control → medios.
3. **La máquina de estados tiene cinco estados y reabre a candidato**, no vuelve a inactivo.

## Regenerar
```bash
cd evidencia/figuras/scripts
python3 fig_a_vista_de_procesos.py && python3 fig_b_calidad_vs_densidad.py && python3 fig_e_maquina_de_estados.py && python3 fig_f_frontera_juzgabilidad.py
```
Requiere `matplotlib` y, para la B, el repo `e-ovrt_experimental-setup` clonado como hermano
(o `EOVRT_RESULTS` apuntando a su carpeta `results/`); la F tiene sus datos embebidos en el
script. `estilo.py` concentra paleta y tipografía: tocarlo cambia las cuatro a la vez.
