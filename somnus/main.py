'''main script for Somnus'''
'''

```
   ▄▄▄▄▄   ████▄ █▀▄▀█     ▄     ▄     ▄▄▄▄▄   
  █     ▀▄ █   █ █ █ █      █     █   █     ▀▄ 
▄  ▀▀▀▀▄   █   █ █ ▄ █ ██   █ █   █ ▄  ▀▀▀▀▄   
 ▀▄▄▄▄▀    ▀████ █   █ █ █  █ █   █  ▀▄▄▄▄▀    
                    █  █  █ █ █▄ ▄█            
                   ▀   █   ██  ▀▀▀             
                                               
```
                                               

Somnus es una app diseñada para facilitar el cuidado de la higiene del sueño.

## Instalación
Descarga el apk desde la [última versión]() y sigue las instrucciones dentro de la aplicación.

## Alcance y funcionalidades
Somnus esta enfocada al cuidado de los siguientes aspectos de la higiene del sueño.

### Deuda
La **deuda de sueño** es la cantidad de horas acumuladas que has dormido de menos.

- Somnus te permite **registrar las horas dormidas** cada noche y **calcula tu deuda** de sueño acumulada.

Una precisión de 14 días es suficientemente completa como para reflejar la realidad, sin dejar la practicidad de poder ver reflejados los esfuerzos en mejorar tu sueño. No obstante, la aplicación permite modificar la precisión de la deuda de sueño en la configuración.

### Regularidad

Establecer un horario fijo de sueño ayuda a mantener un ritmo circadiano saludable. 

- Puedes registrar tus horarios objetivo, de forma que puedas ser sincero contigo mismo y realmente ver si los estas cumpliendo.

No obstante, lo ideal para un descanso reparador es ir a dormir durante **la ventana de melatonina**, la aplicación te recordará cuando es el mejor momento para ir a dormir en base a tus últimas noches.

### Rutinas de inicio y desconexión
Cada uno tiene sus rituales para todo en la vida, el sueño no es una excepción.

- **Establece rutinas** para desconectar preparando el cuerpo para dormir y para despertar. 

Ambas con sugerencias respaldadas cientificamente, pero personalizables para que se adapte a tu día a día.

### Recordatorios útiles
Hay otros factores necesarios para mantener una higiene del sueño adecuada, como cuando reducir la exposición a la luz azul, cuando evitar sustancias como la cafeína y el alcohol, etc.
- Somnus te recordará estos factores en el momento adecuado.

### ¿Por qué no considerar la calidad del sueño?
La calidad del sueño es difícil de medir con precisión al ser dependiende de muchos factores. Solo equipamiento de nivel hospitalario, generalmente inaccesible a la mayoría de usuarios, puede medir la calidad del sueño de forma útil.

Es por esto que **Somnus** mantiene un enfoque más práctico y objetivo en la higiene del sueño. Siendo una solución más accesible y útil para la mayoría de usuarios.

## Contribuir
Si quieres contribuir al crecimiento de Somnus, puedes hacerlo de las siguientes formas:
- Reportando errores o sugerencias en la sección de [issues]()
- Traduciendo la aplicación a otros idiomas, puedes ver las instrucciones en el archivo [CONTRIBUTING.md]()

## Licencia
La aplicación esta bajo la licencia [MIT]().'''

import flet as ft
import utils as u
import database as db

