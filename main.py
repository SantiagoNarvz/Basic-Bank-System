import os
from banco import ( #Importacion de librerias
    registro_de_usuario,
    numero_cuenta,
    realizar_transferencia,
    realizar_deposito,
    solicitar_avance,
    pagar_cuota_de_avance,
    ver_resumen,
)

def limpiar_consola():
    #en Windows
    if os.name == "nt":
        os.system("cls")
    #para macOS o Linux
    else:
        os.system("clear")
    
#Main function o funcion principal
def main():
    cliente = registro_de_usuario()
    if not cliente:
        return

    # Inicializar
    cliente["saldo"] = cliente["monto_inicial"]
    cliente["linea_credito_total"] = cliente["linea_credito"]
    cliente["contactos"] = [
        {"nombre": "Franklin", "apellido": "Narvaez", "cuenta": "14125085"},
        {"nombre": "Camila",    "apellido": "Narvaez", "cuenta": "27992461"}
    ]

    while True:
        limpiar_consola() 
        print("""
------------------------------------------------------------
|                 MENU DE OPERACIONES BANCARIAS            |
------------------------------------------------------------
1. Ver datos del cliente
2. Realizar transferencia
3. Realizar depósito
4. Solicitar avance con tarjeta de credito
5. Pagar cuota de avance
6. Ver historial de transacciones
7. Ver resumen completo del cliente
0. Salir
------------------------------------------------------------
""")
        op = input("Seleccione una opción: ").strip()
        if op == "1":
            print("\n--- DATOS DEL CLIENTE ---")
            print(f"\nCliente: {cliente['nombre']} {cliente['apellido']}")
            print(f"RUT: {cliente['rut']}    Cuenta: {numero_cuenta(cliente['rut'])}")
            print(f"Saldo: ${cliente['saldo']:.2f}    Línea crédito: ${cliente['linea_credito']:.2f}")
            print(f"Tarjeta de credito: ${cliente['tarjeta_credito']:.2f}\n")

        elif op == "2":
            realizar_transferencia(cliente)

        elif op == "3":
            realizar_deposito(cliente)

        elif op == "4":
            solicitar_avance(cliente)

        elif op == "5":
            pagar_cuota_de_avance(cliente)
        
        elif op == "6":
            print("\n--- HISTORIAL DE TRANSACCIONES ---")
            if cliente["historial"]:
                for i, item in enumerate(cliente["historial"], 1):
                    print(f"{i}. {item}")
                print() 
                
            else:
                print("No hay transacciones registradas aun.")
        
        elif op == "7":
            ver_resumen(cliente)
            
        elif op == "0":
            print("Gracias por usar Banco Inacapino. ¡Hasta luego!")
            break

        else:
            print("Opción inválida. Intente nuevamente.")
        
        input("Presione Enter para continuar...")

if __name__ == "__main__": #para llevar control al importar y que no se ejecute como quiere
    main()
