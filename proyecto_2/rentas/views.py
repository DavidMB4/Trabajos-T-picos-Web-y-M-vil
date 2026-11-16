import json
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render, get_object_or_404

from .models import Herramienta, Renta
from .recomendador import obtener_recomendador, CAMPOS, CAMPOS_NUMERICOS


def estado_api(request):
    return JsonResponse({
        "servicio": "API Renta de Herramientas",
        "estado": "activo",
        "version": "1.0",
        "cliente_frontend": "Flutter",
        "endpoints": [
            "/api/catalogo/",
            "/api/recomendar/",
            "/api/rentas/",
            "/api/rentas/<folio>/"
        ]
    }, json_dumps_params={"ensure_ascii": False})


@require_GET
def listar_catalogo(request):
    categoria = request.GET.get('categoria')
    tipo = request.GET.get('tipo')

    items = Herramienta.objects.all()
    if categoria:
        items = items.filter(categoria=categoria)
    if tipo:
        items = items.filter(tipo=tipo)

    datos = [
        {
            "id": h.id,
            "nombre": h.nombre,
            "tipo": h.tipo,
            "categoria": h.categoria,
            "precio_dia": float(h.precio_dia),
            "stock": h.stock,
            "descripcion": h.descripcion,
            "incluye_epp": h.incluye_epp,
        }
        for h in items
    ]
    return JsonResponse({"total": len(datos), "catalogo": datos}, json_dumps_params={"ensure_ascii": False})


@require_GET
def detalle_herramienta(request, id):
    h = get_object_or_404(Herramienta, id=id)
    return JsonResponse({
        "id": h.id,
        "nombre": h.nombre,
        "tipo": h.tipo,
        "categoria": h.categoria,
        "precio_dia": float(h.precio_dia),
        "stock": h.stock,
        "descripcion": h.descripcion,
        "incluye_epp": h.incluye_epp,
    }, json_dumps_params={"ensure_ascii": False})


@csrf_exempt
@require_POST
def recomendar_herramienta(request):
    try:
        cuerpo = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "el cuerpo debe ser un json valido"}, status=400)

    faltantes = [campo for campo in CAMPOS if campo not in cuerpo]
    if faltantes:
        return JsonResponse({"error": "faltan campos obligatorios", "campos": faltantes}, status=400)

    try:
        for campo in CAMPOS_NUMERICOS:
            cuerpo[campo] = float(cuerpo[campo])
            if cuerpo[campo] <= 0:
                return JsonResponse({"error": f"{campo} debe ser mayor a cero"}, status=400)
            if campo == "duracion_dias" and cuerpo[campo] > 30:
                return JsonResponse({"error": "La duración máxima permitida de renta es de 30 días"}, status=400)
    except (TypeError, ValueError):
        return JsonResponse({"error": "duracion_dias debe ser un numero valido"}, status=400)

    try:
        motor = obtener_recomendador()
        resultado = motor.explicar(cuerpo)
    except FileNotFoundError as error:
        return JsonResponse({"error": str(error)}, status=503)

    return JsonResponse(resultado.a_dict(), json_dumps_params={"ensure_ascii": False})


@csrf_exempt
@require_POST
def registrar_renta(request):
    try:
        cuerpo = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "el cuerpo debe ser un json valido"}, status=400)

    cliente_nombre = cuerpo.get("cliente_nombre", "").strip()
    herramienta_sugerida = cuerpo.get("herramienta_sugerida", "").strip()
    tipo_trabajo = cuerpo.get("tipo_trabajo", "general")
    duracion_dias = int(cuerpo.get("duracion_dias", 1))
    if duracion_dias <= 0 or duracion_dias > 30:
        return JsonResponse({"error": "La duración debe estar entre 1 y 30 días"}, status=400)
    es_kit = bool(cuerpo.get("es_kit", False))
    confianza_modelo = float(cuerpo.get("confianza_modelo", 1.0))
    corregido_por_reglas = bool(cuerpo.get("corregido_por_reglas", False))
    motivo_regla = cuerpo.get("motivo_regla", "")

    if not cliente_nombre or not herramienta_sugerida:
        return JsonResponse({"error": "faltan datos para registrar la renta"}, status=400)

    item_catalogo = Herramienta.objects.filter(nombre__iexact=herramienta_sugerida).first()
    precio_dia = item_catalogo.precio_dia if item_catalogo else Decimal("300.00")
    costo_total = precio_dia * Decimal(str(duracion_dias))

    renta = Renta.objects.create(
        cliente_nombre=cliente_nombre,
        herramienta_sugerida=herramienta_sugerida,
        es_kit=es_kit,
        tipo_trabajo=tipo_trabajo,
        duracion_dias=duracion_dias,
        costo_total=costo_total,
        estado='Registrado',
        confianza_modelo=confianza_modelo,
        corregido_por_reglas=corregido_por_reglas,
        motivo_regla=motivo_regla
    )

    return JsonResponse({
        "folio": renta.id,
        "codigo_folio": renta.codigo_folio,
        "mensaje": f"Renta {renta.codigo_folio} registrada",
        "cliente": renta.cliente_nombre,
        "herramienta": renta.herramienta_sugerida,
        "es_kit": renta.es_kit,
        "duracion_dias": renta.duracion_dias,
        "costo_total": float(renta.costo_total),
        "estado": renta.estado,
        "fecha": renta.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")
    }, status=201, json_dumps_params={"ensure_ascii": False})


@require_GET
def consultar_renta_por_folio(request, folio):
    folio_str = str(folio).strip()
    id_busqueda = None
    if "-" in folio_str:
        partes = folio_str.split("-")
        try:
            id_busqueda = int(partes[-1])
        except ValueError:
            pass
    else:
        try:
            id_busqueda = int(folio_str)
        except ValueError:
            pass

    if id_busqueda is not None:
        renta = get_object_or_404(Renta, id=id_busqueda)
    else:
        return JsonResponse({"error": "Formato de folio inválido"}, status=400)

    return JsonResponse({
        "folio": renta.id,
        "codigo_folio": renta.codigo_folio,
        "cliente": renta.cliente_nombre,
        "herramienta_sugerida": renta.herramienta_sugerida,
        "es_kit": renta.es_kit,
        "tipo_trabajo": renta.tipo_trabajo,
        "duracion_dias": renta.duracion_dias,
        "costo_total": float(renta.costo_total),
        "estado": renta.estado,
        "confianza_modelo": renta.confianza_modelo,
        "corregido_por_reglas": renta.corregido_por_reglas,
        "motivo_regla": renta.motivo_regla,
        "fecha_creacion": renta.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")
    }, json_dumps_params={"ensure_ascii": False})


@csrf_exempt
@require_POST
def asistente_chat(request):
    try:
        cuerpo = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "el cuerpo debe ser un json valido"}, status=400)

    mensaje = cuerpo.get("mensaje", "").strip()
    if not mensaje:
        return JsonResponse({"error": "el campo mensaje no puede estar vacio"}, status=400)

    try:
        from .asistente import responder
        resultado = responder(mensaje)
    except FileNotFoundError as e:
        return JsonResponse({"error": str(e)}, status=503)

    return JsonResponse(resultado, json_dumps_params={"ensure_ascii": False})
