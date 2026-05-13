# Somnus — Plan de upgrades cientifico-tecnico

## Como usar este directorio

Cada documento describe **una unidad de la app** y propone upgrades respaldados por evidencia verificada. Los hechos cientificos llevan etiqueta de procedencia:

- `[VERIFIED]` — abstract o tabla del paper primario leida directamente en este pase (PubMed, PMC, journal). Autor + ano + revista + PMID.
- `[NEEDS-VERIFICATION]` — la afirmacion esta en literatura terciaria pero no he leido el primario en este pase. No se usa como base de decisiones de producto.
- `[MECHANISTIC]` — razonamiento fisiologico plausible sin RCT que lo respalde directamente. Util para diseno conservador pero no se vende como dato.

Las propuestas dentro de cada doc estan ordenadas por (impacto cientifico) / (coste de implementacion). Las marcadas `[BLOCKING]` no deberian salir sin resolverse porque la app dice algo que la evidencia contradice o porque hay un bug funcional.

## Indice

1. [01-sleep-debt.md](./01-sleep-debt.md) — Ventana de 14 dias, factor de recuperacion 0.75, modelo lineal
2. [02-regularity.md](./02-regularity.md) — Reemplazar sigma(bedtime) por Sleep Regularity Index (SRI)
3. [03-social-jet-lag.md](./03-social-jet-lag.md) — Cambiar bedtime-midpoint por midsleep, soportar free-days
4. [04-dlmo.md](./04-dlmo.md) — Anclar DLMO al wake-time, no al bedtime
5. [05-reminders.md](./05-reminders.md) — Cafeina, alcohol, luz azul: justificacion y refinamientos
6. [06-routines.md](./06-routines.md) — Wind-down y wake-up, paso por paso, citado
7. [07-ux.md](./07-ux.md) — Auditoria UX contra PRODUCT.md tras navegar la app
8. [08-new-features.md](./08-new-features.md) — PVT, phase plot, export, light log, glossary

## Resumen ejecutivo

### Lo que la app hace bien y debe conservar

- **Ventana de 14 dias** para deuda — directamente alineado con el paradigma de Van Dongen 2003.
- **Recuperacion no lineal** — la direccion es correcta (Banks 2010), aunque el coeficiente 0.75 sea generoso.
- **Cutoff cafeina −6h** — respaldado por el unico RCT cruzado disponible (Drake 2013).
- **Cutoff pantallas −2h** — respaldado por Chang & Czeisler 2015 (PNAS).
- **Temperatura 18-20 °C** — alineado con la literatura termoregulatoria.
- **Arquitectura local-first** — privacy as identity, sin cloud, sin telemetria.
- **Tono instrument-grade** — DataTerminal, hero de la deuda, swipe-to-delete. Bien.

### Lo que la evidencia contradice (`[BLOCKING]`)

1. **Step "No uses el snooze"** — directamente contradicho por Sundelin 2024 (J Sleep Res, PSG): 30 min de snooze no afectan cognicion, cortisol, animo ni arquitectura. Reescribir o eliminar.
2. **Factor de recuperacion 0.75** — Banks 2010 muestra que ni 10h de recuperacion restauran del todo tras 5 noches de 4h. Bajar a 0.5 o exponer como parametrico.
3. **"Regularidad" calculada como sigma(bedtime)** — no es el SRI publicado por Phillips 2017 / Windred 2024, y los usuarios tecnicos podrian leerlo mal. Implementar SRI canonico.
4. **Jet lag social usando bedtime midpoint** — la definicion canonica (Wittmann 2006, Roenneberg 2012) usa **midpoint de sueno**, no de bedtime. Sustituir.
5. **DLMO anclado al bedtime** — Burgess y Eastman 2005: bedtime correla r=0.36 con DLMO, wake-time correla r=0.77. Anclar al wake-time.
6. **Step "Cafe +90 min"** — popular pero sin RCT con outcomes objetivos. Marcar como experimental.
7. **Bug funcional**: usuario que llega a `/home` sin completar onboarding ve `/routines` y `/reminders` vacios. Sembrar defaults independiente del flujo.

