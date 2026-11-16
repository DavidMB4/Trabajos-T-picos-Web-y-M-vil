# asistente y respuestas del bot

import re
import joblib
from pathlib import Path

from .models import Herramienta, Renta

RUTA_MODELO = Path(__file__).parent / "modelo_asistente.joblib"

_modelo_asistente = None

CATEGORIAS_MAP = {
    'plomeria': {
        'nombre': 'Plomería',
        'claves': ['plomer', 'tubo', 'tuberia', 'tubería', 'fuga', 'desague', 'desagüe', 'bomba destapadora', 'terraja', 'tarraja'],
    },
    'carpinteria': {
        'nombre': 'Carpintería',
        'claves': ['carpinter', 'madera', 'lija', 'lijadora', 'sierra', 'cepillo', 'formon', 'formón'],
    },
    'demolicion': {
        'nombre': 'Demolición y Construcción',
        'claves': ['demolic', 'concreto', 'muro', 'rotomartillo', 'martillo demoledor', 'cincel', 'revolvedora', 'romper'],
    },
    'electricidad': {
        'nombre': 'Electricidad',
        'claves': ['electr', 'cable', 'cableado', 'multimetro', 'multímetro', 'voltaje', 'amperímetro', 'pinza'],
    },
    'jardineria': {
        'nombre': 'Jardinería y Poda',
        'claves': ['jardin', 'jardín', 'poda', 'cesped', 'césped', 'pasto', 'motosierra', 'desbrozadora', 'podar'],
    },
    'pintura': {
        'nombre': 'Pintura y Acabados',
        'claves': ['pintur', 'pintar', 'brocha', 'rodillo', 'compresor', 'pistola', 'acabado'],
    },
}


def cargar_modelo():
    global _modelo_asistente
    if _modelo_asistente is None:
        if not RUTA_MODELO.exists():
            raise FileNotFoundError(
                "No se encontró modelo_asistente.joblib. "
                "Ejecuta: python entrenamiento/entrenar_asistente.py"
            )
        _modelo_asistente = joblib.load(RUTA_MODELO)
    return _modelo_asistente


def sacar_folio(texto):
    # Busca un código tipo DEM-202611-0001 o un número simple
    patron_codigo = r'\b[A-Za-z]{2,5}-\d{6}-\d{1,6}\b'
    patron_numero = r'\b\d{1,6}\b'

    match = re.search(patron_codigo, texto)
    if match:
        partes = match.group().split("-")
        try:
            return int(partes[-1])
        except ValueError:
            pass

    match = re.search(patron_numero, texto)
    if match:
        return int(match.group())

    return None


def detectar_categoria(texto):
    t = texto.lower()
    for cat_slug, info in CATEGORIAS_MAP.items():
        if any(clave in t for clave in info['claves']):
            return cat_slug, info['nombre']
    return None, None


def es_pregunta_como_rentar(texto):
    t = texto.lower()
    frases = [
        "como rent", "cómo rent", "como pido", "cómo pido",
        "como se renta", "cómo se renta", "pasos para rent",
        "proceso de renta", "quiero rentar", "como solicito", "cómo solicito",
        "como funciona la renta", "cómo funciona la renta", "donde rent", "dónde rent"
    ]
    return any(f in t for f in frases)


