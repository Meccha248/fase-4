import tkinter as tk
from tkinter import messagebox

# --- Clases de Lógica (POO) ---

class Device:
    def __init__(self, name):
        self.name = name
        self.is_on = False  # Estado inicial: apagado

    def turn_on(self):
        self.is_on = True

    def turn_off(self):
        self.is_on = False

    def status(self):
        # Método polimórfico base
        return f"{self.name} is {'ON' if self.is_on else 'OFF'}"

    def configure(self, *args):
        pass

# Clases concretas que sobrescriben los métodos
class SmartBulb(Device):
    def status(self):
        return f"[Bulb Alert] {self.name} light intensity is active." if self.is_on else f"[Bulb Alert] {self.name} is dark."

class SmartCurtain(Device):
    def status(self):
        return f"[Curtain Alert] {self.name} is fully OPEN." if self.is_on else f"[Curtain Alert] {self.name} is CLOSED."

class SmartThermostat(Device):
    def status(self):
        return f"[Thermostat Alert] {self.name} climate control is active (22°C)." if self.is_on else f"[Thermostat Alert] {self.name} is ECO mode (OFF)."


class ControlCentral:
    def __init__(self):
        self.devices = []

    def add_device(self, device):
        self.devices.append(device)


# --- Interfaz Gráfica (Tkinter) ---

class SmartHomeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Home Device Manager")
        self.root.geometry("550x400")
        
        # Inicializar el sistema de control central
        self.system = ControlCentral()
        self.system.add_device(SmartBulb("Living Room Bulb"))
        self.system.add_device(SmartCurtain("Bedroom Curtain"))
        self.system.add_device(SmartThermostat("Main AC"))

        # Diccionario para guardar las etiquetas de estado de la interfaz y poder actualizarlas
        self.status_labels = {}

        # Título principal
        tk.Label(root, text="Device Control Panel", font=("Arial", 16, "bold")).pack(pady=15)

        # Contenedor principal de dispositivos
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(pady=10, fill="x", padx=20)

        self.create_device_ui()

    def create_device_ui(self):
        for device in self.system.devices:
            # Frame contenedor para cada fila de dispositivo
            row_frame = tk.Frame(self.main_frame, pady=8)
            row_frame.pack(fill="x")

            # 1. Nombre del aparato
            name_label = tk.Label(row_frame, text=device.name, font=("Arial", 11, "bold"), width=18, anchor="w")
            name_label.pack(side="left")

            # 2. Estado (encendido/apagado) - Etiqueta visual
            status_lbl = tk.Label(row_frame, text="[OFF]", font=("Arial", 10, "bold"), fg="red", width=8)
            status_lbl.pack(side="left", padx=5)
            # Guardamos la referencia de la etiqueta usando el objeto del dispositivo como clave
            self.status_labels[device] = status_lbl

            # 3. Método encender() - Botón ON
            btn_on = tk.Button(
                row_frame, text="Turn ON", 
                command=lambda d=device: self.action_turn_on(d), 
                bg="#c8e6c9", width=8
            )
            btn_on.pack(side="left", padx=5)

            # 4. Método apagar() - Botón OFF
            btn_off = tk.Button(
                row_frame, text="Turn OFF", 
                command=lambda d=device: self.action_turn_off(d), 
                bg="#ffcdd2", width=8
            )
            btn_off.pack(side="left", padx=5)

            # 5. Método polimórfico status() - Botón Check Status
            btn_status = tk.Button(
                row_frame, text="Status Check", 
                command=lambda d=device: self.action_popup_status(d), 
                bg="#e0e0e0", width=12
            )
            btn_status.pack(side="left", padx=5)

    def action_turn_on(self, device):
        device.turn_on()  # Llama al método del objeto
        self.status_labels[device].config(text="[ON]", fg="green")  # Actualiza la interfaz gráfica

    def action_turn_off(self, device):
        device.turn_off()  # Llama al método del objeto
        self.status_labels[device].config(text="[OFF]", fg="red")  # Actualiza la interfaz gráfica

    def action_popup_status(self, device):
        # Llama al método polimórfico status() y muestra la respuesta única de cada clase en un mensaje flotante
        info_msg = device.status()
        messagebox.showinfo(f"{device.name} System Status", info_msg)


# --- Ejecución ---
if __name__ == "__main__":
    root = tk.Tk()
    app = SmartHomeApp(root)
    root.mainloop()