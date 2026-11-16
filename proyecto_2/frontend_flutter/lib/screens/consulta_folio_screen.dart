import 'package:flutter/material.dart';
import '../models/renta.dart';
import '../services/api_service.dart';

class ConsultaFolioScreen extends StatefulWidget {
  const ConsultaFolioScreen({super.key});

  @override
  State<ConsultaFolioScreen> createState() => _ConsultaFolioScreenState();
}

class _ConsultaFolioScreenState extends State<ConsultaFolioScreen> {
  final TextEditingController _folioController = TextEditingController(text: '1');
  bool _cargando = false;
  Renta? _renta;
  String _error = '';

  Future<void> _buscarFolio() async {
    final folioText = _folioController.text.trim();
    if (folioText.isEmpty) {
      setState(() => _error = 'Por favor ingresa un número de folio o código para buscar.');
      return;
    }

    setState(() {
      _cargando = true;
      _error = '';
      _renta = null;
    });

    try {
      final res = await ApiService.consultarFolio(folioText);
      setState(() {
        _renta = res;
        _cargando = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString().replaceFirst('Exception: ', '');
        _cargando = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Card(
              elevation: 2,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Búsqueda por folio',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 12),
                    Row(
                      children: [
                        Expanded(
                          child: TextField(
                            controller: _folioController,
                            decoration: const InputDecoration(
                              labelText: 'Número o Código de Folio',
                              hintText: 'Ej. 1 o DEM-202611-0005',
                              border: OutlineInputBorder(),
                            ),
                          ),
                        ),
                        const SizedBox(width: 8),
                        ElevatedButton.icon(
                          icon: const Icon(Icons.search),
                          label: const Text('Buscar'),
                          style: ElevatedButton.styleFrom(
                            padding: const EdgeInsets.symmetric(
                                horizontal: 16, vertical: 16),
                            backgroundColor: const Color(0xFFF96302),
                            foregroundColor: Colors.white,
                          ),
                          onPressed: _cargando ? null : _buscarFolio,
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),

            if (_cargando)
              const Padding(
                padding: EdgeInsets.all(24.0),
                child: Center(child: CircularProgressIndicator()),
              ),

            if (_error.isNotEmpty)
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 12.0),
                child: Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.red.shade50,
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: Colors.red.shade200),
                  ),
                  child: Row(
                    children: [
                      Icon(Icons.info_outline, color: Colors.red.shade700),
                      const SizedBox(width: 10),
                      Expanded(
                        child: Text(
                          _error.replaceFirst('Exception: ', ''),
                          style: TextStyle(color: Colors.red.shade900, fontSize: 13),
                        ),
                      ),
                    ],
                  ),
                ),
              ),

            if (_renta != null) ...[
              const SizedBox(height: 16),
              Card(
                elevation: 3,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                _renta!.codigoFolio,
                                style: const TextStyle(
                                  fontSize: 22,
                                  fontWeight: FontWeight.w900,
                                  color: Colors.blue,
                                ),
                              ),
                              Text(
                                'Registro #${_renta!.folio}',
                                style: TextStyle(
                                  fontSize: 12,
                                  color: Colors.grey.shade600,
                                ),
                              ),
                            ],
                          ),
                          Chip(
                            label: Text(_renta!.estado),
                            backgroundColor: Colors.green.shade100,
                            labelStyle: TextStyle(
                              color: Colors.green.shade800,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ],
                      ),
                      const Divider(),
                      _itemFila('Cliente:', _renta!.cliente),
                      _itemFila('Herramienta:', _renta!.herramientaSugerida),
                      _itemFila('Tipo:', _renta!.esKit ? 'Kit de Trabajo' : 'Herramienta Individual'),
                      _itemFila('Trabajo registrado:', _renta!.tipoTrabajo),
                      _itemFila('Duración:', '${_renta!.duracionDias} días'),
                      _itemFila('Costo total:', '\$${_renta!.costoTotal.toStringAsFixed(2)} MXN'),
                      _itemFila('Confianza del modelo:', '${(_renta!.confianzaModelo * 100).toInt()}%'),
                      _itemFila('¿Regla intervino?:', _renta!.corregidoPorReglas ? 'Sí' : 'No'),
                      if (_renta!.motivoRegla.isNotEmpty)
                        Padding(
                          padding: const EdgeInsets.only(top: 8.0),
                          child: Container(
                            padding: const EdgeInsets.all(8),
                            color: Colors.amber.shade50,
                            child: Text(
                              'Motivo: ${_renta!.motivoRegla}',
                              style: TextStyle(fontSize: 12, color: Colors.amber.shade900),
                            ),
                          ),
                        ),
                      const SizedBox(height: 8),
                      Text(
                        'Fecha: ${_renta!.fechaCreacion}',
                        style: TextStyle(fontSize: 11, color: Colors.grey.shade600),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _itemFila(String etiqueta, String valor) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 140,
            child: Text(
              etiqueta,
              style: const TextStyle(fontWeight: FontWeight.w600, color: Color(0xFF475569)),
            ),
          ),
          Expanded(
            child: Text(
              valor,
              style: const TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF1E293B)),
            ),
          ),
        ],
      ),
    );
  }
}
