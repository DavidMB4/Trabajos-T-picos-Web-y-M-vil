import 'package:flutter/material.dart';
import 'screens/catalogo_screen.dart';
import 'screens/recomendador_screen.dart';
import 'screens/consulta_folio_screen.dart';
import 'screens/asistente_screen.dart';

void main() {
  runApp(const RentasApp());
}

class RentasApp extends StatelessWidget {
  const RentasApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Renta de Herramientas',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFFF96302),
          brightness: Brightness.light,
        ),
        scaffoldBackgroundColor: const Color(0xFFFBF8F3),
        useMaterial3: true,
      ),
      home: const MainNavigationScreen(),
    );
  }
}

class MainNavigationScreen extends StatelessWidget {
  const MainNavigationScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 4,
      child: Scaffold(
        appBar: AppBar(
          backgroundColor: const Color(0xFFF96302),
          foregroundColor: Colors.white,
          elevation: 1,
          title: const Text(
            'Renta de Herramientas',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white),
          ),
          bottom: PreferredSize(
            preferredSize: const Size.fromHeight(56),
            child: Container(
              width: double.infinity,
              color: Colors.white,
              child: TabBar(
                dividerColor: Colors.transparent,
                indicatorSize: TabBarIndicatorSize.tab,
                indicator: const BoxDecoration(
                  color: Color(0xFFF5F2EB),
                  border: Border(
                    bottom: BorderSide(
                      color: Color(0xFFF96302),
                      width: 3.0,
                    ),
                  ),
                ),
                labelColor: const Color(0xFFF96302),
                labelStyle: const TextStyle(fontWeight: FontWeight.bold),
                unselectedLabelColor: const Color(0xFF1E293B),
                unselectedLabelStyle: const TextStyle(fontWeight: FontWeight.w500),
                tabs: const [
                  Tab(
                    icon: Icon(Icons.psychology_outlined, size: 20),
                    text: 'Recomendador',
                  ),
                  Tab(
                    icon: Icon(Icons.handyman_outlined, size: 20),
                    text: 'Catálogo',
                  ),
                  Tab(
                    icon: Icon(Icons.receipt_long_outlined, size: 20),
                    text: 'Buscar Folio',
                  ),
                  Tab(
                    icon: Icon(Icons.chat_outlined, size: 20),
                    text: 'Asistente',
                  ),
                ],
              ),
            ),
          ),
        ),
        body: const SelectionArea(
          child: TabBarView(
            children: [
              RecomendadorScreen(),
              CatalogoScreen(),
              ConsultaFolioScreen(),
              AsistenteScreen(),
            ],
          ),
        ),
      ),
    );
  }
}
