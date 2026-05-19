
---

## `Documentacion.md`

```md
# Documentación del Proyecto  
## Algoritmo Grandulón (Bully Algorithm) - Simulación Visual en Python

## 1. Descripción general

Este proyecto implementa una simulación visual del **Algoritmo Grandulón**, también conocido como **Bully Algorithm**, utilizando **Python** y la biblioteca **Tkinter**.

La aplicación representa cinco procesos (`P1` a `P5`) que participan en una elección de coordinador.  
El objetivo es mostrar de forma clara y visual cómo funciona la elección distribuida cuando el coordinador falla o cuando un proceso se recupera.

---

## 2. Objetivo del proyecto

El objetivo principal es demostrar el funcionamiento del algoritmo de elección de líder en sistemas distribuidos mediante una interfaz gráfica local.

Se busca que el usuario pueda observar:

- la caída de un proceso,
- la detección del fallo,
- la ejecución de una elección,
- el envío de mensajes entre procesos,
- la elección del nuevo coordinador,
- la recuperación de un proceso y su posible reintegro como coordinador.

---

## 3. Algoritmo implementado

### 3.1 ¿Qué es el Algoritmo Grandulón?

El Algoritmo Grandulón es un algoritmo de elección de coordinador en el que el proceso con el **identificador más alto activo** se convierte en líder.

Cuando un proceso detecta que el coordinador actual ha fallado:

1. inicia una elección,
2. envía mensajes `ELECTION` a los procesos con mayor ID,
3. los procesos que responden con `OK` también pueden iniciar su propia elección,
4. el proceso con mayor ID activo termina ganando,
5. el nuevo coordinador informa a los demás mediante mensajes `COORDINATOR`.

### 3.2 Mensajes usados

El proyecto muestra tres tipos de mensajes:

- **ELECTION**: un proceso solicita una nueva elección.
- **OK**: un proceso de mayor prioridad responde que está activo.
- **COORDINATOR**: el proceso ganador anuncia que ya es el nuevo coordinador.

---

## 4. Estructura del programa

El programa está dividido en dos partes principales:

### 4.1 Lógica del algoritmo

La clase `BullyAlgorithm` contiene toda la lógica del comportamiento distribuido.

Se encarga de:

- registrar procesos,
- marcar procesos como activos o caídos,
- iniciar elecciones,
- resolver quién gana,
- declarar coordinador,
- simular recuperación.

### 4.2 Interfaz gráfica

La clase `BullyGUI` se encarga de la visualización.

Se encarga de:

- dibujar los nodos,
- cambiar colores según el estado,
- mostrar mensajes temporales,
- dibujar flechas entre procesos,
- mostrar una barra de estado general,
- registrar eventos en consola visual.

---

## 5. Explicación de las clases

### 5.1 `Process`

Representa un proceso del sistema distribuido.

#### Atributos

- `pid`: identificador del proceso.
- `active`: indica si el proceso está activo.
- `coordinator`: indica si el proceso es coordinador.
- `last_round`: evita repetir la misma ronda de elección.

---

### 5.2 `BullyAlgorithm`

Es la clase central del comportamiento del algoritmo.

#### Atributos principales

- `processes`: diccionario con los procesos del sistema.
- `coordinator_id`: ID del coordinador actual.
- `round_counter`: contador de rondas de elección.
- `round_winner`: registro del ganador por ronda.

#### Métodos principales

- `fail_process(pid)`: simula la caída de un proceso.
- `recover_process(pid)`: simula la recuperación de un proceso.
- `start_election(pid)`: inicia una elección.
- `_run_election(pid, round_id)`: ejecuta la lógica recursiva de elección.
- `_declare_coordinator(pid, round_id)`: asigna el coordinador ganador.
- `demo()`: ejecuta una secuencia automática de prueba.

---

### 5.3 `BullyGUI`

Es la clase encargada de la interfaz gráfica.

#### Funciones principales

- `set_banner(text)`: actualiza el mensaje superior.
- `log(message)`: escribe en el área de logs.
- `refresh_process(pid)`: actualiza visualmente un proceso.
- `flash_message(from_pid, to_pid, kind)`: muestra mensajes animados entre nodos.
- `run_demo()`: ejecuta la demostración automática.
- `fail_coordinator()`: hace caer el coordinador actual.
- `recover_process(pid)`: recupera un proceso.
- `start_election(pid)`: inicia una elección manual.

---

## 6. Estados visuales

La interfaz muestra los procesos con distintos colores:

- **Verde**: proceso activo.
- **Rojo**: proceso caído.
- **Dorado**: coordinador.
- **Azul**: mensaje `ELECTION`.
- **Morado**: mensaje `OK`.
- **Naranja**: mensaje `COORDINATOR`.

Además, debajo de cada nodo se muestra un texto temporal con el mensaje actual que está siendo visualizado.

---

## 7. Flujo de funcionamiento

### 7.1 Estado inicial

Al iniciar la aplicación:

- todos los procesos están activos,
- `P5` es el coordinador inicial.

### 7.2 Caída del coordinador

Cuando el coordinador cae:

- su estado cambia a rojo,
- el sistema indica que se requiere una nueva elección.

### 7.3 Elección

Cuando un proceso inicia la elección:

1. se muestra el mensaje `ELECTION`,
2. los procesos mayores responden `OK`,
3. el proceso de mayor prioridad sigue participando,
4. el proceso con mayor ID activo gana,
5. se anuncia como `COORDINATOR`.

### 7.4 Recuperación

Cuando un proceso se recupera:

- vuelve a estar activo,
- puede iniciar automáticamente una nueva elección,
- si tiene mayor ID que el coordinador actual, puede volver a ganar.

---

## 8. Decisiones de diseño

### 8.1 Separación de lógica e interfaz

Se separó la lógica del algoritmo de la interfaz gráfica para lograr:

- mejor organización,
- mantenimiento más sencillo,
- claridad en el código,
- posibilidad de modificar la interfaz sin alterar el algoritmo.

### 8.2 Uso de hilos

Se utilizan `threading.Thread` para ejecutar la simulación sin congelar la interfaz gráfica.

### 8.3 Uso de `after()`

Tkinter usa `after()` para actualizar elementos visuales temporales sin bloquear la ventana.

---

## 9. Comportamiento esperado

Durante la simulación, el usuario debe observar:

- el coordinador inicial en color dorado,
- la caída del coordinador,
- el envío de mensajes `ELECTION`,
- respuestas `OK`,
- elección del nuevo coordinador,
- mensajes `COORDINATOR`,
- recuperación de `P5` y nueva elección si corresponde.

---

## 10. Pasos de ejecución

### En Windows

```bash
python -m venv venv
venv\Scripts\activate
python bully_visual.py