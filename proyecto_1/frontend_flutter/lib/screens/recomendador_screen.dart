import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../models/recomendacion.dart';
import '../models/renta.dart';
import '../services/api_service.dart';

class RecomendadorScreen extends StatefulWidget {
  const RecomendadorScreen({super.key});

  @override
  State<RecomendadorScreen> createState() => _RecomendadorScreenState();
}

class _RecomendadorScreenState extends State<RecomendadorScreen> {
  String _tipoTrabajo = 'demolicion';
  String _escalaTrabajo = 'remodelacion_media';
  String _experiencia = 'intermedio';
  int _duracionDias = 2;
  String _areaTrabajo = 'interior';

  final TextEditingController _clienteController = TextEditingController();
  final TextEditingController _diasController =
      TextEditingController(text: '2');

  bool _cargando = false;
  Recomendacion? _recomendacion;
  String? _herramientaElegida;
  Renta? _rentaRegistrada;
  String _error = '';
  String? _errorDias;
  String? _errorCliente;

  Future<void> _solicitarRecomendacion() async {
    final textoDias = _diasController.text.trim();
    if (textoDias.isEmpty) {
      setState(() {
        _errorDias = 'Ingresa la cantidad de días';
        _cargando = false;
      });
      return;
    }

    final dias = int.tryParse(textoDias);
    if (dias == null || dias < 1 || dias > 30) {
      setState(() {
        _errorDias = dias != null && dias > 30
            ? 'El límite máximo es de 30 días'
            : 'Debe ser al menos 1 día';
        _cargando = false;
      });
      return;
    }

    setState(() {
      _errorDias = null;
      _errorCliente = null;
      _duracionDias = dias;
      _cargando = true;
      _error = '';
      _rentaRegistrada = null;
    });

    final payload = {
      'tipo_trabajo': _tipoTrabajo,
      'escala_trabajo': _escalaTrabajo,
      'experiencia_usuario': _experiencia,
      'duracion_dias': _duracionDias,
      'area_trabajo': _areaTrabajo,
    };

    try {
      final res = await ApiService.pedirRecomendacion(payload);
      setState(() {
        _recomendacion = res;
        _herramientaElegida = res.eleccion;
        _cargando = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _cargando = false;
      });
    }
  }

