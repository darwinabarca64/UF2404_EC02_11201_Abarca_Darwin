"""
Ejercicio 7: Clases que deben funcionar juntas (Classes que han de funcionar juntes).
Módulo: MF0227_3 - Programación orientada a objetos (UF2404).

Este módulo implementa el ecosistema académico compuesto por:
1. Clase base `Persona`.
2. Subclases especializadas `Alumno` y `Profesor` mediante Herencia ("es-un").
3. Clase contenedora `Curso` mediante Composición y Agregación ("tiene-un").
4. Control de tipo estricto, prevención de duplicados y respeto de capacidad máxima.
5. Formateo legible de ficha de curso mediante `__str__`.
"""

from __future__ import annotations
from typing import Tuple, Optional


def _validar_texto_no_vacio(texto: str, nombre_campo: str) -> str:
    """Valida que una cadena de texto sea válida y no esté vacía."""
    if not isinstance(texto, str):
        raise TypeError(f"El campo '{nombre_campo}' debe ser de tipo str, recibido: {type(texto).__name__}")
    limpio = texto.strip()
    if not limpio:
        raise ValueError(f"El campo '{nombre_campo}' no puede estar vacío.")
    return limpio


class Persona:
    """Clase base que modela a una persona con identidad civil."""

    def __init__(self, nombre: str, dni: str) -> None:
        self._nombre: str = _validar_texto_no_vacio(nombre, "nombre")
        self._dni: str = _validar_texto_no_vacio(dni, "dni")

    @property
    def nombre(self) -> str:
        """Nombre de la persona."""
        return self._nombre

    @property
    def dni(self) -> str:
        """Documento Nacional de Identidad de la persona."""
        return self._dni

    def __eq__(self, other: object) -> bool:
        """Dos personas son iguales si tienen el mismo DNI."""
        if not isinstance(other, Persona):
            return False
        return self._dni.upper() == other._dni.upper()

    def __hash__(self) -> int:
        return hash(self._dni.upper())

    def __str__(self) -> str:
        return f"{self._nombre} (DNI: {self._dni})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(nombre={self._nombre!r}, dni={self._dni!r})"


class Alumno(Persona):
    """Representa a un estudiante que puede matricularse en cursos académicos."""

    def __init__(self, nombre: str, dni: str, expediente: str = "") -> None:
        super().__init__(nombre, dni)
        # Si no se especifica expediente, se genera automáticamente a partir del DNI
        self._expediente: str = expediente.strip() if expediente else f"EXP-{self.dni}"

    @property
    def expediente(self) -> str:
        """Número de expediente académico del alumno."""
        return self._expediente

    def __str__(self) -> str:
        return f"Alumno: {self._nombre} [Exp: {self._expediente}, DNI: {self._dni}]"


class Profesor(Persona):
    """Representa a un docente cualificado para impartir cursos."""

    def __init__(self, nombre: str, dni: str, especialidad: str = "Informática") -> None:
        super().__init__(nombre, dni)
        self._especialidad: str = _validar_texto_no_vacio(especialidad, "especialidad")

    @property
    def especialidad(self) -> str:
        """Área o departamento de especialización del docente."""
        return self._especialidad

    def __str__(self) -> str:
        return f"Profesor: {self._nombre} [Especialidad: {self._especialidad}, DNI: {self._dni}]"


# Alias en catalán
Alumne = Alumno
Professor = Profesor


