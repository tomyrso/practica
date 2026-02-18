# Presentación Claude Code
## Claude.md
### ¿Qué es y dónde vive?
Un archivo markdown con instrucciones que Claude Code carga automáticamente al iniciar una sesión. Funciona como la "memoria persistente" del proyecto — todo lo que Claude debería saber siempre sobre cómo trabajar en este contexto.

Se puede tener a nivel global (aplica a todos los proyectos) o a nivel proyecto (aplica solo al proyecto actual):

Si se quiere disponible para todos los proyectos:
`~/.claude/CLAUDE.md`

Si se quiere disponible para el proyecto actual nada más:
`./CLAUDE.md` (en la raíz del proyecto)

También se puede poner dentro de `.claude/CLAUDE.md` en el proyecto. Claude Code carga todos los niveles y los combina, con el más específico (proyecto) tomando precedencia sobre el global.

### Formato de un CLAUDE.md
No tiene un formato estricto — es markdown libre. Pero la convención es organizar por secciones claras. Contenido típico incluye:
- Descripción del proyecto y tech stack
- Reglas críticas (estilo de código, testing, seguridad)
- Estructura de archivos del proyecto
- Patrones clave y convenciones
- Variables de entorno necesarias
- Comandos disponibles
- Workflow de Git

Lo importante es que sea conciso y actualizado. Instrucciones desactualizadas hacen que Claude tome decisiones incorrectas.

### Ejemplo
Un CLAUDE.md a nivel proyecto:
````
# Mi Proyecto

## Project Overview
API REST en Node.js + Express con PostgreSQL.

## Critical Rules
- No hardcodear secretos — usar variables de entorno
- TDD: escribir tests primero
- Conventional commits: feat:, fix:, refactor:, docs:, test:
- Nunca commitear directo a main

## File Structure
src/
|-- app/          # Express app setup
|-- routes/       # API endpoints
|-- services/     # Business logic
|-- models/       # Database models
|-- utils/        # Helpers

## Key Patterns
- Todas las respuestas de API siguen el formato { success, data, error }
- Input validation con Zod en cada endpoint
- Error handling con try/catch en cada controller

## Environment Variables
DATABASE_URL=
API_KEY=
````

Un CLAUDE.md a nivel usuario (~/.claude/CLAUDE.md):
````
# Preferencias Globales

## Filosofía
- TDD siempre
- Archivos chicos (200-400 líneas max)
- Organizar por feature, no por tipo

## Estilo
- No emojis en código ni comentarios
- Inmutabilidad — nunca mutar objetos o arrays
- Validar inputs en boundaries del sistema

## Git
- Conventional commits
- Nunca force push a main
- PRs requieren review
````
## Skills
### ¿Qué son y donde viven?
Técnicamente son archivos markdown ".md"

Se añade un directory con un "SKILL.md". Donde se agreguen depende de donde uno las quiere disponibles, si global o localmente. 

Si se quiere disponible para todos los proyectos:  
` ` `~/.claude/skills/<skill-name>/SKILL.md` ` `    

Si se quiere disponible para el proyecto actual nada más:  
` ` `.claude/skills/<skill-name>/SKILL.md` ` `

### Formato de una Skill
Toda skill es esencialmente:
```text
---
name: my-skill
description: Lo que hace la skill
---
Las instrucciones de la skill
```
Solo los campos name y description son obligatorios, pero hay muchas más opciones para modificar el comportamiento. Campos alternativos, que se añaden en el frontmatter, son:
- description: lo que hace la skill y cuando usarla. Claude lo utiliza para decidir si usarla o no.
- argument-hint: pista para indicar "arguments" esperados como [filename][format]
- disable-model-invocation: seleccionar `true` para que claude no la pueda usar automaticamente.
- user-invocable: seleccionar `false` para esconder del menu `/` así el usuario no la puede invocar.
- allowed-tools: tools claude podrá usar sin permiso
- model: modelo a usar con esta skill
- context: seleccionar `fork` para que corra en un forked subagent context
- agent: cual subagente usar cuando `context:fork` 
- hooks: hooks atados a mientras corra la skill

El cuerpo del markdown, luego del frontmatter contiene las instrucciones de la skill. No hay restricciones, pero se recomienda instrucciones paso a paso, ejemplos de inputs/outputs o "edge cases" comunes.
### String Substitutions
Una skill admite "string substitution" para valores dinamicos en el contenido de la skill, mediante el input????
- $ARGUMENTS: todos los argumentos que se le dan a la skill al momento de invocarla

### Ejemplo
Veamos en detalle la Skill "deep-research":
````
---
name: deep-research
description: Research a topic thoroughly in the codebase
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:

1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
4. Note any patterns or potential issue
````
***********Será necesario un ejemplo de vdd onda verlo en accion?**************