  Future<void> _confirmarRenta() async {
    if (_recomendacion == null) return;
    final nombre = _clienteController.text.trim();
    if (nombre.isEmpty) {
      setState(() {
        _errorCliente = 'Por favor ingresa el nombre del cliente';
      });
      return;
    }

    setState(() {
      _errorCliente = null;
      _cargando = true;
    });

    final herramientaFinal = _herramientaElegida ?? _recomendacion!.eleccion;
    final esKitFinal = herramientaFinal.toLowerCase().contains('kit');

    final payload = {
      'cliente_nombre': _clienteController.text.trim(),
      'herramienta_sugerida': herramientaFinal,
      'tipo_trabajo': _tipoTrabajo,
      'duracion_dias': _duracionDias,
      'es_kit': esKitFinal,
      'confianza_modelo': _recomendacion!.confianza,
      'corregido_por_reglas': _recomendacion!.corregidoPorReglas,
      'motivo_regla': _recomendacion!.motivo,
    };

    try {
      final renta = await ApiService.registrarRenta(payload);
      setState(() {
        _rentaRegistrada = renta;
        _cargando = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
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
            _construirFormularioTrabajo(),
            if (_cargando)
              const Padding(
                padding: EdgeInsets.all(24.0),
                child: Center(child: CircularProgressIndicator()),
              ),
            if (_error.isNotEmpty) _construirMensajeError(),
            if (_recomendacion != null) ...[
              _construirTarjetaRecomendacion(),
              _construirRankingAlternativas(),
              _construirConfirmacionRenta(),
            ],
            if (_rentaRegistrada != null) _construirTicketFolio(),
          ],
        ),
      ),
    );
  }

  Widget _construirFormularioTrabajo() {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Datos del trabajo',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              initialValue: _tipoTrabajo,
              decoration: const InputDecoration(labelText: 'Tipo de Trabajo'),
              items: const [
                DropdownMenuItem(value: 'demolicion', child: Text('Demolición')),
                DropdownMenuItem(value: 'carpinteria', child: Text('Carpintería')),
                DropdownMenuItem(value: 'plomeria', child: Text('Plomería')),
                DropdownMenuItem(value: 'electricidad', child: Text('Electricidad')),
                DropdownMenuItem(value: 'jardineria', child: Text('Jardinería y Poda')),
                DropdownMenuItem(value: 'pintura', child: Text('Pintura y Acabados')),
              ],
              onChanged: (val) => setState(() => _tipoTrabajo = val!),
            ),
            const SizedBox(height: 8),
            DropdownButtonFormField<String>(
              initialValue: _escalaTrabajo,
              decoration: const InputDecoration(labelText: 'Escala del Trabajo'),
              items: const [
                DropdownMenuItem(value: 'reparacion_menor', child: Text('Reparación Menor (Casera)')),
                DropdownMenuItem(value: 'remodelacion_media', child: Text('Remodelación Media')),
                DropdownMenuItem(value: 'obra_mayor', child: Text('Obra Mayor (Pesada / Civil)')),
              ],
              onChanged: (val) => setState(() => _escalaTrabajo = val!),
            ),
            const SizedBox(height: 8),
            DropdownButtonFormField<String>(
              initialValue: _experiencia,
              decoration: const InputDecoration(labelText: 'Experiencia del Usuario'),
              items: const [
                DropdownMenuItem(value: 'principiante', child: Text('Principiante')),
                DropdownMenuItem(value: 'intermedio', child: Text('Intermedio')),
                DropdownMenuItem(value: 'profesional', child: Text('Profesional')),
              ],
              onChanged: (val) => setState(() => _experiencia = val!),
            ),
            const SizedBox(height: 8),
            DropdownButtonFormField<String>(
              initialValue: _areaTrabajo,
              decoration: const InputDecoration(labelText: 'Área de Trabajo'),
              items: const [
                DropdownMenuItem(value: 'interior', child: Text('Interior')),
                DropdownMenuItem(value: 'exterior', child: Text('Exterior')),
                DropdownMenuItem(value: 'taller', child: Text('Taller')),
              ],
              onChanged: (val) => setState(() => _areaTrabajo = val!),
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _diasController,
              keyboardType: TextInputType.number,
              inputFormatters: [
                FilteringTextInputFormatter.digitsOnly,
              ],
              decoration: InputDecoration(
                labelText: 'Días de renta',
                floatingLabelBehavior: FloatingLabelBehavior.always,
                hintText: 'Ej. 3',
                errorText: _errorDias,
                border: const OutlineInputBorder(),
              ),
              onChanged: (val) {
                if (val.isEmpty) {
                  setState(() {
                    _errorDias = null;
                  });
                  return;
                }
                final n = int.tryParse(val);
                if (n == null || n > 30) {
                  setState(() {
                    _errorDias = 'El límite máximo es de 30 días';
                  });
                } else if (n < 1) {
                  setState(() {
                    _errorDias = 'Debe ser al menos 1 día';
                  });
                } else {
                  setState(() {
                    _errorDias = null;
                    _duracionDias = n;
                  });
                }
              },
            ),
            const SizedBox(height: 12),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                icon: const Icon(Icons.psychology),
                label: const Text('Consultar recomendación'),
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 12),
                  backgroundColor: const Color(0xFFF96302),
                  foregroundColor: Colors.white,
                ),
                onPressed: _cargando ? null : _solicitarRecomendacion,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _construirMensajeError() {
    return Padding(
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
            Icon(Icons.error_outline, color: Colors.red.shade700),
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
    );
  }

  Widget _construirTarjetaRecomendacion() {
    return Card(
      color: _recomendacion!.corregidoPorReglas
          ? Colors.amber.shade50
          : Colors.green.shade50,
      shape: RoundedRectangleBorder(
        side: BorderSide(
          color: _recomendacion!.corregidoPorReglas
              ? Colors.amber.shade400
              : Colors.green.shade400,
          width: 2,
        ),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Chip(
                  avatar: Icon(
                    _recomendacion!.corregidoPorReglas
                        ? Icons.policy_outlined
                        : Icons.check_circle_outline,
                    color: Colors.white,
                    size: 18,
                  ),
                  label: Text(
                    _recomendacion!.corregidoPorReglas
                        ? 'Ajuste de seguridad'
                        : 'Sugerencia directa',
                    style: const TextStyle(color: Colors.white, fontSize: 11),
                  ),
                  backgroundColor: _recomendacion!.corregidoPorReglas
                      ? Colors.amber.shade800
                      : Colors.green.shade700,
                ),
                Text(
                  '${(_recomendacion!.confianza * 100).toInt()}% Confianza',
                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Text(
              _recomendacion!.eleccion,
              style: const TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.w900,
                color: Color(0xFF1E293B),
              ),
            ),
            Text(
              _recomendacion!.esKit
                  ? 'Tipo: Kit Completo de Herramientas'
                  : 'Tipo: Herramienta Individual',
              style: TextStyle(color: Colors.grey.shade700, fontSize: 13),
            ),
            if (_recomendacion!.corregidoPorReglas) ...[
              const SizedBox(height: 10),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(8),
                  border: Border(
                    left: BorderSide(color: Colors.amber.shade800, width: 4),
                  ),
                ),
                child: Text(
                  _recomendacion!.motivo,
                  style: TextStyle(
                    color: Colors.brown.shade900,
                    fontSize: 13,
                    height: 1.3,
                  ),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _construirRankingAlternativas() {
    if (_recomendacion!.ranking.isEmpty) return const SizedBox.shrink();

    return Padding(
      padding: const EdgeInsets.only(top: 16.0),
      child: Card(
        elevation: 1,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'Alternativas evaluadas por el recomendador',
                style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 4),
              Text(
                'Puedes confirmar la opción recomendada o seleccionar otra alternativa evaluada:',
                style: TextStyle(fontSize: 12, color: Colors.grey.shade600),
              ),
              const SizedBox(height: 12),
              ..._recomendacion!.ranking.map((item) {
                final esSeleccionada = item.opcion == _herramientaElegida;
                final porcentaje = (item.confianza * 100).toInt();

                return Container(
                  margin: const EdgeInsets.only(bottom: 8),
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                  decoration: BoxDecoration(
                    color: esSeleccionada ? const Color(0xFFFFF7ED) : Colors.grey.shade50,
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(
                      color: esSeleccionada ? const Color(0xFFF97316) : Colors.grey.shade300,
                      width: esSeleccionada ? 1.5 : 1.0,
                    ),
                  ),
                  child: Row(
                    children: [
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              item.opcion,
                              style: TextStyle(
                                fontWeight: esSeleccionada ? FontWeight.bold : FontWeight.w500,
                                color: esSeleccionada ? const Color(0xFFC2410C) : Colors.black87,
                              ),
                            ),
                            if (porcentaje > 0)
                              Text(
                                'Probabilidad calculada: $porcentaje%',
                                style: TextStyle(fontSize: 11, color: Colors.grey.shade600),
                              ),
                          ],
                        ),
                      ),
                      if (esSeleccionada)
                        Chip(
                          label: const Text('Elegida para rentar',
                              style: TextStyle(
                                  fontSize: 11,
                                  fontWeight: FontWeight.bold,
                                  color: Color(0xFFC2410C))),
                          backgroundColor: const Color(0xFFFFEDD5),
                          side: const BorderSide(color: Color(0xFFFDBA74)),
                          padding: EdgeInsets.zero,
                          visualDensity: VisualDensity.compact,
                        )
                      else
                        TextButton(
                          onPressed: () {
                            setState(() {
                              _herramientaElegida = item.opcion;
                            });
                          },
                          style: TextButton.styleFrom(
                            foregroundColor: const Color(0xFFEA580C),
                          ),
                          child: const Text('Seleccionar'),
                        ),
                    ],
                  ),
                );
              }),
            ],
          ),
        ),
      ),
    );
  }

  Widget _construirConfirmacionRenta() {
    return Padding(
      padding: const EdgeInsets.only(top: 16.0),
      child: Card(
        elevation: 2,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'Confirmar orden de renta',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 4),
              Text(
                'Confirme el nombre del cliente para registrar la orden y generar el folio oficial.',
                style: TextStyle(fontSize: 13, color: Colors.grey.shade600),
              ),
              const SizedBox(height: 10),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                decoration: BoxDecoration(
                  color: const Color(0xFFFFF7ED),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: const Color(0xFFFDBA74)),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.handyman_outlined, size: 20, color: Color(0xFFF96302)),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        'Herramienta seleccionada: ${_herramientaElegida ?? _recomendacion!.eleccion}',
                        style: const TextStyle(
                          fontWeight: FontWeight.bold,
                          color: Color(0xFFC2410C),
                          fontSize: 13,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 12),
              TextField(
                controller: _clienteController,
                decoration: InputDecoration(
                  labelText: 'Nombre del Cliente',
                  hintText: 'Ej. Juan Pérez',
                  errorText: _errorCliente,
                  border: const OutlineInputBorder(),
                ),
                onChanged: (val) {
                  if (_errorCliente != null && val.trim().isNotEmpty) {
                    setState(() {
                      _errorCliente = null;
                    });
                  }
                },
              ),
              const SizedBox(height: 12),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  icon: const Icon(Icons.shopping_bag_outlined),
                  label: const Text('Confirmar renta'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFFF96302),
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 12),
                  ),
                  onPressed: _cargando ? null : _confirmarRenta,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _construirTicketFolio() {
    return Padding(
      padding: const EdgeInsets.only(top: 16.0),
      child: Card(
        color: Colors.green.shade50,
        shape: RoundedRectangleBorder(
          side: const BorderSide(color: Colors.green, width: 2),
          borderRadius: BorderRadius.circular(12),
        ),
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            children: [
              const Text(
                'Renta registrada',
                style: TextStyle(
                    color: Colors.green,
                    fontWeight: FontWeight.bold,
                    fontSize: 14),
              ),
              const SizedBox(height: 6),
              Text(
                _rentaRegistrada!.codigoFolio,
                style: const TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: Colors.green),
              ),
              Text(
                'Registro #${_rentaRegistrada!.folio}',
                style: TextStyle(fontSize: 12, color: Colors.green.shade800),
              ),
              const Divider(),
              Text('Cliente: ${_rentaRegistrada!.cliente}'),
              Text('Herramienta: ${_rentaRegistrada!.herramientaSugerida}'),
              Text('Duración: ${_rentaRegistrada!.duracionDias} días'),
              Text(
                'Costo Total: \$${_rentaRegistrada!.costoTotal.toStringAsFixed(2)} MXN',
                style: const TextStyle(fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 4),
              Text(
                'Estado: ${_rentaRegistrada!.estado}',
                style: const TextStyle(color: Colors.teal, fontWeight: FontWeight.w600),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
