           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
             EXAMEN — MICROSERVICIOS, GATEWAY Y EL MONOLITO
                                CON API
              Tópicos Selectos de Tecnologías Web y Móvil

                            Eduardo Alcaraz
           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

David Maldonado Barajas

Indicaciones
════════════

Este examen _no_ se aprueba de memoria. Casi todas las preguntas
tienen una respuesta que «suena bien» y está mal, o dos opciones
defendibles donde se califica el argumento.

Reglas:

• Expliquen el _porqué_. Una conclusión sin razonamiento vale la mitad
(o menos).
• Cuando digan «depende», digan _de qué_.
• No hace falta código que compile; sí hace falta que el diseño cierre
(quién llama a quién, qué pasa si algo falla, qué ve el cliente).
• Pueden dibujar. Un dibujo contradictorio con el texto resta.

Puntaje: _100 puntos_ (10 × 10).

1 — La frase del compañero (10 puntos)
══════════════════════════════════════

En el pizarrón quedó:

        La API separa clientes del servidor; los microservicios
        separan servidores entre sí.

Un compañero dice: «Entonces, si mi monolito Django expone una API y
además lo meto en Docker, ya cumplí las dos mitades de la frase.»

a) Desarmen su argumento. ¿Qué parte de la frase cree cumplir con la
API? ¿Qué parte cree cumplir con Docker? ¿En qué se equivoca en cada
una?

_En este caso la API solo separa el frontend del backend, pero no divide al servidor por dentro, todas las partes siguen acopladas en el mismo codigo y memoria. Con docker esta mal por que solo sirve como herramienta de empaquetado, no lo esta haciendo un microservicio._

b) Den un contraejemplo mínimo: mismo código Django, _con_ API y _con_
Docker, que _sigamos_ pudiendo llamar monolito. ¿Qué tendría que
añadir (o partir) para que deje de serlo?

c) ¿La frase del pizarrón habla de _tecnologías_ (Docker, REST) o de
_límites de proceso / despliegue_? Defiendan su lectura con lo que
vieron en clase.

_De limites de proceso / despliegue, ya que los microservicios para que si algo falle solo sea una parte y no afecte al resto de la aplicación._

2 — Tres rutas, una trampa (10 puntos)
══════════════════════════════════════

El equipo muestra este `urls.py' de un solo proyecto Django:

┌────
│ path("usuarios/", ...),
│ path("pedidos/", ...),
│ path("recomendar/", ...),
└────

y este `docker-compose.yml':

┌────
│ services:
│ api:
│ build: .
│ ports: ["8000:8000"]
│ deploy:
│ replicas: 3
└────

Afirman: «Tres rutas + tres réplicas = microservicios con alta
disponibilidad.»

a) Separen las dos ideas que mezclaron (rutas vs réplicas). ¿Qué
problema resuelve cada una y cuál _no_ resuelve?

_Las rutas sirven para el cliente, pero no separa los procesos que estan en el codigo. Minetras que las replicas ayudan al balanceo de la carga._

b) Si una de las tres réplicas se cae a mitad de un `POST /pedidos',
¿el sistema dejó de ser monolito? ¿Por qué sí o por qué no?

_Sigue siendo un monolito, ya que si una replica muere otra de las 2 lo remplaza, pero si el fallo es por un error de logico es muy probable que las otras replicas tambien fallen._

c) Rediseñen _solo con palabras_ el `compose' para que sí ilustre
microservicios (nombres de servicios y responsabilidades; no hace
falta YAML perfecto). ¿Cuántas _imágenes distintas_ mínimo y por qué
esa cantidad?

3 — El gateway que «hace de más» (10 puntos)
════════════════════════════════════════════

