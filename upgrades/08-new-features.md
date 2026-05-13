# 08 — Features nuevas

Propuestas alineadas con `PRODUCT.md`: instrument-grade, local-first, sin coaching, sin gamificacion. Cada feature lleva justificacion cientifica donde aplica y motivacion de identidad cuando no.

## U8.1 — Micro-PVT diaria

### Que es

Psychomotor Vigilance Task (PVT) en 60-180 segundos, ejecutada al despertar o por la manana.

Mecanica: el usuario presiona un boton cuando aparece un punto en la pantalla. El sistema mide reaction time (RT) durante ~1-3 minutos. Cada vez que el usuario espera el estimulo y luego presiona, se registra una latencia. Outcomes:

- Mediana de RT
- Numero de lapsus (>500 ms)
- Tiempo de respuesta del decil mas rapido

### Por que es coherente con Somnus

`[VERIFIED]` Van Dongen 2003: los sujetos restringidos a 6h o menos durante 14 dias **no percibian** sus propios deficits cognitivos. La PVT capturaba esos deficits objetivamente.

La PVT es:
- **El standard clinico** para medir alertness aguda (Dinges, Basner).
- **Ejecutable en cualquier dispositivo** con touch.
- **No coaching** — solo te dice un numero.
- **Distintivo**: ni Whoop ni Oura ni Apple Health la implementan, porque rompe el feel-good de scores agregados.

Es **exactamente el tipo de feature** que el manifiesto Somnus pide: muestra una medida objetiva de deterioro, deja que el usuario decida.

### Como integrarlo

Schema nuevo:

```dart
class PvtRuns extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get date => text()(); // YYYY-MM-DD
  IntColumn get timestampMs => integer()(); // ms unix epoch del start
  RealColumn get medianRtMs => real()();
  RealColumn get fastestDecileRtMs => real()();
  IntColumn get lapses => integer()(); // >500 ms
  IntColumn get falseStarts => integer()(); // pressed too early
  IntColumn get durationS => integer()(); // 60 / 120 / 180
}
```

UI:

- Tile en `/home`: `PVT  248 ms · 2 lapses (Q3)` con percentil personal.
- Botton "RUN PVT" debajo del DataTerminal.
- Pantalla `/pvt` con fondo negro, punto que aparece cada 2-10 s aleatorio, contador de tiempo arriba.

Crucial — **lo que NO hacer**:

- No mostrar streaks ("3 dias seguidos en Q1!").
- No mostrar leaderboards.
- No celebrar mejorias con animaciones/sonidos.
- No ofrecer "challenges".
- No correlacionar publicamente con humor / energia / cualquier metrica subjetiva.

Solo mostrar el numero, su percentil personal, y la evolucion en `/debt` como una serie temporal secundaria.

### Validacion cientifica

Basner M, Dinges DF (2011). **Maximizing sensitivity of the psychomotor vigilance test (PVT) to sleep loss.** *Sleep* 34(5):581-591. `[NEEDS-VERIFICATION primaria en pase futuro]`.

Antes de shippeear, verificar:
- Duracion minima fiable (3 min standard, 5 min ideal).
- Intervalos inter-estimulo (2-10 s aleatorio uniforme, standard).
- Como calcular percentil personal con N < 30 runs.

### Coste y prioridad

Medio. Es una nueva pantalla, schema, y UI. Tarda 2-4 dias bien hecho.

**Prioridad alta** por ser distintivo de identidad.

---

## U8.2 — Phase plot circular (actographic radial)

### Que es

Visualizacion canonica en cronobiologia: un circulo que representa 24h, con bands radiales para cada noche reciente mostrando inicio/fin de sueno. Permite ver de un golpe la regularidad y los outliers.

### Por que

- `[VERIFIED]` Phillips 2017: los Irregular sleepers se diferenciaban visualmente de los Regular cuando se ploteaba como "double-plotted raster" — exactamente este formato. Es el standard de chronobiology desde Pittendrigh.
- Estetica: encaja con eclectic restraint. Un grafico no convencional bien hecho > tres graficos cartesianos genericos.
- Reemplaza con ventaja el scatter actual en `/schedule`.

### Como integrarlo

Sustituir `_ConsistencyChart` en `schedule_screen.dart:163` por un `CustomPainter` que dibuje:

1. Un circulo de 24h en mono, con tick marks cada hora.
2. Por cada noche reciente, un arco coloreado entre bedtime y wakeTime.
3. Centro: mediana de sleep midpoint, en mono.
4. Una linea radial discreta marcando `targetBedtime` y `targetWakeTime`.

Coste: medio (CustomPainter, 1-2 dias). Impacto: alto en identidad + utility cognitiva.

---

## U8.3 — Heatmap de presencia (probabilidad asleep)

### Que es

Hoy para cada minuto del dia, color = probabilidad de estar dormido en esa hora del dia, basado en los ultimos 14-30 dias.