class Curso:
    """Modela una acción formativa con un profesor titular y un cupo limitado de alumnos."""

    def __init__(self, nombre: str, profesor: Profesor, capacidad_maxima: int) -> None:
        self._nombre: str = _validar_texto_no_vacio(nombre, "nombre")

        if not isinstance(profesor, Profesor):
            raise TypeError(f"El profesor asignado debe ser una instancia de Profesor, recibido: {type(profesor).__name__}")
        self._profesor: Profesor = profesor

        if isinstance(capacidad_maxima, bool) or not isinstance(capacidad_maxima, int):
            raise TypeError(f"La capacidad máxima debe ser un entero (int), recibido: {type(capacidad_maxima).__name__}")
        if capacidad_maxima <= 0:
            raise ValueError(f"La capacidad máxima debe ser estrictamente positiva (> 0), recibido: {capacidad_maxima}")
        self._capacidad_maxima: int = capacidad_maxima

        self._alumnos: list[Alumno] = []

    @property
    def nombre(self) -> str:
        """Nombre o título del curso."""
        return self._nombre

    @property
    def profesor(self) -> Profesor:
        """Profesor titular del curso."""
        return self._profesor

    @property
    def capacidad_maxima(self) -> int:
        """Capacidad máxima de plazas del curso."""
        return self._capacidad_maxima

    @property
    def alumnos(self) -> Tuple[Alumno, ...]:
        """Tupla inmutable con los alumnos matriculados en el curso."""
        return tuple(self._alumnos)

    def matricular(self, alumno: Alumno) -> None:
        """Matricula a un alumno en el curso cumpliendo todas las invariantes de dominio.

        Args:
            alumno: Objeto de tipo Alumno a matricular.

        Raises:
            TypeError: Si el objeto recibido no es una instancia de Alumno.
            ValueError: Si el alumno ya está matriculado en este curso.
            OverflowError: Si el curso ha alcanzado su capacidad máxima de plazas.
        """
        if not isinstance(alumno, Alumno):
            raise TypeError(f"Únicamente pueden matricularse objetos Alumno, recibido: {type(alumno).__name__}")

        if alumno in self._alumnos:
            raise ValueError(f"El alumno '{alumno.nombre}' (DNI: {alumno.dni}) ya está matriculado en el curso.")

        if len(self._alumnos) >= self._capacidad_maxima:
            raise OverflowError(
                f"No se puede matricular a '{alumno.nombre}': Capacidad máxima alcanzada "
                f"({self._capacidad_maxima}/{self._capacidad_maxima} plazas ocupadas)."
            )

        self._alumnos.append(alumno)

    def desmatricular(self, alumno: Alumno) -> None:
        """Da de baja a un alumno previamente matriculado en el curso.

        Args:
            alumno: Objeto de tipo Alumno a desmatricular.

        Raises:
            TypeError: Si el objeto recibido no es una instancia de Alumno.
            ValueError: Si el alumno no se encuentra matriculado en el curso.
        """
        if not isinstance(alumno, Alumno):
            raise TypeError(f"El objeto a desmatricular debe ser Alumno, recibido: {type(alumno).__name__}")

        if alumno not in self._alumnos:
            raise ValueError(f"No se puede desmatricular: '{alumno.nombre}' no figura matriculado en este curso.")

        self._alumnos.remove(alumno)

    def cambiar_profesor(self, nuevo_profesor: Profesor) -> None:
        """Asigna un nuevo profesor titular al curso.

        Args:
            nuevo_profesor: Instancia de Profesor.

        Raises:
            TypeError: Si nuevo_profesor no es una instancia de Profesor.
        """
        if not isinstance(nuevo_profesor, Profesor):
            raise TypeError(f"Solamente un objeto Profesor puede impartir el curso, recibido: {type(nuevo_profesor).__name__}")
        self._profesor = nuevo_profesor

    # Alias en catalán
    canviar_professor = cambiar_profesor

    def __len__(self) -> int:
        """Retorna el número de alumnos inscritos actualmente."""
        return len(self._alumnos)

    def __str__(self) -> str:
        """Genera una ficha descriptiva detallada y legible del curso."""
        lineas = [
            f"==================================================",
            f"FICHA DEL CURSO: {self._nombre}",
            f"==================================================",
            f"Profesor Titular : {self._profesor.nombre} ({self._profesor.especialidad})",
            f"Ocupación Plazas : {len(self)} / {self._capacidad_maxima} alumnos",
            f"--------------------------------------------------",
            f"Alumnos Matriculados:"
        ]
        if not self._alumnos:
            lineas.append("  (No hay alumnos matriculados actualmente)")
        else:
            for idx, alu in enumerate(self._alumnos, start=1):
                lineas.append(f"  {idx}. {alu.nombre:<20} | Exp: {alu.expediente:<12} | DNI: {alu.dni}")
        lineas.append("==================================================")
        return "\n".join(lineas)

    def __repr__(self) -> str:
        return f"Curso(nombre={self._nombre!r}, profesor={self._profesor.nombre!r}, matriculados={len(self)}/{self._capacidad_maxima})"


# Alias en catalán según PDF
Curs = Curso


