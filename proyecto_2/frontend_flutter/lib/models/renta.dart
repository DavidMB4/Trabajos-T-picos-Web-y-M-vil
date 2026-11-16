class Renta {
  final int folio;
  final String codigoFolio;
  final String cliente;
  final String herramientaSugerida;
  final bool esKit;
  final String tipoTrabajo;
  final int duracionDias;
  final double costoTotal;
  final String estado;
  final double confianzaModelo;
  final bool corregidoPorReglas;
  final String motivoRegla;
  final String fechaCreacion;

  Renta({
    required this.folio,
    required this.codigoFolio,
    required this.cliente,
    required this.herramientaSugerida,
    required this.esKit,
    required this.tipoTrabajo,
    required this.duracionDias,
    required this.costoTotal,
    required this.estado,
    required this.confianzaModelo,
    required this.corregidoPorReglas,
    required this.motivoRegla,
    required this.fechaCreacion,
  });

  factory Renta.fromJson(Map<String, dynamic> json) {
    final idNum = json['folio'] as int? ?? json['id'] as int? ?? 0;
    final codigo = json['codigo_folio'] as String? ?? 'FOL-$idNum';

    return Renta(
      folio: idNum,
      codigoFolio: codigo,
      cliente: json['cliente'] as String? ?? json['cliente_nombre'] as String? ?? '',
      herramientaSugerida: json['herramienta_sugerida'] as String? ?? json['herramienta'] as String? ?? '',
      esKit: json['es_kit'] as bool? ?? false,
      tipoTrabajo: json['tipo_trabajo'] as String? ?? 'general',
      duracionDias: json['duracion_dias'] as int? ?? 1,
      costoTotal: (json['costo_total'] as num?)?.toDouble() ?? 0.0,
      estado: json['estado'] as String? ?? 'Registrado',
      confianzaModelo: (json['confianza_modelo'] as num?)?.toDouble() ?? 1.0,
      corregidoPorReglas: json['corregido_por_reglas'] as bool? ?? false,
      motivoRegla: json['motivo_regla'] as String? ?? '',
      fechaCreacion: json['fecha_creacion'] as String? ?? json['fecha'] as String? ?? '',
    );
  }
}
