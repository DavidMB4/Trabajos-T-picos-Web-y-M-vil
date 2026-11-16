class ElementoRanking {
  final String opcion;
  final double confianza;

  ElementoRanking({
    required this.opcion,
    required this.confianza,
  });

  factory ElementoRanking.fromJson(dynamic json) {
    if (json is Map) {
      return ElementoRanking(
        opcion: json['opcion']?.toString() ?? '',
        confianza: (json['confianza'] as num?)?.toDouble() ?? 0.0,
      );
    }
    if (json is List && json.isNotEmpty) {
      return ElementoRanking(
        opcion: json[0]?.toString() ?? '',
        confianza: (json.length > 1 ? (json[1] as num?)?.toDouble() : 0.0) ?? 0.0,
      );
    }
    return ElementoRanking(opcion: json.toString(), confianza: 0.0);
  }
}

class Recomendacion {
  final String eleccion;
  final bool esKit;
  final String motivo;
  final String preferidoPorModelo;
  final bool corregidoPorReglas;
  final double confianza;
  final List<ElementoRanking> ranking;

  Recomendacion({
    required this.eleccion,
    required this.esKit,
    required this.motivo,
    required this.preferidoPorModelo,
    required this.corregidoPorReglas,
    required this.confianza,
    required this.ranking,
  });

  factory Recomendacion.fromJson(Map<String, dynamic> json) {
    final rawRanking = json['ranking'] as List<dynamic>? ?? [];
    return Recomendacion(
      eleccion: json['eleccion'] as String? ?? '',
      esKit: json['es_kit'] as bool? ?? false,
      motivo: json['motivo'] as String? ?? '',
      preferidoPorModelo: json['preferido_por_modelo'] as String? ?? '',
      corregidoPorReglas: json['corregido_por_reglas'] as bool? ?? false,
      confianza: (json['confianza'] as num?)?.toDouble() ?? 0.0,
      ranking: rawRanking.map((item) => ElementoRanking.fromJson(item)).toList(),
    );
  }
}
