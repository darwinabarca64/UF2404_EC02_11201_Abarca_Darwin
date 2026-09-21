"""
Ejercicio 9: Sistema de préstamos (Sistema de préstec).
Módulo: MF0227_3 - Programación orientada a objetos (UF2404).

Este módulo implementa el ecosistema de biblioteca mediante:
1. Entidades `Libro` y `Usuario` con identificadores únicos (ISBN, id_usuario).
2. Clase de asociación `Prestamo` que almacena referencias directas a objetos.
3. Clase orquestadora `Biblioteca` con control de invariantes:
   - Máximo 3 préstamos activos simultáneos por usuario.
   - Disponibilidad física de libros (sin dobles préstamos).
   - Finalización consistente de préstamos en devoluciones.
   - Consulta inmutable de préstamos activos.
"""

from __future__ import annotations
import datetime
from typing import Dict, List, Optional, Tuple


def _validar_cadena_no_vacia(valor: str, nombre_campo: str) -> str:
    """Valida que una cadena no sea nula ni esté compuesta exclusivamente de espacios."""
    if not isinstance(valor, str):
        raise TypeError(f"El campo '{nombre_campo}' debe ser una cadena (str), recibido: {type(valor).__name__}")
    limpio = valor.strip()
    if not limpio:
        raise ValueError(f"El campo '{nombre_campo}' no puede estar vacío.")
    return limpio


class Libro:
    """Representa un libro del catálogo bibliográfico.

    Attributes:
        isbn (str): Código identificador unívoco internacional del libro.
        titulo (str): Título de la obra.
        autor (str): Autor o autores de la publicación.
        disponible (bool): Estado de disponibilidad para préstamo.
    """

    def __init__(self, isbn: str, titulo: str, autor: str) -> None:
        self._isbn: str = _validar_cadena_no_vacia(isbn, "isbn")
        self._titulo: str = _validar_cadena_no_vacia(titulo, "titulo")
        self._autor: str = _validar_cadena_no_vacia(autor, "autor")
        self._disponible: bool = True

    @property
    def isbn(self) -> str:
        """ISBN del libro."""
        return self._isbn

    @property
    def titulo(self) -> str:
        """Título de la obra."""
        return self._titulo

    # Alias en catalán
    titol = titulo

    @property
    def autor(self) -> str:
        """Autor del libro."""
        return self._autor

    @property
    def disponible(self) -> bool:
        """Indica si el libro se encuentra disponible para préstamo."""
        return self._disponible

    def marcar_prestado(self) -> None:
        """Cambia el estado del libro a no disponible."""
        if not self._disponible:
            raise ValueError(f"El libro '{self._titulo}' (ISBN: {self._isbn}) ya está prestado.")
        self._disponible = False

    def marcar_devuelto(self) -> None:
        """Cambia el estado del libro a disponible."""
        if self._disponible:
            raise ValueError(f"El libro '{self._titulo}' (ISBN: {self._isbn}) ya se encuentra disponible en biblioteca.")
        self._disponible = True

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Libro):
            return False
        return self._isbn == other._isbn

    def __hash__(self) -> int:
        return hash(self._isbn)

    def __str__(self) -> str:
        estado = "Disponible" if self._disponible else "Prestado"
        return f"Libro[{self._isbn}] '{self._titulo}' por {self._autor} ({estado})"

    def __repr__(self) -> str:
        return f"Libro(isbn={self._isbn!r}, titulo={self._titulo!r}, disponible={self._disponible})"


