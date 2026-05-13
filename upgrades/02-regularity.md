# 02 — Regularidad

## Lo que computa Somnus hoy

`lib/core/services/circadian.dart:107-116`

```
regularityIndex = clamp(100 · (1 − stddev(bedtimes_minutos) / 120), 0, 100)
```

Es decir: desviacion estandar del bedtime, normalizada contra 120 minutos. Solo usa `bedtime`. Ignora wake-time, duracion, despertares, siestas.

Umbrales mostrados (`circadian.dart:27-32`):
- ≥85: "Excelente"
- ≥65: "Buena"
- ≥40: "Irregular"
- <40: "Muy irregular"

## Evidencia verificada

### Definicion canonica del Sleep Regularity Index (SRI)

`[VERIFIED]` Phillips AJK, Clerx WM, O'Brien CS, Sano A, Barger LK, Picard RW, Lockley SW, Klerman EB, Czeisler CA (2017). **Irregular sleep/wake patterns are associated with poorer academic performance and delayed circadian and sleep/wake timing.** *Scientific Reports* 7(1):3216. PMID: [28607474](https://pubmed.ncbi.nlm.nih.gov/28607474/) · DOI: [10.1038/s41598-017-03171-4](https://doi.org/10.1038/s41598-017-03171-4).

> Definicion (del paper): el SRI es la probabilidad porcentual de que un individuo este en el mismo estado (dormido vs despierto) en dos puntos cualesquiera separados 24h, promediada sobre la ventana de estudio. Escalado: 100 = perfecto, 0 = aleatorio.

> Diseno del paper original: 61 universitarios, 30 dias de diario de sueno. Compararon Regular vs Irregular (12 vs 12, en quintiles extremos).

> Hallazgos: DLMO mas tardio en Irregular (00:08 ± 1:54 vs 21:32 ± 1:48; p<0.003). Pico de propension al sueno mas tardio (06:33 vs 04:45; p<0.005). Amplitud de luz menor (102 ± 19 vs 179 ± 29 lux; p<0.005). **SRI correlaciono con GPA: r=0.37, p<0.004.**

Caracteristicas formales (del abstract+paper, ya validado):
- **No requiere designar un episodio principal de sueno** (funciona con siestas o all-nighters).
- **Sensible a cambios dia-a-dia.** Captura el patron, no solo el promedio.
- **Independiente de la duracion.** Dos individuos con el mismo SRI pueden dormir distinta cantidad.

### El SRI predice mortalidad mas que la duracion