if __name__ == "__main__":
    print("=" * 65)
    print("DEMOSTRACIÓN COMPLETA - EJERCICIO 7: SISTEMA ACADÉMICO")
    print("=" * 65)

    # 1. Creación de entidades
    profe_python = Profesor("Dr. Alan Turing", "11223344A", especialidad="Ciencias de la Computación")
    profe_ia = Profesor("Dra. Ada Lovelace", "99887766Z", especialidad="Inteligencia Artificial")

    a1 = Alumno("Mireia García", "12345678B", "EXP-2026-01")
    a2 = Alumno("Jordi Sánchez", "87654321C", "EXP-2026-02")
    a3 = Alumno("Sergi Ramos", "55443322D", "EXP-2026-03")

    # 2. Creación del Curso con aforo máximo de 2 plazas
    curso_poo = Curso("Programación Orientada a Objetos en Python", profesor=profe_python, capacidad_maxima=2)

    # 3. Matriculaciones normales
    print("\n--- Matriculación de alumnos ---")
    curso_poo.matricular(a1)
    curso_poo.matricular(a2)
    print(f"Alumnos matriculados: {len(curso_poo)}/2")
    assert len(curso_poo) == 2
    assert a1 in curso_poo.alumnos
    assert a2 in curso_poo.alumnos

    # 4. Impresión de la ficha legible (__str__)
    print("\n--- Ficha del Curso (__str__) ---")
    print(curso_poo)

    # 5. Cambio de profesor
    print("\n--- Cambio de profesor titular ---")
    curso_poo.cambiar_profesor(profe_ia)
    print(f"Nuevo docente: {curso_poo.profesor.nombre} ({curso_poo.profesor.especialidad})")
    assert curso_poo.profesor == profe_ia
    print("[OK] Cambio de profesor completado.")

    # 6. Comprobación de Casos Límite y Reglas de Negocio
    print("\n" + "=" * 65)
    print("PRUEBAS DE VALIDACIÓN Y CASOS LÍMITE")
    print("=" * 65)

    # a) Intento de matricular objeto no Alumno (ej: una Persona o un string)
    persona_generica = Persona("Carlos Invitado", "00000000P")
    try:
        curso_poo.matricular(persona_generica)  # type: ignore[arg-type]
        raise AssertionError("Fallo: Debería haber impedido matricular una Persona genérica.")
    except TypeError as e:
        print(f"[OK] Rechazada matrícula de objeto no Alumno: {e}")

    # b) Intento de asignar profesor que no es Profesor
    try:
        curso_poo.cambiar_profesor(a1)  # type: ignore[arg-type]
        raise AssertionError("Fallo: Debería haber impedido asignar un Alumno como Profesor.")
    except TypeError as e:
        print(f"[OK] Rechazada asignación de docente no válido: {e}")

    # c) Intento de matricular dos veces al mismo alumno
    try:
        curso_poo.matricular(a1)
        raise AssertionError("Fallo: Debería haber impedido matrícula duplicada.")
    except ValueError as e:
        print(f"[OK] Rechazada matrícula duplicada: {e}")

    # d) Intento de superar la capacidad máxima (aforo completo)
    try:
        curso_poo.matricular(a3)
        raise AssertionError("Fallo: Debería haber bloqueado la matrícula por exceso de aforo.")
    except OverflowError as e:
        print(f"[OK] Rechazado sobrepaso de capacidad máxima: {e}")

    # e) Desmatriculación y nueva inscripción
    print("\n--- Desmatriculación de alumnos ---")
    curso_poo.desmatricular(a1)
    assert len(curso_poo) == 1
    print(f"Mireia desmatriculada. Plazas ocupadas: {len(curso_poo)}/2")

    # Ahora Sergi sí cabe
    curso_poo.matricular(a3)
    assert a3 in curso_poo.alumnos
    print(f"Sergi matriculado exitosamente. Plazas ocupadas: {len(curso_poo)}/2")

    # f) Intento de desmatricular alumno no matriculado
    try:
        curso_poo.desmatricular(a1)
        raise AssertionError("Fallo: Debería haber fallado al desmatricular alumno ausente.")
    except ValueError as e:
        print(f"[OK] Rechazada baja de alumno no inscrito: {e}")

    # g) Comprobación de encapsulación en la propiedad alumnos
    lista_externa = curso_poo.alumnos
    try:
        lista_externa.append(a1)  # type: ignore[attr-defined]
    except AttributeError:
        print("[OK] Encapsulación validada: La propiedad 'alumnos' es una tupla inmutable.")

    print("\nTodas las pruebas del Ejercicio 7 concluyeron satisfactoriamente.")
