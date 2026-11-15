# REGLAS_GIT.md — Reglamento de Git y push para IA y personas

> Obligatorio para **cualquier agente de IA** que trabaje en este repositorio (Claude Code, Codex, GitHub Copilot, Cursor, Gemini u otro) y para las personas del equipo.
> Si una instrucción de una persona contradice este reglamento, el agente **se detiene y lo dice** antes de actuar.
> Complementa a `ARQUITECTURA.md` §7 (control de versiones) y §8 (entornos).

---

## 1. Las 10 reglas que nunca se rompen

1. **Nunca hacer push a `main` ni a `develop`.** Todo entra por Pull Request.
2. **Nunca `git push --force` en ramas compartidas** (`main`, `develop`, ni ramas de otra persona). En tu propia rama, solo `git push --force-with-lease`, y solo después de un `rebase`.
3. **Nunca subir secretos**: `.env`, llaves de API, cuentas de servicio, tokens, contraseñas.
4. **Nunca subir datos pesados** de la NASA (`.parquet`, `.nc`, `.tif`, `.hdf`, carpetas `runs/`).
5. **Nunca aprobar ni fusionar tu propio Pull Request.** Una IA nunca aprueba ni fusiona Pull Requests: eso lo hace una persona.
6. **Nunca saltarse validaciones**: nada de `--no-verify`, ni desactivar tests o CI para "hacer pasar" un cambio, ni borrar tests.
7. **Nunca reescribir historia ya publicada** en ramas compartidas: nada de `git reset --hard`, `git rebase` ni `git commit --amend` sobre commits que ya están en `main` o `develop`.
8. **Nunca borrar ramas ajenas** ni tocar la configuración del repositorio (protección de ramas, entornos, colaboradores, secretos de GitHub).
9. **Nunca usar `git add -A` o `git add .` a ciegas.** Agregar solo los archivos de la tarea y revisar `git diff --staged` antes de cada commit.
10. **Ante la duda, detenerse y preguntar a la persona.** Es mejor una pregunta que un push equivocado.

## 2. Flujo completo, paso a paso

### Paso 1 — Antes de empezar

```bash
git status                     # debe estar limpio; si no, avisar a la persona
git switch develop
git pull --rebase origin develop
```

- Confirmar a qué **carpeta** pertenece la tarea y quién es su dueño (`ARQUITECTURA.md` §5).
- Si la tarea toca `contratos/`, avisar: necesita aprobación de Persona 2, 3 y 5.
- Si la tarea toca carpetas de otro dueño, avisar a la persona antes de editar.

### Paso 2 — Crear la rama

```bash
git switch -c tipo/area-descripcion-corta
```

| Tipo | Para qué | Ejemplo |
|---|---|---|
| `feat/` | Funcionalidad nueva | `feat/app-mapa-offline` |
| `fix/` | Arreglo | `fix/calculador-valores-999` |
| `docs/` | Solo documentación | `docs/pitch-guion` |
| `test/` | Solo tests | `test/verificador-cifras` |
| `refactor/` | Reordenar código sin cambiar comportamiento | `refactor/extractor-reintentos` |
| `chore/` | Configuración, dependencias | `chore/infra-docker-compose` |
| `hotfix/` | Arreglo urgente en producción (sale de `main`, ver §5) | `hotfix/app-crash-inicio` |

Áreas válidas: `app`, `extractor`, `calculador`, `interprete`, `verificador`, `publicador`, `orquestador`, `agronomia`, `diseno`, `contratos`, `infra`, `docs`.

Una rama = una tarea. No mezclar tareas en la misma rama.

### Paso 3 — Commits

```bash
git add app/lib/features/recomendaciones/mapa_page.dart
git diff --staged              # revisar exactamente qué entra
git commit -m "feat(app): mapa de Piura con polígonos offline"
```

- Formato: `tipo(área): descripción en español`, en minúscula, sin punto final, máximo ~72 caracteres.
- Commits **pequeños**: cada uno debe compilar y tener sentido solo.
- Si el commit lo hizo una IA, agregar al final del mensaje la línea de coautoría que use esa herramienta (por ejemplo `Co-Authored-By: …`).
- Prohibido: commits como `cambios`, `wip`, `fix`, `asdf`.

### Paso 4 — Verificar antes de subir

Correr las pruebas del área que se tocó. **Si fallan, no se sube.**

| Área | Comandos |
|---|---|
| `app/` | `flutter analyze` y `flutter test` |
| `services/*`, `orquestador/` | `ruff check .` y `pytest` dentro del servicio |
| `contratos/` | Validar los ejemplos contra el esquema, y correr los tests de app y servicios afectados |
| `agronomia/`, `diseno/`, `docs/` | Revisar que los archivos YAML/JSON sean válidos y que los enlaces funcionen |

