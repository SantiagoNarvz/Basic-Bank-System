import re #libreria para validacion del RUT

#REGISTRO DE USUARIO
def registro_de_usuario():
    print("""
------------------------------------------------------------
|                   BANCO INACAPINO                        |   
------------------------------------------------------------
          
          |REGISTRO DE USUARIO|
          """)
    global nombre, apellido, rut, datos
    #Validacion nombre
    try:
        while True:
            nombre = input("Ingrese su nombre: ").strip()
            if nombre.replace(" ", "").isalpha() and nombre.strip() != "":
                break
            else:
                print("Error: El nombre debe contener solo letras.")

        #Validacion apellido
        while True:
            apellido = input("Ingrese su apellido: ").strip() #strip para eliminar espacios en blanco y evitar almacenar " "
            if apellido.replace(" ", "").isalpha() and apellido.strip() != "":
                break

            else:
                print("Error: El apellido debe contener solo letras.")

        #Validacion RUT (xx.xxx.xxx-x)
        while True:
            rut = input("Ingrese su RUT (xx.xxx.xxx-x): ").strip()
            if validar_rut(rut):
                break

            else:
                print("Error: El RUT debe tener el formato correcto (xx.xxx.xxx-x).")         
                
        monto, linea, tarjeta = beneficios_deposito()
        
        #Datos del cliente
        datos = {
            "nombre": nombre,
            "apellido": apellido,
            "rut": rut,
            "monto_inicial": monto,
            "linea_credito": linea,
            "tarjeta_credito": tarjeta,
        }
        
        datos["historial"] = []  #Registro de todas las acciones del cliente
        datos["saldo"] = monto  # para tener saldo disponible
        datos["linea_credito_total"] = linea  # para saber cuánto es su linea de credito
                
        return datos
    
    except Exception as e:
        print("Error al ingresar los datos. Por favor, intente nuevamente.")
        return None
    
#Generar Numero de Cuenta
def numero_cuenta(rut):
    global num_c
    num_c = rut.split("-")[0].replace(".", "") #split desde el guion para crear numero de cuenta parecido a cuenta rut
    return num_c

#Validacion de RUT
def validar_rut(rut):
    patron = r'^\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]$' #Rango de caracteres exactos en la validacion del RUT (xx.xxx.xxx-x o xxxxxxxx-x)
    return bool(re.match(patron, rut)) #Validacion del patron del RUT, True si coincide o False sino

#Beneficios de deposito
def beneficios_deposito():
    beneficios = [
        (0, 100000, 50000, 80000),
        (100001, 500000, 250000, 300000),
        (500001, float('inf'), 500000, 700000)  #float('inf') para cualquier numero infinito superior a 500001
    ]
    
#Validacion de monto
    while True:
        try:
            monto = float(input("Ingrese el monto del primer deposito al banco: "))
            if monto <= 0:
                print("Error: El monto debe ser mayor a 0.")
            else:
                break 

#Mensaje de error
        except ValueError:
            print("Error: Ingrese solo numeros.")
                    
    for minimo, maximo, linea, tarjeta in beneficios:
        if minimo <= monto <= maximo:
            return monto, linea, tarjeta

#Resumen completo y detallado
def ver_resumen(cliente):
    print("\n--- RESUMEN COMPLETO DEL CLIENTE ---")
    print(f"Nombre completo     : {cliente['nombre']} {cliente['apellido']}")
    print(f"RUT                 : {cliente['rut']}")
    print(f"Número de cuenta    : {numero_cuenta(cliente['rut'])}")
    print(f"Saldo disponible    : ${cliente['saldo']:.2f}")
    print(f"Línea de crédito    : ${cliente['linea_credito']:.2f} de ${cliente['linea_credito_total']:.2f}")
    print(f"Tarjeta de crédito  : ${cliente['tarjeta_credito']:.2f}")

    if "avance" in cliente:
        avance = cliente["avance"]
        cuotas = avance["cuotas_totales"]
        pagadas = avance["cuotas_pagadas"]
        cuota_mensual = avance["cuota_mensual"]
        capital_pagado = avance["capital_por_cuota"] * pagadas
        capital_restante = avance["monto"] - capital_pagado

        print("\n--- Detalles del avance ---")
        print(f"Monto solicitado     : ${avance['monto']:.2f}")
        print(f"Cuotas pagadas       : {pagadas} de {cuotas}")
        print(f"Cuota mensual        : ${cuota_mensual:.2f}")
        print(f"Capital abonado      : ${capital_pagado:.2f}")
        print(f"Capital pendiente    : ${capital_restante:.2f}")
    else:
        print("\nNo tiene un avance activo.")
    


