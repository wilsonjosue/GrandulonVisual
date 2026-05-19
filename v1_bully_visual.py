#bully_visual.py
import tkinter as tk
import threading
import time


# =========================================================
# CLASE PROCESS
# =========================================================

class Process:
    def __init__(self, pid):
        self.pid = pid
        self.active = True
        self.coordinator = False


# =========================================================
# CLASE PRINCIPAL
# =========================================================

class BullyGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("Algoritmo Grandulón - Bully Algorithm")
        self.root.geometry("1200x700")
        self.root.configure(bg="#1e1e1e")

        # =============================
        # ESTRUCTURAS
        # =============================

        self.processes = {}
        self.process_labels = {}

        self.coordinator_id = 5

        # =============================
        # CREAR PROCESOS
        # =============================

        self.create_processes()

        # =============================
        # CREAR INTERFAZ
        # =============================

        self.create_interface()

        # =============================
        # COORDINADOR INICIAL
        # =============================

        self.processes[5].coordinator = True

        # =============================
        # ACTUALIZAR VISUAL
        # =============================

        self.update_visuals()

    # =====================================================
    # CREAR PROCESOS
    # =====================================================

    def create_processes(self):

        for i in range(1, 6):
            self.processes[i] = Process(i)

    # =====================================================
    # CREAR INTERFAZ
    # =====================================================

    def create_interface(self):

        # =============================
        # TÍTULO
        # =============================

        title = tk.Label(
            self.root,
            text="SIMULACIÓN DEL ALGORITMO GRANDULÓN",
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#1e1e1e"
        )

        title.pack(pady=10)

        # =============================
        # CANVAS
        # =============================

        self.canvas = tk.Canvas(
            self.root,
            width=1000,
            height=320,
            bg="#2d2d2d",
            highlightthickness=0
        )

        self.canvas.pack(pady=20)

        # =============================
        # POSICIONES
        # =============================

        positions = {
            1: (100, 150),
            2: (280, 150),
            3: (460, 150),
            4: (640, 150),
            5: (820, 150)
        }

        # =============================
        # CREAR NODOS
        # =============================

        for pid, (x, y) in positions.items():

            # CÍRCULO

            circle = self.canvas.create_oval(
                x - 40,
                y - 40,
                x + 40,
                y + 40,
                fill="green",
                outline="white",
                width=3
            )

            # TEXTO P1 P2 ...

            text = self.canvas.create_text(
                x,
                y,
                text=f"P{pid}",
                font=("Arial", 16, "bold"),
                fill="white"
            )

            # ESTADO

            status = self.canvas.create_text(
                x,
                y + 60,
                text="ACTIVO",
                font=("Arial", 10),
                fill="white"
            )

            # GUARDAR REFERENCIAS

            self.process_labels[pid] = {
                "circle": circle,
                "text": text,
                "status": status,
                "x": x,
                "y": y
            }

        # =============================
        # BOTONES
        # =============================

        button_frame = tk.Frame(
            self.root,
            bg="#1e1e1e"
        )

        button_frame.pack(pady=10)

        # BOTÓN DEMO

        tk.Button(
            button_frame,
            text="Ejecutar Demo",
            command=self.run_demo,
            bg="#007acc",
            fg="white",
            width=20,
            height=2,
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, padx=10)

        # BOTÓN FALLAR

        tk.Button(
            button_frame,
            text="Caer Coordinador",
            command=self.fail_coordinator,
            bg="#cc3300",
            fg="white",
            width=20,
            height=2,
            font=("Arial", 10, "bold")
        ).grid(row=0, column=1, padx=10)

        # BOTÓN RECUPERAR

        tk.Button(
            button_frame,
            text="Recuperar P5",
            command=lambda: self.recover_process(5),
            bg="#339933",
            fg="white",
            width=20,
            height=2,
            font=("Arial", 10, "bold")
        ).grid(row=0, column=2, padx=10)

        # =============================
        # ÁREA LOGS
        # =============================

        self.log_text = tk.Text(
            self.root,
            width=120,
            height=15,
            bg="black",
            fg="#00ff00",
            font=("Consolas", 11)
        )

        self.log_text.pack(pady=20)

    # =====================================================
    # LOGS
    # =====================================================

    def log(self, message):

        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

        print(message)

    # =====================================================
    # ACTUALIZAR VISUAL
    # =====================================================

    def update_visuals(self):

        for pid, process in self.processes.items():

            label = self.process_labels[pid]

            color = "green"
            status = "ACTIVO"

            # PROCESO CAÍDO

            if not process.active:

                color = "red"
                status = "CAÍDO"

            # COORDINADOR

            elif process.coordinator:

                color = "gold"
                status = "COORDINADOR"

            # ACTUALIZAR

            self.canvas.itemconfig(
                label["circle"],
                fill=color
            )

            self.canvas.itemconfig(
                label["status"],
                text=status
            )

        self.root.update()

    # =====================================================
    # FALLAR PROCESO
    # =====================================================

    def fail_process(self, pid):

        self.processes[pid].active = False
        self.processes[pid].coordinator = False

        self.log(f"\n[P{pid}] HA FALLADO")

        self.update_visuals()

        if self.coordinator_id == pid:

            self.coordinator_id = None

            self.log("El coordinador cayó.")

    # =====================================================
    # FALLAR COORDINADOR
    # =====================================================

    def fail_coordinator(self):

        if self.coordinator_id:

            self.fail_process(self.coordinator_id)

    # =====================================================
    # RECUPERAR PROCESO
    # =====================================================

    def recover_process(self, pid):

        self.processes[pid].active = True

        self.log(f"\n[P{pid}] SE RECUPERÓ")

        self.update_visuals()

        time.sleep(1)

        self.start_election(pid)

    # =====================================================
    # DECLARAR COORDINADOR
    # =====================================================

    def declare_coordinator(self, pid):

        for p in self.processes.values():

            p.coordinator = False

        self.processes[pid].coordinator = True

        self.coordinator_id = pid

        self.log(f"\n[P{pid}] ES EL NUEVO COORDINADOR")

        self.update_visuals()

    # =====================================================
    # ELECCIÓN
    # =====================================================

    def start_election(self, pid):

        if not self.processes[pid].active:
            return

        self.log(f"\n[P{pid}] inicia ELECCIÓN")

        time.sleep(1)

        higher = []

        # BUSCAR IDS MAYORES ACTIVOS

        for other_pid, process in self.processes.items():

            if other_pid > pid and process.active:

                higher.append(other_pid)

        # SI NO HAY MAYORES -> GANA

        if not higher:

            self.declare_coordinator(pid)

            return

        responses = []

        # ENVIAR ELECTION

        for hp in higher:

            self.log(f"[P{pid}] -> [P{hp}] : ELECTION")

            self.highlight_message(pid, hp)

            time.sleep(1)

            self.log(f"[P{hp}] -> [P{pid}] : OK")

            responses.append(hp)

            time.sleep(1)

        # MAYOR ACTIVO CONTINÚA

        highest = max(responses)

        self.log(f"\n[P{highest}] continúa la elección")

        time.sleep(1)

        self.start_election(highest)

    # =====================================================
    # MENSAJE VISUAL
    # =====================================================

    def highlight_message(self, from_pid, to_pid):

        p1 = self.process_labels[from_pid]
        p2 = self.process_labels[to_pid]

        # CREAR FLECHA

        line = self.canvas.create_line(
            p1["x"],
            p1["y"],
            p2["x"],
            p2["y"],
            fill="cyan",
            width=4,
            arrow=tk.LAST
        )

        self.root.update()

        time.sleep(0.8)

        # BORRAR FLECHA

        self.canvas.delete(line)

    # =====================================================
    # DEMO
    # =====================================================

    def run_demo(self):

        threading.Thread(
            target=self.demo_sequence
        ).start()

    # =====================================================
    # SECUENCIA DEMO
    # =====================================================

    def demo_sequence(self):

        self.log("\n=========== DEMO DEL BULLY ALGORITHM ===========")

        time.sleep(1)

        self.log("\nInicialmente P5 es coordinador")

        time.sleep(1)

        # FALLA P5

        self.fail_process(5)

        time.sleep(2)

        # P2 DETECTA FALLA

        self.log("\n[P2] detectó la caída del coordinador")

        time.sleep(1)

        # INICIAR ELECCIÓN

        self.start_election(2)


# =========================================================
# MAIN
# =========================================================

root = tk.Tk()

app = BullyGUI(root)

root.mainloop()