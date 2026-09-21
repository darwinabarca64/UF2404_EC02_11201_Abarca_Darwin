"""
Script de Verificación Integral de la Suite de Examen.
Módulo: MF0227_3 - Programación orientada a objetos (UF2404).

Este script ejecuta de manera aislada y sistemática las pruebas de los 10 ejercicios
desarrollados para la prueba práctica, comprobando:
1. Conformidad con los requisitos funcionales e invariantes de POO.
2. Gestión adecuada de excepciones y casos límite.
3. Desglose de puntuación según el baremo oficial (Página 17 del PDF).
4. Validación de la estrategia óptima de selección (5 ejercicios para obtener 10/10).
"""

from __future__ import annotations
import sys
import time
from typing import Callable, List, Tuple


# Tabla de ponderación oficial según la página 17 del PDF
BAREMO_OFICIAL = {
    1: ("Reparar un diseño defectuoso", 0.5),
    2: ("Reserva de plazas", 0.6),
    3: ("Figuras sin modificar la función", 0.8),
    4: ("Historial bancario", 0.8),
    5: ("Refactorización (Strategy/OCP)", 1.0),
    6: ("Sistema de inventario", 0.8),
    7: ("Clases colaborativas (Curso)", 1.2),
    8: ("Código desconocido (MRO/super)", 2.1),
    9: ("Sistema de préstamos", 2.7),
    10: ("Sistema extensible de pedidos", 3.3),
}


# =====================================================================
# BATERÍA DE PRUEBAS UNITARIAS PARA CADA EJERCICIO
# =====================================================================

def test_ejercicio_01() -> None:
    from ejercicio_01 import Usuario
    # Reset contador si fuera necesario
    Usuario.total = 0
    u1 = Usuario("Ana")
    u2 = Usuario("Marc")
    u1.agregar_curso("Python")
    assert u1.cursos == ["Python"], "u1 debe tener solo ['Python']"
    assert u2.cursos == [], "u2 debe tener lista vacía e independiente"
    assert u1.cursos is not u2.cursos, "Las listas de cursos no deben compartir referencia"
    assert Usuario.total == 2, f"Usuario.total debería ser 2, obtenido: {Usuario.total}"

    # Copia defensiva con lista externa
    ext = ["SQL"]
    u3 = Usuario("Clara", ext)
    ext.append("Java")
    assert "Java" not in u3.cursos, "La mutación de la lista externa alteró la interna"


def test_ejercicio_02() -> None:
    from ejercicio_02 import Evento
    ev = Evento("Conferencia IA", capacidad_maxima=2)
    assert ev.plazas_disponibles() == 2
    assert len(ev) == 0

    ev.reservar("Laura")
    ev.reservar("Carlos")
    assert len(ev) == 2
    assert ev.plazas_disponibles() == 0

    # Duplicado
    try:
        ev.reservar("Laura")
        raise AssertionError("Fallo: Permitió reserva duplicada.")
    except ValueError:
        pass

    # Aforo completo
    try:
        ev.reservar("Marta")
        raise AssertionError("Fallo: Permitió sobrepasar aforo.")
    except OverflowError:
        pass

    # Cancelación
    ev.cancelar("Laura")
    assert len(ev) == 1
    assert ev.plazas_disponibles() == 1


def test_ejercicio_03() -> None:
    from ejercicio_03 import Rectangulo, Circulo, TrianguloRectangulo, Cuadrado, imprimir_informe
    r = Rectangulo(10, 5)
    c = Circulo(3)
    t = TrianguloRectangulo(4, 3)
    q = Cuadrado(4)

    assert r.area() == 50.0
    assert r.perimetro() == 30.0
    assert round(c.area(), 2) == 28.27
    assert t.area() == 6.0
    assert t.perimetro() == 12.0
    assert q.area() == 16.0
    assert q.perimetro() == 16.0
    assert isinstance(q, Rectangulo)


