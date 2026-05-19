import tkinter as tk
import threading
import time
from dataclasses import dataclass
from typing import Callable, Dict, Optional

# =========================================================
# MODELO DEL PROCESO
# =========================================================

@dataclass
class Process:
    pid: int
    active: bool = True
    coordinator: bool = False
    last_round: int = -1

# =========================================================
# LÓGICA DEL ALGORITMO GRANDULON
# =========================================================

class BullyAlgorithm:
    def __init__(
        self,
        process_ids,
        log_cb: Callable[[str], None],
        refresh_process_cb: Callable[[int], None],
        flash_message_cb: Callable[[int, int, str], None],
        banner_cb: Callable[[str], None],
    ):
        self.processes: Dict[int, Process] = {
            pid: Process(pid) for pid in process_ids
        }
        self.log_cb = log_cb
        self.refresh_process_cb = refresh_process_cb
        self.flash_message_cb = flash_message_cb
        self.banner_cb = banner_cb

        self.round_counter = 0
        self.round_winner: Dict[int, int] = {}

        self.coordinator_id: Optional[int] = max(process_ids)
        self.processes[self.coordinator_id].coordinator = True

        self.banner_cb(f"Coordinador inicial: P{self.coordinator_id}")
        self._refresh_all()

    # ------------------------------
    # Helpers
    # ------------------------------

    def _log(self, msg: str):
        self.log_cb(msg)

    def _banner(self, msg: str):
        self.banner_cb(msg)

    def _refresh(self, pid: int):
        self.refresh_process_cb(pid)

    def _refresh_all(self):
        for pid in self.processes:
            self._refresh(pid)

    def _sleep(self, seconds: float):
        time.sleep(seconds)

    def _send(self, from_pid: int, to_pid: int, kind: str):
        self._log(f"[P{from_pid}] -> [P{to_pid}] : {kind}")
        self.flash_message_cb(from_pid, to_pid, kind)
        self._sleep(1.5)

    # ------------------------------
    # Fallas y recuperación
    # ------------------------------

    def fail_process(self, pid: int):
        if pid not in self.processes:
            return

        p = self.processes[pid]
        if not p.active:
            return

        p.active = False
        p.coordinator = False

        self._log(f"\n[P{pid}] HA FALLADO")
        self._refresh(pid)

        if self.coordinator_id == pid:
            self.coordinator_id = None
            self._banner("El coordinador cayó. Se requiere una elección.")

    def recover_process(self, pid: int):
        if pid not in self.processes:
            return

        p = self.processes[pid]
        p.active = True

        self._log(f"\n[P{pid}] SE RECUPERÓ")
        self._refresh(pid)
        self._sleep(1.5)

        self._log(f"[P{pid}] inicia una elección al recuperarse.")
        self.start_election(pid)

    # ------------------------------
    # Elección
    # ------------------------------

    def start_election(self, pid: int):
        if pid not in self.processes:
            return

        if not self.processes[pid].active:
            self._log(f"[P{pid}] está caído y no puede iniciar elección.")
            return

        self.round_counter += 1
        round_id = self.round_counter
        self.round_winner.pop(round_id, None)

        self._banner(f"Ronda {round_id}: P{pid} inicia ELECCIÓN")
        self._log(f"\n[P{pid}] inicia ELECCIÓN")
        self._sleep(1.5)

        self._run_election(pid, round_id)

    def _run_election(self, pid: int, round_id: int):
        if self.round_winner.get(round_id) is not None:
            return

        process = self.processes[pid]
        if not process.active:
            return

        if process.last_round == round_id:
            return

        process.last_round = round_id

        higher_active = [
            p.pid for p in self.processes.values()
            if p.pid > pid and p.active
        ]

        if not higher_active:
            self._declare_coordinator(pid, round_id)
            return

        got_ok = False

        for hp in higher_active:
            if self.round_winner.get(round_id) is not None:
                return

            self._send(pid, hp, "ELECTION")

            if not self.processes[hp].active:
                continue

            got_ok = True
            self._send(hp, pid, "OK")

            if self.processes[hp].last_round != round_id:
                self._run_election(hp, round_id)

        if got_ok and self.round_winner.get(round_id) is None:
            self._log(f"[P{pid}] sale de la contienda y espera al ganador.")

    def _declare_coordinator(self, pid: int, round_id: int):
        if self.round_winner.get(round_id) is not None:
            return

        self.round_winner[round_id] = pid

        for p in self.processes.values():
            p.coordinator = False

        self.processes[pid].coordinator = True
        self.coordinator_id = pid

        self._banner(f"P{pid} es el nuevo COORDINADOR")
        self._log(f"\n[P{pid}] se declara COORDINADOR")
        self._refresh_all()
        self._sleep(1.5)

        for other_pid in sorted(self.processes):
            if other_pid != pid and self.processes[other_pid].active:
                self._send(pid, other_pid, "COORDINATOR")

        self._log(f"\n*** NUEVO COORDINADOR: P{pid} ***")
        self._refresh_all()

    # ------------------------------
    # Demo
    # ------------------------------

    def demo(self):
        self._banner("Ejecutando demostración del algoritmo Grandulón...")
        self._sleep(2)

        self._log("\nEstado inicial: P5 es coordinador")
        self._sleep(2)

        self.fail_process(self.coordinator_id)
        self._sleep(2)

        self._log("\n[P2] detectó la caída del coordinador")
        self._sleep(2)

        self.start_election(3)


