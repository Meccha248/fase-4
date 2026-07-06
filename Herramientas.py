import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# --- CLASE PRINCIPAL: HerramientaAlquiler ---
class HerramientaAlquiler:
    def __init__(self, id_herramienta, tarifa_hora):
        self._id_herramienta = id_herramienta
        self._tarifa_hora = tarifa_hora  # Tarifa en COP
        self._hora_salida_dt = None

    def registrar_salida(self, hora_str):
        try:
            self._hora_salida_dt = datetime.strptime(hora_str, "%H:%M")
            return True
        except ValueError:
            return False

    def calcular_costo(self, hora_retorno_str):
        try:
            hora_retorno_dt = datetime.strptime(hora_retorno_str, "%H:%M")
            if self._hora_salida_dt is None or hora_retorno_dt <= self._hora_salida_dt:
                return None, None
            
            diferencia = hora_retorno_dt - self._hora_salida_dt
            horas_totales = diferencia.total_seconds() / 3600
            costo_final = horas_totales * self._tarifa_hora
            
            return horas_totales, costo_final
        except ValueError:
            return None, None

    def obtener_id(self):
        return self._id_herramienta

# --- INTERFAZ GRÁFICA ---
class AppAlquiler:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Alquiler - Colombia")
        self.root.geometry("450x400")
        
        # Ajustamos las tarifas a valores en COP (ej: 15.000 la hora)
        self.inventario = [
            HerramientaAlquiler("Taladro Industrial", 15000),
            HerramientaAlquiler("Sierra Circular", 20000),
            HerramientaAlquiler("Andamio Tubo", 5000),
            HerramientaAlquiler("Compresor de aire", 7000),
            HerramientaAlquiler("Planta Eléctrica", 45000),
            HerramientaAlquiler("Pulidora de Disco", 12000)            
        ]
        self.pantalla_login()

    def pantalla_login(self):
        self.limpiar_pantalla()
        tk.Label(self.root, text="SISTEMA DE GESTIÓN HERRAMIENTAS", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(self.root, text="Autor: Cristhian Hernández").pack()
        
        tk.Label(self.root, text="\nUsuario:").pack()
        self.ent_user = tk.Entry(self.root)
        self.ent_user.pack()
        
        tk.Label(self.root, text="Contraseña:").pack()
        self.ent_pass = tk.Entry(self.root, show="*")
        self.ent_pass.pack()
        
        tk.Button(self.root, text="Ingresar", command=self.validar_login).pack(pady=20)

    def validar_login(self):
        if self.ent_user.get() == "programación" and self.ent_pass.get() == "programación":
            self.pantalla_gestion()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    def pantalla_gestion(self):
        self.limpiar_pantalla()
        tk.Label(self.root, text="FACTURACIÓN EN PESOS (COP)", font=("Arial", 10, "bold")).pack(pady=10)
        
        tk.Label(self.root, text="Herramienta:").pack()
        self.lista_h = tk.StringVar(self.root)
        self.lista_h.set(self.inventario[0].obtener_id())
        opciones = [h.obtener_id() for h in self.inventario]
        tk.OptionMenu(self.root, self.lista_h, *opciones).pack(pady=5)

        tk.Label(self.root, text="Hora Salida (HH:MM):").pack()
        self.ent_h_salida = tk.Entry(self.root)
        self.ent_h_salida.insert(0, "08:00")
        self.ent_h_salida.pack()

        tk.Label(self.root, text="Hora Retorno (HH:MM):").pack()
        self.ent_h_retorno = tk.Entry(self.root)
        self.ent_h_retorno.insert(0, "13:30")
        self.ent_h_retorno.pack()

        tk.Button(self.root, text="Generar Cobro COP", command=self.procesar_alquiler, bg="#008CBA", fg="white").pack(pady=20)

        tk.Button(self.root, text="Salir del Sistema", command=self.root.destroy, bg="#f44336", fg="white").pack(pady=10)

    def procesar_alquiler(self):
        id_sel = self.lista_h.get()
        h_salida_str = self.ent_h_salida.get()
        h_retorno_str = self.ent_h_retorno.get()
        
        herramienta = next(h for h in self.inventario if h.obtener_id() == id_sel)
        
        if herramienta.registrar_salida(h_salida_str):
            horas, costo = herramienta.calcular_costo(h_retorno_str)
            
            if horas is not None:
                # Formateo de moneda: 
                # {:,.0f} agrega comas como separadores de miles y 0 decimales
                costo_formateado = "{:,.0f}".format(costo).replace(",", ".")
                
                res = (f"RECIBO DE ALQUILER\n"
                       f"--------------------------\n"
                       f"Herramienta: {id_sel}\n"
                       f"Tiempo: {horas:.2f} horas\n"
                       f"TOTAL A PAGAR: ${costo_formateado} COP")
                messagebox.showinfo("Factura Final", res)
            else:
                messagebox.showwarning("Error", "Verifique las horas ingresadas.")
        else:
            messagebox.showerror("Error", "Formato de hora inválido.")

    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AppAlquiler(root)
    root.mainloop()