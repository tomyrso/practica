# Demo: Compound Engineering en acción

## El concepto

Compound Engineering propone que **cada unidad de trabajo debería hacer que la siguiente sea más fácil**. En vez de resolver el mismo tipo de problema desde cero cada vez, se documenta la solución y se reutiliza automáticamente.

El ciclo es:
```text
Implementar → Documentar (/workflows:compound) → La próxima vez, Claude encuentra el doc
```
---

## El proyecto

Un pequeño proyecto Python con dos archivos:
- `validators.py` — funciones de validación
- `tests.py` — tests con unittest

Convención del proyecto: cada validator retorna `(bool, str)` — un booleano indicando si es válido y un string explicando por qué.

---

## Acto 1 — Sin conocimiento previo

**Tarea:** agregar `validate_email(value) -> (bool, str)`

### Lo que hizo Claude al planificar (`/workflows:plan`)

Lanzó dos subagentes en paralelo:

**`repo-research-analyst`** → leyó el proyecto, encontró el CLAUDE.md, entendió las convenciones.

**`learnings-researcher`** → buscó en `docs/solutions/` si había soluciones documentadas anteriormente.

Resultado del `learnings-researcher`:
```bash
No docs/solutions/ directory exists in this location.
```
Claude tuvo que investigar el proyecto completamente desde cero para armar el plan.

### Implementación (`/workflows:work`)

- Escribió `validate_email` con checks secuenciales: vacío → espacios → `@` → parte local → punto en dominio
- Escribió 6 tests cubriendo cada regla
- Todos los tests pasaron

```bash
Ran 6 tests in 0.000s — OK
```
---

## El paso clave: `/workflows:compound`

Después de implementar, se corrió `/workflows:compound`. Esto lanzó 5 subagentes en paralelo para documentar lo aprendido:

| Subagente | Qué hizo |
|---|---|
| Context Analyzer | Identificó el tipo de problema y extrajo el frontmatter YAML |
| Solution Extractor | Leyó el código y documentó el patrón paso a paso |
| Related Docs Finder | Confirmó que no había docs previas |
| Prevention Strategist | Documentó errores comunes y edge cases |
| Category Classifier | Determinó la categoría y nombre del archivo |

El resultado fue un único archivo:

**`docs/solutions/patterns/input-validator-bool-str-pattern.md`**

Contenido relevante del documento generado:
```markdown
## Template para nuevos validators

def validate_X(value: str) -> tuple[bool, str]:
    if not value:
        return False, "X cannot be empty"
    # checks...
    return True, "Valid X"

## Ejemplo: validate_phone

def validate_phone(value: str) -> tuple[bool, str]:
    if not value:
        return False, "Phone cannot be empty"
    digits = "".join(c for c in value if c.isdigit())
    if len(digits) < 10:
        return False, "Phone must have at least 10 digits"
    ...
    return True, "Valid phone number"
```

---

## Acto 2 — Con conocimiento documentado

**Tarea:** agregar `validate_phone(value) -> (bool, str)`

### Lo que hizo Claude al planificar (`/workflows:plan`)

Mismos dos subagentes en paralelo que en el Acto 1.

Resultado del `learnings-researcher` esta vez:
```text
Found: docs/solutions/patterns/input-validator-bool-str-pattern.md

- Patrón (bool, str) documentado
- Template para nuevos validators
- Ejemplo de validate_phone ya escrito
- Errores comunes y edge cases a testear
```
Claude no tuvo que investigar nada. El plan se armó directamente desde el documento encontrado, incluyendo la implementación completa y los tests sugeridos.

### Implementación (`/workflows:work`)

- Reutilizó el template documentado
- Escribió `validate_phone` con el enfoque de digit-stripping (acepta `+1 (800) 555-1234`, `800-555-1234`, etc.)
- Escribió 5 tests
- Todos los tests pasaron (6 de email + 5 de teléfono)

```bash
Ran 11 tests in 0.000s — OK
```
---

## El contraste

| | Acto 1 | Acto 2 |
|---|---|---|
| `learnings-researcher` | "No docs/solutions found" | "Found: input-validator-bool-str-pattern.md" |
| Fase de investigación | Explorar el proyecto desde cero | Lookup directo en docs/solutions/ |
| Plan incluyó | Lo que descubrió investigando | Template + ejemplo + edge cases ya documentados |
| Tiempo de planificación | Investigar convenciones, patrones, estructura | Ninguno — todo estaba documentado |

---

## La estructura de archivos al final

```text
compound-demo/
├── CLAUDE.md
├── validators.py               ← validate_email + validate_phone
├── tests.py                    ← 11 tests pasando
└── docs/
    ├── plans/
    │   ├── 2026-02-20-feat-email-validator-plan.md   ← Acto 1
    │   └── 2026-02-20-feat-phone-validator-plan.md   ← Acto 2
    └── solutions/
        └── patterns/
            └── input-validator-bool-str-pattern.md   ← generado por /workflows:compound
```
---

## Por qué importa

La primera vez que se resuelve un problema, hay investigación. La segunda vez, hay un lookup. La tercera vez, hay un lookup de 2 segundos.

Si el equipo tiene 10 personas y cada una documenta lo que aprende, el conocimiento se acumula para todos. Eso es compound engineering.
