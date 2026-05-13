# Somnus — QA científico, contraste con literatura, y propuestas

Auditoría de la app contra la literatura del sueño. Tres bloques: lo que ya hace bien, lo que no se sostiene, y dónde puede crecer sin traicionar el manifiesto (instrument-grade, local-first, sin coaching).

---

## 0. Nota de cobertura

La instancia en `localhost:5050` no fue alcanzable durante esta sesión (la extensión Chrome no estaba conectada y el sandbox no llega al host de macOS). El análisis se hace sobre el código fuente Flutter — `lib/core/services/sleep_debt.dart`, `lib/core/services/circadian.dart`, las cinco pantallas, el esquema Drift y los seeds por defecto de `database.dart`. Para una verificación visual final de la UI renderizada, basta con habilitar la extensión y volver a pedirlo.

---

## 1. Mapa del producto, en una página

| Métrica | Cómo se calcula hoy | Fuente en código |
|---|---|---|
| **Deuda de sueño** | Σ déficits diarios − (Σ superávits × 0.75), ventana 7/14/30 d, clamp ≥ 0 | `sleep_debt.dart:50–106` |
| **Regularidad** | `100 · (1 − σ_bedtime/120 min)`, clamp [0,100] | `circadian.dart:107–116` |
| **Jet lag social** | \|mean(bedtime L–V) − mean(bedtime S–D)\|, en horas | `circadian.dart:119–144` |
| **DLMO estimado** | mean(bedtime) − 120 min | `circadian.dart:147–150` |
| **Bedtime sugerido** | 0.6 · habitual + 0.4 · objetivo | `circadian.dart:152–167` |
| **Recordatorios** | Café −6h, alcohol −4h, pantallas −2h, rutina −30m, bedtime 0 | `database.dart:236–242` |
| **Wind-down** | Atenuar luz · sin pantallas · 18–20 °C · lectura · 4-7-8 | `database.dart:183–189` |
| **Wake-up** | Luz natural · no snooze · agua · movimiento · café +90m | `database.dart:191–197` |

Privacidad: SQLite local vía Drift, sin red salvo Fitbit opcional. Migración v2 añade `stagesJson` y `efficiencyPct`. Notificaciones locales (zoned daily) via `flutter_local_notifications`.

---

## 2. Lo que está bien anclado a la literatura

**Ventana 14 días.** Es exactamente el paradigma de Van Dongen, Maislin, Mullington & Dinges (2003) — 14 noches consecutivas de restricción a 4h, 6h, 8h. La elección por defecto está literalmente alineada con el experimento canónico de la deuda crónica. El copy en Settings ("14 días es el estándar clínico") es defendible.

**Recuperación no lineal.** El factor 0.75 expresa un principio correcto: la recuperación no es 1:1. Banks & Dinges (2007) y la revisión de Pejovic et al. mostraron que ni una noche larga ni un fin de semana entero recuperan el rendimiento PVT tras 5 noches de restricción a 4h. Direccionalmente, Somnus tiene razón donde la mayoría de apps mienten.

**Cafeína −6h.** Drake et al. (2013), JCSM — 400 mg administrados 6h antes de dormir todavía cuestan ~1h de tiempo total de sueño medido objetivamente. La etiqueta "Último café" anclada a −360 min está respaldada por el único RCT cruzado serio sobre este intervalo concreto.

**Pantallas −2h.** Chang, Aeschbach, Duffy & Czeisler (2015), PNAS — lectura en iPad antes de dormir suprime melatonina, retrasa DLMO y reduce alerta a la mañana siguiente. La AASM y la NSF coinciden en cortar ~2h antes. Defendible.

**Temperatura 18–20 °C.** Okamoto-Mizuno & Mizuno (2012) y la revisión de Kräuchi sobre termorregulación coinciden: óptimo 19–21 °C ambiental para mantener microclima cutáneo 31–35 °C. El step está en el rango correcto.

**DLMO ≈ bedtime −2h.** Burgess y colaboradores documentan que la melatonina sube ~2–3h antes del inicio habitual de sueño. La heurística mínima de Somnus es razonable como primera aproximación.

**4-7-8.** No hay RCTs grandes pero la mecánica vagal/parasimpática es plausible y respaldada por estudios pequeños sobre HRV y respiración lenta. Es el wind-down step más débil en evidencia pero el más barato en coste/riesgo.

