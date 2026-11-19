# Cómo leer la consola

<!-- Generado por e-ovrt_experimental-setup/webconsole/tools/exportar_como_leer.py desde
     results/evidence-vista/documentacion.yaml. No editar a mano: se edita el YAML y se vuelve a exportar. -->

La consola de `e-ovrt_experimental-setup/webconsole` muestra la evidencia del informe y la plataforma funcionando. Lo que sigue es la documentación que la acompaña: cómo se trabajó, qué aporta cada cosa, cómo aparece cada término en el código, los símbolos que significan más de una cosa y el vocabulario completo. Dentro de la consola, cada término marcado muestra su definición al pasar el mouse.

## Cómo se trabajó

### 1. De dónde salen los datos

- **Qué se hizo.** Se juntaron datasets públicos de obra, se los tradujo a un vocabulario único de cuatro clases y se congeló un banco de imágenes sobre tres fuentes independientes. Aparte se filmó un rodaje guionado y se sumó un lote de video de obra real, anotados a mano con el momento exacto en que cada condición empieza y termina.
- **Por qué.** Cada dataset le pone su propio nombre a la misma cosa. Sin un vocabulario único no se puede comparar un modelo contra otro. Y el banco se estratifica por fuente porque un agregado de una sola fuente mide la fuente, no el modelo: el primer banco resultó un cuarto fuera del dominio de obra —selfies con barbijo, un aeropuerto, un casino— y se auditó y se reemplazó.
- **Qué quedó.** El banco de imágenes congelado con su huella por estrato, y el banco de clips con sus episodios de referencia. Los nombres de clase que se leen en toda la consola salen de ahí.

### 2. Cómo se eligió el modelo

- **Qué se hizo.** Primero seis modelos crudos, para tener un punto de partida. Después la matriz de selección: diez combinaciones de modelo y resolución, sobre el banco de imágenes anterior. Ganó gdino-tiny-560, que pasó a ser el perfil operativo. Recién entonces se lo re-midió estrato por estrato sobre el banco vigente, y ahí se confirmó.
- **Por qué.** El modelo no se elige por reputación: se elige midiéndolo sobre el material propio. Y el agregado solo no alcanza, porque está dominado por el estrato más numeroso: un modelo que gana únicamente ahí estaría ganando la fuente, no la tarea.
- **Qué quedó.** Un perfil operativo robusto a la fuente, y una asimetría que condiciona todo lo que viene después: persona y casco sólidas, chaleco débil y cabeza descubierta fuerte solo en el contraste base-560.

### 3. Cómo se pregunta por una condición de riesgo

- **Qué se hizo.** Se compararon dos maneras de escribir la pregunta. Por ausencia del EPP (E-IND) se pregunta por lo que se ve —persona, casco, chaleco— y se deduce la ausencia. Estrategia directa (E-DIR) se pregunta derecho por la infracción. La comparación se escribió antes de correr, con su criterio de corte fijado antes de mirar los números.
- **Por qué.** En detección open-vocabulary la pregunta es parte del sistema. Cambiar cómo está redactada cambia el resultado sin tocar el modelo, así que hay que medirla como se mide un componente, no elegirla por gusto.
- **Qué quedó.** Gana deducir la ausencia del EPP, en imágenes y en el rodaje. La detección directa quedó vetada por el criterio de precisión escrito antes de medir. Lo que manda es la formulación, no el mecanismo.

### 4. Qué agrega la plataforma sobre la detección cruda

- **Qué se hizo.** Sobre las mismas detecciones se midieron dos capas del motor de reglas: la persistencia temporal, que confirma una condición recién cuando se sostiene, y la identidad por sujeto, que sigue a cada persona en vez de mirar la escena entera.
- **Por qué.** Un detector de fotogramas no alerta: parpadea. La plataforma es lo que convierte detecciones intermitentes en una alerta con estado. Había que separar cuánto de la mejora es del modelo y cuánto del motor, y la única forma limpia es dejar las detecciones fijas y cambiar sólo la capa.
- **Qué quedó.** Seguir a cada persona suma sobre mirar la escena con las mismas detecciones, aunque con la referencia corregida esa ganancia ya no se puede afirmar como un efecto robusto. La persistencia es una palanca de doble filo: rescata percepción intermitente y multiplica las falsas alarmas.

