# 03 — Jet lag social

## Lo que computa Somnus hoy

`lib/core/services/circadian.dart:119-144`

```
weekday_mean = circularMean(bedtimes de Mon-Fri)
weekend_mean = circularMean(bedtimes de Sat-Sun)
jetLagSocial = |weekend_mean − weekday_mean| en horas
```

Solo usa `bedtime`. Asume que "free days" = sabado y domingo.

Umbrales (`circadian.dart:34-39`):
- <0.5h: "Sin jet lag social"
- <1.0h: "Leve"
- <2.0h: "Moderado"
- ≥2.0h: "Severo"

## Evidencia verificada

### Definicion canonica — Wittmann 2006

`[VERIFIED via search abstract]` Wittmann M, Dinich J, Merrow M, Roenneberg T (2006). **Social jetlag: misalignment of biological and social time.** *Chronobiology International* 23(1-2):497-509. PMID: [16687322](https://pubmed.ncbi.nlm.nih.gov/16687322/) · DOI: [10.1080/07420520500545979](https://doi.org/10.1080/07420520500545979).

> El paper introduce el termino *social jetlag* como la discrepancia entre tiempo social y tiempo biologico, operacionalizada via la **diferencia entre los midpoints de sueno en dias libres y dias de trabajo**, medidos por el Munich ChronoType Questionnaire (MCTQ).

> n = 501 voluntarios, MCTQ + cuestionarios complementarios de calidad de sueno, bienestar y consumo de estimulantes.

> Formula central: 
> ```
> MSF = midpoint de sueno en dias libres
> MSW = midpoint de sueno en dias de trabajo (los dias "with alarm clock")
> jetLagSocial = |MSF − MSW|
> ```

> El **midpoint** es: `bedtime + duracion/2`. No es bedtime.

### MSFsc — correccion por oversleep

`[NEEDS-VERIFICATION en pase futuro — la formula concreta esta en el paper de MCTQ, no en Wittmann 2006]`. La correccion estandar para neutralizar la deuda de sueno acumulada en la semana laboral es:

```
MSFsc = MSF − 0.5 × (SDF − ((5 × SDW + 2 × SDF) / 7))
```

donde SDF = duracion de sueno en dias libres, SDW = duracion en dias de trabajo. Esto **resta** el efecto de "dormir mas el finde para compensar".

### Prevalencia y umbrales clinicos

`[VERIFIED via search abstract]` Roenneberg T, Allebrandt KV, Merrow M, Vetter C (2012). **Social jetlag and obesity.** *Curr Biol* 22(10):939-943. PMID: [22578422](https://pubmed.ncbi.nlm.nih.gov/22578422/) · DOI: [10.1016/j.cub.2012.03.038](https://doi.org/10.1016/j.cub.2012.03.038).

> El paper reporta que **>1h de jet lag social se asocia con BMI elevado** independientemente de la duracion del sueno.

> Estimaciones de prevalencia citadas en revisiones secundarias: ~70% de la poblacion adulta tiene ≥1h de jet lag social, ~33% tiene ≥2h. `[Estos numeros concretos NEEDS-VERIFICATION primaria — vienen de la revision de Roenneberg/Merrow en NHANES y otras cohortes; antes de citarlos en copy, leer el full text]`.

## Diagnostico

### Bedtime midpoint ≠ sleep midpoint

Este es el bug conceptual mas serio. Considera dos perfiles:

**Persona A**: lun-vie se acuesta 23:00, despierta 06:00 (medio del sueno = 02:30). Sab-dom se acuesta 23:00, despierta 09:00 (medio = 04:00). Diferencia de midpoint = 1.5h. Diferencia de bedtime = 0h.

Somnus dice: "Sin jet lag social".
Literatura dice: jet lag social = 1.5h. Riesgo metabolico aumentado.

Esto es **falso negativo sistematico** para uno de los patrones mas comunes (acostarse igual, levantar mas tarde el finde).

**Persona B**: lun-vie se acuesta 23:00, despierta 06:00 (medio = 02:30). Sab-dom se acuesta 02:00, despierta 09:00 (medio = 05:30). Diferencia de midpoint = 3h. Diferencia de bedtime = 3h.

Somnus dice: "Severo (>2h)".
Literatura dice: jet lag social severo.

Coincide. Pero Persona A tambien deberia salir como severa o moderada — Somnus lo perderia.

### Sabado/domingo ≠ free days

`free days` en MCTQ = dias sin despertador, no necesariamente sabado/domingo. Para:

- Trabajadores en turnos.
- Freelancers / autonomos.
- Estudiantes en periodo de examenes.
- Trabajadores en oficios de fin de semana (hosteleria, sanitarios).

la regla "weekday = Mon-Fri" produce datos sin sentido. Es facil de arreglar: anadir un setting de free-day mask, o detectar free-days automaticamente como dias donde el wake-time desvia significativamente del wake-time mediano.

### Los umbrales si estan bien

0.5/1/2h coincide con el corte clinico publicado: >1h se asocia con BMI elevado (Roenneberg 2012), >2h con peor salud mental (revisiones recientes). Los thresholds actuales son razonables — el problema es **lo que se compara**, no donde se ponen las lineas.

## Upgrades

### `[BLOCKING]` U3.1 — Calcular midpoint de sueno, no de bedtime

Sustituir en `circadian.dart:119-144`:

```dart
// ANTES: midpoint de bedtime
final m = _parseTime(r.bedtime!);

// DESPUES: midpoint del periodo de sueno
final bedMins = _parseTime(r.bedtime!);
final wakeMins = _parseTime(r.wakeTime!);
if (bedMins == null || wakeMins == null) continue;
var sleepMins = wakeMins - bedMins;
if (sleepMins <= 0) sleepMins += 1440;
final midpoint = (bedMins + sleepMins / 2) % 1440;
```

Requisito: el registro tiene que tener `bedtime` Y `wakeTime`. Records con solo `hoursSlept` no se pueden usar (decision honesta: que el numero no aparezca, no que aparezca mal).

Coste: bajo. Impacto: alto (alineamiento exacto con Wittmann 2006 / Roenneberg).

### U3.2 — Definir free-days en Settings

Anadir un setting:

```
DIAS LIBRES
[ ] Lunes  [ ] Martes  [ ] Miercoles  ... [x] Sabado  [x] Domingo
```

Default: sabado-domingo. Permite a usuarios atipicos personalizar.

Bonus opcional: deteccion automatica. Un dia se considera "libre" si el wake-time desvia >60 min de la mediana de wake en la semana, durante al menos 3 ocurrencias en el mes.

Coste: bajo. Impacto: medio.

### U3.3 — Implementar MSFsc

Para usuarios con ≥7 dias de datos, calcular tambien la version corregida MSFsc segun la formula MCTQ. Mostrarla junto a la version cruda:

```
JET LAG SOCIAL    1.4h
MSFsc (chronotype)  03:45
```

Coste: bajo (matematica trivial). Impacto: medio. El usuario tecnico que lea sobre cronotipo encuentra el numero estandar.

### U3.4 — Concept card honesto

Reescribir `schedule_screen.dart:132-135`:

> *"Jet lag social*
>
> *Diferencia entre el midpoint del sueno en dias libres y dias de trabajo (Wittmann et al. 2006, Chronobiol Int; Roenneberg et al. 2012, Curr Biol). >1h se asocia con BMI elevado independiente de la duracion. >2h con peor salud mental y metabolica. La mayoria de adultos tiene ≥1h."*

Coste: trivial. Impacto: alto.

### U3.5 — Mostrar el "chronotype shift" como visual

En `/schedule`, anadir debajo de las concept cards un mini-visual:

```
WEEKDAY    23:30 ────────► 06:30      mid 03:00
WEEKEND    01:00 ──────────► 09:00    mid 05:00
                                       Δ 2h
```

Coste: bajo (CustomPainter o Stack con Text). Impacto: medio. Es la visualizacion canonica de MCTQ.

### U3.6 — Edge cases del unwrap circular

`circadian.dart:170-180` desempaqueta times alrededor de la mediana. Si hay bimodalidad real (un usuario que en un mismo periodo trabaja noches y dias), el unwrap puede producir means absurdas. Anadir:

- Si la sigma post-unwrap es >180 min, mostrar `—` con leyenda "Patron bimodal detectado".
- Permitir al usuario marcar manualmente "Shift work" en Settings, lo que aplica un calculo alternativo basado en cronotipos separados por bloque.

Coste: bajo. Impacto: bajo en usuarios mayoritarios, alto en shift workers.

### U3.7 — Reportar Δwake-time tambien

Algunos epidemiologistas (Parsons, NHANES) operacionalizan jet lag social via la diferencia de wake-time porque correlaciona mejor con DLMO (ver doc 04). Mostrar ambos:

```
SLEEP MIDPOINT Δ     1.5h
WAKE TIME Δ          2.0h
```

Coste: trivial (ya tienes wake-time). Impacto: medio.

## Resumen — accionable

| ID | Cambio | Coste | Prioridad |
|---|---|---|---|
| U3.1 | Cambiar bedtime-midpoint → sleep-midpoint | Bajo | BLOCKING |
| U3.2 | Setting de free-days (default Sab-Dom) | Bajo | Alta |
| U3.3 | Calcular MSFsc | Bajo | Media |
| U3.4 | Concept card con citas verificadas | Trivial | Alta |
| U3.5 | Visual de chronotype shift weekday/weekend | Bajo | Media |
| U3.6 | Edge cases bimodalidad | Bajo | Baja |
| U3.7 | Mostrar Δwake-time complementario | Trivial | Baja |