---

## 3. QA crítico — donde la app diverge de la ciencia

### 3.1 La "regularidad" que computa Somnus no es el Sleep Regularity Index

Hoy: desviación estándar del bedtime, normalizada contra 120 min.

Problema: el SRI publicado (Lunsford-Avery, Phillips et al. 2018; Phillips et al. 2017) es la probabilidad de estar en el mismo estado (sueño/vigilia) en dos instantes separados 24h, promediada sobre la ventana. Escala 0–100. Es lo que Windred et al. (2024, UK Biobank) muestra como **predictor de mortalidad más fuerte que la duración del sueño**: hazard ratio 1.53 para SRI percentil 5 vs mediana. El umbral de riesgo en esa cohorte es **SRI < 70**.

La métrica actual ignora:
- La hora de despertar (mitad del comportamiento circadiano).
- Las siestas o discontinuidades.
- Las desviaciones simétricas: alguien que duerme 23:00 ± 5 min toda la semana excepto un sábado a las 04:00 sale con la misma σ que alguien que oscila ±60 min cada día. El SRI los separa con claridad.

**Implicación para el copy**: la pantalla Schedule llama "regularidad circadiana" a algo que es "consistencia del bedtime". El concept-card es engañoso.

### 3.2 El jet lag social está midiendo bedtime, no midsleep

Hoy: `|mean(bedtime weekday) − mean(bedtime weekend)|`.

Problema: Roenneberg & Wittmann (2006, *Curr Biol*; 2012, *Curr Biol* sobre obesidad) definen jet lag social como **|MSF − MSW|**, donde MS = punto medio entre inicio y fin de sueño. La métrica "bedtime" no es invariante al patrón "me acuesto igual pero el finde duermo dos horas más". Esa persona tiene jet lag social real (~1h de desfase del punto medio) y Somnus se lo perdería.

Además, "free day" ≠ sábado/domingo. Para shift workers, freelancers o estudiantes con horarios atípicos, la regla Mon–Fri/Sat–Sun es estructuralmente errónea. El MCTQ define "free days" por ausencia de despertador, no por etiqueta de calendario.

Umbrales actuales (0.5/1/2h) están bien — `>1h` se asocia con riesgo metabólico (Wittmann 2006, Parsons 2015) y `>2h` con peor salud mental (revisiones recientes).

### 3.3 DLMO anclado al bedtime, no al wake-time

Hoy: `DLMO = mean(bedtime) − 120 min`.

Problema: Burgess y otros documentan que **DLMO correlaciona más fuerte con wake-time (r ≈ 0.77) que con bedtime (r ≈ 0.36)**. El reloj interno se ancla mejor a cuándo te expones a luz por la mañana que a cuándo decides apagar la lámpara. La constante 120 min también es promedio poblacional; varía ~60–180 min entre cronotipos.

Mejor heurística: ancla al wake-time del usuario y, si hay datos, ajusta por cronotipo inferido del midsleep.

### 3.4 "No uses el snooze" — paso desactualizado

Hoy: Wake-up step #2 desaconseja el snooze.

Problema: Sundelin et al. (2024, *J Sleep Res* — "Is snoozing losing?") — laboratorio con polisomnografía, 31 snoozers habituales: 30 min de snooze **no perjudicaron** la cognición al levantar (en algunos tests, mejoraron), no afectaron la respuesta de cortisol al despertar, ni el ánimo, ni la arquitectura nocturna. La "regla" que Somnus repite es folklore.

Honestamente: si el manifiesto es "show the number, don't cushion it", el step debería citar la evidencia, no la creencia popular.

### 3.5 Café +90 min — popular, no probado

Hoy: Wake-up step #5 dice esperar 90 min al café.

Problema: la regla de Huberman es mecanísticamente plausible (CAR pica 30–45 min post-wake, decae 60–90 min después; el adenosine load es bajo justo al despertar). Pero no hay RCT que muestre beneficio sobre energía/cognición al diferir el café 90 min vs inmediato en humanos sanos. La revisión de literatura sobre cafeína al despertar es ambigua.

Para una app cuyo lema es no coaching, vender una regla bro-science con el mismo peso que Drake 2013 desbalancea la credibilidad.

### 3.6 Factor de recuperación 0.75 — generoso