def responder(mensaje):
    modelo = cargar_modelo()
    intencion = modelo.predict([mensaje])[0]

    cat_slug, cat_nombre = detectar_categoria(mensaje)

    # si pregunta como pedir renta
    if intencion == "como_rentar" or es_pregunta_como_rentar(mensaje):
        respuesta = (
            "Para rentar una herramienta sigue estos 4 sencillos pasos:\n\n"
            "1. Ve a la pestaña 'Recomendador' en la barra superior.\n"
            "2. Selecciona las características de tu trabajo (tipo de obra, escala, días y área).\n"
            "3. Pulsa 'Consultar recomendación' para que el sistema evalúe la mejor opción para tu caso.\n"
            "4. Ingresa tu nombre de cliente, verifica los días (máximo 30) y presiona 'Confirmar Renta'.\n\n"
            "¡Listo! Se te generará un ticket con tu número de Folio único para que puedas darle seguimiento en cualquier momento."
        )
        return {"intencion": "como_rentar", "respuesta": respuesta}

    # saludo
    if intencion == "saludo":
        respuesta = (
            "¡Hola! Bienvenido a Renta de Herramientas. "
            "Puedo ayudarte a consultar herramientas por categoría (como plomería o carpintería), "
            "revisar el estado de tu renta con tu folio o explicarte cómo solicitar una renta. "
            "¿En qué te puedo apoyar hoy?"
        )

    # catalogo o si pide una categoria directa
    elif intencion == "catalogo" or (cat_slug is not None and intencion not in ["rastreo_folio", "pregunta_recomendador"]):
        if cat_slug:
            herramientas = Herramienta.objects.filter(categoria=cat_slug).order_by('tipo', 'precio_dia')
            if herramientas.exists():
                lineas = [
                    f"• {h.nombre} (${float(h.precio_dia):.0f}/día) — {h.get_tipo_display()}"
                    for h in herramientas
                ]
                respuesta = (
                    f"Para {cat_nombre}, tenemos disponibles las siguientes opciones:\n\n"
                    + "\n".join(lineas)
                    + "\n\nPuedes consultar los detalles completos en la pestaña 'Catálogo' o pedir una sugerencia en 'Recomendador'."
                )
            else:
                respuesta = f"Por el momento no tenemos herramientas registradas en la categoría de {cat_nombre}."
        else:
            total = Herramienta.objects.count()
            respuesta = (
                f"Contamos con {total} herramientas y kits de trabajo divididos en 6 categorías:\n\n"
                "• Demolición y Construcción (rotomartillos, martillos demoledores)\n"
                "• Carpintería (sierras circulares, lijadoras, kits completos)\n"
                "• Plomería (bombas destapadoras, terrajas)\n"
                "• Electricidad (multímetros, guías jalacables)\n"
                "• Jardinería y Poda (desbrozadoras, motosierras)\n"
                "• Pintura y Acabados (compresores, rodillos, pistolas)\n\n"
                "Puedes pedirme herramientas de alguna categoría en específico (por ejemplo: 'qué tienen de plomería') "
                "o ver todo el inventario en la pestaña 'Catálogo'."
            )

    # consulta de folio
    elif intencion == "rastreo_folio":
        folio = sacar_folio(mensaje)
        if folio is None:
            respuesta = (
                "Para consultar tu renta necesito el número o código de tu folio. "
                "Por ejemplo, puedes escribir: 'folio 1' o 'estado de DEM-202611-0001'."
            )
        else:
            try:
                renta = Renta.objects.get(id=folio)
                respuesta = (
                    f"Encontré tu renta {renta.codigo_folio}:\n\n"
                    f"• Estado: {renta.estado}\n"
                    f"• Cliente: {renta.cliente_nombre}\n"
                    f"• Herramienta: {renta.herramienta_sugerida} ({'Kit Completo' if renta.es_kit else 'Herramienta Individual'})\n"
                    f"• Duración: {renta.duracion_dias} día(s)\n"
                    f"• Costo total: ${float(renta.costo_total):.2f}\n\n"
                    f"También puedes consultarla con todo detalle en la pestaña 'Buscar Folio'."
                )
            except Renta.DoesNotExist:
                respuesta = f"No encontré ninguna renta con el folio #{folio}. Verifica el número y vuelve a intentar."

    # explicacion sencilla del recomendador
    elif intencion == "pregunta_recomendador":
        if cat_slug:
            respuesta = (
                f"El recomendador analiza las características de tu trabajo de {cat_nombre} "
                f"(el tamaño de la obra, los días de uso y si es en interior o exterior) "
                f"para sugerirte si te conviene rentar una sola herramienta o un kit completo con todo lo necesario. "
                f"Además, cuida tu seguridad verificando que el equipo sea el adecuado para el lugar de trabajo. "
                f"Puedes probarlo directamente en la pestaña 'Recomendador' de arriba."
            )
        else:
            respuesta = (
                "El recomendador te ayuda a elegir exactamente la herramienta o kit que necesitas para tu trabajo. "
                "Solo seleccionas el tipo de obra, los días que la ocuparás y si es en interior o exterior, y te sugiere la opción más segura y económica para que no gastes de más ni te falte equipo. "
                "Puedes usarlo directamente en la pestaña 'Recomendador' de arriba."
            )

    # fuera de dominio
    else:
        respuesta = (
            "Disculpa, solo puedo orientarte sobre temas de renta de herramientas: "
            "consultar el catálogo por categoría (plomería, carpintería, etc.), revisar el estado de una renta con su folio o explicarte cómo rentar."
        )

    return {"intencion": intencion, "respuesta": respuesta}
