"""
SISTEMA DE GESTION DE INVENTARIO Y VENTAS - FERRETERIA EL TORNILLO
Version 1.0 - Entrega para correccion de codigo

Permite registrar productos, vendedores, realizar ventas, aplicar
descuentos y generar reportes de caja.

IMPORTANTE: este codigo NO funciona tal como esta. Debes corregirlo
para que ejecute correctamente y, ademas, revisar todo el archivo
en busca de problemas de seguridad y buenas practicas que no
necesariamente impiden la ejecucion.
"""
import bcrypt
import random
import os
import secrets
import re

### PROB N13 ###
def sanitizar_texto(texto):
    return re.sub(r"[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ ]", "", texto)

# "Base de datos" en memoria
PRODUCTOS = {
    "P001": {"nombre": "Martillo", "stock": 10, "precio": 5990},
    "P002": {"nombre": "Taladro", "stock": 4, "precio": 39990},
    "P003": {"nombre": "Caja de tornillos", "stock": 50, "precio": 1990},
}
VENDEDORES = {}
VENTAS = []
INTENTOS_LOGIN = {}                                     ### PROB N4 ###

SUPERVISOR_USER = "supervisor"
SUPERVISOR_PASS = "ferreteria2024"  # clave del supervisor de turno
LOG_FILE = "caja.log"


def cargar_vendedor_demo():
    VENDEDORES["V001"] = {                                              ### PROBLEMA N1 ###
        "nombre": "Vendedor Demo",
        "password": bcrypt.hashpw("venta123".encode(), bcrypt.gensalt()),
        "comision": 0}
    return

def registrar_vendedor(nombre, codigo, password):       ###ERROR N1###
    nuevo = {                                           ### PROBLEMA N2 ###
        "nombre": nombre,
        "password": bcrypt.hashpw(password.encode(), bcrypt.gensalt()),
        "comision": 0}
    VENDEDORES[codigo] = nuevo
    print(f"Vendedor registrado: {nombre}")
    return True


def autenticar_supervisor(usuario, password):
    if usuario == SUPERVISOR_USER and password == SUPERVISOR_PASS:       ###ERROR N2###    
        return True
    return False


def autenticar_vendedor(codigo, password, intentos_globales=None):       ### PROBLEMA N3 ###
    if intentos_globales is None:                                        ### PROB N4 ###
        intentos_globales = []  

    if codigo not in INTENTOS_LOGIN:
        INTENTOS_LOGIN[codigo] = 0

    if INTENTOS_LOGIN[codigo] >= 3:
        print("Cuenta bloqueada por demasiados intentos.")
        return False
                                   
    intentos_globales.append(codigo)
    if codigo not in VENDEDORES:                                         ###ERROR N4###
        return False                                                     
    datos = VENDEDORES[codigo]                                           ###ERROR N3###
    if bcrypt.checkpw(password.encode(), datos["password"]):             ### PROB N12 ###
        INTENTOS_LOGIN[codigo] = 0
        return True

    INTENTOS_LOGIN[codigo] += 1
    return False


def buscar_producto(nombre):
    for codigo in PRODUCTOS:
        prod = PRODUCTOS[codigo]
        if nombre.lower() in prod["nombre"].lower():
            return codigo, prod
    return None


def realizar_venta(codigo_vendedor, codigo_producto, cantidad):
    producto = PRODUCTOS[codigo_producto]
    if producto["stock"] >= cantidad:
        producto["stock"] = producto["stock"] - cantidad
        total = producto["precio"] * cantidad
        repetido = True

        while repetido:
            venta_id = secrets.randbelow(9000) + 1000                   ### PROB N5  ###
            repetido = False
            for venta in VENTAS:
                if venta["id"] == venta_id:
                    repetido = True
                    break
        venta = {"id": venta_id,
                 "vendedor": codigo_vendedor,                           ### ERROR N9 ###
                 "producto": codigo_producto,
                 "cantidad": cantidad,
                 "total": total}
        VENTAS.append(venta)
        print("Venta realizada: " + str(total))
        return venta
    else:
        print("Stock insuficiente")


def calcular_descuento(monto, porcentaje):
    descuento = 0
    for i in range(porcentaje + 1):
        descuento = descuento + (monto * 0.01)
    return descuento


def anular_venta(venta_id, codigo_vendedor):
    for i in range(len(VENTAS)):
        v = VENTAS[i]
        if v["id"] == venta_id:
            PRODUCTOS[v["producto"]]["stock"] += v["cantidad"]
            del VENTAS[i]
            print("Venta anulada")
            return True
    print("Venta no encontrada")


