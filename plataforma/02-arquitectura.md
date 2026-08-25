# 2 · Arquitectura

![Vista de procesos](../evidencia/figuras/fig-a-vista-de-procesos.png)

## Tres servicios HTTP config-driven y una consola

| Servicio | Puerto | Hace | No hace |
|---|---|---|---|
| Plano de medios (`e-ovrt_media-plane`) | `:8080` | ingesta (carpeta de imágenes, video, RTSP, OAK-D), inferencia open-vocabulary, publica eventos `media.detection.v1` | patrones, alertas, UI |
| Plano de control (`e-ovrt_control-plane`) | `:8081` | consume detecciones, evalúa CR-01/CR-02 con persistencia temporal e identidad por sujeto, emite alertas confirmadas | notificación externa, UI |
| Distribución (`e-ovrt_alert-distribution`) | `:8082` | consume alertas confirmadas, política de notificación, entrega MQTT QoS 1 idempotente | recalcular severidad |
| Consola web (`e-ovrt_experimental-setup/webconsole`) | `:8090` | cliente HTTP de los tres; define, lanza y compara experimentos reproducibles | consumir el bus |

La plataforma completa está formada por estos tres servicios más la consola que los
orquesta. Los tres son *config-driven*: no hay rutas ni umbrales escritos en el código,
todo se declara en archivos de configuración YAML. Cada uno expone las mismas
operaciones de gobierno — `POST /api/runs` para disparar una corrida, `GET /healthz` y
`GET /readyz` para verificar su estado — y el modelo (o la configuración pesada
equivalente) se carga una única vez al arrancar el servicio, no en cada corrida.

## Contratos versionados

La comunicación entre los servicios se apoya en contratos de datos versionados, no en
acuerdos implícitos. `media.detection.v1` es el evento de detección por cuadro, con un
`track_id` opcional para cuando hay seguimiento entre cuadros. `bus.envelope.v1` es el
sobre que transporta esos eventos por el bus de mensajes, con número de secuencia,
identificador de corrida y marcas de tiempo. A esto se suman los eventos de cambio de
estado del patrón y de alerta que emite el plano de control, y `run.lifecycle.v1`, que
marca el inicio y el cierre de cada corrida. La regla de evolución de estos contratos es
que los cambios son siempre aditivos: quien emite un evento puede omitir un campo nuevo
sin romper a quien lo consume, y quien consume tolera campos que todavía no conoce.

## Dos formas de acoplarse

Los servicios se acoplan de dos maneras, según el escenario de despliegue. Por archivo:
el plano de medios escribe `detections.jsonl` y el plano de control lo relee más tarde.
Y por bus de mensajes: ZeroMQ en modo publicador/suscriptor con serialización msgpack,
para cuando ambos servicios corren al mismo tiempo. El archivo JSONL es la fuente de
verdad en los dos casos — toda corrida en vivo puede reevaluarse después de forma
offline y produce artefactos idénticos. El detalle de cuándo se usa cada camino está en
[`04-escenarios-dbe-ebe.md`](04-escenarios-dbe-ebe.md).

## Deploy integral

Toda la plataforma se despliega con un único `docker compose`: la consola, el plano de
control, la distribución, un broker MQTT y una flota de instancias del plano de medios
—una por modelo, que la propia consola enciende y apaga—, 13 servicios en total. La
regla que hace este despliegue portable entre máquinas es la paridad de rutas: la
consola, el plano de control y la distribución montan el directorio de trabajo
compartido en la misma ruta absoluta que tiene en la máquina anfitriona, porque los
contratos entre ellos intercambian rutas de archivo sobre un sistema de archivos
compartido, no los archivos en sí. Fuente:
[`infra/platform/`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/HEAD/infra/platform)
en `e-ovrt_experimental-setup`.

Siguiente: [`03-flujo-de-una-alerta.md`](03-flujo-de-una-alerta.md)
