import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# --- CLASE PRINCIPAL (LÓGICA DE NEGOCIO) ---
class HerramientaAlquiler:
    def __init__(self, id_herramienta, tarifa_hora):
        self._id_herramienta = id_herramienta
        self._tarifa_hora = tarifa_hora
        self._hora_salida = None

    def registrar_salida(self, hora):
        if 0 <= hora <= 23:
            self._hora_salida = hora
            return True
        return False

    def calcular_costo(self, hora_retorno):
        # Validación: retorno debe ser mayor a salida y estar en rango 0-23
        if self._hora_salida is None or hora_retorno <= self._hora_salida or not (0 <= hora_retorno <= 23):
            return None
        horas_usadas = hora_retorno - self._hora_salida
        return horas_usadas * self._tarifa_hora

    def obtener_id(self):
        return self._id_herramienta

# --- INTERFAZ GRÁFICA CON TKINTER ---
class AppAlquiler:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Alquiler de Herramientas")
        self.root.geometry("400x300")
        
        # Base de datos interna de herramientas
        self.inventario = [
            HerramientaAlquiler("Taladro-01", 10),
            HerramientaAlquiler("Sierra-02", 15),
            HerramientaAlquiler("Pulidora-03", 12)
        ]
        
        self.pantalla_login()

    def pantalla_login(self):
        """Paso 3.3: Interfaz de Inicio / Login"""
        self.limpiar_pantalla()
        
        tk.Label(self.root, text="SISTEMA DE ALQUILER", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(self.root, text="Autor: [Cristhian Hernandez]").pack() 
        
        tk.Label(self.root, text="Usuario:").pack(pady=5)
        self.ent_user = tk.Entry(self.root)
        self.ent_user.pack()
        
        tk.Label(self.root, text="Contraseña:").pack(pady=5)
        self.ent_pass = tk.Entry(self.root, show="*")
        self.ent_pass.pack()
        
        tk.Button(self.root, text="Ingresar", command=self.validar_login).pack(pady=20)

    def validar_login(self):
        """Paso 3.4: Validación de credenciales"""
        u = self.ent_user.get()
        p = self.ent_pass.get()
        
        if u == "programación" and p == "programación":
            self.pantalla_gestion()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def pantalla_gestion(self):
        """Paso 3.4: Interfaz de procesos de alquiler"""
        self.limpiar_pantalla()
        
        tk.Label(self.root, text="Gestión de Alquileres", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Selección de Herramienta
        tk.Label(self.root, text="Seleccione Herramienta:").pack()
        self.lista_h = tk.StringVar(self.root)
        self.lista_h.set(self.inventario[0].obtener_id())
        opciones = [h.obtener_id() for h in self.inventario]
        tk.OptionMenu(self.root, self.lista_h, *opciones).pack()

        # Entradas de Horas
        tk.Label(self.root, text="Hora Salida (0-23):").pack()
        self.ent_h_salida = tk.Entry(self.root)
        self.ent_h_salida.pack()

        tk.Label(self.root, text="Hora Retorno (0-23):").pack()
        self.ent_h_retorno = tk.Entry(self.root)
        self.ent_h_retorno.pack()

        tk.Button(self.root, text="Procesar Alquiler", command=self.procesar_alquiler).pack(pady=15)

    def procesar_alquiler(self):
        """Lógica para registrar y calcular el costo"""
        try:
            id_sel = self.lista_h.get()
            h_salida = int(self.ent_h_salida.get())
            h_retorno = int(self.ent_h_retorno.get())
            
            # Buscar herramienta en inventario
            herramienta = next(h for h in self.inventario if h.obtener_id() == id_sel)
            
            if herramienta.registrar_salida(h_salida):
                costo = herramienta.calcular_costo(h_retorno)
                if costo is not None:
                    messagebox.showinfo("Resultado", f"ID: {id_sel}\nHoras: {h_retorno-h_salida}\nTotal a Pagar: ${costo}")
                else:
                    messagebox.showwarning("Validación", "Horas incorrectas. Verifique el rango y que el retorno sea después de la salida.")
            else:
                messagebox.showwarning("Validación", "Hora de salida no válida.")
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese números válidos en las horas.")

    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Ejecución de la App
if __name__ == "__main__":
    root = tk.Tk()
    app = AppAlquiler(root)
    root.mainloop()