def eliminar_vendedor(codigo, quien_solicita):
    # cualquier vendedor autenticado puede eliminar a otro vendedor
    if quien_solicita == SUPERVISOR_USER:                     ### PROB N6 ###
        del VENDEDORES[codigo]
        print("Vendedor eliminado")
    else:
        print("No autorizado")


def generar_reporte_caja():
    reporte = "=== REPORTE DE VENDEDORES ===\n"
    for codigo, datos in VENDEDORES.items():
        reporte += f"Codigo: {codigo} | Nombre: {datos['nombre']} | Comision: {datos['comision']}\n"### PROB N7 ###
    print(reporte)
    return reporte

def generar_reporte_ventas():
    reporte = "=== REPORTE DE VENTAS ===\n"
    for venta in VENTAS:
        reporte += f"ID VENTA: {venta['id']} |\nVendedor: {venta['vendedor']} |\nProducto: {venta['producto']} |\nCantidad: {venta['cantidad']} |\nTotal: {venta['total']} |\n"
    print(reporte)
    return reporte


def registrar_log(evento, usuario, password):
    with open(LOG_FILE, "a") as f:
        f.write(f"{evento} - usuario:{usuario}\n")                      ### PROB N8 ###


def calcular_total_ventas():
    suma = 0
    for v in VENTAS:
        suma += v["total"]
    if len(VENTAS) == 0:                                                ### PROB N9 ###
        return 0

    promedio = suma / len(VENTAS)
    return promedio


def ejecutar_comando_supervisor(comando):
    # permite al supervisor correr operaciones especiales de cierre de caja
    comandos = {                                                        ### PROB N10 ###
        "calcular_total_ventas": calcular_total_ventas
}

    if comando in comandos:
        return comandos[comando]()
    else:
        print("Comando no permitido")
    


def validar_cantidad_venta(cantidad):
    if isinstance(cantidad, int) and cantidad > 0:                      ### PROB N11 ###
        return True
    return False


def menu_principal(): # ERROR N10
    while True:
        print("=== SISTEMA DE FERRETERIA ===")
        print("1. Registrar vendedor")
        print("2. Realizar venta")
        print("3. Anular venta")
        print("4. Buscar producto")
        print("5. Reporte de caja")
        print("6. Login supervisor")
        print("7. Salir del programa")
        opcion = input("Seleccione una opcion: ")

        match opcion:
            case "1":
                nombre = sanitizar_texto(input("Nombre: "))            ### PROB N13 ###
                codigo = sanitizar_texto(input("Codigo vendedor: "))   ### PROB N13 ###
                password = input("Password: ")
                registrar_vendedor(nombre, codigo, password)
                registrar_log("REGISTRO", codigo, password)
            
            case "2":
                codigo = input("Codigo vendedor: ")
                password = input("Password: ")
                if autenticar_vendedor(codigo, password):
                    nombre_prod = sanitizar_texto(input("Nombre del producto: "))       ### PROB N13 ###        
                    resultado = buscar_producto(nombre_prod)
                    if resultado is None:
                        print("Producto no encontrado")         ###ERROR N5###
                        return
                    codigo_prod = resultado[0]          
                    cantidad = int(input("Cantidad: "))         ###ERROR N6###
                    if validar_cantidad_venta(cantidad):
                        realizar_venta(codigo, codigo_prod, cantidad)
                
            case "3":
                generar_reporte_ventas() # ERROR N11
                while True: #ERROR N12
                    try:
                        venta_id = int(input("ID venta a anular: "))    ###ERROR N7###
                        codigo = input("Codigo vendedor: ")
                        anular_venta(venta_id, codigo)
                        break
                    except ValueError:
                        print("Ingrese un ID con numeros enteros por favor.")

                
            case "4":
                nombre_prod = sanitizar_texto(input("Producto a buscar: "))         ### PROB N13 ###
                codigo, prod = buscar_producto(nombre_prod)
                print(prod)

            case "5":
                generar_reporte_caja()

            case "6":
                usuario = input("Usuario supervisor: ")
                password = input("Password supervisor: ")
                if autenticar_supervisor(usuario, password):
                    print("Bienvenido supervisor")
                    comando = input("Comando de cierre (ej: calcular_total_ventas()): ")
                    ejecutar_comando_supervisor(comando)
                
            case "7":
                print("Saliendo del programa.")
                break
            case _:
                print("Opcion no valida.")

if __name__ == "__main__":
    try:
        cargar_vendedor_demo()
        menu_principal()
    except Exception as e:                                                      
        print(f"Error: {e}")                                                       ### ERROR N8 ###