### ¿Cuando es invocada una Skill?
Depende. Automaticamente, Claude Code cada vez que tiene una tarea en sus manos, lee la description de las Skill para ver si sería útil o no y procede a decidir si activarla o no. Se pueden llamar manualmente tambien, con `/skill-name`.  
Una buena practica para skills, es que en la practica el llamado automatico no puede ser tan certero como a uno le gustaria, por lo que se puede crear un Hook (como `UserPromptSubmit`) para que Claude analice y active las skills más confiablemente.

### ¿Tienen prioridad sobre otras instrucciones?
¿Qué sucede si una skill dice X, pero el CLAUDE.md dice Y sobre un mismo tema? En general no hay una jerarquía clara y definida. 

Una especie de jerarquia podria ser:

  1. Hooks            → barrera "física", imposible de ignorar
  2. Usuario en chat  → instrucción directa
  3. Skills           → prompt inyectado en el momento
  4. CLAUDE.md local  → guía del proyecto
  5. CLAUDE.md global → guía general

Es importante tener en mente que el CLAUDE.md son instrucciones de texto que Claude lee, interpreta e intenta seguir, pero que puede "ignorar" si hay contexto conflictivo. Y que a medida que se llena el contexto claude puede ir "olvidando" lo que está muy atras y le va dando prioridad a lo más reciente.

## Hooks
### ¿Que son y donde viven?
Es un archivo .json.  
Hay un par de maneras distintas para poder crear un hook. Editando directamente el .json, usar el comando interactivo, o pedirle a claude code que lo haga por ti. La segunda suele ser mas facil y rapida. Ya que nos pedira cuando se activa el hook, el matcher, describir el comando a ejecutar.  
Es importante saber, los tipos de eventos: (lista acotada de ejemplos)
- SessionStart: cuando la sesion comuenza
- PreToolUse: antes de que una tool, una accion concreta, se ejecute.
- PostToolUse: luego de que una tool se ejecute
- Notification: cuando claude code envia una notificacion.
- PreCompact: antes que se compacte el contexto.  

Los matcher, que son un filtro que indica que tool activa el hook.

Si se quiere disponible para todos los proyectos:
~/.claude/settings.json

Si se quiere disponible para el proyecto actual nada más:
.claude/settings.json

### Formato de un Hook
### Ejemplo
Desde correr shell commands automaticamente, a formatear codigo, enviar notificaciones, validar comandos o forzar ciertas reglas.
## Subagents
Son agentes que se encargan de tipos específicos de tareas y que corren en su context independiente.  

Los subagentes estan definidos en archivos markdown con YAML frontmatter. Se pueden crear manualmente o con el comando `/agents`.  

Se pueden crear a nivel usuario en `~/.claude/agents/` o nivel del proyecto actual en`.claude/agents/`.  

### Formato de un Subagent
Si se elige hacerlo con ayuda, uno puede poner un prompt que describa la mision del agente como por ejemplo: "A code improvement agent that scans files and suggests improvements
for readability, performance, and best practices. It should explain
each issue, show the current code, and provide an improved version."  
Luego se elige los tools a los cuales tendrá acceso. Hay distintos tipos:
- Read-only tools como Glob, Grep, Read, WebFetch, WebSearch.
- Edit tools como Edit, Write, NotebookEdit.
- Execution tools como Bash.
- Otras como Skill, TaskCreate, TaskGet, TaskUpdate, TaskList, ToolSearch.

Luego se selecciona el modelo que usará y tendremos un agente listo para usarlo. Por otro lado, si se quisiera hacer manualmente, se sigue la misma estructura que para una skill. Se crea un archivo .md como el siguiente:
`````
---
name: identificador unico
description: cuando usarlo. Claude lo utiliza para decidir si usarlo o no. 
model: un modelo distinto o el mismo que en el main
---

Descripcion e instrucciones especificas del subagente
`````
Donde los campos disponibles en el frontmatter, a parte de name y description, son: 
- tools: Los tools que el subagente puede utilizar
- disallowedTools: tools a rechazar
- model: modelo a usar, `sonnet`, `opus`, ...
- permissionMode: `default`, `acceptEdits`, `delegate`, `dontAsk`, `bypassPermissions`, or `plan`.*********
- maxTurns: numero maximo de turns antes que pare.
- skills: las skills a cargar con el subagente.
- hooks: hooks atados a mientras corra el subagente.

### Ejemplo
`````
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
`````
## Plugins
### ¿Qué son y dónde viven?
Paquetes que agrupan skills, hooks, agents y más para distribuir. 

Un plugin vive en un directorio `.claude-plugin/` que contiene un archivo `plugin.json` con el manifest del plugin.

Los plugins instalados se guardan en:
`~/.claude/plugins/`

Se habilitan y deshabilitan en `~/.claude/settings.json` bajo `enabledPlugins`:
```json
{
  "enabledPlugins": {
    "my-plugin@marketplace": true
  }
}
```