Les proponen este diseño «para no complicar»:

        Un solo contenedor nginx+Python que: valida el JWT, elige
        el medio con el `.joblib', guarda el pedido en SQLite,
        manda el correo y devuelve el HTML.

Lo llaman «API Gateway».

a) ¿Es un gateway? Si no, ¿qué es? Usen la analogía del recepcionista
(o otra) y digan qué oficios mezclaron.

_No es un gateway, es un monolito. En este caso gateway seria como un recepcionista del edificio que revisa tu identificacion, en este caso el JWT y luego te dice a donde ir. En el diseño que hicieron, el recepcionista revisa la identificacion, lo analiza con el modelo ML, le cobra, es decir guarda el pedido en SQLite, escrive una carta y se despide. Aqui se mezclo tanto el enrutamiento, la logica de negocio en la infraestructura._

b) Mencionen _tres_ consecuencias malas de ese diseño cuando el modelo
pesado se reentrena cada semana y el correo empieza a fallar.

_Si se reentrena el modelo de .joblib cada semana, se tiene que reiniciar el contenedor, y deja a los clientes sin poder valida JWT o enviar correos durante el reinicio._

_Si el servidor de correos falla y la peticion queda colgada, se agotan los workers del contenedor, deja tirada la validacion de usuarios y el m otodr del ML._

_Si se necesita mas CPU para procesar el modelo de ML, se va a tener que clonar todo el contendor, desperdiciando memoria que no se necestiaba escalar._

c) Partan ese contenedor en piezas. Para cada pieza digan: ¿queda en
el borde (gateway) o detrás? No inventen diez servicios: el mínimo que
separe borde, logística e (si hace falta) aviso.

_Las partes pueden ser:_

_Gateway: Nginx/API Gateway para validar el JWT y la ruta._

_Servicio de pedidos: Python/SQLite para guardar el pedito_

_Servicio de ML: Carga el .joblub y devuelve el medio_

_Servicio de notificaciones: Manda el correo_

4 — `localhost', la trampa favorita (10 puntos)
═══════════════════════════════════════════════

Pedidos corre en un contenedor. Recomendar en otro, misma Compose.
Alguien «arregla» la conexión así:

┌────
│ RECOMENDAR_URL=http://127.0.0.1:8002
└────

En su laptop, _sin_ Docker, ese `curl' a `127.0.0.1:8002' sí
funcionaba.

a) Expliquen por qué en Compose ese arreglo suele fallar _aunque_
Recomendar esté sano. ¿A qué proceso apunta `127.0.0.1' desde dentro
de Pedidos?

b) ¿Por qué `http://recomendar:8002' sí tiene chance de funcionar?
  ¿Quién «inventa» el nombre `recomendar'?

c) Ahora Recomendar se muda a la laptop de otro alumno
(`192.168.0.57'). Escriban la URL que pondrían _y_ dos cosas que
tienen que ser verdad en la WiFi para que no sea teatro (puertos,
firewall, etc.). Si solo cambian la URL y nada más, ¿qué puede seguir
fallando?

5 — Fallo parcial con números (10 puntos)
═════════════════════════════════════════

Escenario medido en laboratorio (inventado pero coherente):

• 1000 `POST /pedidos' por hora en promedio.
• Recomendar tarda 200 ms cuando está bien.
• El 5 % del tiempo Recomendar no responde (timeout 3 s).
• Pedidos, si hay timeout, usa plan B (moto) y responde 200 en 50 ms.
• El gateway añade 5 ms.

a) En la hora «normal» (Recomendar bien), ¿el cliente espera ~200 ms o
~3 s? ¿Quién pone el tiempo dominante?

b) En el 5 % malo, con plan B: ¿el cliente ve error o pedido creado?
¿Qué «mentira útil» están aceptando (medio quizá no óptimo)?

c) Un compañero dice: «Mejor que Pedidos _reintente_ 10 veces hasta
que Recomendar vuelva; así nunca usamos plan B.» ¿Qué le pasa a la
cola de peticiones y al gateway si Recomendar está caído 10 minutos?
¿Plan B siempre es peor que reintentar? Argumenten.

6 — Apagan el «edificio equivocado» (10 puntos)
═══════════════════════════════════════════════

Tres contenedores: gateway, pedidos, recomendar. Hacen tres
experimentos _por separado_:

1. `docker compose stop gateway'
2. `docker compose stop pedidos'
3. `docker compose stop recomendar'