def main(page: ft.Page):

    page.title = "Somnus"
    page.decorations = ft.BoxDecoration(
        gradient = ft.LinearGradient(
            begin = ft.alignment.top_left,
            end = ft.alignment.bottom_right,
            colors = [ft.colors.BLUE, ft.colors.PURPLE]
        )
    )

    def init():
        if db.is_db():
            page.go("/home")
        return ft.Column(
            [
                ft.Text(
                    value = "Somnus",
                ),
                ft.Text(
                    value = "Bienvenido a Somnus, la aplicación para cuidar de tu higiene del sueño.",
                ),
                ft.Text(
                    value = "¿Quieres comenzar?",
                ),
                ft.FilledTonalButton(
                    text = "¡Comencemos!",
                    on_click = lambda e: page.go("/create_config")
                )
            ]
        )

    def home():
        '''app home page'''

        if db.is_db():
            welcome_again = "Bienvenido de vuelta, " + db.get_user() + "!"

        return ft.Column(
            [
                ft.Text(
                    value = "Somnus"
                ),
                ft.Text(
                    value = welcome_again if db.is_db() else "Bienvenido a Somnus"
                ),
                ft.Text(
                    value = "¿Qué deseas hacer hoy?"
                ),
                ft.FilledTonalButton(
                    text = "Registrar horas de sueño",
                    on_click = lambda e: page.go("/register_sleep")
                ),
                ft.FilledTonalButton(
                    text = "Ver deuda de sueño",
                    on_click = lambda e: page.go("/debt")
                ),
                ft.FilledTonalButton(
                    text = "Ver horarios objetivo",
                    on_click = lambda e: page.go("/schedule")
                ),
                ft.FilledTonalButton(
                    text = "Ver rutinas",
                    on_click = lambda e: page.go("/routines")
                ),
                ft.FilledTonalButton(
                    text = "Ver recordatorios",
                    on_click = lambda e: page.go("/reminders")
                )
            ]
        )
    
    
    def create_config():
        '''screen where the user creates the configuration, defines the user name and the sleep schedule, and sleep objective'''
        def save_config(e):
            '''save the configuration in the database'''
            db.create_db()
            try:
                db.insert_config("user", name.value)
                db.insert_config("wake_up_hour", wake_up_hour.value)
                sleep_hour = u.calculate_sleep_hour(wake_up_hour.value, float(duration.value))
                db.insert_config("sleep_hour", sleep_hour)
                db.insert_config("duration", duration.value)
                page.go("/home")
            except Exception as e:
                # Handle database error (e.g., display an error message)
                print(f"Error saving configuration: {e}") 

        name = ft.TextField(label = "Nombre")
        wake_up_hour = ft.TextField(label = "HH:mm")
        duration = ft.TextField(label = "Duración objetivo (horas e.g. 8.5)")
        submit = ft.FilledTonalButton(text = "Guardar", on_click = save_config)


        return ft.Column(
            [
                ft.Text(
                    value = "Somnus",
                ),
                ft.Text(
                    value = "¡Hola! ¿Cómo te llamas?",
                ),
                name,
                ft.Text(
                    value = "¿A qué hora te vas a despertar?",
                ),
                wake_up_hour,
                ft.Text(
                    value = "¿Cuál es tu objetivo de sueño?",
                ),
                duration,
                submit
            ]
        )

    def register_sleep():
        '''screen where the user registers the hours of sleep'''
        return ft.Column(
            [
                ft.Text(
                    value = "Somnus",
                ),
                ft.Text(
                    value = "¿Cuántas horas dormiste esta noche?",
                ),
                ft.TextField(
                    label = "Horas",
                    hint_text = "e.g. 8.5"
                ),
                ft.FilledTonalButton(
                    text = "Guardar",
                    on_click = lambda: page.go("/home")
                )
            ]
        )
    
    def debt():
        '''screen where the user can see the sleep debt'''
        return ft.Column(
            [
                ft.Text(
                    value = "Somnus",
                ),
                ft.Text(
                    value = "Deuda de sueño"
                ),
                ft.Text(
                    value = "Tu deuda de sueño es de 8 horas."
                ),
                ft.FilledTonalButton(
                    text = "Volver",
                    on_click = lambda: page.go("/home")
                )
            ]
        )
    
    def schedule():
        '''screen where the user can see the sleep schedule'''
        return ft.Column(
            [
                ft.Text(
                    value = "Somnus",
                ),
                ft.Text(
                    value = "Horarios objetivo"
                ),
                ft.Text(
                    value = "Despierta a las 6:30, duerme a las 22:00."
                ),
                ft.FilledTonalButton(
                    text = "Volver",
                    on_click = lambda: page.go("/home")
                )
            ]
        )
    
    def routines():
        '''screen where the user can see the routines'''
        return ft.Column(
            [
                ft.Text(
                    value = "Somnus",
                ),
                ft.Text(
                    value = "Rutinas"
                ),
                ft.Text(
                    value = "Rutina de inicio: Apaga la luz azul."
                ),
                ft.Text(
                    value = "Rutina de desconexión: Evita la cafeína."
                ),
                ft.FilledTonalButton(
                    text = "Volver",
                    on_click = lambda: page.go("/home")
                )
            ]
        )
    
    def route_change(route):
        views = {
            "/": init(),
            "/create_config": create_config(),
            "/home": home(),
            "/register_sleep": register_sleep(),
            "/debt": debt(),
            "/schedule": schedule(),
            "/routines": routines()
        }
        page.views.clear()
        page.views.append(views.get(page.route, views["/"]))
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(main, "android")