Banks et al. (2010) y trabajo posterior: 5 noches de 4h, una noche de recuperación de 10h **no restauró completamente** PVT, somnolencia, ni fatiga. Sustainably, las diferencias persisten más de una semana. Un factor 0.75 implica que 3h de superávit cancelan 2.25h de déficit — la evidencia sugiere algo más cercano a 0.4–0.5, y con saturación: la 6ª hora de superávit aporta mucho menos que la 1ª.

No es un error grave (la dirección es correcta y mejor que la mayoría de apps), pero la calibración optimista significa que la app subestima la deuda real. Si el ethos es "show the truth", el factor debería ser más conservador o explícitamente paramétrico.

### 3.7 Luz matinal de 5 minutos — insuficiente

Hoy: Wake-up step #1, "Luz natural, 5 min".

Problema: revisión sistemática (Blume et al. 2019; Wright et al. 2013): la respuesta dosis-tiempo de avance de fase es aproximadamente lineal entre 0.2 y 2.5h, plateau después. 5 minutos a 100k lux exterior ya dan algo, pero la literatura recomienda 15–30 min en la primera hora tras despertar. El step subestima la dosis útil.

### 3.8 "Calidad del sueño" excluida — defendible, pero parcial

El README justifica no medir calidad porque exige equipo hospitalario. Es razonable para PSG, pero hoy actigrafía + variabilidad cardíaca (Fitbit Sense, Apple Watch, Whoop, Polar) da estimaciones útiles de eficiencia, latencia, despertares y arquitectura aproximada. El schema v2 ya prevé `stagesJson` y `efficiencyPct` desde Fitbit. La postura pública del README ("no consideramos calidad") y la postura del código (sí, vía integración) están desalineadas.

### 3.9 Gaps de robustez no relacionados con ciencia

- `_circularMean` desempaqueta valores con respecto a la mediana, pero si los datos tienen bimodalidad real (turnos partidos, viajes), el unwrap puede romperse y dar medias incoherentes.
- El registro permite `hoursSlept` 1–13h por slider, sin distinguir sueño nocturno principal de siestas. La ciencia de la deuda asume el episodio principal.
- Cuando no hay `bedtime`, el registro sigue contando para deuda pero no para circadiano. Es consistente, pero un usuario que registra solo horas verá DLMO/regularidad vacíos sin entender por qué.
- Las notificaciones se cancelan con `cancelAll` y se reprograman cada vez (`notifications.dart:55`). Si el usuario tiene reminders de otra app con IDs colisionando es improbable, pero conviene namespaceando.

---

## 4. QA de UX, alineado con `PRODUCT.md`

El manifiesto define cinco principios: instrument over app, privacy as identity, cold precision, eclectic restraint, earn every element. Auditoría rápida:

**Aciertos.** Home con `_DataTerminal` (etiquetas en caps tracking 1.5, mono para valores) es exactamente la voz factory.ai/Urbit. El hero del Debt screen con "DEUDA ACUMULADA" en label small + número 56pt weight 100 es el tipo de jerarquía instrument-grade. El "swipe to delete" del SleepRecordTile es el gesto correcto: directo, sin confirmación condescendiente. El reset bajo "Zona peligrosa" con confirmación explícita es coherente con privacy-as-identity.

**Tensiones.**
1. **Concept cards en Schedule (`_ConceptCard`)** — son párrafos de 3–4 líneas con título verde, en un producto que dice "earn every element". Funcionan en onboarding pero permanecen visibles siempre. Considera plegarlos detrás de un icono `?` discreto, o quitarlos.
2. **Wake-up step "No uses el snooze"** — además de la imprecisión científica, el tono ("Cada ciclo de snooze fragmenta el sueño") es coaching motivacional. Contradice "cold precision over warm comfort".
3. **Emojis en reminders** (`'Último café ☕'`, `'Última copa 🍷'`) — colorea contra el manifiesto. Linear no usa emojis. Factory.ai no usa emojis. Sería más coherente: `LAST.COFFEE`, `LAST.DRINK`, `DIM.SCREENS`, `WIND.DOWN`, `BED`.
4. **"Conceptos" en Schedule + "Sobre la deuda" en Debt** — son la misma capa de explicación pegada al final de cada screen. Si quieres mantenerla, mejor centralizada en un `/glossary` accesible desde el AppBar de cualquier screen.
5. **Colores de regularidad** — la lógica devuelve verde ≥75, naranja ≥50, rojo <50. Pero el umbral predictivo de mortalidad en Windred 2024 es SRI < 70. El gradiente de Somnus está más relajado que la literatura sugiere. Si el ethos es show-the-truth, sea estricto: ≥80 verde, ≥70 ámbar, <70 rojo.
6. **Onboarding cita** — "Never waste any time you can spend sleeping" (presumiblemente George R.R. Martin) es lo único en la app con tono motivacional. El manifiesto pide instrument-grade. La cita es agradable pero estilísticamente fuera de personaje.
7. **"En objetivo" / "Déficit"** son labels emocionales suaves. Más cold: `DELTA: −1.2h`, `STATE: BELOW`, `STATE: ON-TARGET`. Esa es la voz Urbit.
8. **El indicador de paginación del onboarding** (línea 110–123) con barra animada que crece a 24px es deliberadamente "cute". Un solo carácter mono — `01/03`, `02/03`, `03/03` — sería más coherente.

