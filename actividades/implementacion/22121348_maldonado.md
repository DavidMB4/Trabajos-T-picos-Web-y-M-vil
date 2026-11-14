# Actividad individual — Lo que hay detrás de la implementación

Nombre: David Maldonado Barajas
Matrícula: 22121348
Equipo:

## A1

El entorno virtual nos sirve para aislar las versiones de nuestras librerias de Python y que choquen con las versiones de otro proyecto, mientras que docker nos sirve para aislar el sistema operativo para que pueda desplegarse en otro entorno, por lo que las 2 opiniones estan mal ya que ningungo hace inecesario al otro.

## A2

a) No perdio el codigo, por que el codigo no esta en .venv, ahi solo estan los ejecutables de python y librerias.
b) Solo necestia volver a crear el entorno virtual, puede usar el comando `python -m venv .venv` activarlo y luego instalar las dependencias que estan en el archivo `requiriments.txt` con el comando `pip install -r requirements.txt` ya que esta es la lista de las dependencias que se usan.
c) Activar el entorno no hace ninguna instalacion, solo le indica a la computadora donde esta la ruta que debe de usar para los ejecutables de Python, pero solo esta activa durante la ventana de sesion de la terminal, por eso en una nueva terminal se require volver a activar.

## A3

a) La carpeta app solo exite dentro del contenedor de Docker, y el comando COPY . . solo copia todo el contenido de la carpeta actual del alumno (con el primer punto) hacia la carpeta de trabajo del contenedor (el segundo punto que es /app).

b) Ignorar .venv/ evita copiar gigabytes de librerías inútiles e incompatibles al contenedor. Mientras que ignorar db.sqlite3 evita sobreescribir la base de datos de producción con datos de prueba o basura locales.

## B1

a) Que como se ejecuta solo en el javascript del navegador, la aplicacion no lo podria leer. Se tendria duplicacion de codigo, si se modifica se tendria que modificar en los 2 lados, en la del navvegador y en la de movil.

b) Por que el backend es el que aplcia las reglas de negocio y entregas los datos estructurados, mientras que el forntend es el que muestra y presenta estos datos, por lo tanto se puede consumir el backend desde diferentes formas de aplicar el frontend sin cambiar la logica en backend.

## B2

La aplicacion movil va a fallar por que esta programada para buscar ese nomnbre en especifico y va a recibir un valor nulo. El contrato es la forma en que se van a comunicar, lleva el qué URLs existen, qué parámetros se envían y exactamente qué nombres de campos y tipos de datos responde el backend. El version sirve para la compatibilidad entre las versiones del backend, de esta forma el backend puede soportar una version vieja que tiene como nombre "medios_disponibles" y una version nueva que tiene "medios".

## B3

No debe quitarse, por que no se puede confiar en que lo manden los usuarios este bien. La valdiacion en frontend sirve para que el usuario pueda saber que esta llenando los datos de forma correcta o que le faltó alguno, pero es facil de burlar. Mientras que la de backend es la que garantiza que se guarden los datos que de verdad sirven, para evtiar datos o corruptos o valores peligrosos sin importar de donde vengan.

## C1

La escala vertical hace tu servidor más potente, esto es por meterle más memoria RAM, mejor procesador o más disco a la misma máquina. Mientras que la horizontal es poner más máquinas o contenedores idénticos al del servidor a trabajar en paralelo.

## C2

No la encuentra porque cada copia de Django corre en su propio contenedor con su propia memoria RAM aislada. Por ejemplo, si la copia 1 guardó el pedido en su memoria, la copia 2 y la copia 3 no tienen forma de leer la memoria RAM de la copia 1.

No la encuentra la copia que lo escribio por que tiene 2 procesos worker, y cuando vuelve a caer la copia no lo encuentra por que el segundo worker tiene la memoria vacia.

No tiene razon en deci rque docker rompio el codigo ya que asumio qu ela memoria del servidor es persistente y compartida, ya que no cumple con stateless.

## C3

Falla con varias copias, por lo mismo de que con un worker lo envia y con otro worker distinto lo confirma, y ese otro worker esta vacio.

En equest.sesion funciona porque Django no guarda los datos de la sesión en la memoria RAM del proceso, si no que le da una cookie de sesión al usuario con un ID y guarda la información en un almacén centralizado compartido. Django guarda las sesiones en la base de datos, y como todas las copias consultan la misma base de datos, cualquiera puede leer la sesión

## C4

a) Se enviarán 5 avisos repetidos a cada cliente, uno por cada copia que tenga el reloj activado. Deberia vivir en un servicio o contenedor independiente dedicado a tareas programadas.

b) Porque aplicar migraciones altera las tablas de la base de datos. Si las 5 copias intentan correr migrate al mismo tiempo al arrancar, pueden provocar bloqueos, errores de concurrencia o tablas corruptas. Debe correr una sola vez en secuencia antes de que las copias inicien.

c) Son 80 conexiones mínimas abiertas. No se puede escalar horizontalmente al infinito solo agregando copias de Django, porque se agotan las conexiones disponibles en PostgreSQL por ejemplo. SQLite es un archivo local en disco que se bloquea por completo cada vez que alguien escribe en él, si hay múltiples copias queriendo escribir al mismo tiempo, el sistema colapsa por bloqueos y errores como "database is locked".

## D1

a) Por que no aprendio los patrones, solo memorizó los datos.

b) Para hacerlo como seria en realidad, por ejemplo se usa el 80% de los datos para entrenar y el 20% para probar.

