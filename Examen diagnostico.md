# Examen diagnostico 2

## David Maldonado Barajas

### 27/08/2026

1. **Metodologías: ¿Cuál es la diferencia principal entre una metodología de desarrollo tradicional (como Cascada) y una metodología ágil (como Scrum) frente a los cambios en los requisitos?**

   R= _Una metodologia como cascada funciona de forma mas lineal, mientras que una metodologia agil como scrum funciona com ciclos o iteraciones. En una metologia como cascada los cambios en los requisitos alteran las fases, ya que no se puede regresar atras facilmente, mientras que en una metologia como scrum integra los cambios en los mismos ciclos haciendo mas facil trabajar estos cambios._

2. **Metodologías: ¿Cuál es la diferencia principal entre una metodología de desarrollo tradicional (como Cascada) y una metodología ágil (como Scrum) frente a los cambios en los requisitos?**

   R= _Los requirimentos funcionales son las acciones que debe hacer el sistema, en este caso el CRUD para la informacion. Mientras que en los no funcionales, se maneja el rendmiento o la seguridad que tendran estas acciones, como que la pagina cargue en poco tiempo o el cifrado que usara en las peticiones HTTPS._

3. **Arquitectura: Describe el modelo Cliente-Servidor y explica brevemente cómo se comunican el frontend y el backend en una aplicación web moderna**

   R= _Se comunican mediante una API, la API funciona como el intermediario, el cliente envia una peticion, la API la lleva al servidor, el servidor la recibo, reune la informacion y la devuelve en una respuesta a la API en formato JSON, la cual devuelve y el frontend puede usar para devolversela al cliente._

4. **Bases de Datos: ¿En qué escenarios recomendarías utilizar una base de datos relacional (SQL) frente a una no relacional (NoSQL) para el almacenamiento de datos en una aplicación?**

   R= _La base de datos relacional cuando la forma de guardar la informacion tenga orden estricto, mientras que la no relacioinal cuando la informacion que se guarde sea mas libre._

5. **APIs: ¿Qué es una API REST y qué papel fundamental juega en la integración entre una aplicación móvil y los servidores (backend)?**

   R= _Una api rest sirve para que dos aplicaciones puedan comunicarse entre si, en este caso la aplicacion movil manda una peticion, la cual el servidor pueden responder con un formato como JSON. Se utilizan metodos como PUT, POST, DELETE, GET. La API funcinoa como un intermetidiario entre los 2 para que se puedan entender._

6. **Control de Versiones: Explica la importancia de utilizar Git en un equipo de desarrollo de software y describe brevemente qué es un "merge conflict" (conflicto de fusión).**

   R= _Git funciona como un control de versiones, de esta forma cada desarrollador puede trabajar en su rama los modulos sin afectar a ¿los demas, al manejar versiones pueden revisar o regresar a una anterior si necesitan revisar algo que se cambio o regresar a una posicion mas estables. Merge conflict pasa cuando se intenta llevar lo qu eesta en un a rama a otra pero hay conflictos, como por ejemplo que en un script un desarrollador escribio algo diferente al de la rama otro, en este caso se debe corregir, ya sea dejar una version u otra del script, o juntar los 2 cambios a mano y aceptarlo como la version final del merge._

7. **Pruebas: ¿Qué son las pruebas unitarias (unit testing) y por qué son cruciales para asegurar la calidad del software antes de su paso a producción?**

   R= _Las pruebas unitarias sirven para probar pequeñas funciones o modulos, para qver que funcionen bien por separado. Si pasa la prueba, hace falta despues probarla en conjunto con el resto de modulos que participan. De esta forma logramos identificar errores antes de unirlo con las demas partes del sistema._

8. **POO: Define los conceptos de encapsulamiento y polimorfismo de la Programación Orientada a Objetos, y menciona cómo ayudan a crear un código más mantenible.**

   R= _El polimorfismo es hacer que 2 objetos puedan hacer la misma accion, pero cada una agregando cosas o caracteristicas que solo cada uno de lelos puedan hacer. El encapsulamiento es guardar las variables y atributos, y sus funciones en una clase, para si poder colocar reglas de que como acceder a ellos. Eso sirve como forma de acceder a las funciones o metodos de forma sencilla sin necesidad de ver como funciona internammente o modificar codigo._

9. **Patrones de Diseño: ¿Qué es el patrón de arquitectura Modelo-Vista-Controlador (MVC) y cómo ayuda a organizar el código en el desarrollo de software?**

10. **Seguridad: Explica la diferencia técnica entre "autenticación" y "autorización" en el contexto de seguridad de una aplicación.**

    R= _La autenticacion es el ver que las credenciales del usuario sean correctos y que sea quien dice ser para poder acceder. Sin la autenticacion cualquier persona podria entrar. Mientras que la autorizacion son las acciones que tiene permitidias hacer dentro del sistema, como leer datos, crear informacion, eliminar o modificar informacion. Sin la autorizacion, cualquier usuario que accede podria hacer lo que quisiera en el sistema, lo que puede poner en riesgo informacion sensible._