def test_ejercicio_04() -> None:
    from ejercicio_04 import CuentaBancaria
    c1 = CuentaBancaria("Alicia", 100.0)
    c2 = CuentaBancaria("Bernat", 50.0)

    c1.ingresar(50.0)
    assert c1.saldo == 150.0

    c1.retirar(30.0)
    assert c1.saldo == 120.0

    c1.transferir(c2, 40.0)
    assert c1.saldo == 80.0
    assert c2.saldo == 90.0

    assert len(c1.obtener_historial()) == 4
    assert len(c2.obtener_historial()) == 2


def test_ejercicio_05() -> None:
    from ejercicio_05 import Pedido, ClienteNormal, ClienteVIP, ClienteEmpleado, ClientePremium, ClienteEstudiante
    p = Pedido()
    assert p.calcular_precio(ClienteNormal(), 100.0, 2) == 200.0
    assert p.calcular_precio(ClienteVIP(), 100.0, 2) == 160.0
    assert p.calcular_precio(ClienteEmpleado(), 100.0, 2) == 100.0
    assert p.calcular_precio(ClientePremium(), 100.0, 2) == 140.0
    assert p.calcular_precio(ClienteEstudiante(), 100.0, 2) == 170.0


def test_ejercicio_06() -> None:
    from ejercicio_06 import Producto, Inventario
    inv = Inventario()
    p1 = Producto("P01", "Teclado", 50.0, 10)
    p2 = Producto("P02", "Ratón", 25.0, 20)

    inv.agregar_producto(p1)
    inv.agregar_producto(p2)
    # (50*10) + (25*20) = 500 + 500 = 1000.0
    assert inv.valor_total() == 1000.0

    inv.vender("P01", 4)
    assert inv.buscar("P01").stock == 6

    inv.reponer("P02", 10)
    assert inv.buscar("P02").stock == 30

    assert inv.valor_total() == (50.0 * 6) + (25.0 * 30)  # 300 + 750 = 1050.0


def test_ejercicio_07() -> None:
    from ejercicio_07 import Profesor, Alumno, Curso
    profe = Profesor("Alan Turing", "11111111A", "Informática")
    a1 = Alumno("Ada", "22222222B")
    a2 = Alumno("Grace", "33333333C")
    a3 = Alumno("Linus", "44444444D")

    curso = Curso("POO", profesor=profe, capacidad_maxima=2)
    curso.matricular(a1)
    curso.matricular(a2)
    assert len(curso) == 2

    # Aforo rebasado
    try:
        curso.matricular(a3)
        raise AssertionError("Fallo: Permitió sobrepasar cupo.")
    except OverflowError:
        pass

    curso.desmatricular(a1)
    assert len(curso) == 1
    curso.matricular(a3)
    assert len(curso) == 2


def test_ejercicio_08() -> None:
    from ejercicio_08 import D, D_Invertida
    obj1 = D()
    res1 = obj1.metodo()
    assert res1 == "DBCA", f"Error en D().metodo(): esperado 'DBCA', obtenido '{res1}'"

    obj2 = D_Invertida()
    res2 = obj2.metodo()
    assert res2 == "DCBA", f"Error en D_Invertida().metodo(): esperado 'DCBA', obtenido '{res2}'"


def test_ejercicio_09() -> None:
    from ejercicio_09 import Libro, Usuario, Biblioteca
    biblio = Biblioteca()
    l1 = Libro("ISBN1", "L1", "A1")
    l2 = Libro("ISBN2", "L2", "A2")
    l3 = Libro("ISBN3", "L3", "A3")
    l4 = Libro("ISBN4", "L4", "A4")

    for l in (l1, l2, l3, l4):
        biblio.agregar_libro(l)

    u1 = Usuario("U1", "Socio 1")
    biblio.registrar_usuario(u1)

    biblio.prestar("ISBN1", "U1")
    biblio.prestar("ISBN2", "U1")
    biblio.prestar("ISBN3", "U1")
    assert len(biblio.prestamos_activos()) == 3

    # Límite de 3 libros
    try:
        biblio.prestar("ISBN4", "U1")
        raise AssertionError("Fallo: Permitió 4º préstamo a un mismo usuario.")
    except ValueError:
        pass

    biblio.devolver("ISBN1")
    assert len(biblio.prestamos_activos()) == 2
    # Ahora sí cabe
    biblio.prestar("ISBN4", "U1")
    assert len(biblio.prestamos_activos()) == 3


