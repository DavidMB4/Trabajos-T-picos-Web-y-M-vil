# Análisis de Patrones de Software (Proyecto 1)

David Maldonado Barajas  
Tópicos Selectos de Tecnologías Web y Móvil  
Eduardo Alcaraz

---

## 1. Patrones en el Backend de la API en Django

### Front Controller (Controlador Frontal)

Esta en `config/urls.py` y `rentas/urls.py`. Todas las peticiones HTTP que llegan al servidor pasan primero por un solo archivoo, en este caso es el `config/urls.py`. Si la ruta empieza con `/api/`, este archivo se la pasa a `rentas/urls.py` y de ahí se reparte a la función correcta en `views.py`.

Con esto se evita el tener scripts sueltos por todos lados donde cada archivo tenga que recibir la petición por su cuenta, tambien centraliza la entrada del servidor en un solo punto y hace mas fácil cambiar o agregar nuevas URLs.

---

### Repository (Repositorio de Datos)

Esta en `rentas/models.py` con las clases de `Herramienta` y `Renta`. Aqui en lugar de escribir consultas SQL a mano como `SELECT` o `INSERT`, usamos el propio ORM que ya trae Django como `Herramienta.objects.all()` o `Renta.objects.create(...)` para guardar y consultar los datos en la base de datos de SQLite.

Con esto se evita escribir codigo SQL directo adentro de las vistas lo que ayuda a que no haya inyecciones SQL, tambien si luego se cambia de SQLite a otra base de datos como Postgres o MySQL no se tiene que modificar nada de las vistas por que los modelos se encargan de traducir todo.

---

### Strategy (Estrategia)

Esta en `rentas/reglas.py` y `rentas/recomendador.py`. Aqui la decision de que herramienta recomendar se divide en dos partes, primero el arbol de decision calcula que probabilidad tiene cada opcion segun los datos que puso el usuario, y luego pasa por las reglas del negocio donde se checa si la opcion es segura o si por ejemplo es principiante y necesita equipo de proteccion o si dura mas de 3 dias y conviene darle el kit.

Con esto se evita tener un archivo lleno de un monton de `if` y `else` adentro de las vistas, y tambien evita el sobreajustar el arbol de Machine Learning intentando que se aprenda reglas humanas de seguridad a la fuerza, si alguna regla de la tienda cambia solo se mueve ese archivo y ya no se tiene que volver a entrenar el arbol.

---

## 2. Patrones en el Frontend y Arquitectura General

### MVC (Modelo - Vista - Controlador a groso modo)

Esta repartido entre Flutter y Django. La vista son las pantallas de Flutter como `recomendador_screen.dart` y `catalogo_screen.dart`, el controlador serian las funciones de `views.py` en Django junto con el `api_service.dart`, y el modelo son las tablas de `models.py` en Django y las clases de datos en `lib/models/` de Flutter. La app de Flutter solo manda los datos en JSON y Django procesa la peticion y le regresa la respuesta para que se pinte en pantalla.

Con esto se evita tener un archivo gigante donde este revuelto el diseño de los botones con las llamadas a la base de datos y la logica, asi si se quiere cambiar el diseño o los colores de la app no se tiene que mover nada del backend de Django.

---

### Decisiones de Diseño en el Cliente Flutter

#### A) Composición de UI (Widget Tree modular)

Esta en `screens/recomendador_screen.dart` con las funciones como `_construirFormularioTrabajo` o `_construirTarjetaRecomendacion`. En lugar de poner todo el codigo visual adentro de la funcion `build()` que haria que midiera mas de 500 lineas todas amontonadas, se corto la pantalla en pequeñas funciones privadas para cada seccion.

Con esto se evita que el codigo se vuelva un desastre con demasiadas sangrias y parentesis de Flutter, haciendo que sea mucho mas facil de leer y de entender que hace cada parte de la pantalla.

#### B) Manejo de Estado Reactivo

Esta en las pantallas de Flutter usando `StatefulWidget` con variables como `_cargando`, `_error` o `_recomendacion`. Cada que el usuario pide una recomendacion o confirma la renta se usa `setState()` para actualizar la pantalla mostrando la ruedita de carga, el resultado de la recomendacion o si falto algun dato mostrar el mensaje en rojo.

Con esto se evita que la pantalla se quede congelada sin que el usuario sepa que esta pasando, y tambien evita que le den varios clics al boton por desesperacion mientras se espera la respuesta del servidor.

#### C) Navegación por Pestañas (Tab Navigation)

Esta en `lib/main.dart` con el `DefaultTabController` y el `TabBar`. Aqui se dejo el menu de navegacion arriba fijo con las tres opciones que son el Recomendador, Catalogo y Buscar Folio, para que el usuario pueda cambiar entre una y otra.

Con esto se evita tener que estar cargando paginas nuevas o cambiando de ruta por completo, permitiendo cambiar de pantalla rapido y sin que se borren los datos de lo que ya habias consultado.
