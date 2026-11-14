# Actividades de análisis con el dataset

## Actividad 1

### Predicciones

1. **Cuando llueve, ¿qué medio crees que domina y por qué?**
   La camioneta, ya que el dron no puede volvar con la lluvia, la bicicleta peude ser incomoda y la moto puede ser un poco mas peligrosa que la camioneta.
2. **Para el centro de la ciudad, ¿qué medio crees que domina y por qué?**
   La moto o la bicicleta, por que son distancias mas cortas.
3. **¿Cuál crees que será la distancia máxima de una bicicleta en los datos?**
   Pueden ser 6 km
4. **¿Crees que habrá envíos cuya etiqueta rompa las reglas del negocio? ¿Por qué?**
   Si por que se menciona que s eagrego ruido humano.

### Comprobación

1. **¿En qué zonas y con qué climas el dron nunca aparece? ¿Qué regla lo explica en cada caso?**
   En climas, el dron tiene 0.00% en lluvia y 0.00% en viento fuerte (solo aparece en despejado con 13.52%). La regla que lo explica es que por seguridad física y normativa de aviación, los drones no pueden volar con lluvia ni con ráfagas de viento.
   En zonas, el dron tiene 0.00% en centro y 0.00% en rural (aparece en residencial con 17.30% y periferia con 12.61%). En el centro no vuela por restricción legal sobre edificios y aglomeraciones urbanas, y en zona rural no aparece porque la distancia mínima a esa zona es 15.93 km y el dron tiene un límite físico de 15 km de alcance.

2. **La bicicleta casi no va a la periferia, aunque ninguna regla se lo prohíbe. ¿Qué otra columna lo explica? Demuéstrenlo con un número.**
   Lo explica la columna distancia_km. La bicicleta tiene un límite físico de 7 km, y los datos muestran que los viajes a la periferia tienen una distancia mínima de 5.23 km y una media de 16.22 km. Por eso solo 18 de las 2,796 bicicletas van a la periferia (el 0.64%), que son únicamente los pocos viajes que quedaron por debajo de los 7 km.

3. **Comparen los máximos de distancia, peso y volumen de cada medio con la tabla LIMITES. ¿Qué límites se pueden adivinar solo mirando los datos? ¿Cuál no y por qué?**
   Comparando los máximos de los datos con los teóricos:
   - Bicicleta: datos (7.00 km, 7.99 kg, 39.70 L) vs límites (7 km, 8 kg, 40 L).
   - Moto: datos (39.90 km, 24.93 kg, 89.99 L) vs límites (40 km, 25 kg, 90 L).
   - Dron: datos (14.99 km, 2.50 kg, 11.98 L) vs límites (15 km, 2.5 kg, 12 L).
   - Camioneta: datos (59.12 km, 80.00 kg, 400.57 L) vs límites (1000 km, 1000 kg, 3000 L).
     Los límites de bicicleta, moto y dron sí se pueden adivinar con total exactitud porque sus valores máximos en los datos tocan casi al milímetro el límite teórico. El de la camioneta no se puede adivinar porque su límite es muy grande (1000 kg y 1000 km) y los envíos reales de los clientes nunca llegaron a esos extremos (el máximo registrado fue 80 kg y 59 km). Los datos muestran la demanda real de los clientes, no la capacidad máxima del vehículo.

4. **Hay más de cien camionetas para viajes de menos de 2 km. ¿Cuántas tienen una razón clara para ir en camioneta? Para las que no, propongan una explicación.**
   Hay 107 camionetas en viajes de menos de 2 km. De esas, 95 tienen una razón técnica obligatoria (paquetes refrigerados, peso mayor a 25 kg o volumen mayor a 90 L que no caben en moto ni en bici). Las 12 restantes no tienen una restricción técnica directa. La explicación es el ruido humano del dataset (operadores que asignaron camioneta por error o por falta de motos disponibles en ese momento) o por criterios de seguridad, ya que la mitad de esos paquetes eran frágiles o tenían un valor declarado considerable.

### Decisión

**Para pensar: Si les dieran solo el CSV, sin las reglas, ¿podrían reconstruir las reglas del negocio a partir de los datos? ¿Cuáles sí y cuáles no? ¿Qué riesgo hay en dejar que un modelo «descubra» las reglas en lugar de escribirlas a mano?**