#Seleccionar contacto
def seleccionar_contacto(cliente):
    contactos = cliente.get("contactos", [])
    print("Contactos registrados: ")
#Lista de contactos
    for i, contacto in enumerate(contactos, 1):
        print(f"{i}. {contacto['nombre']} {contacto['apellido']} (Cuenta: {contacto['cuenta']})")

    print("0. Volver al menu")
    
    while True:
        try:
            opcion = int(input("Seleccione el número del contacto al que desea transferir: "))
            if opcion == 0:
                return None #return None para salir
            if 1 <= opcion <= len(contactos):
                return contactos[opcion - 1]
            else:
                print("Error: Numero fuera de rango.")
#Mensaje de error
        except ValueError:
            print("Error: Debe ingresar un numero.")


#Transferencias
def realizar_transferencia(cliente):
    print("\n--- REALIZAR TRANSFERENCIA ---")
    destinatario = seleccionar_contacto(cliente)
    
    if destinatario is None:
        print("Transferencia cancelada.")
        return
    
    total_disponible = cliente["saldo"] + cliente["linea_credito"]

#Validacion de monto
    while True:
        try:
            monto = float(input("Ingrese el monto a transferir: "))
            if monto <= 0:
                print("Error: El monto debe ser mayor que cero.")
            elif monto > total_disponible:
                print("Saldo insuficiente.")
            else:
                break

#Mensaje de error
        except ValueError: 
            print("Error: Ingrese solo números.") 

#Confirmacion de transferencia
    confirmar = input(f"¿Confirma la transferencia de ${monto:.2f} a {destinatario['nombre']}? (s/n): ").strip().lower()

    if confirmar == "s":
        if monto <= cliente["saldo"]:
            cliente["saldo"] -= monto
            cliente["historial"].append(f"Transferencia de ${monto:.2f} a {destinatario['nombre']} {destinatario['apellido']} (Cuenta: {destinatario['cuenta']})") #A la lista del historial
          
        else:
            restante = monto - cliente["saldo"]
            cliente["saldo"] = 0
            cliente["linea_credito"] -= restante

#Luego de transferir
        print("Transferencia realizada con éxito.")
        print(f"Nuevo saldo: ${cliente['saldo']:.2f}") #2f son 2 decimales en el saldo
        print(f"Línea de crédito restante: ${cliente['linea_credito']:.2f}")

#Transferencia cancelada
    else:
        print("Transferencia cancelada.")


#Realizar Deposito
def realizar_deposito(cliente):
    print("\n--- REALIZAR DEPOSITO ---")
    
    #Validacion de monto
    try:
        monto = float(input("Ingrese el monto a depositar: "))
        if monto <= 0:
            print("Error. El monto debe ser mayor que cero.")
            return
        #Deuda
        deuda = cliente["linea_credito_total"] - cliente["linea_credito"]

        #Pago de deuda y abono a linea de credito
        if deuda > 0:
            if monto >= deuda:
                cliente["linea_credito"] = cliente["linea_credito_total"]
                cliente["saldo"] += (monto - deuda)
                print(f"Se pagó la deuda de la línea de crédito (${deuda:.2f}).")
                print(f"Saldo restante depositado: ${monto - deuda:.2f}")

            else:
                cliente["linea_credito"] += monto
                print(f"Se abonaron ${monto:.2f} a la línea de crédito. Deuda restante: ${deuda - monto:.2f}")

        else:
            cliente["saldo"] += monto
            print(f"Depósito realizado. Nuevo saldo: ${cliente['saldo']:.2f}")

#Mensaje de error
    except ValueError:
        print("Error: Ingrese solo numeros.")

#Avance de tarjeta de credito
def solicitar_avance(cliente):
    print("\n--- SOLICITAR AVANCE CON TARJETA ---")
    if "avance" in cliente:
        avance = cliente["avance"]
        if avance["cuotas_pagadas"] < avance["cuotas_totales"]:
            print("Ya tienes un avance activo, debes pagar todas las cuotas antes de solicitar otro.")
            return
            
    print(f"Monto disponible para el avance: ${cliente['tarjeta_credito']:.2f}")

    while True:
        try:
            monto = float(input("Ingrese el monto a solicitar: "))
            if monto <= 0:
                print("El monto debe ser mayor que cero.")

            elif monto > cliente["tarjeta_credito"]:
                print("El monto excede el maximo de la tarjeta")
            else:
                break

        except ValueError:
            print("Error: ingrese solo numeros.")