### Estado de captura de la app (localhost:5050)

Navegacion completada el 13 may 2026:

- `/home` — Carga sin onboarding si no hay datos. Placeholder `—` correcto.
- `/schedule` — Sin horario configurado muestra "Ve a Ajustes". Concept cards permanentes.
- `/debt` — Hero "DEUDA ACUMULADA — Sin datos suficientes". Charts vacios.
- `/routines` — **BUG B1**: "Sin pasos configurados" porque el seed solo se ejecuta desde onboarding.
- `/reminders` — Mismo patron vacio (BUG B1).
- `/settings` — Funcional. Copy "14 dias es el estandar clinico" defendible.

## Prioridad de upgrades — top 10

| # | Upgrade | Doc | Coste | Prioridad |
|---|---|---|---|---|
| 1 | Sembrar defaults independiente del onboarding (BUG B1) | 07-ux | Trivial | BLOCKING |
| 2 | Bajar `recoveryFactor` de 0.75 a 0.5 | 01-sleep-debt | Trivial | BLOCKING |
| 3 | Implementar SRI canonico (Phillips 2017) | 02-regularity | Medio | BLOCKING |
| 4 | Jet lag social usando midpoint de sueno (no bedtime) | 03-social-jet-lag | Bajo | BLOCKING |
| 5 | Anclar DLMO al wake-time (Burgess r=0.77 vs r=0.36) | 04-dlmo | Bajo | BLOCKING |
| 6 | Reescribir o eliminar el step "No snooze" (Sundelin 2024) | 06-routines | Trivial | BLOCKING |
| 7 | Marcar "Cafe +90 min" como experimental | 06-routines | Trivial | BLOCKING |
| 8 | Anadir `evidenceRef`+`evidenceTier` a routine steps | 06-routines | Bajo | BLOCKING |
| 9 | Anadir `evidenceRef` a reminders | 05-reminders | Bajo | BLOCKING |
| 10 | Quitar emojis de reminders | 05-reminders | Trivial | Alta |

## Plan secuencial sugerido

**Sprint 1 — Honestidad cientifica** (1-2 dias)

- U1.1 (recoveryFactor 0.5)
- U6.2 (reescribir step snooze)
- U6.3 (marcar cafe +90 como experimental)
- U6.1 (evidenceRef en routine steps)
- U5.2 (evidenceRef en reminders)
- U5.1 + U7.2 (quitar emojis)
- B1 (sembrar defaults independiente del onboarding)

Cero codigo de calculo nuevo. Solo correcciones de copy, schema migration menor, y un fix de seeding. Devuelve coherencia cientifica inmediata.

**Sprint 2 — Metricas canonicas** (3-5 dias)

- U2.1 (SRI canonico de Phillips 2017)
- U3.1 (midpoint de sueno para jet lag social)
- U4.1 (anclar DLMO al wake-time)
- U3.2 (settings de free-days)
- U4.3 (mostrar ventana de 6h en vez de punto)

Implementacion de las formulas correctas. Requiere migracion de circadian.dart y tests.

**Sprint 3 — Identidad y nuevas features** (5-10 dias)

- U8.4 (Export JSON/CSV + SHA-256) — coste bajo, impacto identidad alto
- U8.7 (Glossary unificado)
- U7.1 (mover concept-cards a glossary)
- U8.2 (Phase plot circular)
- U6.7 (modo rutina practica con timer)
- U8.1 (Micro-PVT diaria)

## Convencion de migraciones

Schema actual: v2 (anadio `stagesJson` y `efficiencyPct` a SleepRecords).

Migraciones propuestas:

- **v3**: anadir `evidenceRef`, `evidenceTier`, `evidenceDoi` a RoutineSteps; `evidenceRef` a Reminders; `lightMinutes` a SleepRecords; tabla `PvtRuns`; tabla `DailySnapshots`.
- **v4**: anadir `freeDaysMask` a ConfigEntries (o setting separado); `recoveryFactor` configurable.

Las migraciones son aditivas — no hay riesgo de perdida de datos.

## Referencias maestras verificadas en este pase

