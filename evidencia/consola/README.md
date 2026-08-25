# La consola web

Capturas de la consola (`e-ovrt_experimental-setup/webconsole`, React + FastAPI) tomadas con
la plataforma completa levantada en local con el modelo `mock` (sin GPU). Los datos que se
ven son las corridas reales del repositorio. Al momento de la captura no había ningún
experimento efectivamente ejecutado (los manifiestos de experimento existen, pero ninguno
tiene una corrida asociada todavía), así que se omite la captura de detalle de experimento.

| Captura | Pantalla | Qué muestra |
|---|---|---|
| `01-plataforma.png` | Plataforma | badges de estado de los servicios de detección y de reglas, y el aviso de que la orquestación de flota no está habilitada en esta instancia (consola apuntando a una instancia fija); con el deploy integral de `infra/platform/` esta misma pantalla enciende y apaga la flota de instancias del plano de medios |
| `02-componer-corrida.png` | Componer | fuente, prompt set y lanzamiento; modelo, control y distribución quedan en «Opciones avanzadas» |
| `03-corridas.png` | Corridas | historial de corridas del plano de medios |
| `04-detalle-de-corrida.png` | Detalle de corrida | métricas, artefactos y línea de tiempo de una corrida |
| `05-experimentos.png` | Experimentos | manifiestos de experimento por referencia y su estado |
| `07-comparar.png` | Comparar | comparación de corridas/campañas |
| `08-prompt-sets.png` | Prompt sets | ciclo de vida de los prompt sets: alta, edición, congelamiento |

Nota de numeración: la captura `06` (detalle de experimento) se omitió porque ningún
experimento corrió en esta instancia.