# =========================================================
# INTERFAZ GRÁFICA
# =========================================================

class BullyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritmo Grandulón - Bully Algorithm")
        self.root.geometry("1250x780")
        self.root.configure(bg="#1e1e1e")

        self.node_widgets = {}
        self.algorithm: Optional[BullyAlgorithm] = None

        self._build_interface()
        self._build_algorithm()
        self.refresh_all()

    # ------------------------------
    # Utilidad segura para Tkinter
    # ------------------------------

    def ui(self, func, *args):
        self.root.after(0, lambda: func(*args))

    # ------------------------------
    # Construcción visual
    # ------------------------------

    def _build_interface(self):
        title = tk.Label(
            self.root,
            text="SIMULACIÓN VISUAL DEL ALGORITMO GRANDULÓN",
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#1e1e1e"
        )
        title.pack(pady=10)

        self.banner_var = tk.StringVar(value="Listo para iniciar")
        banner = tk.Label(
            self.root,
            textvariable=self.banner_var,
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#333333",
            padx=12,
            pady=8
        )
        banner.pack(pady=5, fill="x")

        self.canvas = tk.Canvas(
            self.root,
            width=1100,
            height=330,
            bg="#2d2d2d",
            highlightthickness=0
        )
        self.canvas.pack(pady=15)

        positions = {
            1: (120, 150),
            2: (320, 150),
            3: (520, 150),
            4: (720, 150),
            5: (920, 150),
        }

        for pid, (x, y) in positions.items():
            circle = self.canvas.create_oval(
                x - 42, y - 42, x + 42, y + 42,
                fill="green", outline="white", width=3
            )

            text = self.canvas.create_text(
                x, y - 5,
                text=f"P{pid}",
                font=("Arial", 16, "bold"),
                fill="white"
            )

            status = self.canvas.create_text(
                x, y + 40,
                text="ACTIVO",
                font=("Arial", 10, "bold"),
                fill="white"
            )

            message = self.canvas.create_text(
                x, y + 70,
                text="",
                font=("Arial", 10, "bold"),
                fill="#00d4ff"
            )

            self.node_widgets[pid] = {
                "circle": circle,
                "text": text,
                "status": status,
                "message": message,
                "x": x,
                "y": y,
            }

        btn_frame = tk.Frame(self.root, bg="#1e1e1e")
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Ejecutar Demo",
            command=self.run_demo,
            bg="#007acc",
            fg="white",
            width=18,
            height=2,
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, padx=8)

        tk.Button(
            btn_frame,
            text="Caer Coordinador",
            command=self.fail_coordinator,
            bg="#cc3300",
            fg="white",
            width=18,
            height=2,
            font=("Arial", 10, "bold")
        ).grid(row=0, column=1, padx=8)

        tk.Button(
            btn_frame,
            text="Recuperar P5",
            command=lambda: self.recover_process(5),
            bg="#339933",
            fg="white",
            width=18,
            height=2,
            font=("Arial", 10, "bold")
        ).grid(row=0, column=2, padx=8)

        tk.Button(
            btn_frame,
            text="Iniciar elección en P2",
            command=lambda: self.start_election(2),
            bg="#6c5ce7",
            fg="white",
            width=18,
            height=2,
            font=("Arial", 10, "bold")
        ).grid(row=0, column=3, padx=8)

        self.log_text = tk.Text(
            self.root,
            width=130,
            height=16,
            bg="black",
            fg="#00ff00",
            font=("Consolas", 11)
        )
        self.log_text.pack(pady=15)

    def _build_algorithm(self):
        self.algorithm = BullyAlgorithm(
            process_ids=[1, 2, 3, 4, 5],
            log_cb=self.log,
            refresh_process_cb=self.refresh_process,
            flash_message_cb=self.flash_message,
            banner_cb=self.set_banner,
        )

    # ------------------------------
    # UI callbacks
    # ------------------------------

    def set_banner(self, text: str):
        self.ui(self._set_banner_impl, text)

    def _set_banner_impl(self, text: str):
        self.banner_var.set(text)

    def log(self, message: str):
        self.ui(self._log_impl, message)

    def _log_impl(self, message: str):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def refresh_process(self, pid: int):
        self.ui(self._refresh_process_impl, pid)

    def refresh_all(self):
        if self.algorithm is None:
            return
        for pid in self.algorithm.processes:
            self.refresh_process(pid)

    def _refresh_process_impl(self, pid: int):
        if self.algorithm is None:
            return

        process = self.algorithm.processes[pid]
        node = self.node_widgets[pid]

        if not process.active:
            color = "#e74c3c"
            outline = "white"
            status = "CAÍDO"
            message = ""
        elif process.coordinator:
            color = "#f1c40f"
            outline = "white"
            status = "COORDINADOR"
            message = ""
        else:
            color = "#2ecc71"
            outline = "white"
            status = "ACTIVO"
            message = ""

        self.canvas.itemconfig(node["circle"], fill=color, outline=outline, width=3)
        self.canvas.itemconfig(node["status"], text=status, fill="white")
        self.canvas.itemconfig(node["message"], text=message, fill="#00d4ff")

    def flash_message(self, from_pid: int, to_pid: int, kind: str):
        self.ui(self._flash_message_impl, from_pid, to_pid, kind)

    def _flash_message_impl(self, from_pid: int, to_pid: int, kind: str):
        if self.algorithm is None:
            return

        colors = {
            "ELECTION": "#3498db",
            "OK": "#9b59b6",
            "COORDINATOR": "#f39c12",
        }
        color = colors.get(kind, "cyan")

        n1 = self.node_widgets[from_pid]
        n2 = self.node_widgets[to_pid]

        x1, y1 = n1["x"], n1["y"]
        x2, y2 = n2["x"], n2["y"]

        # Flecha visible entre nodos
        line = self.canvas.create_line(
            x1, y1, x2, y2,
            fill=color,
            width=3,
            arrow=tk.LAST,
            dash=(5, 3)
        )

        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2 - 18

        tag = self.canvas.create_text(
            mid_x,
            mid_y,
            text=kind,
            font=("Arial", 10, "bold"),
            fill=color
        )

        # Estado temporal debajo de los nodos
        self.canvas.itemconfig(n1["message"], text=kind, fill=color)
        self.canvas.itemconfig(n2["message"], text=f"RECIBE {kind}", fill=color)

        # Flash visual de ambos nodos
        self.canvas.itemconfig(n1["circle"], outline=color, width=5)
        self.canvas.itemconfig(n2["circle"], outline=color, width=5)

        self.banner_var.set(f"P{from_pid} -> P{to_pid} : {kind}")

        def clear_temp():
            if self.canvas.winfo_exists():
                self.canvas.delete(line)
                self.canvas.delete(tag)
            self.canvas.itemconfig(n1["message"], text="")
            self.canvas.itemconfig(n2["message"], text="")
            self.refresh_process(from_pid)
            self.refresh_process(to_pid)

        self.root.after(900, clear_temp)

    # ------------------------------
    # Botones
    # ------------------------------

    def run_demo(self):
        threading.Thread(target=self.algorithm.demo, daemon=True).start()

    def fail_coordinator(self):
        if self.algorithm and self.algorithm.coordinator_id is not None:
            threading.Thread(
                target=self.algorithm.fail_process,
                args=(self.algorithm.coordinator_id,),
                daemon=True
            ).start()

    def recover_process(self, pid: int):
        if self.algorithm:
            threading.Thread(
                target=self.algorithm.recover_process,
                args=(pid,),
                daemon=True
            ).start()

    def start_election(self, pid: int):
        if self.algorithm:
            threading.Thread(
                target=self.algorithm.start_election,
                args=(pid,),
                daemon=True
            ).start()

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = BullyGUI(root)
    root.mainloop()