**Accesibilidad.** No revisé contrastes a píxel pero el theme menciona kSubtle/kMuted como grises. Conviene auditar AA contra el verde acento sobre fondo `#0A0A0A`. WCAG AA exige 4.5:1 para texto normal. El `kGreen` actual contra `kSurface` quizá no llegue.

**Reduced motion.** El `AnimatedOpacity(200ms)` en steps y reminders y el `AnimatedContainer(300ms)` en el page indicator no consultan `MediaQuery.disableAnimations`. Trivial, pero hace falta para cumplir el manifiesto.

---

## 5. Propuestas — features nuevas y refinamientos

Ordenadas por: ratio (impacto científico × coherencia con manifiesto) / coste de implementación.

### 5.1 Reemplazar la "regularidad" por el SRI canónico

**Qué.** Implementar el Sleep Regularity Index de Phillips/Lunsford-Avery: para cada minuto del día, calcular la probabilidad de que el estado (asleep/awake) sea el mismo a t y t+24h, promediar.

**Por qué.** Es el único predictor de mortalidad con mejor capacidad que la duración (Windred 2024, UK Biobank, n=88,975). Reemplazar la σ_bedtime por SRI te da un número con backing prospectivo serio. El display ("regularidad: 73%") no cambia, pero el número detrás sí.

**Esfuerzo.** Medio. Requiere que el SleepRecord almacene también el rango (bedtime + wakeTime), lo que ya está soportado opcionalmente. Para registros que solo tengan `hoursSlept`, se puede excluir o asumir bedtime ± hoursSlept/2 centrado. Una implementación de referencia: bins de 5 min, ventana de 7+ días.

**Caveat.** El SRI necesita 7 días para ser estable. Mantener la métrica simple como fallback con < 7 noches.

### 5.2 Jet lag social usando midsleep, no bedtime

**Qué.** `socialJetLag = |midsleep_workdays − midsleep_freedays|`, donde `midsleep_i = (bedtime_i + (bedtime_i + hours_i)/2) % 24h`, con corrección opcional MSFsc.

**Por qué.** Es la definición de Roenneberg. Cualquier usuario que lea sobre el tema fuera de la app verá midsleep y debe coincidir.

**Esfuerzo.** Bajo. La fórmula está en circadian.dart en 5 líneas. Requiere que la fecha del registro permita inferir si es "free" — opción A: setting "días laborales" en Settings (default Mon–Fri); opción B: detectar free days como aquellos donde el bedtime/wake desvían >1h.

### 5.3 DLMO refinado por wake-time y datos suficientes

**Qué.** Reemplazar `mean(bedtime) − 120 min` por una estimación bayesiana: prior = `wake_time − 14h`, evidencia = `bedtime − 2h`, suficiencia = ≥5 días regulares (σ_wake < 60 min). Si no hay regularidad, no mostrar DLMO.

**Por qué.** Burgess: DLMO correla con wake-time (r=0.77) >> bedtime (r=0.36). Mostrar un DLMO con 3 días de datos irregulares es engañar.

**Esfuerzo.** Bajo. Ya existe el wake-time en el modelo.

### 5.4 Recovery factor honesto y paramétrico