class Usuario:
    """Representa a un socio o usuario registrado en la biblioteca.

    Attributes:
        id_usuario (str): Identificador unívoco del socio.
        nombre (str): Nombre completo del usuario.
    """

    MAX_PRESTAMOS: int = 3

    def __init__(self, id_usuario: str, nombre: str) -> None:
        self._id_usuario: str = _validar_cadena_no_vacia(id_usuario, "id_usuario")
        self._nombre: str = _validar_cadena_no_vacia(nombre, "nombre")
        # Referencias a los préstamos activos del usuario
        self._prestamos_activos: list[Prestamo] = []

    @property
    def id_usuario(self) -> str:
        """Identificador de usuario."""
        return self._id_usuario

    @property
    def nombre(self) -> str:
        """Nombre del usuario."""
        return self._nombre

    # Alias en catalán
    nom = nombre

    @property
    def prestamos_activos(self) -> Tuple[Prestamo, ...]:
        """Tupla inmutable con los préstamos vigentes del usuario."""
        return tuple(self._prestamos_activos)

    def puede_tomar_prestado(self) -> bool:
        """Comprueba si el usuario no ha alcanzado el límite máximo de préstamos activos (3)."""
        return len(self._prestamos_activos) < self.MAX_PRESTAMOS

    def registrar_prestamo(self, prestamo: Prestamo) -> None:
        """Vincula un nuevo préstamo activo al usuario."""
        if not self.puede_tomar_prestado():
            raise ValueError(
                f"El usuario '{self._nombre}' (ID: {self._id_usuario}) ya tiene el número máximo "
                f"de libros permitido ({self.MAX_PRESTAMOS} libros simultáneos)."
            )
        self._prestamos_activos.append(prestamo)

    def liberar_prestamo(self, prestamo: Prestamo) -> None:
        """Desvincula un préstamo tras su devolución."""
        if prestamo in self._prestamos_activos:
            self._prestamos_activos.remove(prestamo)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Usuario):
            return False
        return self._id_usuario == other._id_usuario

    def __hash__(self) -> int:
        return hash(self._id_usuario)

    def __str__(self) -> str:
        return f"Usuario[{self._id_usuario}] '{self._nombre}' ({len(self._prestamos_activos)}/{self.MAX_PRESTAMOS} préstamos activos)"

    def __repr__(self) -> str:
        return f"Usuario(id_usuario={self._id_usuario!r}, nombre={self._nombre!r})"


class Prestamo:
    """Clase de asociación que vincula un objeto Libro con un objeto Usuario.

    Cumple la restricción formal del examen de almacenar referencias a objetos
    reales en lugar de simples cadenas o claves primitivas.
    """

    def __init__(self, libro: Libro, usuario: Usuario) -> None:
        if not isinstance(libro, Libro):
            raise TypeError(f"El parámetro 'libro' debe ser instancia de Libro, recibido: {type(libro).__name__}")
        if not isinstance(usuario, Usuario):
            raise TypeError(f"El parámetro 'usuario' debe ser instancia de Usuario, recibido: {type(usuario).__name__}")

        self._libro: Libro = libro
        self._usuario: Usuario = usuario
        self._activo: bool = True
        self._fecha_inicio: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def libro(self) -> Libro:
        """Objeto Libro asociado al préstamo."""
        return self._libro

    # Alias en catalán
    llibre = libro

    @property
    def usuario(self) -> Usuario:
        """Objeto Usuario asociado al préstamo."""
        return self._usuario

    # Alias en catalán
    usuari = usuario

    @property
    def activo(self) -> bool:
        """Indica si el préstamo sigue vigente."""
        return self._activo

    @property
    def fecha_inicio(self) -> str:
        """Fecha y hora de formalización del préstamo."""
        return self._fecha_inicio

    def finalizar(self) -> None:
        """Finaliza el préstamo y devuelve el libro a estado disponible."""
        if not self._activo:
            raise ValueError(f"Este préstamo para el libro '{self._libro.titulo}' ya estaba finalizado.")
        self._activo = False
        self._libro.marcar_devuelto()

    def __str__(self) -> str:
        estado = "ACTIVO" if self._activo else "FINALIZADO"
        return f"Préstamo [{estado}] - '{self._libro.titulo}' prestado a {self._usuario.nombre} ({self._fecha_inicio})"

    def __repr__(self) -> str:
        return f"Prestamo(libro={self._libro.isbn!r}, usuario={self._usuario.id_usuario!r}, activo={self._activo})"


