# 05 — Recordatorios (cafeina, alcohol, luz azul)

## Lo que tiene Somnus hoy

`lib/core/database.dart:236-242` — defaults insertados desde onboarding:

| Recordatorio | Offset | Label actual |
|---|---|---|
| Ultimo cafe | −360 min (6h antes bedtime) | `Ultimo cafe ☕` |
| Ultima copa | −240 min (4h antes) | `Ultima copa 🍷` |
| Atenuar pantallas | −120 min (2h antes) | `Atenua pantallas 📵` |
| Inicia rutina | −30 min | `Inicia rutina 🌙` |
| Hora de dormir | 0 min | `Hora de dormir 😴` |

`reminders_screen.dart:93` declara:

> *"Los tiempos de corte para cafeina (6h), alcohol (4h) y luz azul (2h) estan basados en sus semividas fisiologicas y su efecto sobre la arquitectura del sueno."*

## Evidencia verificada

### Cafeina — 6h antes del bedtime

`[VERIFIED]` Drake C, Roehrs T, Shambroom J, Roth T (2013). **Caffeine effects on sleep taken 0, 3, or 6 hours before going to bed.** *J Clin Sleep Med* 9(11):1195-1200. PMID: [24235903](https://pubmed.ncbi.nlm.nih.gov/24235903/) · PMC: [3805807](https://pmc.ncbi.nlm.nih.gov/articles/PMC3805807/) · DOI: [10.5664/jcsm.3170](https://doi.org/10.5664/jcsm.3170).

> Diseno (literal del abstract): RCT doble ciego, placebo controlado, intra-sujeto. **Dosis fija de 400 mg de cafeina** administrada a 0h, 3h o 6h antes del bedtime habitual, vs placebo. Sueno auto-reportado en casa + monitor portatil validado.

> Resultado: *"a moderate dose of caffeine at bedtime, 3 hours prior to bedtime, or 6 hours prior to bedtime each have significant effects on sleep disturbance relative to placebo (p < 0.05 for all)."*

> Conclusion: *"The magnitude of reduction in total sleep time suggests that caffeine taken 6 hours before bedtime has important disruptive effects on sleep and provides empirical support for sleep hygiene recommendations to refrain from substantial caffeine use for a minimum of 6 hours prior to bedtime."*

**Implicacion para Somnus.** El cutoff de 6h por defecto **esta directamente respaldado por el unico RCT cruzado** sobre este intervalo. Mantener.

Caveat: la dosis del estudio es 400 mg (≈ 4 espressos / 1 cafe filtrado grande / 4 lattes). Para dosis menores (200 mg), el efecto a 6h es probablemente mas pequeno. La app no diferencia dosis, lo cual es razonable por simplicidad.

### Luz azul — 2h antes del bedtime

`[VERIFIED]` Chang AM, Aeschbach D, Duffy JF, Czeisler CA (2015). **Evening use of light-emitting eReaders negatively affects sleep, circadian timing, and next-morning alertness.** *Proc Natl Acad Sci USA* 112(4):1232-1237. PMID: [25535358](https://pubmed.ncbi.nlm.nih.gov/25535358/) · PMC: [4313820](https://pmc.ncbi.nlm.nih.gov/articles/PMC4313820/) · DOI: [10.1073/pnas.1418490112](https://doi.org/10.1073/pnas.1418490112).

> Diseno: clinical trial intra-sujeto. Lectura de **4h antes del bedtime de 22:00** en LE-eBook (iPad) vs libro impreso, durante 5 noches consecutivas en cada condicion.

> Espectro: LE-eBook pico ~450 nm (azul); luz reflejada del libro impreso pico ~612 nm (rojo-naranja).

> Resultados (LE-eBook vs print):
> - Supresion de melatonina por la tarde-noche.
> - Sleep onset latency mas largo (p=0.009).
> - Reduccion del REM total acumulado (p=0.029).
> - Phase delay del reloj circadiano (DLMO mas tarde).
> - Reduccion de alerta a la manana siguiente.

> Conclusion: *"evening exposure to an LE-eBook phase-delays the circadian clock, acutely suppresses melatonin"* y tiene implicaciones para sueno, rendimiento, salud y seguridad.

**Implicacion para Somnus.** El cutoff de 2h **es conservador respecto al estudio**: Chang et al. usaron 4h de exposicion. Una recomendacion de 2h captura la fase mas critica (la ultima antes del bedtime, cerca del DLMO) sin pedir un cambio drastico al usuario. Es defendible como guideline pragmatica.

Caveat metodologico: Chang et al. midieron con luz ambiente ~3 lx (oscura). En condiciones reales (luz de habitacion 50-200 lx), el efecto incremental del eReader es probablemente menor. Pero la literatura general (Tosini, Hattar) confirma que ipRGCs (celulas ganglionares fotosensibles) responden a luz <450 nm para suprimir melatonina.

### Alcohol — 4h antes del bedtime

`[NEEDS-VERIFICATION primaria]` Ebrahim IO, Shapiro CM, Williams AJ, Fenwick PB (2013). **Alcohol and sleep I: effects on normal sleep.** *Alcohol Clin Exp Res* 37(4):539-549. PMID: [23347102](https://pubmed.ncbi.nlm.nih.gov/23347102/).

Hechos publicados en la literatura terciaria que **citan este review**:

- Alcohol cerca del bedtime reduce sleep onset latency y consolida el primer tercio del sueno, pero suprime REM y fragmenta el segundo tercio.
- REM rebote en la segunda mitad de la noche.
- Efectos dosis-dependientes.

El cutoff de 4h por defecto en Somnus tiene base en la farmacocinetica: clearance hepatica ~0.015-0.020 g/dL por hora, lo que implica que 2 bebidas estandar consumidas 4h antes del bedtime estan **mayoritariamente metabolizadas** al inicio del sueno, evitando la fase de fragmentacion del segundo tercio.

Sin embargo: este razonamiento es `[MECHANISTIC]`. No he leido el paper de Ebrahim directamente en este pase. La afirmacion "4h antes" no esta tan respaldada por un RCT especifico como la cafeina lo esta por Drake 2013. **Antes de defender el cutoff con autoridad, leer el review completo.**

## Diagnostico

### Los cutoffs basicos son defendibles

Cafeina −6h (Drake 2013), pantallas −2h (Chang 2015): respaldados directamente por estudios primarios. Alcohol −4h: respaldado mecanisticamente, no por un RCT especifico que yo haya verificado en este pase.

### El labelado emocional contradice el manifiesto

Hoy: `Ultimo cafe ☕`, `Ultima copa 🍷`, `Atenua pantallas 📵`, `Inicia rutina 🌙`, `Hora de dormir 😴`.

PRODUCT.md dice:
> *"Eclectic restraint. One unusual deliberate choice per surface, not zero and not ten."*
> *"Cold precision over warm comfort."*
> *Referencias: factory.ai, Urbit, Linear*

Ni factory.ai ni Urbit ni Linear usan emojis en labels de UI. El uso de emojis aqui es contradictorio con la identidad declarada.

### El recordatorio "Inicia rutina −30 min" es arbitrario

La duracion de la rutina default (atenua luz 10' + sin pantallas 30' + temp 5' + lectura 20' + 4-7-8 5') = 70 minutos. Recomendar empezarla 30 min antes del bedtime significa que la mayoria de la rutina ocurre **antes** de empezar, lo cual no tiene sentido. Deberia ser igual a la duracion total de la rutina habilitada del usuario, lo cual ya se computa en `routines_screen.dart:127`. Cambiarlo a dinamico.

### No hay recordatorio de luz matinal

Hay reminders nocturnos pero no matutinos. El manifiesto dice "show the truth": la luz matinal es la intervencion circadiana mas potente que existe (ver doc 06). Falta un reminder al despertar.

## Upgrades

### U5.1 — Quitar emojis de los labels

Sustituir:

```
Ultimo cafe ☕       → LAST.COFFEE
Ultima copa 🍷       → LAST.DRINK
Atenua pantallas 📵   → DIM.SCREENS
Inicia rutina 🌙      → WIND.DOWN.START
Hora de dormir 😴     → BED
```

Estilo monospace, caps, separadores con punto — coherente con la voz del DataTerminal en /home. Coste: trivial. Impacto: alto en identidad.

### `[BLOCKING]` U5.2 — Anadir base cientifica visible en cada reminder

Hoy, el `_InfoCard` "Base cientifica" agrupa todos los cutoffs en un parrafo. Mejor: cada reminder muestra su evidencia en el subtitle de su tile:

```
LAST.COFFEE              −360 min          21:00
Drake 2013, JCSM: 400 mg @ −6h reducen sleep aun en RCT
```

Coste: bajo (anadir un campo `evidenceRef` al schema Reminders). Impacto: alto (instrument-grade).

### U5.3 — Reescribir el `_InfoCard "Base cientifica"` con citas exactas

```markdown
BASE CIENTIFICA

- LAST.COFFEE (−6h). Drake et al. 2013, JCSM 9(11):1195-1200. RCT doble ciego, 400 mg de cafeina a 0/3/6h antes del bedtime reducen el sueno significativamente respecto a placebo en los tres timings.
- LAST.DRINK (−4h). Farmacocinetica: clearance ~0.015 g/dL/h. Cuatro horas permiten metabolizar 2 bebidas estandar antes de la fase REM-sensible (Ebrahim et al. 2013, Alcohol Clin Exp Res).
- DIM.SCREENS (−2h). Chang et al. 2015, PNAS 112(4):1232. 4h de eReader vs libro impreso retrasan el reloj circadiano, suprimen melatonina, reducen alerta matinal. Cortar 2h captura la ventana mas critica.
```

Coste: trivial. Impacto: alto.

### U5.4 — Reminder dinamico para inicio de rutina

```dart
// En vez de offset fijo 30 min, calcular desde steps habilitados
final routineDuration = await db.windDownDuration(); // suma de steps enabled
await scheduleReminder(label: 'WIND.DOWN.START', offsetMins: routineDuration);
```

Coste: bajo. Impacto: medio (el reminder ahora coincide con la duracion real).

### U5.5 — Anadir reminder matinal de luz

Nuevo reminder por defecto:

```
MORNING.LIGHT    +5 min despues del wake    07:05
Exposicion a luz exterior 15-30 min en la primera hora tras despertar. Avance de fase circadiana (ver doc 06).
```

Coste: bajo. Impacto: medio. Anclar al `targetWakeTime`, no al bedtime.

### U5.6 — Refinar el flujo de scheduling para no perder reminders al cambiar bedtime

Hoy `notifications.dart:55` hace `cancelAll()` + reschedule. Si el usuario cambia su `targetBedtime`, los reminders se reprograman. Bug potencial: si el reminder dispara hoy a las 19:00 y el usuario cambia el bedtime a las 23:30 en vez de 23:00, el reminder pasa de las 17:00 a las 17:30 — pero si ya disparo hoy, no se vuelve a disparar. No es bug critico pero merece un test.

Coste: bajo. Impacto: bajo.

### U5.7 — Considerar reminder semanal de revision

Opcional: cada domingo, un reminder con "Tu SRI esta semana: X. Jet lag social: Y. Deuda actual: Z." Es solo notificacion local con datos derivados de la BD. Coherente con local-first. Coste: medio. Impacto: medio. **Riesgo**: cae en coaching. Mantener tono factual.

## Riesgos a recordar

- Los reminders pueden caer en patron motivacional si el copy no se cuida. Mantener formato `LAST.X / DIM.Y / BED` y nunca anadir "you got this" / "good job" / similar.
- Si el usuario tiene shift work, los offsets relativos al bedtime estandar son incorrectos. El soporte de free-days del doc 03 puede ayudar parcialmente.

## Resumen — accionable

| ID | Cambio | Coste | Prioridad |
|---|---|---|---|
| U5.1 | Quitar emojis de labels | Trivial | Alta |
| U5.2 | Anadir `evidenceRef` por reminder | Bajo | BLOCKING |
| U5.3 | Reescribir `_InfoCard` con citas exactas | Trivial | Alta |
| U5.4 | Reminder de inicio rutina = duracion real | Bajo | Media |
| U5.5 | Reminder matinal de luz | Bajo | Media |
| U5.6 | Test del scheduling al cambiar bedtime | Bajo | Baja |
| U5.7 | Reminder semanal opcional de revision | Medio | Baja |
