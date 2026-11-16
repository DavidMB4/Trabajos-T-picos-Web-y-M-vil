import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import '../models/herramienta.dart';
import '../models/recomendacion.dart';
import '../models/renta.dart';

class ApiService {
  static String baseUrl = 'http://127.0.0.1:8000';

  static void setBaseUrl(String newUrl) {
    baseUrl = newUrl.endsWith('/') ? newUrl.substring(0, newUrl.length - 1) : newUrl;
  }

  // Mensajes de error sencillos
  static String formatearError(dynamic e) {
    final str = e.toString();
    if (str.contains('ClientException') ||
        str.contains('Failed to fetch') ||
        str.contains('Connection refused') ||
        str.contains('SocketException') ||
        str.contains('NetworkException')) {
      return 'No se pudo conectar con el servidor. Inténtelo más tarde.';
    }
    if (str.contains('TimeoutException')) {
      return 'El servidor tardó en responder. Por favor intente de nuevo.';
    }
    if (str.startsWith('Exception: ')) {
      return str.substring(11);
    }
    return 'Ocurrió un problema de conexión. Inténtelo más tarde.';
  }

  /// Obtener catalogo de herramientas
  static Future<List<Herramienta>> getCatalogo({String? categoria}) async {
    try {
      final uri = Uri.parse('$baseUrl/api/catalogo/${categoria != null ? '?categoria=$categoria' : ''}');
      final response = await http.get(uri).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final data = json.decode(utf8.decode(response.bodyBytes));
        final List lista = data['catalogo'] as List? ?? [];
        return lista.map((item) => Herramienta.fromJson(item as Map<String, dynamic>)).toList();
      } else {
        throw Exception('No se pudo obtener el catálogo. Inténtelo más tarde.');
      }
    } catch (e) {
      debugPrint('Error getCatalogo: $e');
      throw Exception(formatearError(e));
    }
  }

  /// Pide recomendacion segun el trabajo
  static Future<Recomendacion> pedirRecomendacion(Map<String, dynamic> trabajo) async {
    try {
      final uri = Uri.parse('$baseUrl/api/recomendar/');
      final response = await http.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: json.encode(trabajo),
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final data = json.decode(utf8.decode(response.bodyBytes));
        return Recomendacion.fromJson(data as Map<String, dynamic>);
      } else {
        final error = json.decode(utf8.decode(response.bodyBytes));
        throw Exception(error['error'] ?? 'No se pudo procesar la recomendación. Inténtelo más tarde.');
      }
    } catch (e) {
      debugPrint('Error pedirRecomendacion: $e');
      throw Exception(formatearError(e));
    }
  }

  /// Registra renta y generar folio
  static Future<Renta> registrarRenta(Map<String, dynamic> rentaData) async {
    try {
      final uri = Uri.parse('$baseUrl/api/rentas/');
      final response = await http.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: json.encode(rentaData),
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode == 201) {
        final data = json.decode(utf8.decode(response.bodyBytes));
        return Renta.fromJson(data as Map<String, dynamic>);
      } else {
        final error = json.decode(utf8.decode(response.bodyBytes));
        throw Exception(error['error'] ?? 'No se pudo registrar la renta. Inténtelo más tarde.');
      }
    } catch (e) {
      debugPrint('Error registrarRenta: $e');
      throw Exception(formatearError(e));
    }
  }

  /// Consulta un folio existente 
  static Future<Renta> consultarFolio(dynamic folio) async {
    try {
      final folioStr = folio.toString().trim();
      final uri = Uri.parse('$baseUrl/api/rentas/$folioStr/');
      final response = await http.get(uri).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final data = json.decode(utf8.decode(response.bodyBytes));
        return Renta.fromJson(data as Map<String, dynamic>);
      } else if (response.statusCode == 404) {
        throw Exception('No se encontró ninguna renta con el folio $folioStr.');
      } else {
        throw Exception('No se pudo consultar el folio. Inténtelo más tarde.');
      }
    } catch (e) {
      debugPrint('Error consultarFolio: $e');
      throw Exception(formatearError(e));
    }
  }
}