**Qué.** Bajar el `recoveryFactor` por defecto a 0.5 o exponer un slider en Settings (0.3–0.8) con copy: "0.5 = un fin de semana largo no compensa una semana corta. 0.8 = compensación cercana a 1:1 (literatura sugiere lo primero)".

**Por qué.** Banks/Belenky. El 0.75 actual subestima deuda y debilita la promesa "show the truth".

**Esfuerzo.** Trivial. 1 línea + UI.

### 5.5 Wind-down y wake-up con citas inline

**Qué.** Cada step lleva un campo opcional `evidenceRef` (string corto, por ej. `"Drake 2013, JCSM"` o `"Chang & Czeisler 2015, PNAS"`). Renderizar como subtítulo gris pequeño bajo la descripción.

**Por qué.** Manifiesto pide instrument-grade, anti-coaching. Un usuario técnico quiere ver de dónde viene el número. Y, secundariamente, presiona al producto a no incluir steps sin respaldo (snooze, café+90).

**Esfuerzo.** Bajo. Migración de schema, un campo más, una línea en `_StepCard`.

### 5.6 Replantear los pasos discutibles

- **Snooze**: cambiar el step a "Snooze ≤ 30 min" con descripción "Sundelin 2024: hasta 30 min de snooze no afecta cognición ni cortisol al despertar. Más allá fragmenta sueño productivo".
- **Café +90 min**: marcar como opcional/experimental, o reescribirlo: "Si tu sueño fue suficiente, retrasar el café 60–90 min puede mejorar el rebote de energía a media mañana. Evidencia: mecanística, no RCT".
- **Luz natural 5 min**: subir a 15–20 min en la primera hora tras despertar. Añadir nota: "100k lux exteriores ≈ 100–200× luz interior".

### 5.7 Gráfico de fase (phase plot)

**Qué.** En `/schedule`, debajo del scatter actual, añadir un círculo de 24h con bands radiales para:
- mediana de bedtime ± σ
- mediana de wake ± σ
- ventana DLMO
- objetivo

**Por qué.** Es el visual más usado en cronobiología (ej. Pittendrigh, Daan). Encaja con la estética instrument: un actográfico/radial-clock en lugar del scatter cartesiano que ya tienes. Eclectic restraint — una sola pieza visual no convencional.

**Esfuerzo.** Medio. fl_chart no tiene polar nativo, pero se hace con CustomPainter en una tarde.

### 5.8 Detección de chronotype (MEQ corto / MCTQ-Light)

**Qué.** En Settings, un cuestionario opcional de 5–6 preguntas (Horne-Östberg corto o MCTQ-Light). Output: cronotipo categórico (early/intermediate/late) + ajuste de la heurística DLMO.

**Por qué.** Permite ajustar las recomendaciones al usuario sin necesidad de muchas noches de datos. Cronotipos extremos tienen DLMO desfasada ±2h del promedio.

**Esfuerzo.** Bajo si MCTQ-Light, mayor si MEQ completo.

### 5.9 "Conciencia de impairment" — micro-PVT integrada

**Qué.** En el Home, opcional, un test de 60 segundos tipo PVT (Psychomotor Vigilance Task): puntos que aparecen aleatoriamente, mide reaction time. Persistir el percentil personal en función de horas dormidas.

**Por qué.** Van Dongen mostró que el subject percibe poco su propio deterioro. Una métrica objetiva diaria — sin gamificación, sin streaks, sin badges — es exactamente lo que el manifiesto pide: datos para que decidas. Apple/Whoop no lo hacen así porque rompe el feel-good. Es una elección distintiva.

**Esfuerzo.** Medio. Un Stateful con timer, una tabla `pvt_runs`. Crítico: anti-pattern = streaks, gamificación, "tu mejor tiempo".

### 5.10 Export / sovereignty primitives

**Qué.** Botón en Settings: `Export → JSON / CSV`. Botón paralelo: `Verify schema → SHA-256 del SQLite`. Posible: import desde Health Connect / Apple HealthKit con consentimiento explícito.

**Por qué.** Local-first sin export portable es local-prison. Urbit-grade soberanía implica que el usuario puede irse llevándose todo. Es coherente con el manifiesto, low effort, alto valor de identidad.

**Esfuerzo.** Bajo.

### 5.11 Modo "sin gráficos" para alta carga cognitiva

**Qué.** Toggle en Settings: "modo terminal". Reemplaza charts por tablas mono. Mismas métricas, sin píxeles de adorno.

