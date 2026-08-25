# 5 · Método experimental

## Cuatro niveles de medición

| Nivel | Material | Pregunta |
|---|---|---|
| Percepción (imágenes) | `bench_v3` | qué ve el detector sin entrenar; costo de una clase nueva |
| Percepción por sujeto (Nivel A) | `bench_v3` + clips | estado "sin EPP" por persona; E-DIR vs E-IND |
| Plataforma (Nivel B) | banco de clips con referencia humana | alertas contra episodios anotados |
| Operación (EBE) | corridas en vivo | integridad del bus, latencia, throughput, calidad bajo tiempo real |

**Cuatro preguntas, un mismo marco.** La evaluación se organiza en cuatro niveles que
suben de abstracción: qué ve el detector sin haber entrenado con una sola imagen de
obra, si esa percepción alcanza para reconstruir el estado de una persona, si la
plataforma completa —con persistencia, identidad y confirmación— produce alertas que
coinciden con una referencia humana, y qué de todo eso sobrevive cuando la corrida
pasa a ejecutarse en vivo, con hardware real y restricciones de tiempo real. Cada
nivel usa material propio y responde una pregunta distinta; ningún nivel sustituye a
los otros.

## `bench_v3` — 6.477 imágenes, 3 fuentes independientes

**Tres fuentes, un mismo criterio de reporte.** El banco de percepción combina
`bench_obra` (147 imágenes, núcleo curado con pasada visual, licencia CC BY 4.0),
`chv` (1.330 imágenes, uso académico permitido con cita y sin redistribución —
limitación L7) y `shel5k` (5.000 imágenes, licencia CC BY 4.0, con la clase
`bare_head` nativa en el propio material). Cada imagen conserva la marca de a qué
fuente pertenece, y esa marca no es un detalle administrativo: el rendimiento medido
se reporta siempre por estrato además de agregado, porque una sola de las tres
fuentes puede dominar el promedio y esconder cómo se comporta el detector en las
otras dos. El banco tiene además un manifiesto con la huella (sha256) de cada
fuente, lo que permite regenerarlo byte a byte a partir de los datos originales y
verificar que no cambió entre una medición y la siguiente.

## Banco de clips con referencia temporal humana

**47 clips, con procedencia declarada.** El banco temporal —el material que alimenta
el nivel de plataforma— reúne 34 clips de un rodaje propio en obra, guionado, con
hardware real y una referencia anotada en video, en dos pasadas, sobre CVAT, más 13
clips de obra real no guionada tomados de internet. En conjunto suman 32 clips
positivos y 15 negativos, con 37 episodios de referencia. Esa referencia la
construye una persona, no un instrumento, y eso convierte su calidad en un
resultado más de la evaluación: una revisión ciega, hecha después de anotar,
encontró que 5 de las 7 declaraciones de episodio del lote de internet no
correspondían a un cambio de estado real, y el banco se corrigió en consecuencia
antes de reportar. La procedencia completa de cada clip está en
[`../evidencia/material-de-video.md`](../evidencia/material-de-video.md).

## Campañas por pregunta de medición

**Una campaña, una combinación, un veredicto local.** Cada campaña fija una
combinación —modelo, conjunto de prompts, granularidad y densidad de evidencia— y la
corre bajo un protocolo con criterios de veredicto decididos antes de ver el
resultado. Esa pre-registración es lo que permite tratar un NO-GO —una combinación
que no cumple su criterio— como un resultado más de la evaluación, y no como un
experimento fallido: el criterio se fijó antes de correr, así que el resultado, sea
cual sea, confirma el protocolo. Las campañas recorren varios ejes: qué modelo
conviene elegir, cómo conviene formular la condición de riesgo ante el detector
(evidencia positiva más inferencia, prompt directo de ausencia, o una fusión de
ambos —E-IND, E-DIR y E-HYB), a qué granularidad se evalúa (por escena o por
sujeto), a qué densidad de evidencia (30 fps de referencia, y 4,29 / 2,00 / 1,15 fps
emuladas sobre el banco — las cadencias que el camino en vivo sostuvo), qué pasa
sobre obra real no guionada, cómo
se comporta la distribución de alertas, y qué aporta un ajuste fino acotado —una
jornada con protocolo propio, ejecutada en clúster, con puertas de decisión sobre
ganancia, retención y capacidad open-vocabulary fijadas de antemano.

## Reglas de lectura

**Tres reglas para no leer mal una cifra correcta.** Toda cifra citada en los
resultados va acompañada de su material y su tamaño de muestra (`n`): un número sin
esos dos datos no es verificable. Los escenarios del banco están desbalanceados
entre sí, así que el reporte es siempre por escenario y por estrato, nunca sólo
agregado (limitación L5). Y las falsas alarmas por hora se publican como lo que
son —un conteo crudo, derivado de la exposición realmente observada— sin que
sostengan una cota operativa (limitación L1): la exposición disponible queda lejos
de lo que exigiría afirmar un límite horario.

## Licencias de los modelos

**Dos licencias, un mismo criterio de uso.** Grounding DINO se distribuye bajo
Apache-2.0. YOLOE se distribuye bajo AGPL-3.0 y se usó en esta evaluación como
contraste medido, descartado con causa cuando el resultado no lo sostuvo. En ningún
caso se redistribuyen los pesos de los modelos; cada uno se descarga desde su
fuente original.

Ver los resultados: [`../resultados/README.md`](../resultados/README.md)