### Cómo instalar un Plugin
Hay 3 formas:
- Via marketplace: `claude plugin marketplace add <url-del-repo>`
- Via CLI: `claude plugin install <nombre>@<marketplace>`
- Via menú interactivo: `/plugins` dentro de Claude Code

### Formato de un Plugin (plugin.json)
Todo plugin necesita un `.claude-plugin/plugin.json`. La estructura básica es:
```json
{
  "name": "mi-plugin",
  "description": "Lo que hace el plugin",
  "version": "1.0.0",
  "author": {
    "name": "Tu Nombre"
  },
  "skills": ["./skills/"],
  "agents": ["./agents/planner.md", "./agents/reviewer.md"],
  "commands": ["./commands/"]
}
```

Reglas importantes del validador:
- `version` es obligatorio — sin este campo, la instalación falla
- Todos los campos de componentes (skills, agents, commands) deben ser arrays, nunca strings
- `agents` requiere rutas explícitas a archivos (no acepta directorios como `"./agents/"`)
- NO agregar "hooks" al manifest — Claude Code carga `hooks/hooks.json` automáticamente por convención. 

Para validar: `claude plugin validate .claude-plugin/plugin.json`

### Ejemplo
Un plugin simple:
```json
{
  "name": "my-first-plugin",
  "description": "A greeting plugin to learn the basics",
  "version": "1.0.0",
  "author": {
    "name": "Tomas Rojas"
  }
}
```

Un plugin más completo con skills y agents:
```json
{
  "name": "everything-claude-code",
  "version": "1.2.0",
  "description": "Colección completa de configs para Claude Code",
  "skills": ["./skills/", "./commands/"],
  "agents": [
    "./agents/architect.md",
    "./agents/code-reviewer.md",
    "./agents/planner.md"
  ]
}
```
## Interesting Repositories
### Superpowers
Un plugin para Claude Code que **impone un workflow obligatorio** de desarrollo. No sugiere buenas prácticas — las fuerza. Es una colección de 14 skills, 1 agente, y un hook de sesión que trabajan en conjunto para que Claude Code siga un proceso disciplinado: TDD, test driven development, debugging sistemático, y verificación antes de declarar algo como terminado.

Se instala como plugin:
```text
claude plugin marketplace add obra/superpowers-marketplace
claude plugin install superpowers@superpowers-marketplace
```
#### Las 14 Skills

1. **using-superpowers** — Skill introductoria que establece la regla fundamental: si hay un 1% de chance de que una skill aplique, Claude debe invocarla. 

2. **brainstorming** — Antes de cualquier trabajo creativo (features, componentes, cambios de comportamiento). Transforma ideas en diseños.

3. **writing-plans** — Dado un diseño validado, crear un plan de implementación con tareas pequeñas pero detalladas.

4. **test-driven-development** — RED-GREEN-REFACTOR enforcment. Obligatorio: escribir test que falle, escribir código mínimo para que pase, refactor. Si el test pasa de entrada, algo está mal.

5. **executing-plans** — Para ejecutar un plan en una sesión separada. Se ejecutan en batches de 3 tareas, con checkpoints de review humano.

6. **subagent-driven-development** — Para ejecutar planes en la sesión actual. Lanza un subagente fresco por tarea, seguido de review en 2 etapas.

7. **systematic-debugging** — Ante cualquier bug o comportamiento inesperado. Son 4 fases secuenciales: investigar la causa de raíz, analizar patrones, formular hipótesis (una a la vez), implementar los cambios. Si fallan 3+ intentos: cuestionar la arquitectura.

8. **requesting-code-review** — Despacha el subagente code-reviewer con los SHAs del trabajo hecho. Clasifica issues en Critical, Important, Minor.

9. **receiving-code-review** — Cómo recibir feedback del review. Exige: leer, entender, verificar contra el codebase, evaluar, y recién ahí responder o hacer pushback.

10. **dispatching-parallel-agents** — Cuando hay 2+ problemas independientes. Un agente por dominio de problema, investigación en paralelo, integrar resultados al final.

11. **using-git-worktrees** — Crear worktrees aislados para feature work. Detecta directorio, verifica que esté en .gitignore, crea branch, corre setup del proyecto, y verifica baseline limpio.

12. **finishing-a-development-branch** — Cuando la implementación está completa y los tests pasan. Presenta exactamente 4 opciones: merge local, crear PR, dejar la branch, o descartar el trabajo.

13. **verification-before-completion** — Antes de declarar que algo está terminado. Exige correr el comando de verificación, leer el output completo, confirmar que el output soporta el claim. 

14. **writing-skills** — TDD aplicado a la creación de skills. Escribir un escenario de presión sin la skill (RED), escribir la skill mínima (GREEN), cerrar loopholes encontrados (REFACTOR).

#### El workflow que impone
Todo empieza con un hook. Superpowers registra un hook de tipo `SessionStart` que se dispara cada vez que una sesión comienza, se resume, se limpia o se compacta. El hook ejecuta un script que lee la skill `using-superpowers` y la inyecta en el system prompt envuelta en tags `<EXTREMELY_IMPORTANT>`. Esto significa que Claude ve las reglas fundamentales **antes de cualquier mensaje del usuario**.

