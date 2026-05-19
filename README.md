# Algoritmo Grandulón (Bully Algorithm) - Simulación Visual en Python

Este proyecto implementa una **simulación visual del Algoritmo Grandulón** usando **Python + Tkinter**.  
La aplicación permite observar cómo se realiza la elección de coordinador en un sistema distribuido cuando un nodo falla, se recupera o inicia una nueva elección.

## Estructura del proyecto

bully_visual/

│

├── bully_visual.py

├── README.md

└── Documentacion.md

## Requisitos

- Python 3.10 o superior
- Tkinter (normalmente viene incluido con Python)

## Instalacion
### Crear entorno virtual
Windows
python -m venv venv
venv\Scripts\activate

Linux/macOS
python3 -m venv venv
source venv/bin/activate

## Características

- Simulación visual del algoritmo Bully.
- Interfaz gráfica con nodos representados como procesos.
- Estados visuales:
  - **Activo**
  - **Caído**
  - **Coordinador**
- Visualización de mensajes:
  - `ELECTION`
  - `OK`
  - `COORDINATOR`
- Botones para:
  - ejecutar una demostración automática,
  - hacer caer al coordinador,
  - recuperar el proceso `P5`,
  - iniciar manualmente una elección en `P2`.
- Separación entre:
  - **lógica del algoritmo**
  - **interfaz gráfica**