c) Que tengan la misma propocrcion de envios.

## D2

**¿Qué idea falsa le estaría dando al árbol?**
Que un clima vale mas que otro

**¿Cómo lo evita el one-hot encoding**
Crea una columanda binaria con los climas para que esten en igualdad de condicion.

**¿Por qué se guardan la preparación y el árbol juntos en un Pipeline?**
Evita que haya inconsistencias cuando hay datos nuevos.

## D3

a) Se llama sobreajuste (overfitting), El árbol sin límite creó tantas ramas (346 hojas) que memorizó el "ruido" y dejó de entender datos nuevos.

b) Por que duplica las hojas y 8 termina siendo mas rapido y consume menos memoria.

## D4

a) En cuanto a la precision, significa que de todos los paquetes que el modelo dijo que debían ir en dron, el 83.9% si eran para dron, mientras que el otro 16.1% fue un error de asignación. y el recall significa que de todos los paquetes reales que podían viajar en dron, aqui el modelo fue capaz de detectar y mandar en dron al 90.5%, pero se le escapó el 9.5%.

b) Es mucho más grave mandar en dron un paquete que no debía ir en dron, porque podría ser un paquete muy pesado que tire el dron y cause un accidente o rompa equipo costoso. El mandar en dron algo que no debía lo mide la Precision. Y no reconocer un paquete apto lo mide el Recall.

c) Por que siempre hay factores imprevistos o incertidumbre. Si dice 100% muy probablemente hay un sobre ajuste, mientras que con un 92% es que las reglas de seguridad de negocio actuan bien.

## D5

a) Por la transparencia, ya que si una pquete falla se puede saber el por que se tomo una decision. Por el tamaño, ya que solo pesa 14kb y el bosque 50mb

b) No cambia nada porque ambos modelos siguen la misma interfaz, que es el metodo .predict()

## E1

a) Porque en los datos históricos casi no había envíos a las 3:00 AM por que la paqueteria opera de dia. Como el modelo no vio suficientes ejemplos nocturnos, solo se fijó en que el paquete era ligero y a corta distancia.

b) Porque el Machine Learning es probabilístico, y siempre existe un margen de error. Las reglas del negocio como "prohibido volar de noche por ley" son mandatorias y críticas. No se puede arriesgar una multa legal o un choque confiando en la probabilidad de una IA.

c) Por el Principio de responsabilidad unica, ya que el recomendador solo se encarga de dar la sugerencia estadística de la IA. reglas.py se encarga de la política operativa y de seguridad de la empresa. Si cambia el modelo de IA por una red neuronal o una API externa, las reglas de la empresa siguen intactas y funcionando.

## E2

a) **¿Es una contradicción mantener el modelo en memoria con @lru_cache?**
No es contradicción ya que unn pedido es estado dinámico y el modelo es recurso de solo lectura.

b) **Qué pasaría si cada petición cargara el archivo .joblib desde el disco?**
El sistema sería muy lento, porque al leer un archivo de disco y deserializarlo en cada clic consume CPU y disco innecesariamente, tirando el rendimiento del servidor con unas cuantas peticiones simultáneas.

## E3

**¿Por qué pasa esto (no carga el modelo)?**
Porque los archivos .joblib o pickle serializan la estructura binaria exacta de las clases de Python. Si la laptop usaba scikit-learn 1.9.0 y Docker instaló la versión más reciente, la estructura interna de las clases cambia y son incompatibles.

**¿Cómo se evita?**
Congelando las versiones exactas en requirements.txt usando scikit-learn==1.9.0.

**Relación con el entorno virtual y contenedor**
Ambos buscan la reproducibilidad, porque de nada sirve tener un contenedor si se dejan las versiones abiertas para que descargue cualquier cosa nueva que rompa el sistema.

## F1

a) Para conectar el servicio externo necesitamos crear una nueva clase, por ejemplo ServicioExternoIA.py, que use la librería requests para mandar el paquete al servidor de la empresa externa. El patrón que se está usando aquí es el patrón Singleton, porque solo tenemos un único servicio contratado en la nube y no debemos crear múltiples instancias de la conexión para no gastar memoria.
Lo que no cambia en la plataforma es la vista de Django (views.py), pero sí tendríamos que modificar reglas.py para que ahora entienda las palabras en mayúsculas e inglés como "DRONE" y "alta".

b) Cuando el paquete llega a /entregas/recomendar/:

1. Primero, la vista de Django valida que los campos como el peso y la distancia existan (esto necesita diseño de software).

2. Luego, esos datos se mandan al servicio externo. La IA se encarga de todo el proceso inteligente: analiza el paquete, decide que debe ser un dron, calcula la ruta óptima, el consumo de batería y genera el plan de entrega final con el costo.
3. Por ultimo la plataforma solo toma ese plan que entregó la IA y se lo manda al usuario en formato JSON. Como la IA ya resolvió el plan completo, el diseño de software solo se necesita para recibir la petición HTTP inicial.

c) El compañero no tiene razón por 2 cosas:

- Si el servicio se cae: Si la API externa deja de responder o no tiene saldo, toda la página va a marcar error 500. Para solucionar esto no necesitamos patrones, simplemente en la vista ponemos un try/except y un bloque de if/else rápido para que asigne una moto por defecto si la API falla.

- Si cambiamos de proveedor: Cada empresa de inteligencia artificial tiene modelos distintos y más modernos. Si cambiamos a un proveedor mejor, borrar el código viejo nos obligaría a reinstalar todo Django desde cero en Docker para actualizar las librerías de conexión.