### 5. Qué pasa en tiempo real

- **Qué se hizo.** Se repitió el banco con menos fotogramas por segundo, a tres densidades, y se corrió el rodaje en vivo con la plataforma en contenedores: con la OAK-D, con la cámara IP y con varios motores. La entrega por MQTT se midió aparte, como el tramo aparte que es.
- **Por qué.** Offline se procesa cada fotograma; en vivo no. Una ganancia que se evapora al bajar la densidad no sirve para operar. Y los tramos de la cadena tienen cada uno su reloj y su dueño: no se suman percentiles entre tramos.
- **Qué quedó.** En vivo la cadena procesa la cadencia de la cámara de la demo y la alerta llega en segundos, que es lo que la persistencia del patrón espera a propósito; la distribución no es el cuello. Seguir a cada persona sigue sumando con menos densidad, pero su intervalo excluye el cero solo en algunas densidades.

## Qué aporta cada cosa

Corrida, experimento, campaña, evidencia y resultado se usan casi como sinónimos y no lo son.

| Qué es | Identificador | De qué habla | Qué suma |
|---|---|---|---|
| Corrida | `run_id` | Una ejecución de UN plano sobre UNA fuente. El plano de medios escribe sus detecciones; el de control, sus alertas. Es la unidad más chica que deja artefactos en disco. | La prueba material. Sin una corrida no hay detecciones que mirar. Lo que NO dice es qué se quiso probar con ella. |
| Experimento | `experiment_id` | Una corrida paraguas que dispara los tres servicios en el orden correcto y consolida los artefactos de todos en un solo directorio. | Reproducibilidad. El manifiesto declara la combinación entera, así que la misma línea se vuelve a correr sin tener que acordarse de nada. |
| Campaña | sin identificador propio | Un experimento —o un conjunto de ellos— corrido con una intención de contraste: cambia UNA cosa respecto de la línea de base. T1 es la línea de base; T2 cambia el modelo; G1 cambia la granularidad. | El significado. El contraste entre campañas ES el experimento: una campaña sola no prueba nada, y su número no es una nota de aprobación. |
| Evidencia | sin identificador propio | La copia curada y congelada de las corridas que el informe cita, con hash por archivo. Conserva lo textual y deja afuera imágenes y video. | Permanencia. Se lee con los tres servicios apagados y no cambia si mañana se borra un directorio de corridas. Una corrida que no está en el inventario no es evidencia por el solo hecho de existir. |
| Resultado | `result_id` | La unidad que el informe reporta: una campaña con su metrics.json, su procedencia por corrida y su título. El prefijo del identificador es el índice de results/ al que pertenece. | El nivel al que se habla en la defensa. Una corrida es un hecho; un resultado es una afirmación sostenida por corridas. |

## Equivalencias

Cada término del informe y de la consola, su código y cómo aparece en la implementación.