class Biblioteca:
    """Gestiona el catálogo de libros, el censo de socios y el registro de préstamos."""

    def __init__(self) -> None:
        self._libros: Dict[str, Libro] = {}
        self._usuarios: Dict[str, Usuario] = {}
        self._prestamos: List[Prestamo] = []

    def agregar_libro(self, libro: Libro) -> None:
        """Registra un nuevo libro en el catálogo asegurando que el ISBN sea único.

        Args:
            libro: Instancia de Libro a registrar.

        Raises:
            TypeError: Si no es instancia de Libro.
            ValueError: Si el ISBN ya existe en la biblioteca.
        """
        if not isinstance(libro, Libro):
            raise TypeError(f"Solo pueden agregarse objetos Libro, recibido: {type(libro).__name__}")
        if libro.isbn in self._libros:
            raise ValueError(f"Ya existe un libro registrado con el ISBN '{libro.isbn}'.")
        self._libros[libro.isbn] = libro

    # Alias en catalán
    afegir_llibre = agregar_libro

    def registrar_usuario(self, usuario: Usuario) -> None:
        """Registra un nuevo usuario asegurando que su ID sea único.

        Args:
            usuario: Instancia de Usuario a registrar.

        Raises:
            TypeError: Si no es instancia de Usuario.
            ValueError: Si el id_usuario ya existe.
        """
        if not isinstance(usuario, Usuario):
            raise TypeError(f"Solo pueden registrarse objetos Usuario, recibido: {type(usuario).__name__}")
        if usuario.id_usuario in self._usuarios:
            raise ValueError(f"Ya existe un usuario registrado con el ID '{usuario.id_usuario}'.")
        self._usuarios[usuario.id_usuario] = usuario

    # Alias en catalán
    registrar_usuari = registrar_usuario

    def prestar(self, isbn: str, id_usuario: str) -> Prestamo:
        """Formaliza el préstamo de un libro a un usuario si se cumplen todas las condiciones.

        Args:
            isbn: ISBN del libro a prestar.
            id_usuario: ID del usuario solicitante.

        Returns:
            Prestamo: Instancia del objeto Prestamo generado.

        Raises:
            ValueError: Si el libro o usuario no existen, el libro no está disponible o el usuario tiene 3 libros.
        """
        isbn_limpio = _validar_cadena_no_vacia(isbn, "isbn")
        id_limpio = _validar_cadena_no_vacia(id_usuario, "id_usuario")

        if isbn_limpio not in self._libros:
            raise ValueError(f"No existe ningún libro con el ISBN '{isbn_limpio}' en la biblioteca.")

        if id_limpio not in self._usuarios:
            raise ValueError(f"No existe ningún usuario registrado con el ID '{id_limpio}'.")

        libro = self._libros[isbn_limpio]
        usuario = self._usuarios[id_limpio]

        # Regla 1: No se puede prestar un libro que ya está prestado
        if not libro.disponible:
            raise ValueError(f"El libro '{libro.titulo}' (ISBN: {libro.isbn}) ya está prestado y no se encuentra disponible.")

        # Regla 2: Cada usuario puede tener como máximo 3 libros simultáneamente
        if not usuario.puede_tomar_prestado():
            raise ValueError(
                f"Límite alcanzado: El usuario '{usuario.nombre}' ya tiene 3 libros prestados simultáneamente."
            )

        # Creación y vinculación bidireccional del objeto Préstamo
        prestamo = Prestamo(libro=libro, usuario=usuario)
        libro.marcar_prestado()
        usuario.registrar_prestamo(prestamo)
        self._prestamos.append(prestamo)

        return prestamo

    def devolver(self, isbn: str) -> None:
        """Devuelve un libro prestado y finaliza el préstamo correspondiente.

        Args:
            isbn: ISBN del libro a retornar.

        Raises:
            ValueError: Si el libro no existe o no tiene ningún préstamo activo.
        """
        isbn_limpio = _validar_cadena_no_vacia(isbn, "isbn")
        if isbn_limpio not in self._libros:
            raise ValueError(f"No existe ningún libro con el ISBN '{isbn_limpio}'.")

        # Buscar el préstamo activo correspondiente a este libro
        prestamo_activo: Optional[Prestamo] = None
        for p in self._prestamos:
            if p.activo and p.libro.isbn == isbn_limpio:
                prestamo_activo = p
                break

        if prestamo_activo is None:
            raise ValueError(f"No existe ningún préstamo activo para el libro con ISBN '{isbn_limpio}'.")

        # Finalizar el préstamo y liberar del usuario
        prestamo_activo.finalizar()
        prestamo_activo.usuario.liberar_prestamo(prestamo_activo)

    # Alias en catalán
    retornar = devolver

    def prestamos_activos(self) -> Tuple[Prestamo, ...]:
        """Devuelve una tupla inmutable con todos los préstamos que continúan vigentes."""
        return tuple(p for p in self._prestamos if p.activo)

    # Alias en catalán
    prestecs_actius = prestamos_activos

    def __str__(self) -> str:
        activos = len(self.prestamos_activos())
        return f"Biblioteca({len(self._libros)} libros, {len(self._usuarios)} usuarios, {activos} préstamos activos)"


# Alias en catalán según PDF
Llibre = Libro
Usuari = Usuario
Prestec = Prestamo