Se podrían reconstruir con facilidad las reglas que coinciden con los techos observados de la bicicleta, la moto y el dron (peso, volumen y distancia), además de las prohibiciones evidentes como que el dron no va al centro ni vuela con lluvia. Sin embargo, no se podrían reconstruir los límites máximos reales de la camioneta, porque los clientes no suelen enviar paquetes de una tonelada.
El riesgo principal de dejar que el modelo descubra las reglas por su cuenta es que aprendería tanto los patrones correctos como los errores humanos y el ruido (como las 12 camionetas asignadas a paquetes chicos innecesariamente). Además, ante situaciones críticas de seguridad o legales (como no volar drones con lluvia o de noche), un modelo probabilístico podría equivocarse si se presentan condiciones atípicas, mientras que una regla escrita en código garantiza el cumplimiento estricto al 100%.

## Actividad 2

### Predicciones

1. **¿Cuántos drones crees que salen a las 3:00 y por qué?**
   0 drones, porque ninguna regla ni operación de la empresa permite volar drones en la madrugada por falta de visibilidad y seguridad.
2. **¿Qué porcentaje de los envíos crees que sale de noche (antes de las 6 o desde las 21) y por qué?**
   Menos del 5%, porque casi todos los comercios, oficinas y entregas operan en horario de día.

### Comprobación

1. **¿En qué horas no hay ni un solo dron? ¿Coincide exactamente con la regla?**
   No hay drones en las horas 0, 1, 2, 3, 4, 5, 21, 22 y 23. Coincide exactamente con la regla del negocio, la cual prohíbe el vuelo de drones de noche y solo permite su operación diurna desde las 6:00 hasta las 20:00 (en la hora 20 todavía hubo 35 drones y a las 21 ya hubo 0).

2. **¿Cuántos envíos de noche hay, comparados con los de día? ¿Qué consecuencia tiene eso para lo que el modelo puede aprender sobre la noche?**
   Hay 1,053 envíos de noche (10.53%) frente a 8,947 envíos de día (89.47%). La consecuencia es que el modelo tiene muy pocos ejemplos nocturnos para aprender (casi el 90% de los datos son de día). Al ser una minoría, el árbol le da poca importancia a la hora y tiende a fijarse más en el peso o la distancia, provocando que a veces recomiende drones en la madrugada si el paquete es ligero.

3. **Entre las 20:00 y las 21:00 las bicicletas casi desaparecen y las motos aumentan. ¿Qué lo explica?**
   A las 20:00 hay 115 bicicletas y 160 motos, pero a las 21:00 las bicicletas caen a 20 y las motos suben a 240. Esto se explica por la seguridad del repartidor y el fin de turno de ciclistas: de noche el reparto en bicicleta se restringe por falta de iluminación y peligro vial, por lo que todos esos paquetes pequeños que eran para bicicleta se transfieren a las motos.

4. **Un árbol solo pregunta «¿la hora es menor o igual que X?». ¿Por qué le cuesta representar «de noche»? ¿Cuántas preguntas necesitaría como mínimo?**
   Le cuesta porque la noche no es un rango continuo en números, sino que está partida en dos extremos: las primeras horas del día (0 a 5) y las últimas horas (21 a 23), teniendo al día en medio (6 a 20). Un árbol necesita como mínimo 2 preguntas para aislar la noche: una para separar la madrugada (hora <= 5) y otra para separar la noche tardía (hora <= 20). Esto desperdicia profundidad del árbol dividiendo ramas que deberían significar lo mismo.

### Decisión

**Para pensar: Sin mirar los ejercicios de arriba, diseñen una columna nueva que le facilite al árbol entender la noche. Expliquen cómo la calcularían a partir de las columnas que ya existen y cómo comprobarían, con un número, que de verdad ayudó.**

Diseñaría una columna binaria llamada es_noche. Se calcularía con una condición lógica sobre hora_salida: valdría 1 si hora_salida < 6 o si hora_salida >= 21, y 0 para el resto del día. Con esto el árbol solo necesitaría hacer una sola pregunta directa (es_noche == 1) en lugar de gastar dos divisiones numéricas.
Para comprobar con un número que ayudó, evaluaría el conjunto de prueba nocturno y contaría cuántas veces el modelo recomienda dron de noche. Si el modelo original mandaba, por ejemplo, 15 drones de noche y con la nueva columna baja a 0 sugerencias imposibles, tendríamos la prueba numérica de que la columna resolvió el problema.