#Menu de seleccion de cuotas
    print("""
Seleccione la cantidad de cuotas para su avance:
------------------------------------------------------------
1. 12 cuotas  →  1.5% de interés mensual
2. 24 cuotas  →  3.0% de interés mensual
3. 36 cuotas  →  4.0% de interés mensual
4. 48 cuotas  →  5.0% de interés mensual
------------------------------------------------------------
""")

    opciones_cuotas = {
        "1": (12, 0.015),
        "2": (24, 0.03),
        "3": (36, 0.04),
        "4": (48, 0.05)
    }

    while True:
        opcion = (input("Seleccione el numero de opcion que desee: ")).strip()

        if opcion in opciones_cuotas:
            cuotas, interes_mensual = opciones_cuotas[opcion]
            break
        else:
            print("Error: ingrese un numero entre 1 y 4.")

#Calculos
    capital_por_cuota = monto / cuotas
    interes_por_cuota = capital_por_cuota * interes_mensual
    cuota_mensual = capital_por_cuota + interes_por_cuota


#Datos de avance
    cliente["avance"] = {
        "monto": monto,
        "cuotas_totales": cuotas,
        "cuotas_pagadas": 0,
        "capital_por_cuota": capital_por_cuota,
        "interes_por_cuota": interes_por_cuota,
        "cuota_mensual": cuota_mensual,
}

#
    cliente["saldo"] += monto
    cliente["tarjeta_credito"] -= monto

    print("\nAvance solicitado con exito.")
    print(f"Monto depositado a su cuenta: ${monto:.2f}")
    print(f"Nueva tarjeta disponible: ${cliente['tarjeta_credito']:.2f} ")
    print(f"Cuota mensual a pagar: ${cuota_mensual:.2f} en {cuotas} meses")
    
    cliente["historial"].append(f"Avance solicitado: ${monto:.2f} en {cuotas} cuotas de ${cuota_mensual:.2f}") #Al Historial del cliente


def pagar_cuota_de_avance(cliente):
    print("\n--- PAGO DE CUOTA DE AVANCE ---")
    if "avance" not in cliente:
        print("No se ha solicitado avance.")
        return

    avance = cliente["avance"]

    cuota_actual = avance["cuotas_pagadas"] + 1
    cuota_mensual = avance["cuota_mensual"]
    capital_por_cuota = avance["capital_por_cuota"]

    if cuota_actual > avance["cuotas_totales"]:
        print("Todas las cuotas han sido pagadas.")
        return

    print(f"\nCuota a pagar: {cuota_actual} de {avance['cuotas_totales']}")
    print(f"Monto de la cuota: ${cuota_mensual:.2f}")
    confirmar_pago = input("¿Confirma el pago de esta cuota? (s/n): ").strip().lower()

    if confirmar_pago != "s":
        print("Pago cancelado.")
        return

    saldo_disponible = cliente["saldo"]
    linea_credito_disponible = cliente["linea_credito"]

    if saldo_disponible + linea_credito_disponible < cuota_mensual:
        print("Saldo insuficiente para realizar el pago.")
        return
    
    if saldo_disponible >= cuota_mensual:
        cliente["saldo"] -= cuota_mensual
    else:
        restante = cuota_mensual - saldo_disponible
        cliente["saldo"] = 0
        cliente["linea_credito"] -= restante

    cliente["avance"]["cuotas_pagadas"] += 1
    print("Pago realizado con éxito.")
    
    cliente["historial"].append(f"Pago de cuota {cuota_actual} del avance: ${cuota_mensual:.2f}") #Al historial del cliente


    # Resumen de la cuota
    monto_abonado = capital_por_cuota * cliente["avance"]["cuotas_pagadas"]
    monto_adeudado = avance["monto"] - monto_abonado

    print(f"\nResumen de la cuota {cuota_actual}:")
    print(f"Monto abonado (capital pagado): ${monto_abonado:.2f}")
    print(f"Monto adeudado (capital pendiente): ${monto_adeudado:.2f}")