Visualmente: una franja horizontal donde la franja entre 23:30 y 06:30 esta muy oscura (alta probabilidad dormido) y la franja entre 09:00 y 22:00 esta clara.

### Por que

- Es el **calculo intermedio del SRI**. Mostrarlo da intuicion de por que tu SRI es lo que es.
- Es lo que Phillips 2017 muestra en sus Figs 2A/2B.
- Solo se construye con `bedtime + wakeTime` reales.

### Como integrarlo

Pantalla `/schedule` debajo del phase plot, o dentro del concept-card de regularidad expandido. Coste: bajo. Impacto: medio.

---

## U8.4 — Export JSON/CSV + verificacion SHA-256

### Que es

Botones en Settings:

```
DATA SOVEREIGNTY
  EXPORT.JSON       → sleeprecords.json
  EXPORT.CSV        → sleeprecords.csv
  SCHEMA.SHA256     → a3f8c91...
```

Permitir export de:
- `SleepRecords` (raw).
- `SleepTargets`.
- `ConfigEntries`.
- `RoutineSteps` y `Reminders` (la config de la rutina, no las ejecuciones).

Formato JSON crudo. Sin transformaciones, sin enriquecimiento, sin metadata adicional excepto un campo `_schema_version` y `_exported_at`.

### Por que

- Privacy local sin export portable = privacy prison.
- Identidad Urbit: sovereignty primitives.
- Permite al usuario migrar, hacer backups manuales, analizar en otras herramientas.

### Como integrarlo

Anadir tres metodos al `AppDatabase`:

```dart
Future<String> exportAsJson() async { ... }
Future<String> exportAsCsv() async { ... }
Future<String> schemaSha256() async { ... } // hash del archivo SQLite o del JSON canonico
```

En la build mobile/desktop, escribir a un archivo y compartir via `share_plus`. En web, descargar via Blob URL.

Coste: bajo. Impacto: alto en identidad. **No introduce telemetria** — el usuario es quien comparte si quiere.

---

## U8.5 — Light log (registro de luz matinal)

### Que es

Boton opcional en wake-up routine:

```
MORNING.LIGHT — minutes today
0   5   15   30+
```

Persiste `lightMinutes` en SleepRecord. Renderizar en `/schedule` como una segunda serie en el chart de consistencia.

### Por que

- `[VERIFIED]` Khalsa 2003 + Wright 2013: luz matinal es la intervencion circadiana mas potente. Si no se mide, no se puede mostrar su efecto.
- Wright KP et al. (2013) Curr Biol: dos noches de camping reentrenan el DLMO en mediante exposicion solar natural. `[NEEDS-VERIFICATION primaria]` — el numero exacto y diseno habria que confirmar.
- Permite correlacionar: usuarios con mas luz matinal probablemente tienen DLMO mas temprano y mejor SRI.

### Como integrarlo

Schema: anadir `IntColumn get lightMinutes => integer().nullable()()` a `SleepRecords`. Migracion v3.

UI: anadir un campo opcional al SleepLog form, y un step interactivo en la rutina de wake-up.

Coste: bajo. Impacto: medio-alto (es una variable de intervencion, no solo de medicion).

---

## U8.6 — Modo "instrument": tablas mono, sin charts

### Que es

Toggle en Settings: `MODE: INSTRUMENT`. Cuando activo, las pantallas de `/debt`, `/schedule` muestran **tablas monospace** en vez de charts.

Ejemplo `/debt` en modo instrument:

```
WINDOW: 14d   COUNT: 11   AVG: 7.2h   TARGET: 8.0h

DATE         HOURS   DELTA    CUMDEBT
2026-05-12   8.0    +0.0      0.0
2026-05-11   6.5    -1.5      1.5
2026-05-10   8.2    +0.2      0.4
2026-05-09   5.0    -3.0      3.4
...

CURRENT DEBT: 4.2h
```

### Por que

- Urbit-grade restraint. El usuario al despertar en habitacion oscura no necesita un chart, necesita numeros.
- Es la eleccion eclectic canonica. Sleep apps no hacen esto.
- Bonus: rinde mejor en pantallas pequenas o con `prefers-reduced-motion`.

### Como integrarlo

Toggle simple en Settings. Switches en cada widget de chart para renderizar `Table(...)` en su lugar. Coste: bajo-medio. Impacto: medio en identidad, alto en cierto perfil de usuario.

---

## U8.7 — Glossary unificado

### Que es

Una nueva ruta `/glossary` que centraliza la pedagogia que hoy esta repartida en concept-cards.

Contenido:

- Cada termino (Deuda, SRI, MSFsc, DLMO, PRC, CAR, ...) con definicion corta.
- Cada uno con cita primaria (Drake 2013, Phillips 2017, etc.).
- Enlace a DOI / PubMed.
- Tier de evidencia.

