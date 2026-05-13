# 06 — Rutinas (wind-down y wake-up)

## Lo que tiene Somnus hoy

`lib/core/database.dart:179-220`

**Wind-down (orden actual):**

1. Atenua iluminacion (10 min)
2. Sin pantallas (30 min)
3. Temperatura fresca 18-20 °C (5 min)
4. Lectura tranquila (20 min)
5. Respiracion 4-7-8 (5 min)

**Wake-up (orden actual):**

1. Luz natural — abre persianas o sal al exterior (5 min)
2. No uses el snooze (1 min)
3. Hidratacion (2 min)
4. Movimiento suave / estiramientos (5 min)
5. Sin cafeina hasta +90 min (0 min)

Cada step tiene flag `enabled`, descripcion y duracion. La pantalla `/routines` los muestra con togglable switch.

**Bug detectado tras navegar la app**: en `localhost:5050/#/routines` la pestana DESCONEXION muestra "Sin pasos configurados". El seed `insertDefaultRoutines()` se llama desde `onboarding_screen.dart:65`. Si el usuario llega a /home sin completar el onboarding (lo cual es posible en la build web actual — el `app.dart` no parece bloquear navegacion directa), la BD no tiene rutinas y la pantalla es inutil. Bug documentado en `07-ux.md`.

## Evidencia verificada — paso por paso

### Wind-down

#### Step 1 — Atenuar la iluminacion (luz brillante en casa)