`[VERIFIED]` Windred DP, Burns AC, Lane JM, Saxena R, Rutter MK, Cain SW, Phillips AJK (2024). **Sleep regularity is a stronger predictor of mortality risk than sleep duration: A prospective cohort study.** *Sleep* 47(1):zsad253. PMID: [37738616](https://pubmed.ncbi.nlm.nih.gov/37738616/) · DOI: [10.1093/sleep/zsad253](https://doi.org/10.1093/sleep/zsad253).

> Diseno: cohorte prospectiva UK Biobank, n = **60,977 participantes** (62.8 ± 7.8 anos, 55.0% mujeres), **>10 millones de horas de actigrafia**. Seguimiento 6.30 ± 0.83 anos. 1859 muertes (4.84 por 1000 persona-anos).

> SRI mediana[IQR] en la cohorte: **81.0 [73.8 - 86.3]**.

> Resultado central (literal del abstract): *"Higher sleep regularity was associated with a 20%-48% lower risk of all-cause mortality (p < .001 to p = 0.004), a 16%-39% lower risk of cancer mortality (p < 0.001 to p = 0.017), and a 22%-57% lower risk of cardiometabolic mortality (p < 0.001 to p = 0.048), across the top four SRI quintiles compared to the least regular quintile."*

> *"Sleep regularity was a stronger predictor of all-cause mortality than sleep duration."*

> *"Sleep regularity may be a simple, effective target for improving general health and survival."*

## Diagnostico

### Lo que Somnus mide NO es SRI

La metrica actual de Somnus (sigma del bedtime) es una **aproximacion grosera** al SRI. Diferencias practicas:

1. **No usa wake-time.** Dos personas que se acuestan a la misma hora pero se despiertan a horas distintas tienen identica "regularidad" en Somnus, distinto SRI.
2. **No captura desviaciones puntuales.** Alguien que se acuesta 23:00 toda la semana excepto un sabado a las 04:00 tiene una sigma similar a alguien que oscila ±60 min cada dia. El SRI canonico los discrimina (la persona con un solo outlier severo tiene una mejor SRI porque la mayoria de pares de dias se "alinean" mientras solo el outlier rompe).
3. **No mide consistencia de duracion.** El SRI lo hace implicitamente al medir estado-mismo a las 24h.
4. **Normalizacion arbitraria.** Dividir por 120 min y ofrecer un score 0-100 produce un numero que parece comparable con el SRI publicado, pero no lo es. El usuario podria leer literatura sobre "SRI < 70 ↑ mortalidad" y aplicar el umbral incorrectamente.

### Los umbrales tampoco son los de la literatura

Somnus marca "Excelente" a partir de 85. Windred 2024 reporta que la mediana en UK Biobank es 81 — es decir, **la mitad de los participantes estaria en "Buena" o peor segun Somnus, lo cual es razonable**, pero la calibracion no esta atada a la literatura. La forma honesta seria:

- Q5 (mas irregular): SRI < ~64 → mortalidad +20-48% vs Q1
- Q4: ~64-74 → mortalidad +X%
- Q1 (mas regular): SRI > ~86

Esto es lo que el usuario tecnico esperaria leer en una app instrument-grade.

## Upgrades

### `[BLOCKING]` U2.1 — Implementar SRI canonico

Algoritmo de referencia (de Phillips 2017 y el paquete GGIR open-source):

```
1. Discretiza el dia en bins de 1 min (o 5 min para reducir coste).
2. Para cada SleepRecord, marca los minutos entre bedtime y wakeTime como `asleep`.
3. Para cada par de dias consecutivos (d, d+1) y cada bin b dentro de las 24h:
     match[b, d] = 1 si state[b, d] == state[b, d+1], else 0
4. SRI = 200 · mean(match) − 100
     (escala -100 a +100, en la mayoria de implementaciones se reporta 0-100)
```

Notas tecnicas:
- Necesita al menos 7 dias para ser estable. Mostrar `—` con leyenda "Mas datos" si <7 noches con bedtime+wake.
- Para registros que solo tengan `hoursSlept`, **no se pueden incluir**. Marcarlos como datos parciales que cuentan para deuda pero no para SRI.
- La implementacion en GGIR (Wadsworth/Hees) es la referencia open-source: https://wadpac.github.io/GGIR/articles/SleepRegularityIndex.html. Verificar y portar la formula exacta antes del shipping.
- Coste: medio. Es un loop O(dias × bins) en memoria — para 30 dias × 1440 bins son 43k operaciones por evaluacion. Aceptable.

### U2.2 — Calibrar umbrales contra la cohorte UK Biobank

Sustituir el corte Excelente/Buena/Irregular/MuyIrregular por quintiles ancorados a Windred 2024 (al menos en el copy):

| Rango | Label | Posicion en UK Biobank | Riesgo de mortalidad |
|---|---|---|---|
| SRI ≥ 86 | "Q1 — regular" | Top quintile | Referencia (HR 1.0) |
| 74 ≤ SRI < 86 | "Q2-Q3 — medio" | Mid quintiles | HR ≈ 1.1-1.2 |
| 64 ≤ SRI < 74 | "Q4 — irregular" | Q4 | HR ≈ 1.3 |
| SRI < 64 | "Q5 — muy irregular" | Bottom quintile | HR ≈ 1.5 (20-48% mayor) |

Los HRs son aproximados; antes de hardcodearlos en copy, verificar los HR exactos en el full text del paper. `[NEEDS-VERIFICATION en pase futuro]`.

Coste: bajo. Impacto: el usuario tecnico ve el numero en el mismo lenguaje que la literatura.

### U2.3 — Cambiar el label "regularidad circadiana" a "regularidad sueno-vigilia"

`schedule_screen.dart:127` dice *"Regularidad circadiana"* en el concept-card. Tecnicamente impreciso: el SRI mide consistencia del patron sueno-vigilia, no el ritmo circadiano endogeno. El usuario tecnico distingue uno y otro. Sustituir por *"Regularidad sueno-vigilia"* o *"Sleep regularity index"*.

Coste: trivial. Impacto: precision terminologica.

### U2.4 — Concept card honesto

Reescribir el concept-card actual (`schedule_screen.dart:128`):

> *"Regularidad sueno-vigilia (SRI)*
>
> *Probabilidad de estar en el mismo estado (dormido/despierto) en dos minutos separados 24h. Phillips et al. 2017, Sci Rep. La mediana en una cohorte de 61k adultos britanicos es 81. Windred et al. 2024 (Sleep, n=60,977) muestran que el SRI predice mortalidad por todas las causas mas que la duracion del sueno: el quintil mas regular tiene 20-48% menos mortalidad que el menos regular, 6 anos despues."*

Coste: trivial. Impacto: alto.

### U2.5 — Mostrar SRI en /home

Sustituir el `[2]` actual del DataTerminal:

```
REGULARIDAD    73%   buena
```

por:

```
SRI            73    Q3 (UK Biobank)
```

El usuario tecnico ve el numero, el label de quintil, y entiende exactamente que esta mirando. Coste: bajo.

### U2.6 — Heatmap de consistencia

`schedule_screen.dart:163` muestra hoy un scatter chart de bedtimes. Mas informativo seria un heatmap diario: para cada minuto del dia y cada dia, color = state. La probabilidad de estado=mismo se ve a ojo en bandas horizontales.

Coste: medio (CustomPainter en Flutter). Impacto: alta riqueza informacional manteniendo el manifiesto eclectic restraint.

## Notas de implementacion

- El SRI canonico es **simetrico**: penaliza igualmente dormir mas tarde de lo habitual y mas temprano. Esto es correcto desde la cronobiologia y diferente del concepto popular de "te acostaste tarde, mal".
- Para usuarios con menos de 7 dias de datos, hay dos opciones:
  1. Mostrar `—` con leyenda "Necesitas 7 dias para calcular SRI fiable" (recomendado).
  2. Mostrar SRI con N=4-6 marcando "preliminar".

  Recomiendo opcion 1: alineado con instrument-grade.

- Cuidado con el horario de verano. Cuando cambia, dos dias consecutivos tienen 23h o 25h reales. Phillips et al. usaron UTC en el paper original. Documentar la decision.

## Resumen — accionable

| ID | Cambio | Coste | Prioridad |
|---|---|---|---|
| U2.1 | Implementar SRI canonico (Phillips 2017) | Medio | BLOCKING |
| U2.2 | Calibrar umbrales a quintiles Windred 2024 | Bajo | Alta |
| U2.3 | Renombrar "regularidad circadiana" → "regularidad sueno-vigilia" | Trivial | Media |
| U2.4 | Concept-card con citas y mediana UK Biobank | Trivial | Alta |
| U2.5 | DataTerminal /home: SRI + quintil | Bajo | Media |
| U2.6 | Heatmap diario (alternativa o complemento al scatter) | Medio | Baja |
