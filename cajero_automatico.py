import json
import os

ARCHIVO = "cuentas.json"

# pqrte 1
def cargar_cuentas():
    if not os.path.exists(ARCHIVO):
        return []
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_cuentas(cuentas):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(cuentas, f, indent=4, ensure_ascii=False)

def registrar_cliente(cuentas):
    print("\n=== Registrar Nuevo Cliente ===")
    
    # Validar que el nombre no esté vacío
    while True:
        nombre = input("Ingrese nombre del cliente: ").strip()
        if nombre:
            break
        print(" El nombre no puede estar vacío.")
    
    # Número de cuenta automático 
    ultimo = len(cuentas) + 1
    numero_cuenta = str(ultimo).zfill(6)
    
    # PIN con confirmación
    while True:
        pin = input("Ingrese PIN (4 dígitos): ").strip()
        pin_conf = input("Confirme el PIN: ").strip()
        if len(pin) == 4 and pin.isdigit() and pin == pin_conf:
            break
        print(" El PIN debe tener exactamente 4 dígitos y coincidir.")
    
    # Saldo inicial
    while True:
        try:
            saldo = float(input("Ingrese saldo inicial: $").replace(",", ""))
            if saldo >= 0:
                break
            print(" El saldo no puede ser negativo.")
        except ValueError:
            print(" Ingrese un número válido.")
    
    nuevo_cliente = {
        "nombre": nombre,
        "numero_cuenta": numero_cuenta,
        "pin": pin,
        "saldo": saldo
    }
    cuentas.append(nuevo_cliente)
    guardar_cuentas(cuentas)
    print(f" Cliente registrado. Número de cuenta: {numero_cuenta}")
    return numero_cuenta

# Parte 2
def iniciar_sesion(cuentas):
    print("\n=== Iniciar Sesión ===")
    intentos = 0
    max_intentos = 3
    while intentos < max_intentos:
        num_cuenta = input("Ingrese número de cuenta: ").strip()
        pin_ingresado = input("Ingrese su PIN: ").strip()
        cuenta_actual = None
        for c in cuentas:
            if c["numero_cuenta"] == num_cuenta and c["pin"] == pin_ingresado:
                cuenta_actual = c
                break
        if cuenta_actual:
            print(f"\n ¡Bienvenido/a, {cuenta_actual['nombre']}!")
            menu_cajero(cuenta_actual, cuentas)
            return num_cuenta
        else:
            intentos += 1
            restantes = max_intentos - intentos
            if restantes > 0:
                print(f" Datos incorrectos. Le quedan {restantes} intento(s).")
            else:
                print(" Acceso bloqueado. Demasiados intentos fallidos.")
                return None

def consultar_saldo(cuenta, cuentas):
    saldo_formateado = f"${cuenta['saldo']:,.2f}"
    print(f"\n Saldo actual: {saldo_formateado}")
    return cuenta['saldo']

def retirar(cuenta, cuentas):
    print("\n=== Retirar Dinero ===")
    while True:
        try:
            monto = float(input("Ingrese el monto a retirar: $").replace(",", ""))
            break
        except ValueError:
            print(" Ingrese un valor numérico válido.")
    if monto <= 0:
        print(" El monto debe ser mayor a 0.")
        return False
    if monto > cuenta["saldo"]:
        print(" Fondos insuficientes.")
        return False
    if monto % 1000 != 0:
        print(" El monto debe ser múltiplo de $1.000.")
        return False
    cuenta["saldo"] -= monto
    guardar_cuentas(cuentas)
    print(f" Retiro exitoso. Nuevo saldo: ${cuenta['saldo']:,.2f}")
    return True

def depositar(cuenta, cuentas):
    print("\n=== Depositar Dinero ===")
    while True:
        try:
            monto = float(input("Ingrese el monto a depositar: $").replace(",", ""))
            break
        except ValueError:
            print(" Ingrese un valor numérico válido.")
    if monto <= 0:
        print(" El monto debe ser mayor a 0.")
        return False
    cuenta["saldo"] += monto
    guardar_cuentas(cuentas)
    print(f" Depósito exitoso. Nuevo saldo: ${cuenta['saldo']:,.2f}")
    return True

def cambiar_pin(cuenta, cuentas):
    print("\n=== Cambiar PIN ===")
    pin_actual = input("Ingrese su PIN actual: ").strip()
    if pin_actual != cuenta["pin"]:
        print(" PIN actual incorrecto.")
        return False
    while True:
        nuevo_pin = input("Ingrese nuevo PIN (4 dígitos): ").strip()
        confirmar_pin = input("Confirme nuevo PIN: ").strip()
        if len(nuevo_pin) == 4 and nuevo_pin.isdigit() and nuevo_pin == confirmar_pin:
            cuenta["pin"] = nuevo_pin
            guardar_cuentas(cuentas)
            print(" PIN actualizado correctamente.")
            return True
        else:
            print(" Los PIN no coinciden o no tienen 4 dígitos. Intente de nuevo.\n")

def menu_cajero(cuenta, cuentas):
    while True:
        print("\n" + "-"*40)
        print("          MENÚ DEL CAJERO")
        print("-"*40)
        print("1. Consultar saldo")
        print("2. Retirar dinero")
        print("3. Depositar dinero")
        print("4. Cambiar PIN")
        print("5. Cerrar sesión")
        print("-"*40)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            consultar_saldo(cuenta, cuentas)
        elif opcion == "2":
            retirar(cuenta, cuentas)
        elif opcion == "3":
            depositar(cuenta, cuentas)
        elif opcion == "4":
            cambiar_pin(cuenta, cuentas)
        elif opcion == "5":
            print(" Sesión cerrada correctamente.")
            break
        else:
            print(" Opción no válida. Intente de nuevo.")

def menu_principal(cuentas):
    while True:
        print("\n" + "="*40)
        print("     SISTEMA DE CAJERO AUTOMÁTICO")
        print("="*40)
        print("1. Registrar nuevo cliente")
        print("2. Iniciar sesión")
        print("3. Salir del programa")
        print("="*40)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            registrar_cliente(cuentas)
        elif opcion == "2":
            iniciar_sesion(cuentas)
        elif opcion == "3":
            print(" ¡Gracias por usar el sistema! Hasta pronto.")
            guardar_cuentas(cuentas)
            break
        else:
            print(" Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    cuentas = cargar_cuentas()
    menu_principal(cuentas)
