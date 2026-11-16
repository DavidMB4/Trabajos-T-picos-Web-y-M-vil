class Herramienta {
  final int id;
  final String nombre;
  final String tipo;
  final String categoria;
  final double precioDia;
  final int stock;
  final String descripcion;
  final bool incluyeEpp;

  Herramienta({
    required this.id,
    required this.nombre,
    required this.tipo,
    required this.categoria,
    required this.precioDia,
    required this.stock,
    required this.descripcion,
    required this.incluyeEpp,
  });

  factory Herramienta.fromJson(Map<String, dynamic> json) {
    return Herramienta(
      id: json['id'] as int? ?? 0,
      nombre: json['nombre'] as String? ?? 'Sin nombre',
      tipo: json['tipo'] as String? ?? 'individual',
      categoria: json['categoria'] as String? ?? 'general',
      precioDia: (json['precio_dia'] as num?)?.toDouble() ?? 0.0,
      stock: json['stock'] as int? ?? 0,
      descripcion: json['descripcion'] as String? ?? '',
      incluyeEpp: json['incluye_epp'] as bool? ?? false,
    );
  }
}