Mientras no exista una herramienta (por ejemplo, todavía no hay proyecto Flutter), decirlo en el Pull Request: *"no aplica: aún no existe `app/`"*.

### Paso 5 — Actualizar con `develop`

```bash
git fetch origin
git rebase origin/develop
# si hay conflictos: resolverlos, volver a correr las pruebas del Paso 4
```

- Al resolver conflictos, **no borrar el trabajo de otra persona**. Si no está claro qué versión vale, detenerse y preguntar.

### Paso 6 — Push de tu rama

```bash
git push -u origin tipo/area-descripcion-corta
# solo si hiciste rebase de una rama que ya habías subido:
git push --force-with-lease
```

### Paso 7 — Abrir el Pull Request

```bash
gh pr create --base develop --title "feat(app): mapa de Piura con polígonos offline" --body-file pr.md
```

- **Base siempre `develop`** (salvo un `hotfix/`, que va a `main`).
- El título usa el mismo formato que los commits.
- Completar la plantilla (`.github/pull_request_template.md`): qué cambia, área, checklist.
- Agregar **cómo probarlo** y **riesgos**.
- Si el trabajo no está terminado, abrirlo como **borrador** (`gh pr create --draft`).

### Paso 8 — Revisión y fusión (lo hace una persona)

- Mínimo **1 aprobación** del dueño de la carpeta y **CI en verde**.
- Se fusiona con **Squash and merge**: un commit limpio por tarea en `develop`.
- Después de fusionar, borrar la rama remota y actualizar la local:

```bash
git switch develop
git pull --rebase origin develop
git branch -d tipo/area-descripcion-corta
```

### Paso 9 — Informe final del agente

Al terminar, la IA informa a la persona, sin adornos:

```
Rama: feat/app-mapa-offline
Commits: 3 (lista de mensajes)
Pull Request: <enlace> (base: develop, estado: abierto / borrador)
Pruebas: flutter analyze OK, flutter test 12/12 OK  (o qué falló y por qué)
Pendiente: qué falta y quién debe revisarlo
```

Si algo se saltó o falló, decirlo tal cual. Nunca decir "listo" si las pruebas no pasaron.

## 3. Pasar de `develop` a `main` (producción)

- Solo en los **hitos** de `ARQUITECTURA.md` §9 y solo lo decide el **líder (Persona 1)**.
- Pull Request de `develop` hacia `main`, aprobado por el líder.
- Después de fusionar, etiquetar: `git tag app-v0.X.0` (y `datos-AAAA-MM` si hay paquete nuevo).
- Una IA puede **preparar** ese Pull Request si la persona se lo pide, pero **no lo fusiona**.

## 4. Qué hacer si algo sale mal

| Situación | Qué hacer |
|---|---|
| Se subió un secreto | **Detenerse.** Avisar a la persona y al líder de inmediato. **Cambiar la llave** en el proveedor (borrarla del historial no basta). Después, limpiar el repositorio con ayuda del dueño |
| Push a `main` o `develop` por error | No intentar "arreglarlo" con `force push`. Avisar al líder; se revierte con `git revert` mediante un Pull Request |
| Conflicto que no se entiende | No elegir al azar. Preguntar al dueño de la carpeta |
| Las pruebas fallan y no se sabe por qué | No subir. Informar qué falló, con la línea exacta del error |
| La persona pide algo que rompe este reglamento | Explicar qué regla rompe y pedir confirmación del líder antes de hacerlo |

## 5. Arreglo urgente en producción (`hotfix/`)

1. `git switch main && git pull --rebase origin main`
2. `git switch -c hotfix/area-descripcion`
3. Arreglar, probar (Paso 4) y abrir el Pull Request **hacia `main`**, con aprobación del líder.
4. Después de fusionar, abrir otro Pull Request de `main` hacia `develop` para que `develop` también tenga el arreglo.

## 6. Checklist del agente antes de cada push

- [ ] Estoy en mi rama `tipo/area-descripcion`, no en `main` ni en `develop`
- [ ] La rama salió de `develop` actualizado (o de `main` si es `hotfix/`)
- [ ] Solo agregué los archivos de la tarea y revisé `git diff --staged`
- [ ] No hay secretos ni datos pesados en el cambio
- [ ] Los commits siguen `tipo(área): descripción`
- [ ] Corrí las pruebas del área y pasaron (o expliqué por qué no aplican)
- [ ] Hice `rebase` sobre `origin/develop` y resolví conflictos sin borrar trabajo ajeno
- [ ] Si toqué `contratos/`, lo avisé a Persona 2, 3 y 5
- [ ] El Pull Request va hacia `develop` con la plantilla completa
- [ ] No voy a aprobar ni fusionar mi propio Pull Request