if __name__ == "__main__":
    print("=" * 70)
    print("DEMOSTRACIÓN COMPLETA - EJERCICIO 9: SISTEMA DE PRÉSTAMOS")
    print("=" * 70)

    biblio = Biblioteca()

    # 1. Registro de Libros y Usuarios
    l1 = Libro("978-01", "Clean Code", "Robert C. Martin")
    l2 = Libro("978-02", "Design Patterns", "Gang of Four")
    l3 = Libro("978-03", "Fluent Python", "Luciano Ramalho")
    l4 = Libro("978-04", "The Pragmatic Programmer", "Hunt & Thomas")

    biblio.agregar_libro(l1)
    biblio.agregar_libro(l2)
    biblio.agregar_libro(l3)
    biblio.agregar_libro(l4)

    u1 = Usuario("U001", "Helena Rius")
    u2 = Usuario("U002", "Pau Domenech")

    biblio.registrar_usuario(u1)
    biblio.registrar_usuario(u2)

    print(f"Estado inicial: {biblio}")
    assert len(biblio.prestamos_activos()) == 0

    # 2. Préstamos exitosos (Helena pide 3 libros)
    print("\n--- Préstamos para Helena (U001) ---")
    p1 = biblio.prestar("978-01", "U001")
    p2 = biblio.prestar("978-02", "U001")
    p3 = biblio.prestar("978-03", "U001")

    print(f"Préstamo 1: {p1}")
    print(f"Préstamo 2: {p2}")
    print(f"Préstamo 3: {p3}")
    print(f"Préstamos activos totales en biblioteca: {len(biblio.prestamos_activos())}")
    assert len(biblio.prestamos_activos()) == 3
    assert not l1.disponible
    assert not l2.disponible
    assert not l3.disponible
    print("[OK] Préstamos exitosos registrados.")

    # 3. Caso límite: Intento de 4º préstamo por el mismo usuario (Límite = 3)
    print("\n--- Intento de superar el cupo de 3 libros ---")
    try:
        biblio.prestar("978-04", "U001")
        raise AssertionError("Fallo: Debería haber impedido prestar un 4º libro a Helena.")
    except ValueError as e:
        print(f"[OK] Capturado límite máximo de usuario correctamente: {e}")

    # 4. Caso límite: Intento de prestar un libro ya prestado a otro usuario
    print("\n--- Intento de prestar un libro no disponible ---")
    try:
        biblio.prestar("978-01", "U002")  # Pau intenta pedir Clean Code
        raise AssertionError("Fallo: Debería haber impedido prestar un libro no disponible.")
    except ValueError as e:
        print(f"[OK] Capturado libro no disponible correctamente: {e}")

    # 5. Devolución de un libro y liberación de cupo
    print("\n--- Devolución de 'Clean Code' por parte de Helena ---")
    biblio.devolver("978-01")
    assert l1.disponible is True
    assert p1.activo is False
    assert len(biblio.prestamos_activos()) == 2
    print(f"Libro 978-01 devuelto. Disponibilidad: {l1.disponible}. Préstamos activos en biblioteca: {len(biblio.prestamos_activos())}")

    # Ahora Pau sí puede pedir Clean Code
    print("\n--- Pau solicita el libro recién devuelto ---")
    p4 = biblio.prestar("978-01", "U002")
    assert p4.activo is True
    assert not l1.disponible
    print(f"Préstamo para Pau generado: {p4}")
    print("[OK] Devolución y re-préstamo validados.")

    # 6. Intento de devolver un libro que no está prestado
    print("\n--- Intento de devolver libro no prestado ---")
    try:
        biblio.devolver("978-04")  # The Pragmatic Programmer nunca se prestó
        raise AssertionError("Fallo: Debería fallar al devolver un libro no prestado.")
    except ValueError as e:
        print(f"[OK] Capturada devolución errónea correctamente: {e}")

    # 7. Verificación del requerimiento: Prestamo almacena Objetos reales
    print("\n--- Verificación de referencias a Objetos en Prestamo ---")
    prestamo_muestra = biblio.prestamos_activos()[0]
    print(f"Tipo de prestamo.libro: {type(prestamo_muestra.libro).__name__} -> '{prestamo_muestra.libro.titulo}'")
    print(f"Tipo de prestamo.usuario: {type(prestamo_muestra.usuario).__name__} -> '{prestamo_muestra.usuario.nombre}'")
    assert isinstance(prestamo_muestra.libro, Libro)
    assert isinstance(prestamo_muestra.usuario, Usuario)
    print("[OK] Confirmado: Prestamo almacena instancias de objeto, cumpliendo el requisito estricto.")

    print("\nTodas las pruebas del Ejercicio 9 concluyeron con éxito.")
