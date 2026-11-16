"""Reglas de negocio para renta de herramientas y kits.

Aseguran que la decisión final (herramienta individual vs kit completo)
cumpla con normas de seguridad, escala del trabajo y duración.
"""

HERRAMIENTAS_POR_OFICIO = {
    "demolicion": {
        "individual_ligera": "Rotomartillo individual",
        "individual_pesada": "Demoledor hexagonal 15kg",
        "kit": "Kit Demolicion Completo",
    },
    "carpinteria": {
        "individual_ligera": "Lijadora orbital individual",
        "individual_pesada": "Sierra circular de mano",
        "kit": "Kit Carpinteria Integral",
    },
    "plomeria": {
        "individual_ligera": "Bomba destapadora individual",
        "individual_pesada": "Termofusora digital PPR",
        "kit": "Kit Plomeria Profesional",
    },
    "electricidad": {
        "individual_ligera": "Taladro percutor individual",
        "individual_pesada": "Ranuradora de muros",
        "kit": "Kit Electricidad Completo",
    },
    "jardineria": {
        "individual_ligera": "Cortasetos individual",
        "individual_pesada": "Desbrozadora a gasolina",
        "kit": "Kit Jardineria y Poda",
    },
    "pintura": {
        "individual_ligera": "Pistola de pintar individual",
        "individual_pesada": "Lijadora de tablaroca y yeso",
        "kit": "Kit Pintura y Acabados",
    },
}

LIMITES = {
    "Rotomartillo individual": {"nivel_minimo": "intermedio", "dias_max": 2, "admite_obra_mayor": False},
    "Lijadora orbital individual": {"nivel_minimo": "principiante", "dias_max": 2, "admite_obra_mayor": False},
    "Bomba destapadora individual": {"nivel_minimo": "principiante", "dias_max": 2, "admite_obra_mayor": False},
    "Taladro percutor individual": {"nivel_minimo": "principiante", "dias_max": 2, "admite_obra_mayor": False},
    "Cortasetos individual": {"nivel_minimo": "principiante", "dias_max": 2, "admite_obra_mayor": False},
    "Pistola de pintar individual": {"nivel_minimo": "principiante", "dias_max": 2, "admite_obra_mayor": False},

    "Demoledor hexagonal 15kg": {"nivel_minimo": "intermedio", "dias_max": 3, "admite_obra_mayor": False},
    "Sierra circular de mano": {"nivel_minimo": "intermedio", "dias_max": 3, "admite_obra_mayor": False},
    "Termofusora digital PPR": {"nivel_minimo": "intermedio", "dias_max": 3, "admite_obra_mayor": False},
    "Ranuradora de muros": {"nivel_minimo": "intermedio", "dias_max": 3, "admite_obra_mayor": False},
    "Desbrozadora a gasolina": {"nivel_minimo": "intermedio", "dias_max": 3, "admite_obra_mayor": False},
    "Lijadora de tablaroca y yeso": {"nivel_minimo": "intermedio", "dias_max": 3, "admite_obra_mayor": False},

    "Kit Demolicion Completo": {"nivel_minimo": "principiante", "dias_max": 30, "admite_obra_mayor": True},
    "Kit Carpinteria Integral": {"nivel_minimo": "principiante", "dias_max": 30, "admite_obra_mayor": True},
    "Kit Plomeria Profesional": {"nivel_minimo": "principiante", "dias_max": 30, "admite_obra_mayor": True},
    "Kit Electricidad Completo": {"nivel_minimo": "principiante", "dias_max": 30, "admite_obra_mayor": True},
    "Kit Jardineria y Poda": {"nivel_minimo": "principiante", "dias_max": 30, "admite_obra_mayor": True},
    "Kit Pintura y Acabados": {"nivel_minimo": "principiante", "dias_max": 30, "admite_obra_mayor": True},
}


def es_posible(opcion: str, solicitud: dict) -> bool:
    """Evalua si una opcion cumple las reglas del negocio para la solicitud dada."""
    tipo_trabajo = solicitud.get("tipo_trabajo", "").lower()
    if tipo_trabajo in HERRAMIENTAS_POR_OFICIO:
        validas = HERRAMIENTAS_POR_OFICIO[tipo_trabajo].values()
        if opcion not in validas:
            return False

    if opcion not in LIMITES:
        return True

    limite = LIMITES[opcion]
    experiencia = solicitud.get("experiencia_usuario", "principiante")
    dias = float(solicitud.get("duracion_dias", 1))
    escala = solicitud.get("escala_trabajo", "reparacion_menor")

    if experiencia == "principiante" and limite["nivel_minimo"] in ["intermedio", "profesional"]:
        return False

    if dias > limite["dias_max"]:
        return False

    if escala == "obra_mayor" and not limite["admite_obra_mayor"]:
        return False

    return True


def aplicar_reglas(preferido_modelo: str, solicitud: dict, confianza_original: float):
    """
    Aplica las reglas de negocio sobre la recomendacion del modelo.
    Garantiza que la sugerencia pertenezca al oficio correcto y explica el motivo.
    """
    tipo_trabajo = solicitud.get("tipo_trabajo", "demolicion").lower()
    escala = solicitud.get("escala_trabajo", "reparacion_menor")
    experiencia = solicitud.get("experiencia_usuario", "principiante")
    dias = float(solicitud.get("duracion_dias", 1))

    oficio_info = HERRAMIENTAS_POR_OFICIO.get(tipo_trabajo)
    if not oficio_info:
        return preferido_modelo, False, f"Recomendación: {preferido_modelo}", confianza_original

    ligera = oficio_info["individual_ligera"]
    pesada = oficio_info["individual_pesada"]
    kit = oficio_info["kit"]
    validas_oficio = [ligera, pesada, kit]

    if preferido_modelo not in validas_oficio:
        preferido_modelo = ligera if (escala == "reparacion_menor" and dias <= 2) else kit

    # Maximo 30 dias de renta en la tienda
    if dias > 30:
        motivo = "El plazo máximo de renta continua es de 30 días según las políticas de la tienda."
        return kit, True, motivo, confianza_original

    # Si es principiante en demolicion le damos el kit con proteccion
    if tipo_trabajo == "demolicion" and experiencia == "principiante" and preferido_modelo != kit:
        motivo = f"Ajuste por seguridad: Por ser usuario principiante en demolición, se asigna el {kit} con equipo de protección y accesorios incluidos."
        return kit, True, motivo, confianza_original

    # Si son mas de 3 dias o es obra mayor se manda el kit
    if (dias > 3 or escala == "obra_mayor") and preferido_modelo != kit:
        motivo = f"Ajuste por escala y duración: Para proyectos de más de 3 días o de obra mayor, se asigna el {kit} con refacciones y accesorios."
        return kit, True, motivo, confianza_original

    # Si es principiante y pide maquina pesada, le bajamos a ligera o kit
    if experiencia == "principiante" and preferido_modelo == pesada:
        motivo = f"Ajuste por experiencia: Para usuario principiante se sugiere la {ligera} o el {kit} con equipo de protección."
        sugerencia = ligera if dias <= 2 else kit
        return sugerencia, True, motivo, confianza_original

    # Si todo esta en orden dejamos lo que predijo el modelo
    es_kit = "kit" in preferido_modelo.lower()
    tipo_txt = "Kit completo" if es_kit else "Herramienta individual"
    motivo = f"Sugerencia directa del modelo: {preferido_modelo} ({tipo_txt})."
    return preferido_modelo, False, motivo, confianza_original
