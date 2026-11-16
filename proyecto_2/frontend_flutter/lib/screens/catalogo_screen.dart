import 'package:flutter/material.dart';
import '../models/herramienta.dart';
import '../services/api_service.dart';

class CatalogoScreen extends StatefulWidget {
  const CatalogoScreen({super.key});

  @override
  State<CatalogoScreen> createState() => _CatalogoScreenState();
}

class _CatalogoScreenState extends State<CatalogoScreen> {
  List<Herramienta> _herramientas = [];
  List<Herramienta> _filtradas = [];
  bool _cargando = true;
  String _error = '';
  final TextEditingController _busquedaController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _cargarCatalogo();
  }

  Future<void> _cargarCatalogo() async {
    setState(() {
      _cargando = true;
      _error = '';
    });
    try {
      final items = await ApiService.getCatalogo();
      setState(() {
        _herramientas = items;
        _filtradas = items;
        _cargando = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _cargando = false;
      });
    }
  }

  void _filtrar(String query) {
    setState(() {
      if (query.isEmpty) {
        _filtradas = _herramientas;
      } else {
        _filtradas = _herramientas
            .where((h) =>
                h.nombre.toLowerCase().contains(query.toLowerCase()) ||
                h.categoria.toLowerCase().contains(query.toLowerCase()))
            .toList();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SelectionArea(
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.all(12.0),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _busquedaController,
                      onChanged: _filtrar,
                      decoration: InputDecoration(
                        hintText: 'Buscar herramienta o categoría...',
                        prefixIcon: const Icon(Icons.search),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(10),
                        ),
                        contentPadding: const EdgeInsets.symmetric(horizontal: 16),
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  IconButton(
                    icon: const Icon(Icons.refresh),
                    tooltip: 'Recargar catálogo',
                    onPressed: _cargarCatalogo,
                  ),
                ],
              ),
            ),
          Expanded(
            child: _cargando
                ? const Center(child: CircularProgressIndicator())
                : _error.isNotEmpty
                    ? Center(
                        child: Padding(
                          padding: const EdgeInsets.all(24.0),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(Icons.wifi_off, size: 56, color: Colors.grey.shade600),
                              const SizedBox(height: 16),
                              Text(
                                _error.replaceFirst('Exception: ', ''),
                                textAlign: TextAlign.center,
                                style: TextStyle(fontSize: 15, color: Colors.grey.shade800),
                              ),
                              const SizedBox(height: 16),
                              ElevatedButton.icon(
                                onPressed: _cargarCatalogo,
                                icon: const Icon(Icons.refresh),
                                label: const Text('Reintentar'),
                              ),
                            ],
                          ),
                        ),
                      )
                    : _filtradas.isEmpty
                        ? const Center(child: Text('No se encontraron herramientas.'))
                        : ListView.builder(
                            itemCount: _filtradas.length,
                            itemBuilder: (context, index) {
                              final h = _filtradas[index];
                              return Card(
                                margin: const EdgeInsets.symmetric(
                                    horizontal: 12, vertical: 6),
                                elevation: 2,
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(10),
                                ),
                                child: ListTile(
                                  leading: CircleAvatar(
                                    backgroundColor: h.tipo == 'kit'
                                        ? const Color(0xFFFFEDD5)
                                        : const Color(0xFFE7E0D6),
                                    child: Icon(
                                      h.tipo == 'kit'
                                          ? Icons.business_center
                                          : Icons.build,
                                      color: h.tipo == 'kit'
                                          ? const Color(0xFFF96302)
                                          : const Color(0xFF44403C),
                                    ),
                                  ),
                                  title: Text(
                                    h.nombre,
                                    style: const TextStyle(fontWeight: FontWeight.bold),
                                  ),
                                  subtitle: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        'Categoría: ${h.categoria.toUpperCase()} | Stock: ${h.stock} uds',
                                        style: TextStyle(
                                            color: Colors.grey.shade600, fontSize: 12),
                                      ),
                                      if (h.descripcion.isNotEmpty)
                                        Text(
                                          h.descripcion,
                                          style: const TextStyle(fontSize: 12),
                                          maxLines: 2,
                                          overflow: TextOverflow.ellipsis,
                                        ),
                                    ],
                                  ),
                                  trailing: Text(
                                    '\$${h.precioDia.toStringAsFixed(0)}/día',
                                    style: const TextStyle(
                                        fontSize: 15,
                                        fontWeight: FontWeight.bold,
                                        color: Colors.blue),
                                  ),
                                ),
                              );
                            },
                          ),
          ),
        ],
      ),
    ),
  );
}
}