## Actividad 3

### Predicciones

1. **¿Qué confusión crees que será la más frecuente y por qué?**
   Entre moto y bicicleta, porque ambos son vehículos ligeros que compiten en paquetes chicos y distancias cortas, por lo que la frontera entre ellos es muy delgada.
2. **¿El modelo confundirá alguna vez una bicicleta con una camioneta y por qué?**
   No o prácticamente nunca, porque son los dos extremos en peso, volumen y capacidad, así que el árbol los puede separar con mucha facilidad.
3. **¿Qué pasaría con el análisis si se usara otro random_state?**
   Cambiarían los paquetes específicos que quedan en el conjunto de prueba, por lo que el número exacto de errores podría variar un poco, pero las tendencias generales y porcentajes deberían ser casi iguales.

### Comprobación

1. **¿Cuántos errores hay y cuáles son las tres confusiones más frecuentes? ¿Son entre medios parecidos o muy distintos? ¿Qué les dice eso?**
   Hubo 158 errores de 2,000 envíos en la prueba (una exactitud del 92.10%). Las tres confusiones más frecuentes fueron:
   - Real moto y predicho bicicleta: 46 veces.
   - Real camioneta y predicho moto: 32 veces.
   - Real moto y predicho dron: 29 veces.
     Son confusiones entre medios muy parecidos y adyacentes en capacidad. Casi no hay confusiones entre extremos (por ejemplo, bicicleta con camioneta no ocurrió en ninguna dirección directa). Esto dice que el modelo tiene muy clara la escala general de los vehículos y que sus fallas ocurren únicamente en las fronteras delgadas de decisión.

2. **Revisen los envíos que eran moto y el modelo mandó a dron. ¿Cuántos son de noche? ¿Cuáles corregirían las reglas del negocio y cuáles no? ¿Qué tienen en común los que no?**
   Hubo 29 casos de moto a dron. De esos, 26 fueron de noche (horas < 6 o >= 21).
   Las reglas del negocio corrigen de forma automática esos 26 casos descartando el dron por ser horario nocturno prohibido. Los 3 casos restantes ocurrieron de día y sí eran posibles físicamente para el dron, pero el operador prefirió moto en el dataset por preferencia subjetiva o ruido humano.

3. **Revisen los que eran moto y el modelo mandó a bicicleta. ¿Están cerca del límite de 7 km? Si no es la distancia, busquen qué los distingue.**
   En los 46 errores de moto a bicicleta, todos los viajes tuvieron distancias entre 1.35 km y 6.89 km (media de 4.08 km), todos por debajo del límite estricto de 7 km de la bicicleta. El modelo vio un paquete pequeño y a corta distancia y asumió bicicleta, pero en la realidad se enviaron en moto debido a factores como el tráfico alto, la urgencia de la entrega (prioridad alta) o porque eran horarios cercanos a la noche donde ya no salían ciclistas.

### Decisión

**Para pensar: Si solo pudieran arreglar un tipo de error, ¿cuál elegirían y por qué? ¿Lo arreglarían cambiando el modelo, los datos o las reglas del negocio?**

Elegiría arreglar los errores donde el modelo manda paquetes a dron cuando debían ir en moto o bicicleta, especialmente los de noche. Es el error más peligroso para la empresa porque mandar un dron de noche o bajo condiciones no aptas viola normativas aeronáuticas y arriesga equipo costoso en accidentes.
Lo arreglaría mediante las reglas del negocio en el backend. Las reglas son filtros deterministas que garantizan al 100% que ningún dron despegue de noche o con lluvia, sin depender de la probabilidad del árbol ni requerir reentrenar todo el modelo.

## Actividad 4

### Predicciones

1. **Ordenen las catorce columnas de la más importante a la menos importante para elegir el medio:**
   1. peso_kg
   2. distancia_km
   3. volumen_l
   4. refrigerado
   5. clima
   6. trafico
   7. fragil
   8. hora_salida
   9. prioridad
   10. valor_declarado_mxn
   11. zona_destino
   12. zona_origen
   13. dia_semana
   14. id_envio

2. **¿Cuáles columnas crees que el modelo no usa?**
   Creo que no usa id_envio, dia_semana, zona_origen y zona_destino, porque son datos que no imponen restricciones físicas ni reglas para definir la capacidad de un vehículo.

