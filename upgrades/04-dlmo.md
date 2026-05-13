# 04 — DLMO (Dim Light Melatonin Onset)

## Lo que computa Somnus hoy

`lib/core/services/circadian.dart:147-150`

```
mean_bedtime = circularMean(bedtimes_minutos)
DLMO_estimado = (mean_bedtime − 120 min) mod 1440
```

Es decir: el inicio de la ventana de melatonina se asume a **2 horas antes del bedtime medio**.

`schedule_screen.dart:138-140` lo explica como:

> *"El DLMO ... es el momento en que la melatonina comienza a subir. Estimado ~2h antes de tu hora habitual de dormir. Irse a la cama dentro de esta ventana optimiza la latencia del sueno."*

## Evidencia verificada

### DLMO correla mas con wake-time que con bedtime

`[VERIFIED via search abstract]` Burgess HJ, Eastman CI (2005). **The dim light melatonin onset following fixed and free sleep schedules.** *Journal of Sleep Research* 14(3):229-237. PMID: 16120097.

> Correlaciones (jovenes sanos en horario regular):
> - **Wake-time vs DLMO**: r = 0.77
> - **Sleep midpoint vs DLMO**: r = 0.68
> - **Bedtime vs DLMO**: r = 0.36

> Interpretacion fisiologica de los autores: la luz que recibes despues de despertar es de magnitud mucho mayor (interior 200-500 lux, exterior 10,000-100,000 lux) que la luz que precede al bedtime (interior 50-200 lux). La luz matinal cae cerca del crossover de la phase response curve y arrastra el reloj con mas fuerza.

### Magnitud — DLMO ~2-3h antes del sleep onset

Este es el dato que Somnus usa hoy (2h). En la literatura el valor reportado varia entre 2h y 3h en distintas poblaciones. `[NEEDS-VERIFICATION primaria en pase futuro]` — el numero exacto depende de la edad (jovenes vs adultos mayores), cronotipo (matutino vs vespertino), e historial reciente de luz.

## Diagnostico

### Anclar DLMO al bedtime es la decision con menor evidencia

Si tu objetivo es estimar el DLMO sin medirlo (lo cual es razonable: medirlo requiere saliva cada 30 min en oscuridad, no es accesible), **anclar al wake-time da el doble de poder predictivo**:

- bedtime: r² = 0.13 (13% de varianza explicada)
- wake-time: r² = 0.59 (59% de varianza explicada)

Mas que el doble. Es un cambio de un solo numero (`bedtime − 2h` → `wake − 14h` aproximadamente) con casi 5x el poder predictivo.

### La constante 2h es un promedio poblacional

Es razonable usar 2h como default, pero **no captura cronotipos**. Las personas matutinas tienden a tener DLMO 2-3h antes del bedtime; las vespertinas, 1-2h antes. Sin medir cronotipo, no se puede ajustar individualmente.

### El umbral de fiabilidad esta ausente

Hoy `circadian.dart:87-89` requiere ≥3 bedtimes para mostrar DLMO. Esto es muy poco. La literatura clinica sugiere ≥5-7 dias de horario regular antes de estimar DLMO con cualquier fiabilidad. Tres dias irregulares producen un numero pero no es informativo.

## Upgrades

### U4.1 — Cambiar el anclaje a wake-time

Sustituir en `circadian.dart:147-150`:

```dart
// ANTES
int _estimateMelatoninWindow(List<int> bedtimeMins) {
  final mean = _circularMean(bedtimeMins);
  return ((mean - 120 + 1440) % 1440).round();
}

// DESPUES
int _estimateMelatoninWindow(List<SleepRecord> records) {
  final wakes = records
      .where((r) => r.wakeTime != null)
      .map((r) => _parseTime(r.wakeTime!))
      .whereType<int>()
      .toList();
  if (wakes.length < 5) return null;
  final mean = _circularMean(wakes);
  // DLMO ~14h despues del wake-time habitual
  // (Burgess y Eastman: wake-time correla r=0.77 con DLMO; constante derivada de la literatura)
  return ((mean + 14 * 60) % 1440).round();
}
```

Coste: bajo. Impacto: alto en precision del estimador. **Importante**: la constante 14h es una aproximacion derivada de la duracion media de sueno (8h) + offset DLMO-sleep-onset (2h) = 10h de gap wake→DLMO. Es decir DLMO ocurre **antes** del bedtime no despues del wake. Repensar la formula:

Si DLMO ocurre ~2h antes del bedtime, y bedtime = wake − sleep_duration, entonces:
- DLMO = wake − sleep_duration − 2h
- Si sleep_duration es ~8h: DLMO = wake − 10h
- En tiempo de reloj (24h): DLMO = (wake_min − 600 + 1440) mod 1440

Mejor formulacion: usar la duracion media DE ESE usuario:

```dart
final meanSleepMins = records
    .map((r) => r.hoursSlept * 60)
    .reduce((a, b) => a + b) / records.length;
final meanWake = _circularMean(wakes);
final dlmoEstimate = (meanWake - meanSleepMins - 120 + 1440) % 1440;
```

Esto usa wake-time como ancla principal (r=0.77) y la duracion del propio usuario como secundaria. La constante 120 min (2h antes del sleep onset) es el offset poblacional menos discutido.

Coste: bajo. Impacto: alto.

### U4.2 — Subir el umbral a 5-7 dias

`circadian.dart:87`:

```dart
// ANTES: bedtimeMins.length >= 3
// DESPUES: registros completos (bedtime+wake) >= 5
```

Mostrar `—` si <5 dias. Copy: "Necesitas 5 noches con bedtime y wake-time".

Coste: trivial. Impacto: evita mostrar DLMO ficticio.

### U4.3 — Mostrar la ventana, no solo un punto

Hoy se muestra "DLMO 21:30". Mas util: mostrar la ventana de melatonina activa, donde la propension al sueno es alta:

```
VENTANA SUENO    21:30 - 03:30    (DLMO + 6h)
```

Razonamiento `[MECHANISTIC]`: la melatonina sube tras DLMO y se mantiene elevada hasta unas 6-8h despues. Esa es la ventana donde la propension fisiologica al sueno es maxima. Es lo que el usuario realmente quiere saber, no un timestamp aislado.

Coste: bajo. Impacto: medio-alto (mas accionable).

### U4.4 — Mostrar fiabilidad estimada

Cuando el SRI del usuario es bajo (sleep schedule irregular), la estimacion de DLMO **no es fiable**, porque DLMO se desplaza con cada noche irregular. Mostrar:

```
DLMO            21:30
                fiabilidad: baja (SRI < 70)
```

o:

```
DLMO            21:30
                fiabilidad: alta (SRI > 80, 14 noches consistentes)
```

Coste: bajo (depende de tener SRI implementado primero). Impacto: medio.

### U4.5 — Concept card honesto

Reescribir `schedule_screen.dart:138-140`:

> *"Ventana de melatonina (DLMO)*
>
> *Inicio estimado de la subida de melatonina endogena. Anclado a tu wake-time medio (Burgess y Eastman 2005, J Sleep Res: wake-time correla con DLMO r=0.77, bedtime r=0.36). DLMO ~2h antes del inicio habitual de sueno. La estimacion requiere 5+ noches con bedtime y wake-time registrados, y es mas fiable si tu SRI > 70."*

Coste: trivial. Impacto: alto.

### U4.6 — Cronotipo inferido (opcional, futuro)

Con MSFsc del documento 03 + DLMO estimado, se puede clasificar el cronotipo del usuario:

| MSFsc | Cronotipo |
|---|---|
| antes de 03:00 | Matutino temprano |
| 03:00 - 04:00 | Matutino |
| 04:00 - 05:00 | Intermedio |
| 05:00 - 06:00 | Vespertino |
| despues de 06:00 | Vespertino extremo |

Estos cortes son aproximados — la literatura no tiene umbrales unicos. Antes de hardcodear, leer la distribucion en Roenneberg 2007 (PubMed) y elegir cortes basados en quintiles. `[NEEDS-VERIFICATION primaria en pase futuro]`.

Coste: bajo. Impacto: medio.

### U4.7 — Cuestionario MEQ corto (opcional)

Como complemento o alternativa a la inferencia desde diarios, permitir un MEQ-5 (Horne-Ostberg corto) o MCTQ-Light en onboarding. Output: cronotipo categorico que ajusta la constante DLMO-bedtime y la ventana sugerida.

Coste: medio. Impacto: medio. Util en early-onboarding antes de tener datos.

## Riesgos a recordar

- **El usuario no debe medicar con esto.** El DLMO mostrado por Somnus es una estimacion poblacional, no una medida. Cualquier copy que sugiera "toma melatonina a las DLMO_h" es irresponsable. Mantener el lenguaje descriptivo.
- **Cuidado con orthosomnia.** Si la app muestra DLMO con 4 decimales y el usuario duerme 15 min antes/despues "fuera de la ventana", se puede inducir ansiedad. La ventana de 6h en U4.3 ayuda a evitar este sesgo.

## Resumen — accionable

| ID | Cambio | Coste | Prioridad |
|---|---|---|---|
| U4.1 | Anclar DLMO al wake-time + duracion media | Bajo | BLOCKING |
| U4.2 | Subir umbral a 5+ dias con bedtime+wake | Trivial | Alta |
| U4.3 | Mostrar ventana de 6h en vez de punto | Bajo | Alta |
| U4.4 | Mostrar fiabilidad atada al SRI | Bajo | Media |
| U4.5 | Concept card con citas verificadas | Trivial | Alta |
| U4.6 | Inferir cronotipo desde MSFsc | Bajo | Baja |
| U4.7 | MEQ-5 / MCTQ-Light opcional en onboarding | Medio | Baja |
