import 'package:flutter_test/flutter_test.dart';
import 'package:rentas_herramientas_app/main.dart';

void main() {
  testWidgets('Verifica que la app cargue la barra de navegación y título',
      (WidgetTester tester) async {
    await tester.pumpWidget(const RentasApp());

    expect(find.text('Renta de Herramientas'), findsOneWidget);
    expect(find.text('Recomendador'), findsOneWidget);
    expect(find.text('Catálogo'), findsOneWidget);
    expect(find.text('Buscar Folio'), findsOneWidget);
  });
}