La regla central que establece esa skill es:
> "IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT."

Y baja el umbral al mínimo: si hay un 1% de probabilidad de que una skill aplique, hay que invocarla. No hay excepciones.

#### Cómo fuerza el workflow de desarrollo de features
```text
Usuario pide una feature
        ↓
brainstorming → diálogo, explorar enfoques, validar diseño
        ↓
using-git-worktrees → branch aislado, setup, tests baseline
        ↓
writing-plans → plan con tareas de 2-5 min, código completo, TDD
        ↓
Elegir modo de ejecución:
  ├─ subagent-driven-development → subagente por tarea + review 2 etapas
  └─ executing-plans → batches de 3 tareas con checkpoints humanos
        ↓
Cada tarea individual sigue: test-driven-development (red-green-refactor)
        ↓
requesting-code-review → después de cada tarea o batch
        ↓
receiving-code-review → si hay feedback, procesarlo con rigor
        ↓
verification-before-completion → evidencia de que todo funciona
        ↓
finishing-a-development-branch → merge / PR / keep / discard
```
#### Cómo fuerza el workflow de debugging
```text
Usuario reporta un bug
        ↓
systematic-debugging →
  Fase 1: Investigar causa raíz (leer error, reproducir, trazar data flow)
  Fase 2: Analizar patrones (buscar código que sí funciona, comparar)
  Fase 3: Hipótesis (una sola, testear mínimamente, verificar)
  Fase 4: Implementar (test que falle → fix mínimo → verificar)
        ↓
Si fallan 3+ intentos → cuestionar la arquitectura
        ↓
verification-before-completion → evidencia fresca
        ↓
requesting-code-review → validar el fix
```
#### Los mecanismos de enforcement
Superpowers no confía en que Claude "quiera" seguir el proceso. Usa múltiples capas para hacerlo inevitable:

**1.** Reglas absolutas, no negociables, repetidas en cada skill relevante:
- "No production code without a failing test first"
- "No fixes without root cause investigation first"
- "No completion claims without fresh verification evidence"

**2. Tablas de racionalización** — Cada skill anticipa las excusas que Claude podría usar para saltarse el proceso y las contra-argumenta explícitamente:

| Excusa | Realidad |
|--------|----------|
| "Es muy simple para testear" | El código simple se rompe. El test tarda 30 segundos. |
| "Testeo después" | Un test que pasa de entrada no prueba nada. |
| "Ya lo probé manualmente" | Ad-hoc no es sistemático. No queda registro. |
| "Borrar X horas de trabajo es un desperdicio" | Falacia de costo hundido. Código no verificado es deuda técnica. |
| "TDD me hace más lento" | TDD es más rápido que debuggear. |

**3. Red Flags** — Listas explícitas de pensamientos que indican que Claude está racionalizando. Si aparece alguno, debe detenerse y volver al proceso:
- "Esto es solo una pregunta simple" → Las preguntas son tareas.
- "Necesito más contexto primero" → El check de skills viene ANTES de clarificar.
- "Esto no cuenta como tarea" → Acción = tarea.
- "Me acuerdo de esta skill" → Las skills evolucionan; leer la versión actual.
- "Hago solo esta cosita primero" → Checkear ANTES de hacer cualquier cosa.

**4. Review de 2 etapas** — En subagent-driven-development, cada tarea pasa por dos revisores en orden obligatorio:
1. Spec compliance (¿el código hace lo que el plan dice?)
2. Code quality (¿el código está bien construido?)
No se puede avanzar hasta que ambos aprueben. Si el código no cumple el spec, la calidad es irrelevante.

**5. Verificación antes de claims** — La skill `verification-before-completion` prohíbe declarar que algo está terminado sin evidencia fresca. Nada de "debería funcionar" o "estoy seguro" — se exige correr el comando, leer el output, y confirmar que el output soporta el claim.

**6. Invocación recursiva entre skills** — Las skills se referencian entre sí con `REQUIRED SUB-SKILL`. Por ejemplo, `writing-plans` exige usar `executing-plans` para implementar. Esto crea una cadena de dependencias que fuerza el orden del workflow.
### Everything Claude Code
Un plugin que toma el enfoque opuesto a Superpowers. Donde Superpowers impone un workflow más estricto, Everything Claude Code es una colección de herramientas para todo el ciclo de desarrollo. No fuerza un orden, sino que ofrece agentes, skills, comandos y hooks que se pueden usar según se necesiten, como una caja de herramientas.

La otra diferencia fundamental: Everything Claude Code "aprende". Tiene un sistema de aprendizaje continuo que captura patrones de cada sesión y los refina automáticamente.

#### Qué incluye
En total: 12 agentes, 24 skills, 23 comandos, 8 archivos de rules, y hooks. Algunos destacados:

**Agentes** (12 total) — cada uno especializado en un dominio:
- `planner` — descompone features complejas en fases
- `architect` — decisiones de diseño, patrones, trade-offs de escalabilidad
- `tdd-guide` — especialista en TDD, enforcea red-green-refactor y 80%+ de coverage
- `code-reviewer` — review de calidad, seguridad y performance post-código
- `security-reviewer` — detección de vulnerabilidades, OWASP Top 10, detección de secretos
- `build-error-resolver` — arregla errores de build/TypeScript con diffs mínimos
- `refactor-cleaner` — limpieza de código muerto, exports sin usar, dependencias innecesarias
- `doc-updater` — genera y mantiene documentación y codemaps
- `database-reviewer` — especialista en PostgreSQL: optimización de queries, seguridad RLS

**Skills** (24 total) — organizadas por dominio:
- Workflow: `tdd-workflow`, `verification-loop`, `continuous-learning-v2`, `strategic-compact`
- Frontend: `frontend-patterns` (React, hooks, performance)
- Backend: `backend-patterns` (APIs, repository pattern, caching)
- Go: `golang-patterns`, `golang-testing`
- Java/Spring: `springboot-patterns`, `springboot-security`, `springboot-tdd`
- Base de datos: `postgres-patterns`, `clickhouse-io`
- Seguridad: `security-review`

**Comandos** (23 total) — acceso rápido a workflows:
- `/tdd`, `/plan`, `/code-review`, `/build-fix`, `/e2e` — los core del desarrollo
- `/learn`, `/evolve`, `/instinct-status`, `/instinct-export` — sistema de aprendizaje
- `/verify`, `/checkpoint`, `/eval` — verificación continua
- `/go-test`, `/go-review`, `/go-build` — específicos de Go
- `/update-docs`, `/update-codemaps` — documentación

**Rules** (8 archivos) — guías que siempre se siguen, organizadas por tema: seguridad, estilo de código, testing (80% coverage mínimo), git workflow (conventional commits), cuándo delegar a subagentes, performance, y patrones (inmutabilidad, DRY, YAGNI).

**Hooks** — automatizaciones que corren en eventos:
- Auto-format con Prettier después de cada edit en archivos JS/TS
- Detección de `console.log` en archivos modificados
- Persistencia de contexto: guarda estado antes de compactar y lo recarga al iniciar sesión
- Bloqueo de dev servers fuera de tmux
- Type checking automático con TypeScript

#### Patrón de diseño
Cada agente tiene un **scope declarativo** (qué tools puede usar) y **responsabilidades acotadas**. Por ejemplo, `build-error-resolver` solo arregla errores de build — no refactoriza ni agrega features. `refactor-cleaner` solo limpia código muerto — no arregla bugs. Esta separación evita que un agente se pase de su alcance. Las skills cubren múltiples lenguajes y frameworks (no solo JavaScript), lo que lo hace útil para equipos con stacks diversos.

#### Sistema de aprendizaje continuo (Instincts)
La innovación más interesante. En vez de skills estáticas que nunca cambian, Everything Claude Code puede **aprender de cada sesión**:

1. **Captura** — hooks de PreToolUse y PostToolUse registran todas las acciones (100% de cobertura)
2. **Análisis** — un agente Haiku en background analiza los patrones capturados
3. **Creación de instincts** — genera "instincts" atómicos con un score de confianza (0.3 a 0.9)
4. **Evolución** — cuando se acumulan instincts relacionados, `/evolve` los agrupa automáticamente en skills

Cada instinct tiene: un trigger (cuándo aplica), una acción (qué hacer), evidencia (de dónde vino), y un dominio (code-style, testing, git, debugging, etc.). Se pueden exportar con `/instinct-export` e importar con `/instinct-import` para compartir aprendizajes entre miembros del equipo.

#### Comparación con Superpowers

| | Superpowers | Everything Claude Code |
|---|---|---|
| **Filosofía** | Workflow rígido obligatorio | Modular, flexible, mix-and-match |
| **Foco** | TDD + debugging + planning | Ciclo completo + aprendizaje |
| **Agentes** | 1 (code-reviewer) | 12 especializados por dominio |
| **Skills** | 14 enfocadas en proceso | 24 cubriendo múltiples lenguajes |
| **Comandos** | Pocos, con secuencia estricta | 23, encadenables libremente |
| **Innovación** | Anti-racionalización, Iron Laws | Aprendizaje continuo con instincts |
| **Estado** | Sin persistencia entre sesiones | Aprende y persiste contexto |
| **Lenguajes** | Agnóstico (solo proceso) | JS/TS, Go, Java/Spring, PostgreSQL |

No son mutuamente excluyentes — se podrían usar ambos. Superpowers para la disciplina del proceso, Everything Claude Code para las herramientas especializadas y el aprendizaje.

