# Presentación Claude Code
## Claude.md
Un archivo markdown con instrucciones generales para los proyectos, que claude code siempre deberia saber.
### Ejemplos
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
Paquetes que agrupan skills, hooks, agents y más para distribuir como una unidad. A diferencia de una skill (que es un archivo .md individual), un plugin puede contener múltiples skills + hooks + agents.

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
- NO agregar "hooks" al manifest — Claude Code carga `hooks/hooks.json` automáticamente por convención. Declararlo causa error de duplicado.

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