### Comprobación

1. **¿Cuáles son las cuatro columnas más importantes? ¿Coinciden con las primeras preguntas del árbol? ¿Y con su predicción?**
   Las cuatro características más importantes según feature*importances* son:
   - distancia_km (0.3220 o 32.2%)
   - volumen_l (0.1929 o 19.3%)
   - refrigerado (0.1313 o 13.1%)
   - peso_kg (0.1263 o 12.6%)
     Sí coinciden con las primeras preguntas del árbol de decisión (que divide primero por distancia, si requiere refrigeración o si excede volumen/peso) y coinciden con nuestra predicción inicial donde colocamos estas mismas cuatro variables al inicio por ser las limitaciones físicas principales.

2. **¿Qué columna, al quitarla, baja más la exactitud? ¿Cuáles no la cambian nada?**
   La columna que más tira el rendimiento del modelo es distancia_km: al quitarla, la exactitud se desploma de 92.10% a 79.30%, una caída de 12.80 puntos porcentuales, seguida de clima cae 7.65 puntos.
   Las columnas que no cambian nada la exactitud (0.00 puntos de diferencia) son: zona_destino, valor_declarado_mxn y trafico (e incluso prioridad tiene una diferencia casi nula de -0.05).

3. **La zona de destino tiene importancia cero, pero el dron nunca va al centro. ¿Cómo puede ser que el modelo no use la zona y, aun así, la plataforma nunca mande un dron al centro?**
   Porque la restricción de que el dron no entre al centro no la aprendió el árbol de decisión, sino que está implementada como una regla de negocio estricta en reglas.py. La plataforma filtra y descarta el dron mediante esa regla determinista antes de emitir la recomendación final, por lo que el árbol no necesita gastar divisiones en aprender una prohibición que el backend ya controla al 100%.

### Decisión

**Para pensar: La app le pide a la persona catorce datos. Si el modelo no usa algunos, ¿deberían dejar de pedirlos? ¿Hay razones para pedir un dato que el modelo no usa?**

No se deben dejar de pedir. El modelo de Machine Learning es solo una pequeña parte de toda la aplicación, y los datos no se recolectan únicamente para entrenar el árbol.
Existen razones operativas, legales y de negocio indispensables para pedir datos que el modelo ignora:

1. El valor declarado es necesario para cobrar el seguro del paquete y calcular indemnizaciones si se pierde o daña.
2. Las zonas de origen y destino son indispensables para generar la guía de paquetería, calcular la ruta en el mapa y asignar el repartidor en la sucursal adecuada.
3. La prioridad es requerida para el compromiso de entrega con el cliente y definir los tiempos en el sistema de rastreo.
   Pedir un dato tiene sentido si la empresa o el cliente lo necesitan para operar, no solo si la IA lo usa para clasificar.

## Actividad 5

### Parte A — Pensar antes de tocar los datos

1. **¿Qué exactitud tendría un «modelo» que nunca dice dron y siempre acierta todo lo demás? ¿Y uno que siempre dice moto? ¿Qué les dice eso sobre usar la exactitud para juzgar un dataset desbalanceado? ¿Qué medidas usarían en su lugar?**
   Si nunca dice dron tendría un 90.5% de exactitud, porque los drones solo son el 9.5% de los datos. Si siempre dice moto tendría alrededor de 45.8%, que es la proporción de motos. Esto demuestra que la exactitud engaña en datasets desbalanceados, ya que un modelo inútil que ignore a la minoría puede parecer bueno. En su lugar usaría precision, recall y la matriz de confusión.
2. **¿Por qué hay tan pocos drones? ¿Es un error de los datos o refleja cómo funciona la empresa? ¿Cambia eso la decisión de balancear?**
   Refleja cómo funciona la empresa en la realidad, porque los drones tienen límites muy estrictos de peso, clima, distancia y horario. Sí influye en la decisión, porque forzar a que haya 50% de drones crearía una realidad ficticia que no existe en la operación real.
3. **Si deciden balancear, ¿se balancea antes o después de separar los datos de entrenamiento y de prueba? ¿Se balancean también los datos de prueba?**
   Se debe balancear después de separar y únicamente en el conjunto de entrenamiento. Los datos de prueba jamás se deben balancear, porque deben conservar la distribución real del negocio para evaluar cómo funcionará el modelo en el mundo real.