`[VERIFIED]` Chang AM, Aeschbach D, Duffy JF, Czeisler CA (2015). PNAS 112(4):1232-1237. PMID: [25535358](https://pubmed.ncbi.nlm.nih.gov/25535358/).

La luz nocturna suprime melatonina y retrasa el reloj. El paper midio LE-eBooks pero el mismo mecanismo (ipRGCs sensibles a 450-480 nm) aplica a iluminacion ambiental. La PRC humana (Khalsa et al. 2003, J Physiol 549:945-952. PMID: [12717008](https://pubmed.ncbi.nlm.nih.gov/12717008/)) muestra que la luz en la **noche biologica temprana** (~3-6h antes del bedtime) causa phase delay.

Implicacion: atenuar luz ~1-2h antes del bedtime es la guideline canonica. La duracion 10 min en el step actual no es "tiempo de exposicion" sino "tiempo de la accion" — el usuario apaga luces, fin. Es engagement con el mundo, no exposicion temporal. Aceptable.

#### Step 2 — Sin pantallas

`[VERIFIED]` Chang AM et al. 2015 (mismo paper). Lectura en LE-eBook (vs libro impreso) durante 4h antes del bedtime: prolongo sleep latency (p=0.009), redujo REM (p=0.029), retraso DLMO, redujo alerta matinal.

Implicacion: cortar pantallas en la **ventana cercana al bedtime** es defendible. La duracion del step (30 min de "sin pantallas" antes de dormir) es **menos exigente** que el experimento (4h) — pragmatica.

#### Step 3 — Temperatura fresca 18-20 °C

`[NEEDS-VERIFICATION primaria — paper no fetchable en este pase por reCAPTCHA]` Okamoto-Mizuno K, Mizuno K (2012). **Effects of thermal environment on sleep and circadian rhythm.** *J Physiol Anthropol* 31:14. PMID: 22738673.

Lo que las revisiones secundarias (Sleep Foundation; Harding et al. 2019) afirman:
- Temperatura optima ambiental para sueno: 18-20 °C, con microclima cutaneo 31-35 °C.
- La caida nocturna de la temperatura corporal central es necesaria para sleep onset (mecanismo `[MECHANISTIC]` — termoregulacion via vasodilatacion distal).
- Desviaciones ↑ wake, ↓ REM, ↓ SWS.

Es razonable mantener el step pero el numero exacto y los limites de evidencia no han sido verificados en primaria este pase.

#### Step 4 — Lectura tranquila (papel o e-ink)

Razonable como sustituto de pantallas. La eficacia para sueno per se no esta documentada en un RCT especifico (es una de las recomendaciones generales de sleep hygiene incluidas en CBT-I). `[MECHANISTIC + tradicion clinica]`.

Recomendaciones generales: papel o e-ink sin retroiluminacion, contenido ligero, evitar tramas estimulantes.

#### Step 5 — Respiracion 4-7-8

`[NEEDS-VERIFICATION primaria]` La tecnica popularizada por Andrew Weil (no es pranayama yogica original). No hay RCT grande con sueno como outcome primario que yo haya verificado en este pase.

Lo que se sabe `[MECHANISTIC]`:
- Respiracion lenta (especialmente con exhalacion prolongada) aumenta tono vagal → ↓ HR → activacion parasimpatica.
- Algunos estudios pequenos muestran ↑ HRV en agudo.
- La aplicacion al sueno se infiere indirectamente.

Defendible como herramienta de bajo coste, pero **no se puede vender con la misma autoridad** que Drake 2013 o Chang 2015. El step actual no exagera ("activa el sistema parasimpatico" es correcto).

### Wake-up

#### Step 1 — Luz natural

`[VERIFIED]` Khalsa SBS, Jewett ME, Cajochen C, Czeisler CA (2003). *J Physiol* 549:945-952. PMID: [12717008](https://pubmed.ncbi.nlm.nih.gov/12717008/).

La PRC humana muestra que la luz en la **manana biologica** produce phase advances. Esta es la intervencion circadiana mas potente que existe sin farmacos.

`[VERIFIED — Phillips 2017]`: los Irregular sleepers mostraban amplitud de luz mucho menor (102 lux vs 179 lux en los Regular) y DLMO mas tardio. El patron de luz **es** la entrada principal al reloj.

**Numeros relevantes** (de revisiones citadas en `[VERIFIED via search]`, no de primaria leida este pase):
- Sol directo: 10,000 - 100,000 lux.
- Luz exterior nublada: 1,000 - 10,000 lux.
- Luz interior tipica: 100 - 500 lux.
- 30 min de luz brillante (>2,500 lux) en la primera hora tras despertar produce phase advances medibles.

**Implicacion**: el step actual dice **5 min**. Es **subdimensionado** respecto a la literatura. Deberia ser 15-30 min. La excusa "5 min es solo para abrir persianas" no se sostiene: la dosis importa.

#### Step 2 — No uses el snooze

`[VERIFIED]` Sundelin T, Landry S, Axelsson J (2024). **Is snoozing losing? Why intermittent morning alarms are used and how they affect sleep, cognition, cortisol, and mood.** *J Sleep Res* 33(3):e14054. PMID: [37849039](https://pubmed.ncbi.nlm.nih.gov/37849039/) · DOI: [10.1111/jsr.14054](https://doi.org/10.1111/jsr.14054).

> Study 1: n = 1732 encuesta. Snoozing es frecuente especialmente en cronotipos vespertinos y jovenes.

> Study 2 (intra-sujeto con polisomnografia): n = 31 snoozers habituales. *"30 min of snoozing improved or did not affect performance on cognitive tests directly upon rising compared to an abrupt awakening."*

> *"Snoozing resulted in about 6 min of lost sleep, while preventing awakenings from slow-wave sleep (N3)."*

> *"There were no clear effects of snoozing on the cortisol awakening response, morning sleepiness, mood, or overnight sleep architecture."*

> *"A brief snooze period may thus help alleviate sleep inertia, without substantially disturbing sleep, for late chronotypes and those with morning drowsiness."*

**Implicacion**: el step actual *"No uses el snooze — cada ciclo de snooze fragmenta el sueno e incrementa la inercia"* esta **directamente contradicho** por el unico estudio con PSG sobre snooze. Es un step que **no deberia existir tal cual** en una app que se presenta como instrument-grade.

#### Step 3 — Hidratacion al despertar

`[NEEDS-VERIFICATION primaria]`. La intuicion "se pierde liquido durante la noche" es correcta (perdida insensible ~500 mL en 8h sin sudoracion adicional). Pero **no hay evidencia robusta de que beber agua en ayunas mejore outcomes especificos**. Es una recomendacion de bajo coste y bajo riesgo, aceptable como step, pero no merece tono de autoridad.

#### Step 4 — Movimiento suave / estiramientos

`[MECHANISTIC]`. Activacion sistemica, vasoconstriccion → vasodilatacion, levanta core body temperature, sirve como senal de "fase activa". Sin RCT especifico que verifique el effect size de 5 min de estiramientos sobre alerta diurna. Razonable.

#### Step 5 — Sin cafeina hasta +90 min

`[VERIFIED por mecanismo, NO por RCT]`. El razonamiento descansa en:

1. **Cortisol Awakening Response (CAR)**: pico de cortisol 30-45 min tras despertar (Pruessner et al. 1997; multiples replicaciones). `[NEEDS-VERIFICATION primaria]`.
2. **Adenosine load** bajo al despertar (Landolt y otros).
3. **Inferencia**: si el cortisol esta haciendo el trabajo de despertar, anadir cafeina (que bloquea A1/A2a) en ese momento es redundante; mover la cafeina a despues del pico (~90 min) podria ser mas eficiente.

**Importante**: esta logica fue popularizada por Andrew Huberman. **No existe RCT con outcomes objetivos** (alertness, PVT, daily energy curve) comparando cafeina inmediata vs +90 min post-despertar. La regla es **mecanisticamente plausible pero no probada**.

Implicacion: el step deberia marcarse claramente como **experimental** o **opcional**, no como sleep hygiene establecido.

## Diagnostico

### Honestidad asimetrica

Hay dos categorias de steps en la rutina actual:

**Categoria A — respaldo solido**:
- Sin pantallas (Chang 2015)
- Luz natural matinal (Khalsa 2003)
- 4-7-8 (mecanismo solido aunque sin RCT con sueno como outcome)

**Categoria B — sin RCT especifico**:
- No snooze (**contradicho por Sundelin 2024**)
- Cafe +90 min (mecanismo plausible, sin RCT)
- Hidratacion al despertar (intuitivo, sin RCT)
- Estiramientos (mecanismo, sin RCT)

Hoy Somnus presenta A y B con identico peso visual. Eso es una decision de presentacion incoherente con "instrument-grade".

### Dosis subdimensionada en luz matinal

5 min es insuficiente. Deberia ser 15-30 min, anclado a la primera hora tras despertar.

## Upgrades

### `[BLOCKING]` U6.1 — Anadir `evidenceRef` y `evidenceTier` al schema RoutineSteps

Migracion v3:

```dart
class RoutineSteps extends Table {
  // ... existente ...
  TextColumn get evidenceRef => text().nullable()(); // ej: "Chang 2015, PNAS"
  TextColumn get evidenceTier => text().withDefault(const Constant('mechanistic'))(); // 'rct' | 'verified' | 'mechanistic' | 'tradition'
  TextColumn get evidenceDoi => text().nullable()();
}
```

Mostrar en `_StepCard` (`routines_screen.dart:179`):

```
1   ATENUA LA ILUMINACION                   10m
    Reduce la exposicion a luz intensa en casa.
    [VERIFIED] Chang 2015 (PNAS) · Khalsa 2003 (J Physiol)
```

```
2   NO USES EL SNOOZE                       1m
    [TRADITION] Folclore de sleep hygiene. Sundelin 2024 (J Sleep Res, n=31, PSG): 30 min de snooze
    no afectan cortisol, animo, ni arquitectura nocturna. Considera desactivar este paso.
```

Coste: bajo. Impacto: muy alto en identidad.

### `[BLOCKING]` U6.2 — Reescribir el step "No snooze"

Opcion A (recomendada): cambiar el paso a:

```
SNOOZE BREVE                             6m
Snooze de hasta 30 min es aceptable. Sundelin 2024 (J Sleep Res, n=31, PSG):
sin efecto sobre cognicion, cortisol, animo, ni arquitectura del sueno.
Lost sleep ~6 min. Util para cronotipos vespertinos.
```

Opcion B: eliminar el step.

Opcion C (menos preferida): mantener pero con copy honesto: *"La evidencia experimental (Sundelin 2024) no respalda esta recomendacion. Mantenemos el step como sleep hygiene tradicional, no como guideline probada."*

Coste: trivial. Impacto: corregir afirmacion contradicha por evidencia.

### `[BLOCKING]` U6.3 — Marcar `Sin cafeina +90 min` como experimental

```
CAFE: DIFIERE 60-90 MIN                  0m
Mecanismo: el cortisol awakening response cubre los primeros 30-90 min.
EXPERIMENTAL: sin RCT que lo confirme. Util si dependes de la cafeina; opcional.
```

Coste: trivial. Impacto: alineacion con "show the truth".

### U6.4 — Subir el step de luz matinal a 15-30 min

```
1   LUZ NATURAL                              20m
    15-30 min de luz exterior en la primera hora tras despertar. Adelanta fase
    circadiana (Khalsa 2003, J Physiol). 100,000 lux exterior vs ~300 lux interior.
```

Coste: trivial. Impacto: alto en eficacia real.

### U6.5 — Anadir un step de "Luz brillante artificial si no hay sol"

Para inviernos en latitudes altas o personas en casa sin acceso a exterior:

```
ALTERNATIVA: LIGHTBOX                     20m
Si no hay sol, una caja de luz de 10,000 lux a ~30 cm durante 20 min produce
phase advance similar (Eastman & Burgess revisiones).
```

Coste: bajo. Impacto: medio. Para cierto perfil de usuario es la diferencia entre que el step sea util o decorativo.

### U6.6 — Reordenar wind-down por dependencias

Hoy el orden es: atenuar luz → sin pantallas → temperatura → lectura → respiracion.

La temperatura (cool down de la habitacion) tarda en surtir efecto. Reordenar:

1. Temperatura fresca (5 min — el aire necesita tiempo para enfriar)
2. Atenuar la iluminacion (10 min)
3. Sin pantallas (30 min)
4. Lectura tranquila (20 min)
5. Respiracion 4-7-8 (5 min)

Coste: trivial. Impacto: bajo, pero coherente.

### U6.7 — Modo "rutina practica" — flujo guiado con timer

Hoy `/routines` muestra una lista estatica con switches. Falta un modo "practica" donde el usuario, una hora antes de dormir, abre la pantalla y se le guia paso a paso con timer.

Estilo factory.ai/Linear:

```
WIND.DOWN — STEP 2/5

DIM SCREENS                       28:42 / 30:00
                                  ▰▰▰▱▱▱▱▱▱▱▱▱

Drop the phone. Drop the laptop. Drop everything.
```

Sin musica, sin animaciones de respiracion azules tipo Calm. Solo el numero, el progreso, el texto.

Coste: medio. Impacto: alto en utility real (la rutina pasa de "ver una lista" a "ejecutar un protocolo").

### U6.8 — Permitir steps personalizados

Schema ya lo soporta (insercion arbitraria). Falta UI para anadir/editar/borrar steps. Hoy solo se pueden togglear.

Coste: medio. Impacto: medio. Honesto con el manifiesto: la rutina ideal es personal, no pre-empacada.

### U6.9 — Anclar la luz matinal y el inicio de wind-down

Hoy `routines_screen.dart:152-156` dice *"Empieza Xm antes de dormir"* para wind-down y *"Al despertar"* para wake-up. Mejor: mostrar la hora absoluta calculada desde `targetBedtime` / `targetWakeTime`.

```
WIND.DOWN.START → 21:50
WAKE.UP.START   → 07:00
```

Coste: trivial. Impacto: medio.

## Resumen — accionable

| ID | Cambio | Coste | Prioridad |
|---|---|---|---|
| U6.1 | Anadir `evidenceRef` y `evidenceTier` por step | Bajo | BLOCKING |
| U6.2 | Reescribir o eliminar el step "No snooze" | Trivial | BLOCKING |
| U6.3 | Marcar "Cafe +90 min" como experimental | Trivial | BLOCKING |
| U6.4 | Luz matinal: 5 min → 15-30 min | Trivial | Alta |
| U6.5 | Anadir alternativa lightbox | Bajo | Media |
| U6.6 | Reordenar wind-down (temperatura primero) | Trivial | Baja |
| U6.7 | Modo "rutina practica" con timer | Medio | Alta |
| U6.8 | UI para crear/editar steps personalizados | Medio | Media |
| U6.9 | Mostrar hora absoluta calculada en cabecera | Trivial | Media |