**Por qué.** El manifiesto cita Urbit como referencia. El usuario al despertar en cuarto oscuro no necesita un line chart suave; necesita números. Es la elección eclectic restraint canónica.

**Esfuerzo.** Bajo.

### 5.12 Recordatorios contextuales por chronotype

**Qué.** Hoy, todos los reminders son offsets fijos contra `targetBedtime`. Si el usuario es eveningchronotype con DLMO real 02:00, "última café −6h = 20:00" puede ser conservador. Permitir anclar reminders a DLMO estimado en vez de a bedtime objetivo.

**Por qué.** Roenneberg muestra que el chronotype intermedio es minoritario en poblaciones jóvenes urbanas. Una app de precisión debería respetar la fisiología real, no el horario aspiracional.

**Esfuerzo.** Bajo. `offsetMins` ya existe; añadir `anchor: 'bedtime' | 'dlmo'`.

### 5.13 Light log — micro-feature potente

**Qué.** Un botón opcional en wake-up routine para registrar "Luz exterior: 0 / 5 / 15 / 30+ min". Correlar con regularidad/jet lag en `/schedule`.

**Por qué.** Wright et al. (2013) mostraron que dos días de camping reentrena DLMO. La luz matinal es la variable de intervención circadiana #1. Si no la mides, no puedes mostrar su efecto. El registro pesa 1 entero adicional en `SleepRecords`.

**Esfuerzo.** Bajo.

### 5.14 Métricas por encima del fold revisadas

Hoy en Home: anoche, deuda, regularidad, DLMO. Considerar:
- Reemplazar `dlmo` por `próxima ventana de sueño` (DLMO–DLMO+6h) — más accionable.
- Añadir `jet lag social` aquí también (mismo peso predictivo que regularidad).
- Quitar DLMO si <5 noches regulares; mostrar "datos insuficientes" en su lugar.

---

## 6. Riesgo de "saber demasiado" y postura clínica

Una app que muestra DLMO, jet lag social y deuda con cifras precisas puede inducir orthosomnia — ansiedad iatrogénica por sueño perfecto, descrita por Baron et al. (2017). El manifiesto explícitamente rechaza coaching, lo cual es protector, pero conviene:

- No usar lenguaje alarmista en el copy ("riesgo metabólico" en concept-cards está cerca de la línea — está bien si va acompañado de cifras y fuentes).
- Permitir un modo "no metrics" donde la app es solo log + recordatorios, sin scores. Es un setting que muchos usuarios técnicos agradecen: data sí, ranking no.
- En la primera sesión, no mostrar puntuación 0% por ausencia de datos — eso ya está hecho con el "—" placeholder. Mantener.

---

## 7. Cosas que NO recomiendo

- **Notificaciones motivacionales** — rompe el manifiesto.
- **Streaks / badges / "noches consecutivas"** — Whoop/Oura hacen esto. Es exactamente lo que Somnus no debería ser.
- **Sleep score agregado tipo Oura "85"** — composite arbitrario que esconde más que revela. Cuatro números explícitos > un número opaco.
- **Cloud sync opt-in** — viola la identidad. Si alguien lo pide, export JSON ya cubre 95% de la utilidad real.
- **Predicción ML del sueño óptimo** — requiere modelo, datos, validación. Para una app local-first sin telemetría, el coste de overfit/error/falsa precisión supera el valor.
- **Integración con asistentes (Siri/Google)** — atajo a privacy creep.

---

## 8. Resumen de acciones — orden sugerido

1. Bajar `recoveryFactor` a 0.5 + copy explícito. *(trivial, alto impacto en honestidad)*
2. Migrar regularidad a SRI canónico. *(medio, recupera capacidad predictiva)*
3. Cambiar jet lag social a midsleep. *(bajo)*
4. Reescribir los dos steps débiles (snooze, café+90). *(trivial)*
5. Añadir `evidenceRef` a routine steps. *(bajo)*
6. Phase plot circular en `/schedule`. *(medio, alto en identidad)*
7. Export JSON/CSV. *(bajo, alto en identidad)*
8. Micro-PVT diario opcional. *(medio, distintivo)*

---

## 9. Fuentes

Las afirmaciones cuantitativas y los anchors numéricos del análisis vienen de:

- Van Dongen, Maislin, Mullington & Dinges (2003). *The cumulative cost of additional wakefulness*. SLEEP, 26(2), 117–126. [PubMed](https://pubmed.ncbi.nlm.nih.gov/12683469/) · [PDF](https://www.med.upenn.edu/uep/assets/user-content/documents/Van_Dongen_Dinges_Sleep_26_3_2003.pdf)
- Banks, Van Dongen, Maislin & Dinges (2010) y trabajo posterior sobre recuperación. [Banking sleep — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC2647785/) · [Neurobehavioral dynamics following chronic sleep restriction — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC2910531/) · [6 weeks of chronic restriction with weekend recovery — Sleep 2021](https://academic.oup.com/sleep/article/44/8/zsab051/6149527)
- Phillips et al. (2017), Lunsford-Avery et al. (2018) — definición original del Sleep Regularity Index.
- Windred et al. (2024). *Sleep regularity is a stronger predictor of mortality risk than sleep duration*. SLEEP. [PubMed](https://pubmed.ncbi.nlm.nih.gov/37738616/) · [Oxford Academic](https://academic.oup.com/sleep/article/47/1/zsad253/7280269) · [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10782501/)
- Windred et al. (2024). *Sleep regularity and major adverse cardiovascular events — UK Biobank*. [PubMed](https://pubmed.ncbi.nlm.nih.gov/39603689/)
- Roenneberg & Wittmann — Munich ChronoType Questionnaire / MSFsc. [MCTQ](https://www.thewep.org/documentations/mctq) · [Social Jetlag — Roenneberg 2012, Curr Biol](https://www.cell.com/current-biology/fulltext/S0960-9822(12)00325-9) · [Social jet lag review 2022 — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8707256/)
- Burgess et al. — DLMO y su relación con bedtime/wake-time. [Comparing MEQ/MCTQ to DLMO — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC4580371/) · [DLMO across ages and chronotype — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10171641/) · [DLMO on regular schedules — PubMed](https://pubmed.ncbi.nlm.nih.gov/15600132/)
- Drake, Roehrs, Shambroom & Roth (2013). *Caffeine effects on sleep taken 0, 3, or 6 hours before bed*. JCSM. [PubMed](https://pubmed.ncbi.nlm.nih.gov/24235903/) · [JCSM](https://jcsm.aasm.org/doi/10.5664/jcsm.3170)
- Ebrahim et al. (2013). *Alcohol and sleep I: effects on normal sleep*. [PubMed](https://pubmed.ncbi.nlm.nih.gov/23347102/) · [Alcohol disrupts sleep homeostasis — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC4427543/) · [Alcohol on sleep: meta-analysis 2024](https://pubmed.ncbi.nlm.nih.gov/39631226/)
- Chang, Aeschbach, Duffy & Czeisler (2015). *Evening use of light-emitting eReaders*. PNAS. [PubMed](https://pubmed.ncbi.nlm.nih.gov/25535358/) · [Harvard Medical School coverage](https://hms.harvard.edu/news/e-readers-foil-good-nights-sleep)
- Okamoto-Mizuno & Mizuno (2012). *Effects of thermal environment on sleep and circadian rhythm*. J Physiol Anthropol. [PubMed](https://pubmed.ncbi.nlm.nih.gov/22738673/) · [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3427038/)
- Sundelin, Landry & Axelsson (2024). *Is snoozing losing? Why intermittent morning alarms are used and how they affect sleep, cognition, cortisol, and mood*. J Sleep Res. [PubMed](https://pubmed.ncbi.nlm.nih.gov/37849039/) · [Wiley](https://onlinelibrary.wiley.com/doi/10.1111/jsr.14054)
- Lovallo et al. (2006) sobre caffeine + cortisol y la rationale del "+90 min". [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC2257922/)
- Cognitive Behavioral Therapy for Insomnia — overview. [Sleep Foundation](https://www.sleepfoundation.org/insomnia/treatment/cognitive-behavioral-therapy-insomnia) · [CBT-I Primer — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10002474/)
- Phase response curve y luz matinal — síntesis. [Phase advancing — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC4344919/) · [Effects of light on circadian/sleep/mood — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6751071/)
- 4-7-8 breathing — efectos parasimpáticos y HRV. [4-7-8 effects — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9277512/)
- Orthosomnia. Baron et al. (2017), *J Clin Sleep Med*.
