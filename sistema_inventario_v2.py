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

import random
import os

# "Base de datos" en memoria
PRODUCTOS = {
    "P001": {"nombre": "Martillo", "stock": 10, "precio": 5990},
    "P002": {"nombre": "Taladro", "stock": 4, "precio": 39990},
    "P003": {"nombre": "Caja de tornillos", "stock": 50, "precio": 1990},
}
VENDEDORES = {}
VENTAS = []

SUPERVISOR_USER = "supervisor"
SUPERVISOR_PASS = "ferreteria2024"  # clave del supervisor de turno

LOG_FILE = "caja.log"


def cargar_vendedor_demo():
    VENDEDORES["V001"] = {"nombre": "Vendedor Demo", "password": "venta123", "comision": 0}
    return


def registrar_vendedor(nombre, codigo, password)
    nuevo = {"nombre": nombre, "password": password, "comision": 0}
    VENDEDORES[codigo] = nuevo
    print(f"Vendedor registrado: {nombre}")
    return True


def autenticar_supervisor(usuario, password):
    if usuario == SUPERVISOR_USER and password = SUPERVISOR_PASS:
        return True
    return False


def autenticar_vendedor(codigo, password, intentos_globales=[]):
    intentos_globales.append(codigo)
        datos = VENDEDORES[codigo]
    if datos["password"] == password:
        return True
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
        venta_id = random.randint(1000, 9999)
        venta = {"vendedor": codigo_vendedor, "producto": codigo_producto, "cantidad": cantidad, "total": total, "id": venta_id}
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
    if quien_solicita in VENDEDORES:
        del VENDEDORES[codigo]
        print("Vendedor eliminado")
    else:
        print("No autorizado")


def generar_reporte_caja():
    reporte = "=== REPORTE DE VENDEDORES ===\n"
    for codigo, datos in VENDEDORES.items():
        reporte += f"Codigo: {codigo} | Nombre: {datos['nombre']} | Password: {datos['password']} | Comision: {datos['comision']}\n"
    print(reporte)
    return reporte


def registrar_log(evento, usuario, password):
    with open(LOG_FILE, "a") as f:
        f.write(f"{evento} - usuario:{usuario} password:{password}\n")


def calcular_total_ventas():
    suma = 0
    for v in VENTAS:
        suma += v["total"]
    promedio = suma / len(VENTAS)
    return promedio


def ejecutar_comando_supervisor(comando):
    # permite al supervisor correr operaciones especiales de cierre de caja
    resultado = eval(comando)
    return resultado


def validar_cantidad_venta(cantidad):
    if cantidad > 0:
        return True


def menu_principal():
    print("=== SISTEMA DE FERRETERIA ===")
    print("1. Registrar vendedor")
    print("2. Realizar venta")
    print("3. Anular venta")
    print("4. Buscar producto")
    print("5. Reporte de caja")
    print("6. Login supervisor")
    opcion = input("Seleccione una opcion: ")

    if opcion == "1":
        nombre = input("Nombre: ")
        codigo = input("Codigo vendedor: ")
        password = input("Password: ")
        registrar_vendedor(nombre, codigo, password)
        registrar_log("REGISTRO", codigo, password)

    elif opcion == "2":
        codigo = input("Codigo vendedor: ")
        password = input("Password: ")
        if autenticar_vendedor(codigo, password):
            nombre_prod = input("Nombre del producto: ")
            resultado = buscar_producto(nombre_prod)
            codigo_prod = resultado[0]
            cantidad = input("Cantidad: ")
            if validar_cantidad_venta(cantidad):
                realizar_venta(codigo, codigo_prod, cantidad)

    elif opcion == "3":
        venta_id = input("ID venta a anular: ")
        codigo = input("Codigo vendedor: ")
        anular_venta(venta_id, codigo)

    elif opcion == "4":
        nombre_prod = input("Producto a buscar: ")
        codigo, prod = buscar_producto(nombre_prod)
        print(prod)

    elif opcion == "5":
        generar_reporte_caja()

    elif opcion == "6":
        usuario = input("Usuario supervisor: ")
        password = input("Password supervisor: ")
        if autenticar_supervisor(usuario, password):
            print("Bienvenido supervisor")
            comando = input("Comando de cierre (ej: calcular_total_ventas()): ")
            ejecutar_comando_supervisor(comando)


if __name__ == "__main__":
    try:
        cargar_vendedor_demo()
        menu_principal()
    except:
        pass