| En el informe y la consola | Código | En la implementación |
|---|---|---|
| Perfil operativo | — | «campeón» en la campaña; el modelo gdino-tiny-560 y su instancia mp-gdino-tiny-560; el modo de prompts campeon de la demo |
| Contraste base-560 | — | el modelo gdino-base-560 y su instancia mp-gdino-base-560 |
| Sin casco | `CR-01` | el patrón PR-01; cr01 en los conjuntos de prompts y de reglas |
| Sin chaleco | `CR-02` | el patrón PR-02; cr02 en los conjuntos de prompts y de reglas. La condición es «persona sin chaleco de alta visibilidad» (la v0.2 del informe decía «reflectivo») |
| Estrategia indirecta (por ausencia del EPP) | `E-IND` | los prompts eind_v1 y cr01_cr02_v2_short; la campaña T1 (en la campaña final, ALR-01) |
| Estrategia directa (detección directa) | `E-DIR` | los prompts edir_v1 y las reglas cr01_cr02_edir_v1; las dos campañas D1 (en la campaña final, PER-01 y ALR-04) |
| Estrategia híbrida (por disyunción) | `E-HYB` | las reglas cr01_cr02_hyb_or_v1; la campaña H1 (en la campaña final, ALR-05) |
| Por escena y por sujeto | — | la granularidad scene y subject del motor de reglas; las campañas T1 y G1 (en la campaña final, ALR-01 y ALR-02) |
| G2A (latencia por cuadro) | `G2A` | Glass-to-Algorithm; g2a_ms en las métricas del motor de detección |
| FPS efectivos | — | fps_efectivos en los resultados: los cuadros procesados entre el primero y el último. La medición anterior, que dividía por la duración entera de la corrida, queda como fps_sobre_duracion |
| Estado por persona y alerta por episodio | — | «Nivel A» y «Nivel B» en la v0.2 del informe y en la etapa de desarrollo; la carpeta results/bench_nivel_a |
| La concordancia de una prueba | — | el campo veredicto de cada resultado (identico, equivalente_con_diferencia, otra_combinacion), que se firma con evidencia veredicto. «Veredicto» queda solo para el GO / NO-GO del ajuste fino |
| Los estados de la demo: en regla, confirmando, alerta, resolviendo, resuelta | — | los del motor de patrones: inactivo (inactive), candidato (candidate), confirmado o sostenido (confirmed, sustained), sostenido con la histéresis en curso y resuelto (resolved) |
| Densidad de uno de cada 7, 15 o 26 cuadros | — | el stride (paso entre cuadros) con que se decima el clip; las campañas R1 a R6 (en la campaña final, DEN-01 a DEN-06). En la etapa de desarrollo se las llamó «techo en vivo», «intermedia» y «peor caso» |
| Los resultados | — | la carpeta results/gen2, con una carpeta por prueba; gen2 en commits y carpetas |
| La etapa de desarrollo (el Archivo) | — | las carpetas results/clip_bench, results/bench_imagenes, results/bench_nivel_a y results/realtime; gen1 en commits y carpetas |
| Una prueba | `ALR-01, IMG-01…` | su registro previo en experiments/evidencia/<ID>/prueba.yaml y lo que dejó al correr en results/gen2/<ID>; la corre tools/evidencia |
| Lo que se escribió antes de correr | — | el pre-registro (prueba.yaml), copiado en la carpeta de la prueba al correr |
| El banco de imágenes | — | bench_v3, construido sobre el vocabulario canonical_v2 |
| El rodaje y la obra real | — | el banco temporal clip_bench; los clips a_* son el rodaje y los v* la obra real |
| La referencia | — | el GT (ground truth); en el banco temporal, anotado en CVAT; en el de imágenes, el de los datasets públicos |
| Persona, casco, chaleco y cabeza descubierta | — | las clases person, helmet, vest y bare_head |
| Motor de detección, motor de reglas y distribución | — | media-plane, control-plane y alert-distribution |
| Demo con cámara y tomas en vivo | — | /demo; los scripts demo.ps1 y rodaje.ps1; las sesiones en defensa/sesiones |

## Símbolos que significan más de una cosa

### `T1 / T2`

En esta consola T1 y T2 son siempre campañas del banco temporal. Los tres tramos del ajuste fino se llaman «tramo 1», «tramo 2» y «tramo 3», como en el informe. Solo sus archivos conservan el prefijo t1_ y t2_ (carpeta finetuning/), porque son nombres de archivo con huella y no se renombraron.

- **T1 y T2 (campañas).** La línea de base del banco temporal y su contraste de modelo; en la campaña final, ALR-01 y ALR-03. T1 es la referencia por escena; G1, la referencia por sujeto.
- **Tramos 1, 2 y 3 del ajuste fino (archivos t1_ y t2_).** Los tres tramos de la rama de ajuste fino: proyección de clases y ajuste completo, los dos con veredicto NO-GO, y un tercero cerrado con causa técnica sin llegar a veredicto. Ninguno se adoptó como modelo de servicio.

### `D1`

D1 nombra dos campañas distintas de la etapa de desarrollo. La consola las nombra por su prueba de la campaña final, que no se repite: PER-01 y ALR-04. El result_id también las distingue.

- **D1 por persona en imágenes (hoy PER-01).** La comparación, persona por persona, entre deducir la ausencia del EPP y describir la infracción, sobre el banco de imágenes. Estado por persona.
- **D1 de extremo a extremo en el rodaje (hoy ALR-04).** La campaña del banco temporal con los prompts que describen la infracción. Alerta por episodio.

## Vocabulario

### Identificadores

Los nombres que viajan entre los tres servicios. Cada uno identifica una cosa distinta y ninguno reemplaza a otro.