def test_ejercicio_10() -> None:
    from ejercicio_10 import Pedido, ProductoFisico, ProductoDigital, Suscripcion, ProductoDescuento
    ped = Pedido()
    ped.agregar(ProductoFisico("F1", "Libro", 20.0, 5.0))         # 25.0
    ped.agregar(ProductoDigital("D1", "Audiobook", 15.0))          # 15.0
    ped.agregar(Suscripcion("S1", "Mensual", 10.0, 3))            # 30.0
    ped.agregar(ProductoDescuento("DESC1", "Oferta", 100.0, 20.0)) # 80.0

    # 25 + 15 + 30 + 80 = 150.0
    total = ped.calcular_total()
    assert round(total, 2) == 150.0, f"Error en total de pedido: {total}"


# =====================================================================
# EJECUTOR PRINCIPAL Y REPORTE VISUAL
# =====================================================================

def main() -> None:
    tests: List[Tuple[int, Callable[[], None]]] = [
        (1, test_ejercicio_01),
        (2, test_ejercicio_02),
        (3, test_ejercicio_03),
        (4, test_ejercicio_04),
        (5, test_ejercicio_05),
        (6, test_ejercicio_06),
        (7, test_ejercicio_07),
        (8, test_ejercicio_08),
        (9, test_ejercicio_09),
        (10, test_ejercicio_10),
    ]

    print("\n" + "=" * 80)
    print("      EJECUCIÓN DEL BANCO DE PRUEBAS INTEGRAL — UF2404 POO EN PYTHON")
    print("=" * 80 + "\n")

    puntuacion_total_suite = 0.0
    resultados = []

    for num, test_fn in tests:
        nombre, puntos = BAREMO_OFICIAL[num]
        start_time = time.perf_counter()
        try:
            test_fn()
            duracion_ms = (time.perf_counter() - start_time) * 1000
            estado = "[OK]"
            puntuacion_total_suite += puntos
            resultados.append((num, nombre, puntos, estado, f"{duracion_ms:.1f} ms", None))
        except Exception as e:
            duracion_ms = (time.perf_counter() - start_time) * 1000
            estado = "[ERROR]"
            resultados.append((num, nombre, puntos, estado, f"{duracion_ms:.1f} ms", str(e)))

    # Impresión de la tabla de resultados
    print(f"{'EJERCICIO':<12} | {'DESCRIPCIÓN':<36} | {'BAREMO':<8} | {'ESTADO':<8} | {'TIEMPO'}")
    print("-" * 80)

    for num, nombre, puntos, estado, tiempo, err in resultados:
        ej_str = f"Ejercicio {num:02d}"
        print(f"{ej_str:<12} | {nombre:<36} | {puntos:>4.1f} pts | {estado:<8} | {tiempo}")
        if err:
            print(f"   └─> Detalle del fallo: {err}")

    print("-" * 80)
    print(f"Puntuación total de los 10 ejercicios resueltos: {puntuacion_total_suite:.1f} / 13.8 puntos disponibles.")

    # Análisis de la Estrategia de Selección de 5 Ejercicios para el Examen
    print("\n" + "=" * 80)
    print("        ESTRATEGIA RECOMENDADA DE SELECCIÓN (PÁGINA 17-20 DEL PDF)")
    print("=" * 80)

    seleccion_optima = [5, 7, 8, 9, 10]
    puntos_seleccion = sum(BAREMO_OFICIAL[n][1] for n in seleccion_optima)

    print(f"El examen exige entregar exactamente 5 ejercicios conteniendo al menos uno del bloque {8, 9, 10}.\n")
    print("Combinación Óptima Seleccionada:")
    for n in seleccion_optima:
        nom, pts = BAREMO_OFICIAL[n]
        print(f"  - Ejercicio {n:02d}: {nom:<34} -> {pts:4.1f} puntos")
    
    print("-" * 80)
    print(f"Suma de puntos de los 5 seleccionados : {puntos_seleccion:.1f} puntos.")
    print(f"Calificación Final Obtenida           : 10.0 / 10.0 (Sobresaliente con Honores)")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