### Compound Engineering
Un plugin se define en que: **cada unidad de trabajo de ingeniería debería hacer que la siguiente sea más fácil, no más difícil**. En vez de acumular deuda técnica con cada feature, se acumula conocimiento documentado. La inversión propuesta es 80% planning y review, 20% ejecución.

La primera vez que se resuelve un problema, digamos ocurren 30 minutos de investigación. Se documenta en `docs/solutions/`. La próxima vez que aparece → 2 minutos de lookup. Eso es "compound engineering".

#### El workflow core
Un ciclo de 4 pasos que se repite:
```text
/workflows:plan → /workflows:work → /workflows:review → /workflows:compound → Repeat
```

| Comando | Qué hace |
|---------|----------|
| `/workflows:plan` | Investiga el codebase + docs externos, crea un plan detallado en `docs/plans/` |
| `/workflows:work` | Ejecuta el plan: crea branch, trackea progreso con todos, commits incrementales |
| `/workflows:review` | Lanza 10+ agentes especializados **en paralelo** que revisan desde distintos ángulos |
| `/workflows:compound` | Documenta la solución en `docs/solutions/` para referencia futura |

El paso clave es `compound` — lo que diferencia a este plugin de los demás. No es solo codear y mergear, es cerrar el loop documentando lo aprendido.

#### Qué incluye
En total: 29 agentes, 22 comandos, 19 skills, 1 MCP server (Context7 para docs de frameworks).

**Agentes** (29 total) — organizados por función:

*Review (15)* — el grupo más grande. Cada uno revisa desde una perspectiva distinta:
- `kieran-rails-reviewer` — convenciones Rails, estricto con código existente, pragmático con código nuevo
- `dhh-rails-reviewer` — review con la filosofía de DHH / 37signals
- `kieran-python-reviewer` / `kieran-typescript-reviewer` — review especializado por lenguaje
- `security-sentinel` — auditorías de seguridad y vulnerabilidades
- `performance-oracle` — análisis de performance y optimización
- `architecture-strategist` — decisiones arquitectónicas
- `code-simplicity-reviewer` — pase final de simplicidad y minimalismo
- `data-migration-expert` — seguridad en migraciones de datos
- `agent-native-reviewer` — verifica que las features sean accesibles para agentes

*Research (5)* — investigación antes de planificar:
- `repo-research-analyst` — estructura y convenciones del repo
- `best-practices-researcher` — mejores prácticas externas
- `framework-docs-researcher` — documentación de frameworks
- `learnings-researcher` — busca en soluciones pasadas documentadas (el compound en acción)
- `git-history-analyzer` — analiza evolución del código

*Design (3)* — sincronización con diseño:
- `figma-design-sync` — sincroniza implementaciones web con diseños de Figma
- `design-iterator` — refina UI de forma iterativa
- `design-implementation-reviewer` — verifica que la UI matchee el diseño

*Workflow (5)* — automatización del proceso:
- `bug-reproduction-validator` — reproduce y valida bug reports
- `pr-comment-resolver` — resuelve comentarios de PR
- `lint` — linting y quality checks
- `spec-flow-analyzer` — analiza flujos de usuario e identifica gaps

**Comandos** (22 total) — además de los 4 del workflow core:
- `/lfg` — workflow autónomo completo (plan + work + review + compound de una)
- `/slfg` — lo mismo pero en swarm mode con ejecución paralela
- `/deepen-plan` — enriquece planes existentes lanzando agentes de research en paralelo por cada sección
- `/resolve_pr_parallel` — resuelve comentarios de PR en paralelo
- `/create-agent-skill` — crea o edita skills
- `/reproduce-bug` — reproduce bugs usando logs y consola
- `/feature-video` — graba video walkthroughs y los agrega a la descripción del PR

**Skills** (19 total) — conocimiento reutilizable:
- `agent-native-architecture` — cómo construir apps donde los agentes son ciudadanos de primera clase
- `compound-docs` — patrones de documentación para el paso compound
- `orchestrating-swarms` — guía completa de orquestación multi-agente
- `frontend-design` — interfaces frontend production-grade
- `dhh-rails-style` — código Ruby/Rails al estilo DHH
- `file-todos` — sistema de todos basado en archivos
- `git-worktree` — manejo de worktrees para desarrollo paralelo
- `agent-browser` — automatización de browser con Vercel's agent-browser

#### El patrón de orquestación
Lo más potente del plugin. Cuando se corre `/workflows:review`, actúa como **orquestador** que spawnea múltiples subagentes en paralelo:
```text
         ┌────────────────────┐
         │  /workflows:review │  ← Orquestador
         └─────────┬──────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
    ▼              ▼              ▼
┌────────┐  ┌────────────┐  ┌──────────┐
│kieran- │  │security-   │  │dhh-rails-│  ... 10+ más
│rails-  │  │sentinel    │  │reviewer  │
│reviewer│  │            │  │          │
└────────┘  └────────────┘  └──────────┘
```
Cada agente aplica su propio filtro especializado al mismo código. El resultado: un review multidimensional donde seguridad, performance, arquitectura, simplicidad y convenciones se evalúan simultáneamente.

