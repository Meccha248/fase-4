import logging
import re
from abc import ABC, abstractmethod

# --- 1. GESTOR DE LOGS ---
class GestorLogs:
    logging.basicConfig(
        filename='registro_errores.log',
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    @staticmethod
    def registrar_error(mensaje, excepcion=None):
        if excepcion:
            logging.error(f"{mensaje} | Detalle: {str(excepcion)}")
        else:
            logging.error(mensaje)


# --- 2. EXCEPCIONES PERSONALIZADAS ---
class SistemaGestionError(Exception):
    pass

class ClienteInvalidoError(SistemaGestionError):
    pass

class ServicioNoDisponibleError(SistemaGestionError):
    pass

class ReservaInvalidaError(SistemaGestionError):
    pass


# --- 3. CLASES BASE Y ENTIDADES ---
class EntidadBase(ABC):
    def __init__(self, id_entidad):
        self._id_entidad = id_entidad

    @property
    def id_entidad(self):
        return self._id_entidad

    @abstractmethod
    def mostrar_detalles(self):
        pass


class Cliente(EntidadBase):
    def __init__(self, id_entidad, nombre, documento, email):
        super().__init__(id_entidad)
        self.__nombre = None
        self.__documento = None
        self.__email = None
        
        self.nombre = nombre
        self.documento = documento
        self.email = email

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")
        self.__nombre = valor.strip()

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        if not str(valor).isdigit():
            raise ClienteInvalidoError("El documento debe contener únicamente números.")
        self.__documento = str(valor)

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(patron, valor):
            raise ClienteInvalidoError(f"El correo '{valor}' no tiene un formato válido.")
        self.__email = valor

    def mostrar_detalles(self):
        return f"Cliente: {self.nombre} | Documento: {self.documento} | Email: {self.email}"


class Servicio(EntidadBase):
    def __init__(self, id_entidad, nombre_servicio, precio_base):
        super().__init__(id_entidad)
        self._nombre_servicio = nombre_servicio
        self._precio_base = precio_base

    @abstractmethod
    def calcular_costo_final(self):
        pass

    def mostrar_detalles(self):
        return f"Servicio: {self._nombre_servicio} | Precio Base: ${self._precio_base}"
    
    # --- 4. SERVICIOS ESPECIALIZADOS (Herencia y Polimorfismo) ---

class ReservaSala(Servicio):
    def __init__(self, id_entidad, nombre_servicio, precio_base, capacidad):
        # Usamos super() para inicializar los atributos de la clase padre
        super().__init__(id_entidad, nombre_servicio, precio_base)
        self.capacidad = capacidad

    # Polimorfismo y Sobrecarga: Método con parámetros opcionales
    def calcular_costo_final(self, horas, descuento=0.0, impuesto=0.0):
        costo_inicial = self._precio_base * horas
        costo_con_descuento = costo_inicial - (costo_inicial * descuento)
        costo_final = costo_con_descuento + (costo_con_descuento * impuesto)
        return costo_final

    def mostrar_detalles(self):
        return f"Sala: {self._nombre_servicio} | Capacidad: {self.capacidad} personas | Precio/Hora: ${self._precio_base}"


class AlquilerEquipo(Servicio):
    def __init__(self, id_entidad, nombre_servicio, precio_base, requiere_deposito):
        super().__init__(id_entidad, nombre_servicio, precio_base)
        self.requiere_deposito = requiere_deposito  # Booleano (True/False)

    def calcular_costo_final(self, dias, descuento=0.0, impuesto=0.0):
        costo_inicial = self._precio_base * dias
        # Lógica distinta: Si requiere depósito, sumamos un 20% extra al inicio
        deposito = costo_inicial * 0.2 if self.requiere_deposito else 0
        costo_con_descuento = costo_inicial - (costo_inicial * descuento)
        costo_final = costo_con_descuento + (costo_con_descuento * impuesto) + deposito
        return costo_final

    def mostrar_detalles(self):
        deposito_txt = "Sí" if self.requiere_deposito else "No"
        return f"Equipo: {self._nombre_servicio} | Depósito Requerido: {deposito_txt} | Precio/Día: ${self._precio_base}"


class AsesoriaEspecializada(Servicio):
    def __init__(self, id_entidad, nombre_servicio, precio_base, nivel_experto):
        super().__init__(id_entidad, nombre_servicio, precio_base)
        self.nivel_experto = nivel_experto  # Ej: 'Junior' o 'Senior'

    def calcular_costo_final(self, sesiones, descuento=0.0, tarifa_adicional=0.0):
        # Lógica distinta: La asesoría cobra por sesiones. Si es Senior, es más costoso.
        costo_inicial = self._precio_base * sesiones
        if self.nivel_experto.lower() == 'senior':
            costo_inicial *= 1.5  # 50% de recargo por ser Senior
            
        costo_con_descuento = costo_inicial - (costo_inicial * descuento)
        costo_final = costo_con_descuento + tarifa_adicional
        return costo_final

    def mostrar_detalles(self):
        return f"Asesoría: {self._nombre_servicio} | Nivel: {self.nivel_experto} | Precio/Sesión Base: ${self._precio_base}"
    
    # --- 5. CLASE RESERVA Y MANEJO AVANZADO DE EXCEPCIONES ---

class Reserva:
    def __init__(self, id_reserva, cliente, servicio, duracion):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"  # Estados posibles: Pendiente, Confirmada, Cancelada, Finalizada

    def confirmar_reserva(self):
        """Método que demuestra el uso de try / except / else / finally y encadenamiento"""
        print(f"\n--- Procesando confirmación de Reserva ID: {self.id_reserva} ---")
        
        try:
            # Validaciones para forzar posibles errores
            if not isinstance(self.cliente, Cliente):
                raise ValueError("El objeto cliente no es de la clase Cliente.")
            
            if not isinstance(self.servicio, Servicio):
                raise ValueError("El objeto servicio no es válido.")
                
            if self.duracion <= 0:
                raise ValueError("La duración del servicio debe ser mayor a 0.")

            if self.estado == "Cancelada":
                raise ReservaInvalidaError("No se puede confirmar una reserva que ya fue cancelada.")
                
        except ValueError as e:
            # Encadenamiento de excepciones: Capturamos un ValueError y lanzamos nuestro error personalizado
            GestorLogs.registrar_error(f"Fallo de validación en Reserva {self.id_reserva}", e)
            raise ReservaInvalidaError(f"Datos inconsistentes en la reserva: {str(e)}") from e
            
        except ReservaInvalidaError as e:
            # Capturamos errores específicos de la lógica de negocio
            GestorLogs.registrar_error(f"Operación no permitida en Reserva {self.id_reserva}", e)
            print(f"❌ Error al confirmar: {e}")
            
        else:
            # El bloque ELSE solo se ejecuta si el TRY no generó ninguna excepción
            self.estado = "Confirmada"
            print(f"✅ Éxito: La reserva {self.id_reserva} ha sido confirmada correctamente.")
            
        finally:
            # El bloque FINALLY se ejecuta SIEMPRE, haya ocurrido un error o no
            print(f"ℹ️ Fin del proceso de confirmación para la reserva {self.id_reserva}.")

    def procesar_pago(self, descuento=0.0):
        """Procesa el pago solo si la reserva está confirmada"""
        try:
            if self.estado != "Confirmada":
                raise ReservaInvalidaError("Solo se pueden procesar pagos de reservas confirmadas.")
            
            # Polimorfismo en acción: No importa qué servicio sea, Python sabrá cómo calcularlo
            costo_total = self.servicio.calcular_costo_final(self.duracion, descuento=descuento)
            self.estado = "Finalizada"
            print(f"💰 Pago procesado. Costo total: ${costo_total:.2f}. Estado de reserva: {self.estado}")
            return costo_total
            
        except ReservaInvalidaError as e:
            GestorLogs.registrar_error(f"Error de pago en Reserva {self.id_reserva}", e)
            print(f"❌ Error al pagar: {e}")
            return None

    def cancelar_reserva(self):
        try:
            if self.estado in ["Cancelada", "Finalizada"]:
                raise ReservaInvalidaError(f"No se puede cancelar una reserva en estado: {self.estado}")
            self.estado = "Cancelada"
            print(f"🚫 Reserva {self.id_reserva} cancelada correctamente.")
        except ReservaInvalidaError as e:
            GestorLogs.registrar_error(f"Intento de cancelación fallido en Reserva {self.id_reserva}", e)
            print(f"❌ Error al cancelar: {e}")
            
    def mostrar_resumen(self):
        nombre_cliente = self.cliente.nombre if hasattr(self.cliente, 'nombre') else "Desconocido"
        nombre_servicio = self.servicio._nombre_servicio if hasattr(self.servicio, '_nombre_servicio') else "Desconocido"
        return f"Reserva [{self.id_reserva}] | Estado: {self.estado} | Cliente: {nombre_cliente} | Servicio: {nombre_servicio}"
    
# --- 6. SIMULACIÓN DEL SISTEMA (10 OPERACIONES) ---

if __name__ == "__main__":
    print("="*50)
    print(" INICIANDO SIMULACIÓN DEL SISTEMA SOFTWARE FJ")
    print("="*50)

    # 1. Registro de cliente VÁLIDO
    try:
        cliente_valido = Cliente(1, "Carlos Ramirez", "1020304050", "carlos@email.com")
        print(f"1. ✅ ÉXITO: {cliente_valido.mostrar_detalles()}")
    except Exception as e:
        print(f"1. ❌ ERROR: {e}")

    # 2. Registro de cliente INVÁLIDO (Correo mal formateado)
    try:
        cliente_invalido = Cliente(2, "Ana", "987654", "ana_sin_arroba_email.com")
    except ClienteInvalidoError as e:
        GestorLogs.registrar_error("Fallo al registrar cliente 2", e)
        print(f"2. 🛡️ EXCEPCIÓN ATRAPADA (Cliente): {e}")

    # 3. Creación de servicio VÁLIDO (Sala)
    sala_juntas = ReservaSala(101, "Sala de Juntas Principal", 50000, 15)
    print(f"3. ✅ ÉXITO: {sala_juntas.mostrar_detalles()}")

    # 4. Creación de servicio VÁLIDO (Asesoría Senior)
    asesoria_bd = AsesoriaEspecializada(102, "Optimización de Código", 120000, "Senior")
    print(f"4. ✅ ÉXITO: {asesoria_bd.mostrar_detalles()}")

    # 5. Creación de Reserva VÁLIDA
    reserva_ok = Reserva(1001, cliente_valido, sala_juntas, duracion=4)
    print(f"5. ✅ ÉXITO: {reserva_ok.mostrar_resumen()} ha sido creada en estado Pendiente.")

    # 6. Confirmación de Reserva (Uso de Try/Except/Else/Finally)
    print("\n--- Operación 6: Intentando confirmar reserva válida ---")
    reserva_ok.confirmar_reserva()

    # 7. Procesamiento de Pago Exitoso (Con polimorfismo y sobrecarga de descuento)
    print("\n--- Operación 7: Procesando pago ---")
    reserva_ok.procesar_pago(descuento=0.10)  # 10% de descuento

    # 8. Intento de Pago INVÁLIDO (La reserva no está confirmada)
    reserva_fallida1 = Reserva(1002, cliente_valido, asesoria_bd, duracion=2)
    print("\n--- Operación 8: Intentando pagar sin confirmar ---")
    reserva_fallida1.procesar_pago()

    # 9. Cancelación de Reserva VÁLIDA
    print("\n--- Operación 9: Cancelando reserva ---")
    reserva_fallida1.cancelar_reserva()

   # 10. Confirmación INVÁLIDA (Datos corruptos)
    print("\n--- Operación 10: Intentando confirmar reserva con datos corruptos ---")
    try:
        reserva_corrupta = Reserva(1003, cliente_valido, "Esto no es un servicio", duracion=-5)
        reserva_corrupta.confirmar_reserva()
    except ReservaInvalidaError as e:
        # Atrapamos el error encadenado para que el programa no se estrelle
        print(f"10. 🛡️ EXCEPCIÓN ATRAPADA CON ÉXITO: {e}")

    print("\n" + "="*50)
    print(" SIMULACIÓN FINALIZADA SIN INTERRUPCIONES")
    print("="*50)