- `run_id`: Corrida de un plano. Vive en runs/<run_id>/ del repositorio de ese plano. En vivo la relación es uno a uno: una corrida de control por cada corrida de medios.
- `experiment_id`: Identificador de la ejecución experimental: la unidad que agrupa las corridas independientes de los componentes que participan en una misma instancia del experimento (informe, §17.3.4.1). Cada componente conserva su propio run_id; el experimental-setup consolida los artefactos: lo liviano se copia y el JSONL de detecciones se referencia.
- `unit_id`: Identidad de un fotograma dentro de una corrida. Es la clave con la que se cruzan detecciones, descartes, progreso y alertas entre planos; cruzar por número de fotograma colapsa cuando la fuente es una carpeta de imágenes.
- `clip_id`: Identidad de un clip del banco de video. Por convención coincide con el identificador de la fuente, y es lo que permite unir una alerta con el episodio anotado que le corresponde.
- `source_id`: Identidad de la fuente visual de una corrida: la carpeta, el archivo de video, la cámara. En el banco temporal es igual al clip_id.
- `track_id`: Identidad de una persona a lo largo del tiempo. Se produce con un seguidor por solapamiento de cajas y es lo que habilita la granularidad por sujeto. No hay métricas de seguimiento: quedaron fuera de alcance declaradas.
- `result_id`: La unidad que reporta el informe. Su prefijo es el índice de results/ al que pertenece, y por eso agrupar por prefijo reproduce exactamente los cuatro índices.

### Condiciones de riesgo y clases

Qué se busca y con qué palabras. La condición es lo que le importa a la obra; la clase es lo que el detector sabe nombrar.

- `CR-01`: Presencia de persona sin casco. Severidad alta. Es una de las dos condiciones del núcleo validable.
- `CR-02`: Persona sin chaleco de alta visibilidad. Severidad media. La otra condición del núcleo validable.
- `PR-01`: El patrón que operacionaliza CR-01 con persistencia temporal: la condición confirma recién cuando se sostiene 4.000 ms, y se resuelve a los 2.000 ms de dejar de verse. El valor sale de la banda que le corresponde a su SEVERIDAD (alta: 3 a 5 s), declarada antes de medir nada y nunca recalibrada entre corridas de una misma comparación.
- `PR-02`: El patrón que operacionaliza CR-02. Confirma a los 7.000 ms y resuelve a los 3.000 ms. Es más lento que PR-01 por SEVERIDAD, no por el detector: su banda es la de severidad media (5 a 10 s), y la de PR-01 la de severidad alta (3 a 5 s). Los umbrales quedaron fijados antes de que se midiera ninguna clase — el motor no se ajustó a lo que el detector hace bien o mal, y ésa es la condición para que las campañas se puedan comparar entre sí.
- `person`: Persona. Una de las cuatro clases del vocabulario canónico, y la más sólida del detector.
- `helmet`: Casco puesto. Es evidencia POSITIVA: CR-01 se deduce de que haya una persona y no haya casco, no de un prompt que pregunte por la ausencia.
- `vest`: Chaleco de alta visibilidad. Es la clase DÉBIL del perfil operativo —bastante por debajo de person y helmet— pero no la más floja: esa es bare_head. Nada de esto explica los umbrales de PR-02, que salen de la severidad de la condición y se fijaron antes de medir las clases.
- `bare_head`: Cabeza descubierta. Es la vía directa a CR-01 y la clase MÁS FLOJA del perfil operativo, bastante por debajo de vest. Sólo el modelo grande la detecta con algo de solvencia, y ésa es UNA de las dos razones por las que hay un especialista: la otra es vest, donde también rinde mejor. Los modelos de la familia YOLOE son directamente ciegos a esta clase.
- `canonical_v2`: El vocabulario canónico compartido entre repositorios: person, helmet, vest y bare_head. Todo dataset se traduce a estas cuatro clases antes de entrar a cualquier medición.

### Las cinco clases de corrida

Para qué sirvió cada corrida. Se clasifica el ROL que cumple en el registro, no la corrida una por una, y la clasificación se propaga sola. Si una corrida cumple dos roles, vale el más fuerte.

