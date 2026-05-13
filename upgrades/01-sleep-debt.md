# 01 — Deuda de sueno

## Lo que computa Somnus hoy

`lib/core/services/sleep_debt.dart:50-106`

```
deuda = max(0, suma_de_deficits − suma_de_superavits × 0.75)
ventana = 7 / 14 / 30 dias (default 14)
deficit_dia = max(0, target − horas)
superavit_dia = max(0, horas − target)
```

Las noches sin registrar se saltan (no acumulan deuda).

## Evidencia verificada

### Ventana de 14 dias

`[VERIFIED]` Van Dongen HPA, Maislin G, Mullington JM, Dinges DF (2003). *Sleep* 26(2):117-126. PMID: [12683469](https://pubmed.ncbi.nlm.nih.gov/12683469/).

> Diseno: 48 adultos sanos (21-38 anos), randomizados a 4h, 6h u 8h de tiempo en cama (TIB) durante **14 noches consecutivas**, mas 3 noches de baseline y 3 de recuperacion. Una rama paralela tuvo 3 dias de privacion total (0h TIB).

> Resultado central (literal del abstract): *"Chronic restriction of sleep periods to 4h or 6h per night over 14 consecutive days resulted in significant cumulative, dose-dependent deficits in cognitive performance on all tasks."*

> *"chronic restriction of sleep to 6h or less per night produced cognitive performance deficits equivalent to up to 2 nights of total sleep deprivation."*

> *"Subjects were largely unaware of these increasing cognitive deficits."*

> Modelo: *"lapses in behavioral alertness were near-linearly related to the cumulative duration of wakefulness in excess of 15.84h (s.e. 0.73h)."*

**Implicacion para Somnus.** La ventana de 14 dias por defecto esta directamente alineada con el paradigma canonico de la deuda cronica. El copy de Settings *"14 dias es el estandar clinico"* es defendible. Esta es probablemente la decision con mejor evidencia detras en toda la app.

### Recuperacion no es 1:1

`[VERIFIED via search abstract]` Banks S, Van Dongen HPA, Maislin G, Dinges DF (2010). *Sleep* 33(8):1013-1026. PMID: [20815182](https://pubmed.ncbi.nlm.nih.gov/20815182/).

> Diseno: 5 noches de 4h TIB seguidas de **1 noche** de recuperacion con randomizacion a 0, 2, 4, 6, 8 o 10h TIB.

> Resultado: *"Neurobehavioral deficits induced by 5 nights of sleep restricted to 4h improved monotonically as acute recovery sleep dose increased, but some deficits remained after 10h TIB for recovery. Complete recovery from such sleep restriction may require a longer sleep period during 1 night, and/or multiple nights of recovery sleep."*

`[VERIFIED via search abstract]` Belenky G, Wesensten NJ, Thorne DR, et al. (2003). *J Sleep Res* 12(1):1-12. PMID: [12603781](https://pubmed.ncbi.nlm.nih.gov/12603781/).

> Diseno: 66 voluntarios, 3h / 5h / 7h / 9h TIB durante **7 dias**, luego 3 dias de recuperacion a 8h TIB.

> Resultado: en el grupo 3h, las lapsus del PVT (>500 ms) crecieron monotonicamente sin estabilizarse. En 5h y 7h se estabilizaron a un nivel reducido. La recuperacion con 3 x 8h **no restauro completamente** el rendimiento en los grupos restringidos.

**Implicacion para Somnus.** Un factor 0.75 implica que 3h de superavit cancelan 2.25h de deficit acumulado. La evidencia indica que ni siquiera **una unica noche de 10h** restaura completamente tras 5 noches de 4h, y que **3 noches de 8h** tampoco restauran tras 7 dias de 3h. El factor 0.75 esta optimisticamente calibrado.

## Diagnostico

### El factor 0.75 subestima la deuda

Para que la curva de recuperacion sea compatible con Banks 2010 y Belenky 2003, hace falta:

1. Un coeficiente significativamente menor (algo cercano a **0.5 o menos**).
2. **Saturacion**: cada hora adicional de superavit aporta menos que la anterior (en Banks, la pendiente de mejora se aplana entre 8h y 10h de recuperacion).
3. **Limites**: superavits >2-3h por encima del target probablemente no aportan nada en una sola noche.

La implementacion actual aplica un descuento lineal sin saturacion, sin limites por noche, y con un coeficiente alto.

### El modelo es coarse pero la direccion es correcta

Hay que reconocer lo positivo: la mayoria de apps de consumo (Sleep Cycle, Apple Health) restan superavits 1:1 o ignoran la deuda. Somnus al menos modela que la recuperacion es asimetrica. La direccion del coeficiente es correcta; solo la magnitud es generosa.

## Upgrades

### `[BLOCKING]` U1.1 — Bajar `recoveryFactor` a 0.5

Trivial. Cambia `static const double recoveryFactor = 0.75` a `0.5` en `sleep_debt.dart:50`.

Anade en `debt_screen.dart:135` el copy:

> *"La recuperacion no es 1:1. Banks 2010: ni siquiera 10h de recuperacion restauran del todo tras 5 noches de 4h. Somnus aplica un factor del 50%."*

Coste: 1 linea de codigo + 1 frase. Impacto: alineacion con literatura y mantencion de la promesa show-the-truth.

### U1.2 — Saturacion en el descuento

Sustituir el descuento lineal por uno que sature:

```dart
// Por noche, el credito maximo es 2h
final cappedSurplus = min(entry.surplus, 2.0);
// Aplicar descuento decreciente
cumulativeDebt -= cappedSurplus * recoveryFactor * exp(-running / 10);
```

Razonamiento `[MECHANISTIC]`: si la deuda acumulada es muy grande, una sola noche de superavit aporta menos en terminos relativos. La saturacion exponencial es una aproximacion barata pero defensible. **No hay un modelo cuantitativo cerrado en la literatura humana**, asi que esto debe ofrecerse como heuristica con copy honesto: *"aproximacion conservadora basada en evidencia de recuperacion incompleta"*.

Coste: bajo. Impacto: medio.

### U1.3 — Slider parametrico de factor en Settings

Anadir en `settings_screen.dart` un slider 0.3-0.8 para `recoveryFactor`. Persist en `configEntries`.

Copy:

> *Factor de recuperacion: 0.5*
>
> *0.3: conservador. La deuda apenas se compensa con superavits, modela Banks 2010 sin recuperacion incompleta.*
> *0.5: por defecto. Compromiso entre Banks 2010 y la intuicion del usuario.*
> *0.8: permisivo. Los superavits compensan casi 1:1 (no respaldado por evidencia).*

Coste: bajo. Impacto: dar control sin abandonar el rigor.

### U1.4 — Mostrar "cumulative excess wakefulness"

Van Dongen 2003 propuso que **las lapsus de atencion son lineales en la vigilia acumulada por encima de 15.84h**. Esto sugiere mostrar, junto a la deuda, un segundo numero:

> *VIGILIA EXCEDENTE 23.4h*

Calculo: por cada noche, vigilia = 24h − horas_dormidas. Exceso = max(0, vigilia − 15.84h). Suma sobre la ventana. Es un dato derivado de Van Dongen 2003 directamente y tiene proceddencia mas limpia que la "deuda de sueno" en horas.

Es una metrica complementaria, no sustitutiva. Coste: medio. Impacto: medio. Antes de implementar, releer la Tabla del paper para confirmar la formula exacta del modelo. `[NEEDS-VERIFICATION en pase futuro]`

### U1.5 — Charts: anadir linea de target medio

Hoy el barchart muestra horas por noche con linea horizontal target. El linechart de deuda acumulada solo muestra deuda. Anadir una segunda serie en el linechart con la **vigilia acumulada** (eje secundario), permitiria ver simultaneamente "cuanto debo" y "cuanto he estado despierto".

Coste: bajo (fl_chart lo soporta). Impacto: bajo a menos que se haga muy bien.

### U1.6 — Subestimacion subjetiva, hacerla visible

El abstract de Van Dongen 2003 dice literalmente: *"Subjects were largely unaware of these increasing cognitive deficits."*

Esto es **el hallazgo psicologicamente mas potente** del estudio y la app no lo refleja. Propuesta: en `/debt`, despues de N noches con deuda creciente, mostrar un info-box discreto:

> *PERCEPCION:*
> *Van Dongen 2003: los sujetos restringidos a 6h o menos durante 14 dias tenian deficits cognitivos equivalentes a 2 noches sin dormir — y no lo percibian.*

Sin emojis, sin alarmas. Solo el hecho. Coste: trivial. Impacto: alto en credibilidad. Anclalo al volumen de deuda actual, para que no aparezca cuando no hay deuda.

## Que NO hacer

- No anadir prediccion ML de "horas que necesitas dormir hoy para no deber". La literatura no permite extrapolar individualmente con la fidelidad necesaria.
- No mostrar la deuda como un timer en cuenta atras o gauge. Es coaching.
- No introducir el termino "sleep score" agregado. Composite arbitrario que esconde mas que revela.

## Resumen — accionable

| ID | Cambio | Coste | Prioridad |
|---|---|---|---|
| U1.1 | recoveryFactor: 0.75 → 0.5 | Trivial | BLOCKING |
| U1.2 | Saturacion en descuento | Bajo | Media |
| U1.3 | Slider parametrico en Settings | Bajo | Media |
| U1.4 | Mostrar vigilia excedente (15.84h) | Medio | Media |
| U1.5 | Linea de vigilia acumulada en chart | Bajo | Baja |
| U1.6 | Info-box "Van Dongen — no lo percibes" | Trivial | Alta |