#### El sistema compound en detalle
El paso `/workflows:compound` es un pipeline de 5 etapas:
1. **Context Analyzer** — extrae tipo de problema y síntomas
2. **Solution Extractor** — captura causa raíz y fix que funcionó
3. **Related Docs Finder** — vincula con soluciones existentes
4. **Prevention Strategist** — crea guías de prevención
5. **Documentation Writer** — escribe en `docs/solutions/[categoría]/`

Las categorías: `build-errors/`, `test-failures/`, `performance-issues/`, `security-issues/`, `database-issues/`, etc. El agente `learnings-researcher` busca en estas soluciones documentadas durante la fase de planning, cerrando el loop del conocimiento compuesto.

#### Comparación con Superpowers y Everything Claude Code

| | Superpowers | Everything Claude Code | Compound Engineering |
|---|---|---|---|
| **Filosofía** | Disciplina obligatoria | Caja de herramientas flexible | Conocimiento que se acumula |
| **Foco** | TDD + debugging | Ciclo completo + aprendizaje | Planning + review + documentación |
| **Agentes** | 1 | 12 | 29 |
| **Innovación** | Anti-racionalización | Instincts con confidence score | Review paralelo masivo + compound docs |
| **Documentación** | No persiste | Aprende automáticamente | First-class: `docs/solutions/` |
| **Orquestación** | No | No | Sí (10+ agentes en paralelo) |
| **Mejor para** | "Forzar disciplina de TDD" | "Tener toda herramienta disponible" | "Acumular conocimiento del equipo" |

## Parallelization
Claude Code puede ejecutar varias tareas a la vez. Hay distintos niveles de paralelización, cada uno con más capacidad pero también más complejidad y costo:

1. **Subagents** (dentro de una sesión) — la tool `Task` lanza agentes que trabajan en paralelo y reportan resultados
2. **Múltiples terminales** — sesiones independientes de Claude Code abiertas manualmente
3. **Git Worktrees** — sesiones paralelas con aislamiento de archivos para evitar conflictos
4. **Agent Teams** — coordinación automatizada entre múltiples instancias

### Subagents (Tool Task)
El nivel más básico. Dentro de una misma sesión, Claude puede lanzar subagentes que trabajan en paralelo y devuelven resultados. Por ejemplo, si se pide "explícame cómo funciona X y también arregla el bug en Y":
```text
En paralelo:
├── Agente Explore: investiga X
└── Agente Bash: corre los tests de Y para entender el bug
```
En vez de hacer uno después del otro, los dos corren al mismo tiempo. La skill `dispatching-parallel-agents` de Superpowers se activa cuando hay 2+ tareas independientes y organiza este trabajo de forma estructurada.

### Múltiples terminales
Se pueden abrir varias sesiones de Claude Code en terminales separadas. Un flujo de trabajo recomendado: usar el chat principal para efectuar cambios en el código y las sesiones adicionales (forks) para preguntas sobre el codebase, su estado actual o búsqueda de información.

Una regla a seguir siempre: abrir nuevas terminales por necesidad real. Siempre tener en mente: *"How much can you get done with the minimum viable amount of parallelization?"*

El problema aparece cuando se escala: si dos instancias de Claude editan el mismo archivo en el mismo directorio, se cruzan los cambios. Para eso existen los worktrees.

### Git Worktrees
`git worktree` permite trabajar con múltiples branches de un mismo repositorio en directorios separados. Cada worktree tiene su propio directorio con sus propios archivos, compartiendo el mismo Git history. Esto resuelve el problema central: cada instancia de Claude trabaja en su propio file state, así no hay conflictos.

```bash
# Crear worktrees para trabajo paralelo
git worktree add ../project-feature-a feature-a
git worktree add ../project-feature-b feature-b
git worktree add ../project-refactor refactor-branch

# Cada worktree tiene su propia instancia de Claude
cd ../project-feature-a && claude
```

```bash
# Comandos útiles
git worktree list                              # Listar todos los worktrees
git worktree remove ../project-feature-a       # Eliminar un worktree
```

Ventajas:
- No hay conflictos de git entre instancias
- Cada una tiene un directorio limpio con el que trabajar
- Fácil de comparar resultados entre branches
- Se puede benchmarkear una misma tarea con distintas técnicas