- **Resultado**: La corrida sostiene una cifra que el informe reporta. Es la clase más fuerte: si algo es Resultado en algún lado, es Resultado.
- **Instrumento**: La corrida valida el aparato de medición, no el fenómeno: la claqueta con reloj externo, la paridad entre vivo y archivo, la instrumentación de la latencia.
- **Ensayo**: Prueba previa a una campaña: verificar que el camino entero anda antes de gastar el material. No sostiene ninguna cifra reportada.
- **Prueba de plataforma**: La máquina probándose a sí misma. Son los smokes que escribe la suite de tests, y su total crece solo con cada corrida de la suite: se cita la proporción, nunca el número absoluto.
- **Fuera del registro**: La corrida existe en disco pero su rol no está declarado. Es el default, nunca una conclusión: que algo caiga acá puede significar que es basura o que falta declararlo.

### Campañas

Son los códigos de la etapa de desarrollo. Cada campaña cambia una sola cosa respecto de su referencia, y el contraste entre filas es el experimento. Hoy cada una tiene su prueba en la campaña final, y ése es el nombre que se usa: el código sirve para encontrarla en el Archivo. En el banco de VIDEO hay DOS referencias, una por granularidad: T2, D1, H1, G1, B1 y las densidades por escena (R1, R3, R5) se leen contra T1; las densidades por sujeto (R2, R4, R6), contra G1. I1 e I2 cambian el material y se leen aparte. S1 y B5 son del banco de imágenes y NA1 mide el estado por persona: ninguno de los tres se compara contra T1.

