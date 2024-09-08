# 🗓️ WeeklyPlanner - Planificador Semanal en Python

**WeeklyPlanner** es una aplicación de escritorio simple y estilizada desarrollada en Python utilizando PyQt6. Permite a los usuarios planificar actividades diarias para los 7 días de la semana, con características avanzadas de notificación, repetición de actividades y generación de estadísticas.

## 📋 Características

- **Planificación Semanal**: Gestiona actividades para los 7 días de la semana en un formato de calendario.
- **Gestión de Actividades**: Agrega, edita, elimina y marca actividades como completadas utilizando un `QCheckBox`.
- **Notificaciones Personalizadas**: Configura notificaciones para actividades específicas, incluyendo alertas emergentes y sonidos.
- **Repetición de Notificaciones**: Opción para repetir notificaciones diariamente o semanalmente.
- **Posponer Notificaciones**: Posibilidad de posponer una notificación por 5, 10 o 15 minutos.
- **Sincronización con Google Calendar**: (Funcionalidad sugerida) Sincronización opcional con Google Calendar para importar y exportar eventos.
- **Estadísticas de Actividades**: (Funcionalidad sugerida) Generación de estadísticas sobre la duración y frecuencia de actividades completadas.
- **Minimizar a Área de Notificaciones**: La aplicación se minimiza al área de notificaciones de Windows, mostrando notificaciones de estado.

## 🛠️ Requisitos

- **Python 3.12**
- Librerías necesarias:
  - PyQt6
  - pandas
  - openpyxl
  - plyer
  - pygame

## 📦 Instalación

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/tu_usuario/WeeklyPlanner.git
   cd WeeklyPlanner

Crear y activar un entorno virtual (opcional pero recomendado)

venv\Scripts\activate

Instalar las dependencias

pip install -r requirements.txt



Funciones Básicas:

Agregar Actividades: Doble clic en la celda de la tabla para agregar una nueva actividad.
Editar/Eliminar Actividades: Clic derecho en una celda de actividad para abrir el menú contextual.
Marcar como Completada: Usa el QCheckBox dentro de cada celda de actividad.
Configurar Notificaciones: Usa el menú contextual para configurar notificaciones con ventanas emergentes y sonido.
Repetición de Notificaciones: Selecciona repetir notificaciones diariamente o semanalmente desde la configuración de notificaciones.
Minimizar a Área de Notificaciones: La aplicación se moverá al área de notificaciones cuando se minimice.
Salir de la Aplicación: Usa la opción de "Salir" en el menú de la bandeja del sistema para cerrar completamente la aplicación.

📊 Funcionalidades Avanzadas
Repetición de Notificaciones: Configura tus notificaciones para que se repitan diariamente o semanalmente, lo que es útil para actividades recurrentes.
Posponer Notificaciones: (Sugerido) Posibilidad de posponer notificaciones para ser recordado más tarde.
Integración con Google Calendar: (Sugerido) Sincronización con Google Calendar para manejar eventos desde un solo lugar.
Estadísticas de Uso: (Sugerido) Genera estadísticas de las actividades completadas versus las planificadas, ayudando a analizar tu productividad.

📝 Registro de Actividades
Todas las interacciones del usuario (agregar, editar, eliminar, configurar notificación) se registran en un archivo app.log ubicado en el directorio raíz del proyecto. Este archivo es útil para realizar un seguimiento de las actividades y posibles errores.

🔔 Notificaciones
La aplicación utiliza la biblioteca pygame para reproducir un archivo de sonido .mp3 para las notificaciones y muestra un cuadro de mensaje centrado en la pantalla. Asegúrate de tener las notificaciones del sistema habilitadas.

👥 Contribución
Si deseas contribuir a este proyecto, por favor haz un fork del repositorio y crea un pull request con tus mejoras. Todos los comentarios y sugerencias son bienvenidos.

📜 Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.






📁 Estructura del Proyecto

WeeklyPlanner/
│
├── Source/                # Carpeta que contiene el icono y las imágenes de la aplicación
│   ├── calendar.ico       # Icono de la aplicación
│   └── sound.mp3          # Sonido para las notificaciones
│
├── main.py                # Código fuente principal de la aplicación
├── requirements.txt       # Lista de dependencias del proyecto
├── README.md              # Documentación del proyecto
└── planificador.xlsx      # Archivo Excel para persistencia de datos (se genera al ejecutar)





pyinstaller --onefile --windowed --icon=Source/calendar.ico main.py

pip install -r requirements.txt
