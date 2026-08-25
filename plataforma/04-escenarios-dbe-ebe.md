# 4 · Dos escenarios: offline (DBE) y en vivo (EBE)

## DBE — acople por archivo

En el escenario diferido (DBE) los dos planos no corren al mismo tiempo: el plano de
medios escribe cada evento de detección en `runs/<id>/detections.jsonl`, y el plano
de control lee ese archivo completo para evaluar los patrones. Ese archivo —el
repositorio de artefactos de la corrida— es la fuente de verdad: permite reevaluar
cualquier corrida más adelante con otra configuración de patrones, sin volver a
ejecutar el detector sobre el video original. Cambiar el conjunto de prompts sí
exige una corrida nueva del detector, porque el prompt es una entrada del plano de
medios, no del plano de control que relee el archivo.

## EBE — acople por bus

En el escenario en vivo (EBE) los tres servicios corren al mismo tiempo y se acoplan
por un bus de mensajes ZeroMQ en modo publicador/suscriptor, con serialización
msgpack sobre el contrato `bus.envelope.v1`, que numera cada evento con un `seq`. Los
huecos que aparecen en esa secuencia se cuentan como `bus_dropped_events` y degradan
la corrida; nunca se silencian ni se descuentan de la medición.

El orden de arranque es **inverso al orden en que fluyen los datos**: primero se
suscribe la distribución, después el plano de control, y recién al final se dispara
el plano de medios. La razón es que un socket publicador/suscriptor pierde todo lo
que se publicó antes de que el consumidor se suscriba, así que cada consumidor tiene
que estar escuchando antes de que su productor emita el primer evento. Advertencia
de lectura para la figura de vista de procesos: el orden que dibuja —①distribución,
②control, ③medios— es el operativo vigente, y va en sentido contrario al de la
detección que termina viajando por la cadena.

## Hardware real

La plataforma se probó con dos tipos de fuente de video: una cámara OAK-D Pro PoE,
con IP fija y el SDK DepthAI —que admite además una preselección liviana de personas
hecha on-device, opcional y apagada por defecto— y cámaras RTSP genéricas. La consola
web puede grabar el video en vivo y recortar clips a partir de él.

## Cómo se cita el tiempo (sin sumar percentiles)

| Tramo | Qué mide |
|---|---|
| `capture_to_host` | fotón → dequeue en el host |
| G2A | dequeue → alerta, por frame |
| `t_alert-system` | inicio anotado del episodio → alerta; dominado por la persistencia deliberada (4–7 s) |
| `t_alert-notification` | bus de alertas → PUBACK MQTT |

Cada tramo tiene reloj, responsable y cifra propios, y no se suman percentiles entre
tramos: un p95 de captura y un p95 de notificación no se encadenan en un solo número.
Las cifras, siempre acompañadas del tamaño de muestra `n` que las respalda, están en
[`resultados/`](../resultados/README.md).

Siguiente: [`05-metodo-experimental.md`](05-metodo-experimental.md)
