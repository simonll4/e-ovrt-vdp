# 1 · El problema y el enfoque

## El riesgo que se mira

En una obra de construcción, el uso de elementos de protección personal (EPP) es una
condición observable a simple vista: alcanza con mirar si una persona lleva puesto el
casco o el chaleco reflectivo. La plataforma se concentra en dos condiciones de riesgo
sobre esa base — **CR-01, persona sin casco**, y **CR-02, persona sin chaleco** —,
elegidas porque son observables en video, frecuentes en el día a día de una obra y
tienen consecuencias de gravedad distinta: CR-01 se trata como severidad alta y CR-02
como severidad media.

## Por qué detección open-vocabulary sin entrenar

Un detector open-vocabulary recibe la clase que tiene que buscar escrita en lenguaje
natural — "person", "helmet", "vest", "bare head" — y no necesita un dataset etiquetado
específico para la obra donde se lo despliega: la condición se declara, no se entrena.
Esa capacidad es lo que este trabajo pone a prueba. La apuesta **no** es que un detector
open-vocabulary reconozca cascos o chalecos mejor que un modelo entrenado a medida para
esa tarea puntual; la apuesta es medir, con rigor, qué rendimiento da hoy un detector
así, sin haber entrenado con una sola imagen de obra, y qué le agrega, alrededor, la
plataforma que lo rodea.

## La hipótesis de plataforma

Una detección por cuadro de video no es una alerta. Entre una y otra hay un tramo
completo: agrupar la evidencia por sujeto, sostenerla en el tiempo, confirmarla como una
condición real y decidir cuándo y cómo notificarla. Ese tramo — evidencia por sujeto,
persistencia temporal, confirmación y política de notificación — es la plataforma
propiamente dicha, y es lo que este trabajo diseña, construye y mide: no solamente el
detector.

## Qué se mide

La evaluación cubre cuatro niveles: el nivel de percepción, sobre bancos de imágenes; el
nivel de percepción por sujeto (Nivel A), que reconstruye el estado "sin EPP" por
persona; el nivel de plataforma (Nivel B), que compara las alertas que produce el
sistema contra una referencia humana construida sobre clips de video; y la operación en
vivo, con el bus de eventos, la latencia y el throughput bajo restricciones de tiempo
real. Ver [`05-metodo-experimental.md`](05-metodo-experimental.md).

Siguiente: [`02-arquitectura.md`](02-arquitectura.md)