- **T1**: La línea de base del banco temporal: perfil operativo, prompt set congelado y granularidad de escena. No cambia nada: es la referencia de escena contra la que se leen las campañas que sí cambian algo. Las campañas por sujeto tienen la suya, que es G1. En la campaña final, ALR-01. Resultados: [`clip_bench/t1_gdinotiny560_v2short_scene`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/main/results/clip_bench/t1_gdinotiny560_v2short_scene).
- **T2**: Cambia el MODELO: el grande en lugar del perfil operativo, con todo lo demás igual. Sirve para separar qué mejora da el modelo y qué da la plataforma. En la campaña final, ALR-03. Resultados: [`clip_bench/t2_gdinobase560_v2short_scene`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/main/results/clip_bench/t2_gdinobase560_v2short_scene).
- **D1**: Cambia los PROMPTS: pregunta derecho por la ausencia en vez de deducir la infracción. Ojo, son dos experimentos distintos con el mismo nombre, uno por nivel — ver las colisiones de símbolos. Son dos campañas: la de imágenes, persona por persona, es hoy PER-01; la del rodaje, ALR-04. Resultados: [`bench_nivel_a/d1_gdinotiny560_edir_vs_eind`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/main/results/bench_nivel_a/d1_gdinotiny560_edir_vs_eind), [`clip_bench/d1_gdinotiny560_edirpair_scene`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/main/results/clip_bench/d1_gdinotiny560_edirpair_scene).
- **H1**: Cambia la ESTRATEGIA: fusiona las dos formulaciones de prompt. La fusión por unión quedó refutada. En la campaña final, ALR-05. Resultados: [`clip_bench/h1_gdinotiny560_hybor_scene`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/main/results/clip_bench/h1_gdinotiny560_hybor_scene).
- **G1**: Cambia la GRANULARIDAD: por sujeto en vez de por escena, con las detecciones bit a bit idénticas a T1. Es el mejor resultado del banco, y toda la ganancia es del motor. En la campaña final, ALR-02. Resultados: [`clip_bench/g1_gdinotiny560_v2short_subject`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/main/results/clip_bench/g1_gdinotiny560_v2short_subject).
- **B1**: Cambia el VOCABULARIO: pregunta por cabeza descubierta de forma directa, con el modelo grande. Gana cobertura del episodio y pierde precision. En la campaña final, ALR-06. Resultados: [`clip_bench/b1_gdinobase560_barehead_scene`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/main/results/clip_bench/b1_gdinobase560_barehead_scene).
- **R1**: Densidad de evidencia: uno de cada 7 fotogramas (≈4,29 por segundo), por escena. Se ancló al techo que se había medido en vivo en la etapa de desarrollo, con la medición de cuadros por segundo que después se corrigió. En la configuración de la demo el vivo procesa 5 por segundo, así que R1 queda apenas por debajo y es su mejor sustituto. En la campaña final, DEN-01. Resultados: [`clip_bench/r1_gdinotiny560_v2short_scene_s7`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/main/results/clip_bench/r1_gdinotiny560_v2short_scene_s7).
- **R2**: Uno de cada 7 fotogramas, por sujeto. Es el par de R1: juntos miden si la ganancia de la identidad sobrevive al decimado. En la campaña final, DEN-02. Resultados: [`clip_bench/r2_gdinotiny560_v2short_subject_s7`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/main/results/clip_bench/r2_gdinotiny560_v2short_subject_s7).
- **R3**: Uno de cada 15 fotogramas, por escena. En la campaña final, DEN-03. Resultados: [`clip_bench/r3_gdinotiny560_v2short_scene_s15`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/main/results/clip_bench/r3_gdinotiny560_v2short_scene_s15).
- **R4**: Uno de cada 15 fotogramas, por sujeto. El par de R3. En la campaña final, DEN-04. Resultados: [`clip_bench/r4_gdinotiny560_v2short_subject_s15`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/main/results/clip_bench/r4_gdinotiny560_v2short_subject_s15).
- **R5**: Uno de cada 26 fotogramas, por escena. En la campaña final, DEN-05. Resultados: [`clip_bench/r5_gdinotiny560_v2short_scene_s26`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/main/results/clip_bench/r5_gdinotiny560_v2short_scene_s26).
- **R6**: Uno de cada 26 fotogramas, por sujeto. El par de R5. En la campaña final, DEN-06. Resultados: [`clip_bench/r6_gdinotiny560_v2short_subject_s26`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/main/results/clip_bench/r6_gdinotiny560_v2short_subject_s26).
- **I1**: Cambia el MATERIAL: obra real no guionada, por escena. Se reporta siempre como fila aparte, nunca fusionada al rodaje. En la campaña final, ALR-07. Resultados: [`clip_bench/i1_gdinotiny560_v2short_scene_internet`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/main/results/clip_bench/i1_gdinotiny560_v2short_scene_internet).
- **I2**: Obra real no guionada, por sujeto. El par de I1. Acá el seguidor fragmenta identidades en multitud, y eso explica su precision. En la campaña final, ALR-08. Resultados: [`clip_bench/i2_gdinotiny560_v2short_subject_internet`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/main/results/clip_bench/i2_gdinotiny560_v2short_subject_internet).
- **NA1**: Estado por persona sobre video, fotograma a fotograma, sin motor temporal. Mide el derrumbe de precision al salir de las imágenes. En la campaña final, PER-03. Resultados: [`bench_nivel_a/na1_gdinotiny560_v2short_video`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/main/results/bench_nivel_a/na1_gdinotiny560_v2short_video).
- **S1**: La selección del perfil operativo, sobre imágenes: DIEZ combinaciones de modelo y resolución, medidas sobre el banco de imágenes ANTERIOR (las 20 corridas del inventario son esas diez por los dos splits). El umbral no fue un eje de diseño, y la única excepción DOCUMENTADA —gdino-tiny a 800, que corrió a un umbral distinto del resto— es justamente lo que confunde la comparación de resolución en ese par: está declarado como defecto, no como método. No se repitió en la campaña final: la selección del modelo no se vuelve a hacer. Resultados: [`bench_imagenes/seleccion_s1`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/main/results/bench_imagenes/seleccion_s1).
- **B5**: La confirmación por estratos, y la única del banco de imágenes que corrió sobre el banco vigente: el perfil operativo sostiene el resultado en cada una de las tres fuentes por separado, no sólo en el agregado. En la campaña final, IMG-01, con IMG-02 e IMG-03 como contrastes. Resultados: [`bench_imagenes/confirmacion_b5`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/main/results/bench_imagenes/confirmacion_b5).

### Métricas y bancos

Qué mide cada número, y cuándo NO se puede comparar con otro. Las trampas escritas acá salieron de artefactos cazados antes de reportar.