### Parte B — Probar estrategias (Comprobación)

**Tabla comparativa de estrategias:**
| Estrategia | Envíos entreno | Exactitud | Precision dron | Recall dron | Veces predice dron | Sugerencias imposibles |
|---|---|---|---|---|---|---|
| Sin balancear | 8000 | 92.1% | 0.839 | 0.905 | 205 | 31 |
| Ponderar clases (class_weight) | 8000 | 90.2% | 0.766 | 1.000 | 248 | 35 |
| Repetir drones (Oversampling) | 9242 | 92.5% | 0.956 | 0.905 | 180 | 18 |
| Reducir mayoritarias (Undersampling) | 5132 | 88.9% | 0.753 | 0.932 | 235 | 58 |
| Trampa (Repetir antes de separar) | 12000 | 93.8% | 0.955 | 0.993 | 1238 | 16 |

_(Nota: en el conjunto de prueba hay 190 drones reales)._

1. **Explicación del experimento con trampa a propósito (balancear antes de separar):**
   Al duplicar drones antes de hacer train_test_split, los números se disparan falsamente a 93.8% de exactitud y 0.993 de recall. La mejora es completamente artificial debido a una fuga de datos (data leakage): filas idénticas quedaron tanto en entrenamiento como en prueba, por lo que el modelo simplemente memorizó esos paquetes en lugar de aprender a generalizar. Además, el conjunto de prueba se contaminó artificialmente y por eso predice dron 1,238 veces en lugar de las ~200 normales.

### Parte C — Interpretar

1. **¿Qué pasó con el recall del dron y qué pasó con su precision? ¿Por qué una sube cuando la otra baja?**
   Con estrategias como class_weight o undersampling el recall sube (hasta 1.000 y 0.932), pero la precision baja cae a 0.766 y 0.753. Esto sucede por el intercambio natural entre ambas métricas: al forzar al modelo a no perderse ningún dron subir recall, el modelo se vuelve más atrevido y predice dron con mayor frecuencia, pasa de 205 a 248 veces, cometiendo más falsos positivos y castigando la precision.

2. **¿Alguna estrategia dejó al modelo con muchos menos datos de entrenamiento? ¿Qué se pierde con eso?**
   El undersampling redujo los datos de entrenamiento de 8,000 a solo 5,132 envíos, se tiraron casi 3,000 ejemplos a la basura. Con eso se pierde información valiosa sobre las demás clases, lo que provocó que la exactitud general cayera a 88.9% y las sugerencias imposibles se dispararan a 58.

3. **Si dos estrategias dieron números parecidos para el dron, ¿por qué son en el fondo la misma idea?**
   Ponderar con class_weight y hacer oversampling son matemáticamente la misma idea: ambas aumentan la penalización por fallar en la clase minoritaria. Darle el triple de peso numérico a un dron en la función de costo tiene el mismo efecto que clonar tres veces la fila de ese dron en los datos.

4. **¿El motivo «confianza 84%» sigue significando lo mismo después de balancear?**
   No, ya no significa lo mismo. La confianza que da el árbol en sus hojas refleja la proporción de ejemplos que vio al entrenar. Si inflamos artificialmente la cantidad de drones en el entrenamiento, el árbol asignará porcentajes de certeza mucho más altos de lo que realmente corresponden a la probabilidad real del negocio.

### Parte D — Decidir

**Para pensar: ¿Deben usar el modelo balanceado en la plataforma? Recomendación y justificación.**

Recomiendo no usar un balanceo agresivo y quedarse con el modelo sin balancear.
Las razones son:

1. Para la empresa es mucho más grave mandar un dron cuando no convenía (falso positivo, baja precision) porque pone en riesgo el equipo y puede violar leyes, mientras que no usar el dron cuando sí convenía solo significa que el paquete se enviará en moto de manera segura.
2. El modelo sin balancear ya tiene un recall bastante alto, 0.905, detecta más del 90% de los drones y mantiene una buena precisión sin saturar el sistema con sugerencias riesgosas.
3. Si la empresa llegara a duplicar su flotilla de drones en el futuro, no se necesitaría alterar los datos del pasado con trucos estadísticos, sino recopilar los nuevos envíos reales con esa mayor disponibilidad y reentrenar con la nueva realidad operativa.
