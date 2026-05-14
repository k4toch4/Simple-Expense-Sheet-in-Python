import argparse
import pyexcel_ods3 as ods
from datetime import datetime

ARCHIVO = "registros.ods"
HOJA = "Hoja1"
ENCABEZADOS = ["Fecha", "Descripcion", "Tipo", "Monto"]

def leer_ods():
    # Carga los datos del archivo ODS. Retorna lista de filas incluyendo encabezados.
    try:
        datos = ods.get_data(ARCHIVO)
        filas = (datos.get(HOJA, []))
        # Codigo para eliminar errores en las filas
        # Si fila esta vacia devuelve el encabezado
        if not filas:
            filas = [ENCABEZADOS]
        # Asegura que la primera fila sea el encabezado correcto
        if filas[0] != ENCABEZADOS:
            filas.insert(0, ENCABEZADOS)
        return filas    
    except FileNotFoundError:
        return [ENCABEZADOS]

def escribir_ods(filas):
    # Guarda la lista de filas en el archivo ODS.
    ods.save_data(ARCHIVO, {HOJA: filas})

def agregar_registro(tipo, descripcion, monto, fecha=None):
    # Verificar que tipo sea ingreso o egreso
    if tipo not in ("ingreso", "egreso"):
        raise ValueError("Tipo debe ser 'ingreso' o 'egreso'")
    # Usar la fecha actual por defecto
    if fecha is None:
        fecha = datetime.now().strftime("%Y-%m-%d")
    # Monto como float para sumar los decimales
    monto = float(monto)
    # Llamamos a la funcion para leer filas y creamos filas nuevas
    filas = leer_ods()
    nueva_fila = [fecha, descripcion, tipo, str(monto)]
    filas.append(nueva_fila)
    # Escribimos la fila nueva en el documento
    escribir_ods(filas)

def obtener_saldo(mes=None, anio=None):
    # Calcula el saldo (ingresos - gastos). Si se especifica mes, filtra por ese mes y año.
    filas = leer_ods()
    ingresos = 0.0
    egresos = 0.0
    ahora = datetime.now()
    
    #Si se da el mes y no el anio se toma el anio actual
    if mes is not None:
        if anio is None:
            anio = ahora.year
        prefijo = f"{anio}-{mes:02d}-"
    
    #
    for fila in filas[1:]:  # Saltar encabezado
        if len(fila) < 4:
            continue
        fecha, desc, tipo, monto_str = fila[0], fila[1], fila[2], fila[3]
        if mes is not None and not fecha.startswith(prefijo):
            continue
        monto = float(monto_str)
        if tipo == "ingreso":
            ingresos += monto
        elif tipo == "egreso":
            egresos += monto
    return ingresos - egresos

def listar_registros(tipo, fecha_desde=None, fecha_hasta=None, descripcion=None):
    # Devuelve lista de registros que coinciden con los filtros. No incluye encabezado.
    filas = leer_ods()
    resultados = []
    
    for fila in filas[1:]:
        if len(fila) < 4:
            continue
        fecha, desc, tipo_reg, monto = fila[0], fila[1], fila[2], fila[3]
        if tipo_reg != tipo:
            continue
        if fecha_desde and fecha < fecha_desde:
            continue
        if fecha_hasta and fecha > fecha_hasta:
            continue
        if descripcion and descripcion.lower() not in desc.lower():
            continue
        resultados.append(fila)
    return resultados

def main():
    # Utilizamos argparse para definir argumentos
    parse = argparse.ArgumentParser(description="Gestor de gastos en ODS")
    subparse = parse.add_subparsers(dest="comando", required=True)

    # Subcomando: add
    parse_add = subparse.add_parser("add", help="Agregar registro")
    parse_add.add_argument("tipo", choices=["ingreso", "egreso"], help="Tipo de registro")
    parse_add.add_argument("descripcion", help="Descripcion del movimiento")
    parse_add.add_argument("monto", type=float, help="Monto (positivo)")
    parse_add.add_argument("--fecha", help="Fecha en formato YYYY-MM-DD (por defecto hoy)")

    # Subcomando saldo
    parser_saldo = subparse.add_parser("saldo", help="Consultar saldo global o mensual")
    parser_saldo.add_argument("--mes", type=int, choices=range(1,13), help="Mes (1-12)")
    parser_saldo.add_argument("--anio", type=int, help="Año (YYYY). Por defecto, año actual si se especifica mes")
    
    # Subcomando listar
    parser_listar = subparse.add_parser("listar", help="Listar registros con filtros")
    parser_listar.add_argument("--tipo", choices=["ingreso", "egreso"], required=True, help="Tipo de registro")
    parser_listar.add_argument("--fecha-desde", help="Fecha mínima (YYYY-MM-DD)")
    parser_listar.add_argument("--fecha-hasta", help="Fecha máxima (YYYY-MM-DD)")
    parser_listar.add_argument("--descripcion", help="Texto a buscar en la descripción (parcial)")

    args = parse.parse_args()

    if args.comando == "add":
        agregar_registro(args.tipo, args.descripcion, args.monto, args.fecha)
        print("Registro agregado.")

    elif args.comando == "saldo":
        saldo = obtener_saldo(args.mes, args.anio)
        if args.mes:
            anio = args.anio if args.anio else datetime.now().year
            print(f"Saldo para {args.mes:02d}/{anio}: {saldo:.2f}")
        else:
            print(f"Saldo global: {saldo:.2f}")

    elif args.comando == "listar":
        resultados = listar_registros(args.tipo, args.fecha_desde, args.fecha_hasta, args.descripcion)
        if resultados:
            print(f"{'Fecha':<12} {'Descripción':<30} {'Tipo':<8} {'Monto':>10}")
            print("-" * 65)
            for fila in resultados:
                print(f"{fila[0]:<12} {fila[1]:<30} {fila[2]:<8} {float(fila[3]):>10.2f}")
            print(f"\nTotal de registros: {len(resultados)}")
        else:
            print("No se encontraron registros con los filtros especificados.")

if __name__ == "__main__":
    main()