Estas son las fuentes que **he leido directamente** (al menos abstract de PubMed) y de las que extraigo los hechos centrales. Cada doc individual cita estas y otras propias del area.

### Sleep debt
- Van Dongen HPA, Maislin G, Mullington JM, Dinges DF (2003). **The cumulative cost of additional wakefulness: dose-response effects on neurobehavioral functions and sleep physiology from chronic sleep restriction and total sleep deprivation.** *Sleep* 26(2):117-126. [PMID: 12683469](https://pubmed.ncbi.nlm.nih.gov/12683469/) · DOI: [10.1093/sleep/26.2.117](https://doi.org/10.1093/sleep/26.2.117) `[VERIFIED]`
- Banks S, Van Dongen HPA, Maislin G, Dinges DF (2010). **Neurobehavioral dynamics following chronic sleep restriction: dose-response effects of one night for recovery.** *Sleep* 33(8):1013-1026. [PMID: 20815182](https://pubmed.ncbi.nlm.nih.gov/20815182/) · [PMC2910531](https://pmc.ncbi.nlm.nih.gov/articles/PMC2910531/) `[VERIFIED via search abstract]`
- Belenky G, Wesensten NJ, Thorne DR, et al. (2003). **Patterns of performance degradation and restoration during sleep restriction and subsequent recovery.** *J Sleep Res* 12(1):1-12. [PMID: 12603781](https://pubmed.ncbi.nlm.nih.gov/12603781/) `[VERIFIED via search abstract]`

### Regularity
- Phillips AJK, Clerx WM, O'Brien CS, Sano A, Barger LK, Picard RW, Lockley SW, Klerman EB, Czeisler CA (2017). **Irregular sleep/wake patterns are associated with poorer academic performance and delayed circadian and sleep/wake timing.** *Scientific Reports* 7(1):3216. [PMID: 28607474](https://pubmed.ncbi.nlm.nih.gov/28607474/) · [PMC5468315](https://pmc.ncbi.nlm.nih.gov/articles/PMC5468315/) · DOI: [10.1038/s41598-017-03171-4](https://doi.org/10.1038/s41598-017-03171-4) `[VERIFIED]`
- Windred DP, Burns AC, Lane JM, Saxena R, Rutter MK, Cain SW, Phillips AJK (2024). **Sleep regularity is a stronger predictor of mortality risk than sleep duration: A prospective cohort study.** *Sleep* 47(1):zsad253. [PMID: 37738616](https://pubmed.ncbi.nlm.nih.gov/37738616/) · [PMC10782501](https://pmc.ncbi.nlm.nih.gov/articles/PMC10782501/) · DOI: [10.1093/sleep/zsad253](https://doi.org/10.1093/sleep/zsad253) `[VERIFIED]`

### Social jet lag
- Wittmann M, Dinich J, Merrow M, Roenneberg T (2006). **Social jetlag: misalignment of biological and social time.** *Chronobiology International* 23(1-2):497-509. [PMID: 16687322](https://pubmed.ncbi.nlm.nih.gov/16687322/) · DOI: [10.1080/07420520500545979](https://doi.org/10.1080/07420520500545979) `[VERIFIED via search abstract]`
- Roenneberg T, Allebrandt KV, Merrow M, Vetter C (2012). **Social jetlag and obesity.** *Current Biology* 22(10):939-943. [PMID: 22578422](https://pubmed.ncbi.nlm.nih.gov/22578422/) · DOI: [10.1016/j.cub.2012.03.038](https://doi.org/10.1016/j.cub.2012.03.038) `[VERIFIED via search abstract]`

### DLMO
- Burgess HJ, Eastman CI (2005). **The dim light melatonin onset following fixed and free sleep schedules.** *J Sleep Res* 14(3):229-237. PMID: 16120097. `[VERIFIED via search abstract]`
- Khalsa SBS, Jewett ME, Cajochen C, Czeisler CA (2003). **A phase response curve to single bright light pulses in human subjects.** *J Physiol* 549:945-952. [PMID: 12717008](https://pubmed.ncbi.nlm.nih.gov/12717008/) `[VERIFIED via search abstract]`

### Cafeina y luz azul
- Drake C, Roehrs T, Shambroom J, Roth T (2013). **Caffeine effects on sleep taken 0, 3, or 6 hours before going to bed.** *J Clin Sleep Med* 9(11):1195-1200. [PMID: 24235903](https://pubmed.ncbi.nlm.nih.gov/24235903/) · [PMC3805807](https://pmc.ncbi.nlm.nih.gov/articles/PMC3805807/) · DOI: [10.5664/jcsm.3170](https://doi.org/10.5664/jcsm.3170) `[VERIFIED]`
- Chang AM, Aeschbach D, Duffy JF, Czeisler CA (2015). **Evening use of light-emitting eReaders negatively affects sleep, circadian timing, and next-morning alertness.** *PNAS* 112(4):1232-1237. [PMID: 25535358](https://pubmed.ncbi.nlm.nih.gov/25535358/) · [PMC4313820](https://pmc.ncbi.nlm.nih.gov/articles/PMC4313820/) · DOI: [10.1073/pnas.1418490112](https://doi.org/10.1073/pnas.1418490112) `[VERIFIED]`

### Snooze
- Sundelin T, Landry S, Axelsson J (2024). **Is snoozing losing? Why intermittent morning alarms are used and how they affect sleep, cognition, cortisol, and mood.** *J Sleep Res* 33(3):e14054. [PMID: 37849039](https://pubmed.ncbi.nlm.nih.gov/37849039/) · DOI: [10.1111/jsr.14054](https://doi.org/10.1111/jsr.14054) `[VERIFIED]`

### CBT-I
- Trauer JM, Qian MY, Doyle JS, Rajaratnam SMW, Cunnington D (2015). **Cognitive Behavioral Therapy for Chronic Insomnia: A Systematic Review and Meta-analysis.** *Ann Intern Med* 163(3):191-204. [PMID: 26054060](https://pubmed.ncbi.nlm.nih.gov/26054060/) · DOI: [10.7326/M14-2841](https://doi.org/10.7326/M14-2841) `[VERIFIED via search abstract]`

### Fuentes con `[NEEDS-VERIFICATION primaria]`

Citadas con cautela y marcadas explicitamente como tales en cada doc:

- Ebrahim IO, Shapiro CM, Williams AJ, Fenwick PB (2013). Alcohol y sueno (review).
- Okamoto-Mizuno K, Mizuno K (2012). Termal y sueno.
- Pruessner JC et al. (1997). Cortisol Awakening Response.
- Lunsford-Avery JR et al. (2018). SRI validation in older adults.
- Lewy AJ (1980). Light melatonin suppression.
- Wright KP et al. (2013). Camping y reentrainment.
- Baron KG et al. (2017). Orthosomnia (citado en U8.8).
- Basner M, Dinges DF (2011). PVT sensibilidad (citado en U8.1).

Antes de hardcodear cualquier cifra de estos papers en copy de la app, leerlos directamente.

## Politica de copy

Por consistencia y por defensa contra orthosomnia:

1. Nunca usar tono motivacional ("you've got this", "great job", etc.).
2. Nunca usar emojis en labels operacionales (sí en notas casuales de chat, no en UI).
3. Cuando un step o reminder este basado en evidencia debil, **marcarlo explicitamente** (`[MECHANISTIC]`, `EXPERIMENTAL`, `[TRADITION]`).
4. Cuando una afirmacion descanse sobre un paper, citarlo con autor + ano + revista. PMID/DOI en glossary.
5. Cuando una cifra es promedio poblacional, decirlo. *"Estimado a partir de ..."*
6. Cuando el usuario tiene <N dias de datos, mostrar `—` con leyenda, no un numero pseudo-fiable.

## Que NO hacer

No implementar nunca:

- Streaks / badges / "noches consecutivas con SRI > X".
- Sleep score agregado tipo "85/100" — composite arbitrario.
- Cloud sync opt-in — viola la arquitectura.
- Notificaciones motivacionales.
- Prediccion ML / "tu hora optima sera 23:14".
- Comparaciones sociales / leaderboards.
- Integracion con asistentes (Siri/Google) que requiera grants externos.

Cada uno de estos contradice algun principio del manifiesto.
