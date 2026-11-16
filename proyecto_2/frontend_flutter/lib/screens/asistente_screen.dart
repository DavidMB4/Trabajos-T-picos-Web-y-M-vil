import 'package:flutter/material.dart';
import '../services/api_service.dart';

class AsistenteScreen extends StatefulWidget {
  const AsistenteScreen({super.key});

  @override
  State<AsistenteScreen> createState() => _AsistenteScreenState();
}

class _Mensaje {
  final String texto;
  final bool esUsuario;

  const _Mensaje({required this.texto, required this.esUsuario});
}

class _AsistenteScreenState extends State<AsistenteScreen> {
  final List<_Mensaje> _mensajes = [
    const _Mensaje(
      texto: 'Hola, soy el asistente de Renta de Herramientas. '
          'Puedo ayudarte a buscar tu folio, consultar el catálogo '
          'o explicarte cómo funciona el recomendador.',
      esUsuario: false,
    ),
  ];
  final TextEditingController _controlador = TextEditingController();
  final ScrollController _scroll = ScrollController();
  bool _cargando = false;

  Future<void> _enviar() async {
    final texto = _controlador.text.trim();
    if (texto.isEmpty) return;

    setState(() {
      _mensajes.add(_Mensaje(texto: texto, esUsuario: true));
      _cargando = true;
    });
    _controlador.clear();
    _irAlFinal();

    try {
      final resultado = await ApiService.preguntarAsistente(texto);
      setState(() {
        _mensajes.add(_Mensaje(
          texto: resultado['respuesta'] ?? 'Sin respuesta.',
          esUsuario: false,
        ));
      });
    } catch (e) {
      setState(() {
        _mensajes.add(_Mensaje(
          texto: 'No pude conectarme con el servidor. Verifica que Django esté corriendo.',
          esUsuario: false,
        ));
      });
    } finally {
      setState(() => _cargando = false);
      _irAlFinal();
    }
  }

  void _irAlFinal() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scroll.hasClients) {
        _scroll.animateTo(
          _scroll.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  void dispose() {
    _controlador.dispose();
    _scroll.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Expanded(
          child: ListView.builder(
            controller: _scroll,
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            itemCount: _mensajes.length,
            itemBuilder: (context, index) {
              final m = _mensajes[index];
              return _construirBurbuja(m);
            },
          ),
        ),
        if (_cargando)
          const Padding(
            padding: EdgeInsets.symmetric(vertical: 4),
            child: LinearProgressIndicator(
              color: Color(0xFFF96302),
              backgroundColor: Color(0xFFF5F2EB),
            ),
          ),
        _construirBarraTexto(),
      ],
    );
  }

  Widget _construirBurbuja(_Mensaje m) {
    final esUsuario = m.esUsuario;
    return Align(
      alignment: esUsuario ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 4),
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
        constraints: BoxConstraints(
          maxWidth: MediaQuery.of(context).size.width * 0.75,
        ),
        decoration: BoxDecoration(
          color: esUsuario ? const Color(0xFFF96302) : Colors.white,
          borderRadius: BorderRadius.only(
            topLeft: const Radius.circular(16),
            topRight: const Radius.circular(16),
            bottomLeft: Radius.circular(esUsuario ? 16 : 4),
            bottomRight: Radius.circular(esUsuario ? 4 : 16),
          ),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.07),
              blurRadius: 4,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: Text(
          m.texto,
          style: TextStyle(
            color: esUsuario ? Colors.white : const Color(0xFF1E293B),
            fontSize: 14,
          ),
        ),
      ),
    );
  }

  Widget _construirBarraTexto() {
    return Container(
      padding: const EdgeInsets.fromLTRB(12, 8, 12, 12),
      decoration: const BoxDecoration(
        color: Colors.white,
        border: Border(top: BorderSide(color: Color(0xFFE2E8F0))),
      ),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: _controlador,
              textInputAction: TextInputAction.send,
              onSubmitted: (_) => _enviar(),
              decoration: InputDecoration(
                hintText: 'Escribe tu pregunta...',
                hintStyle: const TextStyle(color: Color(0xFF94A3B8)),
                filled: true,
                fillColor: const Color(0xFFF5F2EB),
                contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(24),
                  borderSide: BorderSide.none,
                ),
              ),
            ),
          ),
          const SizedBox(width: 8),
          GestureDetector(
            onTap: _enviar,
            child: Container(
              padding: const EdgeInsets.all(10),
              decoration: const BoxDecoration(
                color: Color(0xFFF96302),
                shape: BoxShape.circle,
              ),
              child: const Icon(Icons.send, color: Colors.white, size: 20),
            ),
          ),
        ],
      ),
    );
  }
}