Para _cada_ experimento digan qué ve el navegador en `http://IP:8080/'
(página / crear pedido) y qué sigue vivo por dentro. No basta «no
jala»: digan _qué_ no jala y qué sí podría seguir respondiendo si
alguien hablara por dentro de la red.

Luego: ¿en cuál de los tres el sistema «parece» más muerto hacia
afuera aunque más piezas sigan arriba? ¿Qué les enseña eso del borde?

7 — WiFi del salón, conflicto de roles (10 puntos)
══════════════════════════════════════════════════

Cuatro alumnos:

• Ana: gateway + HTML
• Beto: pedidos
• Carla: recomendar
• Diana: «yo también levanté un gateway en mi laptop por si Ana falla»

Todos en la misma WiFi. El cliente (otro equipo) configura a veces la
IP de Ana y a veces la de Diana.

a) ¿Qué problema de _diseño_ introdujo Diana aunque «todo responda
200»? (Piensen en una sola puerta vs dos puertas.)

b) Beto configuró `RECOMENDAR*URL=http://localhost:8002' porque en su
máquina desarrolló Pedidos y Recomendar juntos. En el salón Recomendar
está en la laptop de Carla. ¿Qué falla y cómo lo corrigen \_sin* juntar
otra vez los dos servicios en la laptop de Beto?

c) La WiFi del campus aísla clientes («AP isolation»). `ping' entre
alumnos falla. ¿Pueden hacer la práctica tal cual? Si no, propongan
_un_ plan B de laboratorio que preserve la lección «procesos
separados» (aunque no sea WiFi del salón).

8 — El front que conoce demasiado (10 puntos)
═════════════════════════════════════════════

El HTML hace esto al enviar el formulario:

┌────
│ await fetch("http://192.168.1.20:8002/sugerir", { ... }); // Recomendar
│ await fetch("http://192.168.1.30:8001/pedidos", { ... }); // Pedidos
└────

El autor dice: «Más rápido: me salto el gateway.»

a) Listen _tres_ problemas (seguridad, cambio de IP, orden de
llamadas, consistencia del folio, CORS, etc.).

b) Rediseñen la secuencia correcta con gateway: _una_ llamada desde el
navegador. ¿Quién habla con Recomendar y por qué no el navegador?

c) El selector de modelo (`arbol=|=bosque=|=red') va en el JSON. Si el
front llama directo a Recomendar _y_ a Pedidos, ¿quién debería crear
el folio para no duplicar lógica? ¿Qué invariante rompen si los dos
«crean» algo?

9 — El LLM vendedor (10 puntos)
═══════════════════════════════

Producto: tienda + envíos.

• Modelo `.joblib': medio de transporte.
• LLM: texto para convencer al cliente en la ficha del producto.

Un arquitecto propone _un solo_ microservicio `cerebro' que: recibe el
  carrito, elige el medio con el árbol *y* genera el pitch de ventas con
  el LLM, todo en la misma petición `/inteligente'.

a) Critiquen el nombre y el corte. ¿Qué dos oficios distintos
mezclaron? ¿Qué falla cuando el LLM tarda 8 s y el despacho necesita
responder en < 500 ms?

b) Propongan dos endpoints (o dos servicios) y digan cuál usa el
_front de tienda_ y cuál el _flujo de pedido/envío_.

c) El LLM vive en un server con GPU en otra red. El front de tienda
¿apunta a la GPU o al gateway? Si mañana cambian de proveedor LLM
(otro host), ¿qué archivo/config quieren tocar _una sola vez_?

10 — El inversionista y la semana imposible (10 puntos)
═══════════════════════════════════════════════════════

Hoy:

• Panel interno: monolito Django (funciona, poco tráfico).
• App clientes: gateway + pedidos + recomendar.
• Idea: LLM de ventas (aún no).
• Equipo: 5 personas.
• Inversionista: «Todo a microservicios en 7 días, incluido el panel,
o no hay dinero.»

a) Escriban la respuesta al inversionista (máx. 8 líneas) con postura
_y_ riesgo concreto si obedecen a ciegas.

b) Ordenen _estas cuatro_ iniciativas de más a menos urgente para
_esta_ semana y justifiquen el orden (no el catálogo soñado):

1. Partir el panel Django en 6 microservicios.
2. Sacar el reentrenamiento del `.joblib' a un pipeline que no tumbe
   Pedidos.
3. Meter auth + rate limit en el gateway público.
4. Subir el LLM de ventas a producción sin timeouts ni plan B.

c) Inventen _una_ métrica que les diga «ya toca partir X del monolito»
(no «porque está de moda»). Tiene que ser observable (tiempo, errores,
despliegues, equipo…).

d) Cierren con una frase propia (no copien el apunte) que capture:
¿microservicios son el objetivo o la herramienta?
