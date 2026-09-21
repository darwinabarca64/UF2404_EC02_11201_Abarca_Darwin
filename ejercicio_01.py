"""
Ejercicio 1: Reparar un diseño defectuoso.
Módulo: MF0227_3 - Programación orientada a objetos (UF2404).

Este módulo define la clase `Usuario`, solucionando los errores de diseño y ejecución
del código original:
1. Argumento mutable por defecto (`cursos=[]` -> `cursos=None` con copia defensiva).
2. Ámbito incorrecto en variable de clase (`total += 1` -> `Usuario.total += 1`).
3. Falta de referencia de instancia en método (`cursos.append` -> `self.cursos.append`).
4. Validación robusta de tipos y cadenas no vacías para evitar estados inconsistentes.
"""

from __future__ import annotations
from typing import Optional


class Usuario:
    """Representa a un usuario y el conjunto de cursos en los que está matriculado.

    Attributes:
        total (int): Contador a nivel de clase que registra el número total de
                     instancias creadas.
        nombre (str): Nombre del usuario (no vacío).
        cursos (list[str]): Lista independiente de nombres de cursos matriculados.
    """

    total: int = 0

    def __init__(self, nombre: str, cursos: Optional[list[str]] = None) -> None:
        """Inicializa una nueva instancia de Usuario.

        Args:
            nombre: Nombre identificativo del usuario (debe ser una cadena no vacía).
            cursos: Lista inicial opcional de cursos. Si no se indica, se inicializa
                    con una lista vacía e independiente. Se realiza copia defensiva.

        Raises:
            TypeError: Si los tipos de los argumentos no son válidos.
            ValueError: Si el nombre está vacío o contiene solo espacios en blanco.
        """
        # Validación defensiva de 'nombre'
        if not isinstance(nombre, str):
            raise TypeError(f"El nombre debe ser una cadena de texto (str), recibido: {type(nombre).__name__}")
        
        nombre_limpio = nombre.strip()
        if not nombre_limpio:
            raise ValueError("El nombre no puede estar vacío ni contener únicamente espacios en blanco.")

        self.nombre: str = nombre_limpio

        # Solución al argumento mutable por defecto y copia defensiva
        if cursos is None:
            self.cursos: list[str] = []
        else:
            if not isinstance(cursos, list):
                raise TypeError(f"El parámetro 'cursos' debe ser una lista (list), recibido: {type(cursos).__name__}")
            
            # Validamos que cada elemento de la lista sea una cadena válida y hacemos copia
            self.cursos = []
            for item in cursos:
                if not isinstance(item, str) or not item.strip():
                    raise ValueError(f"Todos los cursos deben ser cadenas no vacías. Valor inválido: {item!r}")
                self.cursos.append(item.strip())

        # Incremento correcto de la variable de clase (ámbito de clase)
        Usuario.total += 1

    def agregar_curso(self, curso: str) -> None:
        """Añade un nuevo curso a la lista de cursos del usuario.

        Args:
            curso: Nombre del curso a matricular (cadena no vacía).

        Raises:
            TypeError: Si 'curso' no es de tipo str.
            ValueError: Si 'curso' está vacío o formado únicamente por espacios.
        """
        if not isinstance(curso, str):
            raise TypeError(f"El curso debe ser una cadena de texto (str), recibido: {type(curso).__name__}")
        
        curso_limpio = curso.strip()
        if not curso_limpio:
            raise ValueError("El nombre del curso no puede estar vacío ni contener solo espacios.")

        # Modificación explícita sobre el atributo de instancia
        self.cursos.append(curso_limpio)

    def __str__(self) -> str:
        """Representación legible del usuario."""
        return f"Usuario(nombre='{self.nombre}', cursos={self.cursos})"

    def __repr__(self) -> str:
        """Representación técnica del objeto."""
        return f"Usuario(nombre={self.nombre!r}, cursos={self.cursos!r})"


if __name__ == "__main__":
    print("=" * 60)
    print("EJECUCIÓN DEL CASO DE PRUEBA OFICIAL (ENUNCIADO)")
    print("=" * 60)

    # Creación de instancias con el valor por defecto de cursos
    u1 = Usuario("Ana")
    u2 = Usuario("Marc")

    # Modificación solo en u1
    u1.agregar_curso("Python")

    # Verificación de listas independientes
    print(f"u1.cursos -> {u1.cursos}")  # Esperado: ['Python']
    print(f"u2.cursos -> {u2.cursos}")  # Esperado: []
    print(f"Usuario.total -> {Usuario.total}")  # Esperado: 2

    # Aserciones de verificación automatizada
    assert u1.cursos == ["Python"], "Error: u1 debería tener ['Python']"
    assert u2.cursos == [], "Error: u2 debería tener una lista vacía e independiente"
    assert u1.cursos is not u2.cursos, "Error: Las listas u1 y u2 no deben compartir la misma referencia de memoria"
    assert Usuario.total == 2, "Error: Usuario.total debe ser 2"

    print("\n" + "=" * 60)
    print("PRUEBAS DE ROBUSTEZ Y COPIA DEFENSIVA ADICIONALES")
    print("=" * 60)

    # Demostración de copia defensiva con lista externa
    cursos_externos = ["Bases de Datos", "Docker"]
    u3 = Usuario("Clara", cursos_externos)
    cursos_externos.append("Ciberseguridad")  # Modificamos la lista externa

    print(f"u3.cursos: {u3.cursos}")
    print(f"cursos_externos: {cursos_externos}")
    assert "Ciberseguridad" not in u3.cursos, "Error: La lista interna fue modificada por cambio externo"
    print("[OK] Copia defensiva validada con exito.")

    # Total actualizado
    print(f"Nuevo total de usuarios: {Usuario.total}")
    assert Usuario.total == 3, "Error: Usuario.total debe ser 3"

    print("\nTodas las pruebas y aserciones pasaron satisfactoriamente.")