Cuando se trabaja con varias instancias, se puede usar el Cascade Method para organizarse: abrir nuevas tareas en pestañas a la derecha, ordenar de izquierda a derecha (más viejo a más nuevo), y enfocarse en 3-4 tareas a la vez. Se puede renombrar cada chat con `/rename` para no perder el hilo.
### Agent Teams
Es el siguiente nivel en paralelización. Actualmente experimental y desactivado por defecto. Se habilita agregando en `settings.json`:
```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

#### Qué son
Múltiples sesiones de Claude Code coordinadas como equipo. Una sesión actúa como **team lead** (coordina, asigna tareas, sintetiza resultados) y el resto como **teammates** (trabajan independientemente, cada uno con su propia ventana de contexto). Los teammates se comunican directamente entre sí.

#### Diferencia con Subagents
Los subagents que ya vimos  y los agent teams paralelizan trabajo, pero operan distinto:

| | Subagents                                         | Agent Teams                                          |
|--------------------|---------------------------------------------------|------------------------------------------------------|
| **Contexto**       | Ventana propia; resultados vuelven al caller       | Ventana propia; completamente independientes          |
| **Comunicación**   | Solo reportan resultados al agente principal       | Teammates se comunican directamente entre sí          |
| **Coordinación**   | El agente principal maneja todo                    | Task list compartida con auto-coordinación            |
| **Ideal para**     | Tareas enfocadas donde solo importa el resultado   | Trabajo complejo que requiere discusión y colaboración|
| **Costo en tokens**| Menor: resultados resumidos al contexto principal  | Mayor: cada teammate es una instancia separada de Claude|

#### Diferencia con Git Worktrees
Con worktrees uno maneja manualmente sesiones paralelas de Claude Code en branches separadas. Agent teams automatizan esa coordinación: el lead crea tareas, las asigna a los teammates , y se comunican sin intervención manual. Worktrees son manuales pero simples; agent teams son autónomos pero más costosos en terminos de tokens.

#### Cómo funcionan
La arquitectura tiene 4 componentes:

| Componente     | Rol                                                              |
|----------------|------------------------------------------------------------------|
| **Team lead**  | La sesión principal que crea el equipo, spawnea teammates, y coordina |
| **Teammates**  | Instancias separadas de Claude Code que trabajan en tareas asignadas  |
| **Task list**  | Lista compartida de tareas que los teammates reclaman y completan     |
| **Mailbox**    | Sistema para la comunicación entre agentes                 |

Se le pide al lead en lenguaje natural que cree un equipo:
```text
Create an agent team to review PR #142. Spawn three reviewers:
- One focused on security implications
- One checking performance impact
- One validating test coverage
Have them each review and report findings.
```
El lead crea el equipo, spawnea teammates, y cada uno trabaja en paralelo. Se puede interactuar con cualquier teammate directamente.

Las tareas tienen 3 estados (pending, in progress, completed) y pueden tener dependencias entre sí. Cuando un teammate completa una tarea de la que dependen otras, las bloqueadas se desbloquean automáticamente. El claiming usa file locking para evitar race conditions.

#### Buenas prácticas
- **Dar contexto suficiente en el spawn prompt** — los teammates cargan CLAUDE.md y skills del proyecto, pero NO heredan el historial de conversación del lead. Incluir detalles específicos de la tarea.
- **Dimensionar bien las tareas** — muy simples: el overhead de coordinación supera el beneficio. Muy grandes: los teammates trabajan demasiado sin check-ins. Lo ideal: unidades autocontenidas con un deliverable claro (una función, un archivo de tests, un review). Apuntar a 5-6 tareas por teammate.
- **Evitar conflictos de archivos** — dos teammates editando el mismo archivo causa overwrites. Dividir el trabajo para que cada uno trabaje con archivos distintos.
- **Empezar con research/review** — si es la primera vez, empezar con tareas que no requieran escribir código o que claramente causen overlap: revisar un PR, investigar una librería, debuggear un issue.
- **Monitorear y redirigir** — no dejar al equipo correr sin supervisión demasiado tiempo. Checkear progreso, redirigir lo que no funciona, sintetizar hallazgos a medida que llegan.
- **Usar delegate mode** (Shift+Tab) — evita que el lead se ponga a implementar él mismo. Lo restringe a coordinar: spawnear, mensajear, asignar tareas.
- **Requerir aprobación de plan** — para tareas riesgosas, pedir que el teammate planifique primero en modo read-only antes de implementar.

#### Ejemplo
Investigar un bug con hipótesis competidoras — cada teammate investiga una teoría distinta y se desafían entre sí:
```text
Users report the app exits after one message instead of staying connected.
Spawn 5 agent teammates to investigate different hypotheses. Have them talk to
each other to try to disprove each other's theories, like a scientific debate. 
Update the findings doc with whatever consensus emerges.
```
Esto evita el problema del "anchoring" que tiene una investigación secuencial: una vez que se explora una teoría, las siguientes están sesgadas hacia ella. Con múltiples investigadores desafiándose activamente, la teoría que sobrevive es más probable que sea la causa real.

#### Limitaciones actuales
- No se pueden resumir sesiones con teammates in-process (`/resume` no los restaura)
- Un solo equipo por sesión
- No hay equipos anidados (teammates no pueden crear sus propios equipos)
- El lead es fijo — no se puede promover un teammate
- Todos los teammates arrancan con los permisos del lead