Estilo: tabla mono / lista cerrada. Sin imagenes.

### Por que

- Cumple "earn every element": la pedagogia tiene su lugar, no contamina los instrumentos operacionales.
- Acceso unificado: en vez de leer concept-card en `/schedule` distinto al de `/debt`, todo en un sitio.
- Honra al manifiesto: instrument operates, glossary educates.

### Como integrarlo

Anadir entrada en `app.dart` router: `GET /glossary`. Tile en `/settings` o en cada AppBar (icon `library_books`). Coste: bajo. Impacto: alto en identidad.

---

## U8.8 — Detector de orthosomnia (warning suave)

### Que es

Si la app detecta patrones de uso compatibles con orthosomnia, mostrar un info-box discreto en `/home`:

Heuristica: el usuario abre la app >5 veces al dia, ajusta target hours mas de 2 veces por semana, y/o muestra ansiedad textual (texto en notas, si llegase a implementarse).

Mostrar:

```
NOTE
Frequent self-monitoring of sleep can paradoxically worsen sleep
(Baron 2017, J Clin Sleep Med — "orthosomnia"). Consider:
- Reduce app opens to once daily
- Stop adjusting target nightly
- Set the data and walk away
```

### Por que

- Una app que mide DLMO y deuda puede causar el problema que pretende ayudar.
- El manifiesto rechaza coaching pero "no induzcas patologia" es proteccion del usuario, no coaching.
- Baron KG, Abbott S, Jao N, Manalo N, Mullen R (2017). **Orthosomnia: Are some patients taking the quantified self too far?** *J Clin Sleep Med* 13(2):351-354. `[NEEDS-VERIFICATION primaria en pase futuro]`.

### Como integrarlo

Tracking local de:
- `appOpensPerDay`
- `targetChangesPerWeek`

Si exceden umbrales (e.g. 5/d, 3/w), mostrar el note. Permitir desactivarlo permanentemente.

Coste: bajo. Impacto: medio. **Riesgo**: si se hace mal, condescendiente. Mantener tono factual.

---

## U8.9 — Comparison view (semana actual vs anterior)

### Que es

En `/debt` y `/schedule`, una pestana `COMPARE` que muestra esta semana vs la anterior:

```
              ESTA       ANTERIOR    DELTA
AVG HOURS     7.2        6.8         +0.4
SRI           74         71          +3
JET LAG       1.4h       1.7h        -0.3
DEBT          4.2h       6.1h        -1.9
```

### Por que

- Es una vista periodica. Util para revisiones semanales sin necesidad de un dashboard agresivo.
- Tono factual: numeros, deltas, sin emoji ni color emocional.
- Util cuando el usuario quiere ver el efecto de un cambio (e.g. "esta semana corte el cafe a las 4pm").

### Como integrarlo

Pestana adicional o slot dentro de cada pantalla. Coste: bajo. Impacto: medio.

---

## U8.10 — Scheduled snapshot diario (no telemetria)

### Que es

Una vez al dia, automaticamente, la app calcula un snapshot:

```json
{
  "date": "2026-05-13",
  "debt": 4.2,
  "sri": 74,
  "jetLagH": 1.4,
  "dlmo": "21:30",
  "lastNightHours": 7.2
}
```

Se persiste en una tabla `DailySnapshots`. **NO se envia a ningun lado.** Es solo memoria historica para evitar tener que recalcular las metricas a posteriori si se cambia la formula.

### Por que

- Si en el futuro cambias el SRI o el factor de recuperacion, los datos pasados se recomputan automaticamente (correcto), pero el usuario pierde la "vista historica de lo que veia entonces". Snapshots arreglan esto.
- Permite mostrar "tu SRI ha caido 8 puntos en 30 dias" sin recomputar todo desde cero cada vez.
- No es telemetria: queda en local.

### Como integrarlo

Coste: bajo (cron via WorkManager / equivalent en mobile; en web, on-open if not already today). Impacto: medio. Util de cara a evoluciones futuras de las formulas.

---

## Resumen — accionable

| ID | Feature | Coste | Prioridad |
|---|---|---|---|
| U8.1 | Micro-PVT diaria | Medio | Alta — feature distintivo |
| U8.2 | Phase plot circular | Medio | Alta — identidad |
| U8.3 | Heatmap de probabilidad de sueno | Bajo | Media |
| U8.4 | Export JSON/CSV + SHA-256 | Bajo | Alta — identidad |
| U8.5 | Light log (registro de luz matinal) | Bajo | Media |
| U8.6 | Modo "instrument" sin charts | Bajo-Medio | Media — identidad |
| U8.7 | Glossary unificado | Bajo | Alta |
| U8.8 | Detector de orthosomnia (warning suave) | Bajo | Media |
| U8.9 | Comparison view semanal | Bajo | Media |
| U8.10 | Daily snapshot persistido | Bajo | Baja |
