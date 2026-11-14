# app/ — App Flutter offline

**Responsable:** Persona 3 · **Suplente:** Persona 5

Lee el paquete mensual (SQLite) y muestra Mi zona, Recomendaciones y Tips sin internet.

- Entradas: `lib/main_dev.dart` (desarrollo) y `lib/main_prod.dart` (producción).
- Estructura por funcionalidad en `lib/features/` (ver ARQUITECTURA.md §4).
- `assets/paquete_demo/`: paquete incluido para la demo en modo avión.
- La app **no guarda llaves de APIs**: solo descarga archivos públicos.

Crear el proyecto aquí con `flutter create --org pe.rotacion --project-name rotacion_piura .`