- **F1**: La media armónica entre precision y recall. Es la cifra de cabecera del banco temporal. Los clips negativos no entran: su métrica son los falsos positivos.
- **precision**: De todo lo que el sistema afirmó, qué fracción era cierta. En la alerta por episodio se cuenta sobre alertas contra episodios; en el estado por persona, sobre estados de cada persona. Es el criterio que vetó a los prompts directos de ausencia.
- **recall**: De todo lo que había que encontrar, qué fracción se encontró. En la alerta por episodio son episodios anotados; en el estado por persona, personas en estado de infracción. Ojo con una intuición que la medición NO sostiene: preguntar derecho por la ausencia no compra recall a cambio de precision. En el estado por persona el costo es precision —un brazo directo llega a recuperar una parte de lo que la formulación indirecta no ve, afirmando de más—, pero en la alerta por episodio caen las DOS: el recall se desploma junto con la precision.
- **mAP50**: La métrica del banco de IMÁGENES: precisión promedio por clase con medio solapamiento exigido, promediada entre clases. No es comparable con el F1 del banco de video: son niveles distintos.
- **SDR**: Qué fracción del episodio anotado quedó cubierta por detecciones. Trampa: NO se compara entre cadencias — sube al bajar la densidad y esa subida es casi toda artefacto del instrumento.
- **TTFD**: Cuántos milisegundos pasan entre el inicio del episodio anotado y la primera detección que le corresponde.
- `t_alert-system`: Del inicio anotado del episodio a la alerta. Está dominado por la persistencia del patrón, no por el transporte: no se encadena aritméticamente con los tramos físicos. Trampa: su promedio no se compara entre densidades sin control de supervivencia, porque los episodios lentos se pierden y su salida baja el promedio justo cuando el costo sube.
- `t_alert-notification`: Del bus de alertas al acuse del broker MQTT. Es el último tramo de la cadena y NO es el cuello: queda muy por debajo del G2A del modelo que detecta en vivo (las cifras, en «¿Funciona en vivo?»). No representa sensor a notificación y se cita separado. Resultados: [`realtime/t_alert_notification`](https://github.com/simonll4/e-ovrt_experimental-setup/tree/main/results/realtime/t_alert_notification).
- **G2A (latencia por cuadro)**: Del momento en que el fotograma se saca de la cola en el host al resultado del algoritmo, por fotograma. No incluye la captura ni el transporte hasta el host, que se miden aparte.
- **FPS efectivos**: Cuadros procesados por segundo, contados entre el primer y el último cuadro de la corrida. No se divide por la duración entera: el arranque y el cierre no los diluyen.
- `re_alerts`: Alertas repetidas del mismo episodio, porque el motor emite en cada confirmación. Se cuentan aparte y NO son falsos positivos.
- `bench_v3`: El banco de imágenes vigente: 6.477 imágenes sobre tres fuentes independientes, congelado con hash por estrato. El banco viejo de 196 imágenes es un artefacto histórico y no se cita como resultado.
- **estrato**: En el banco de IMÁGENES, la partición del material: son tres, y salen de tres fuentes independientes. Ojo, los NOMBRES de los tres estratos no son los de las tres fuentes: dos coinciden y el tercero es el subconjunto curado internamente de su dataset de origen, no un cuarto dataset. Se reporta siempre por estrato Y agregado, nunca sólo el agregado: uno de los tres es el 77 % de las imágenes y se lleva puesto el promedio. ⚠ La misma palabra nombra otra cosa en el banco de VIDEO: ahí «estrato A» y «estrato B» son los dos bloques de material —el rodaje guionado y el lote de obra real— y son dos, no tres. Al leer «las campañas de estrato B» se habla de video, no de imágenes.
- **clip bench**: El banco de video con anotación temporal: 47 clips, 32 positivos y 15 negativos, en dos bloques — el rodaje guionado y el lote de obra real.
- **episodio**: Una ventana de tiempo anotada a mano donde una condición está presente y es observable. Con la referencia corregida son 35 en el banco (33 en el rodaje y 2 en la obra real), y son la unidad contra la que se juzga cada alerta.

### Limitaciones declaradas

Lista canónica y cerrada. Se declaran, no se esconden. Ojo al citar L1: la fase L del plan maestro usa L0 y L1 para sus hitos, que son otra cosa — escribir siempre "limitación L1".

- **L1**: Las falsas alarmas por hora se reportan como conteo crudo y no sostienen ninguna cota. Harían falta 3 horas de cumplimiento anotado y el banco llega a 0,27 h de tiempo negativo. La evidencia principal de falsas alarmas es el control de negativos. [Fuente](https://github.com/Pandulc/e-ovrt_datasets/blob/main/datasets/registry/clip_bench.md).
- **L2**: Sin doble anotación ni medida de acuerdo entre anotadores. Es una decisión declarada, no una omisión.
- **L3**: Los bordes del ground truth se adjudicaron a mano en 6 clips por oclusión, con firma en el archivo del clip. No hubo cambio de estado, sólo de borde.
- **L4**: Un solo bloque guionado. El lote de obra real existe, pero después de la revisión ciega quedan 2 episodios evaluables: caracteriza dónde el sistema deja de ser evaluable, no lo valida sobre obra real.
- **L5**: Los escenarios están desbalanceados. De ahí sale la regla de reportar siempre por escenario y por estrato.
- **L6**: El seguidor no está medido con métricas de seguimiento. En multitud real fragmenta identidades, y esa fragmentación es un dato medido, no un hueco.
- **L7**: Una de las tres fuentes del banco de imágenes no tiene licencia formal: uso permitido con cita, sin redistribución.
- **L8**: CR-02 en el estado por persona no está cerrada: un solo estrato y intervalos de confianza solapados.

### Escenarios de despliegue y plataforma

Dónde corre el sistema y cómo se hablan sus partes. Hay dos patrones de acople, no tres: HTTP config-driven en los tres servicios, y bus de eventos.

- `DBE`: Evaluación sobre dataset: el escenario offline. El plano de medios escribe sus detecciones en un archivo y el de control lo relee. El archivo es la fuente de verdad.
- `EBE`: Evaluación sobre entorno: el escenario en vivo. Los planos se acoplan por un bus de eventos y la corrida es uno a uno. Toda corrida en vivo es re-evaluable offline y produce artefactos idénticos.
- **captura → host**: El tramo que va desde que la cámara captura el cuadro hasta que el cuadro sale de la cola en el host. Se mide aparte del G2A, que arranca recién ahí: sumados, por cuadro, dan el recorrido de la imagen a la detección.
- **testigo MQTT**: Un suscriptor del broker, independiente del distribuidor, que registra cada notificación con su hora de llegada. Es la prueba de que la alerta pasó por el broker, no la palabra del que la envió.
- **Por escena**: La condición se juzga sobre el cuadro entero, sin identidad de personas. Es el núcleo validable. En los documentos internos se la llama G0.
- **Por sujeto**: La condición se juzga por persona seguida. Es la que mide la campaña G1 (en la campaña final, ALR-02). En los documentos internos se la llama G1, como la campaña.
- `OVD`: Detección de vocabulario abierto: el detector se guía por texto en vez de por un conjunto fijo de clases entrenadas. Es lo que permite pedir una clase nueva sin reentrenar.
- `E-IND`: Estrategia indirecta: se detecta la persona y el equipo, y la ausencia se deduce. Es el encuadre adoptado.
- `E-DIR`: Estrategia directa: el prompt describe la infracción. Medida y vetada por precision como núcleo.
- `E-HYB`: Fusión de las dos estrategias. La variante por unión quedó refutada; la variante por intersección no se ejecutó, y eso está declarado con causa.
- **prompt set**: El conjunto versionado de prompts con el que corre una campaña. Se congela con hash: una campaña congelada no puede cambiar de pregunta sin cambiar de identidad.
- **pattern set**: El conjunto versionado de patrones del motor de reglas: qué condición confirma, cuándo y con qué severidad.
- **histéresis**: La persistencia temporal del motor: una condición pasa por cinco estados y sólo emite alerta al entrar en confirmada. Es lo que evita alertar por un parpadeo, y también lo que retrasa la alerta a propósito.
- `bus.envelope.v1`: El sobre de los eventos del bus, con número de secuencia monótono. Un hueco en la secuencia se cuenta como evento perdido y degrada la corrida: nunca se silencia.
- **stride**: Cada cuántos fotogramas se procesa uno. Stride 7 significa uno de cada siete: es la palanca con la que se simula la densidad del camino en vivo sobre material offline.
- **Estado por persona**: Se juzga el estado de cada persona —por imagen o por fotograma, según el material— sin motor temporal en el medio. Mide percepción. Es lo que antes se llamaba «Nivel A».
- **Alerta por episodio**: Se juzga la alerta contra el episodio anotado, con el motor temporal en el medio. Mide la plataforma. Es lo que antes se llamaba «Nivel B».
