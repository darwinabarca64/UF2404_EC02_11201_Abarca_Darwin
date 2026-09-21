"""
Ejercicio 2: Reserva de plazas (Reserva de places).
Módulo: MF0227_3 - Programación orientada a objetos (UF2404).

Este módulo implementa la clase `Evento` (y su alias `Esdeveniment`) para gestionar
el aforo y las inscripciones de personas a un evento garantizando:
1. Encapsulación de la colección interna de asistentes (inmutable desde el exterior).
2. Control estricto de duplicados y capacidad máxima de plazas.
3. Gestión de cancelaciones con control de excepciones.
4. Soporte del protocolo de longitud de Python mediante el método especial `__len__`.
"""

from __future__ import annotations
from typing import Tuple


class Evento:
    """Representa un evento con control de aforo y gestión de inscripciones.

    Attributes:
        nombre (str): Nombre o título descriptivo del evento.
        capacidad_maxima (int): Aforo máximo permitido de personas.
    """

    def __init__(self, nombre: str, capacidad_maxima: int) -> None:
        """Inicializa un nuevo Evento con un límite de plazas.

        Args:
            nombre: Nombre del evento (cadena no vacía).
            capacidad_maxima: Número entero positivo que indica el aforo máximo.

        Raises:
            TypeError: Si los tipos de los argumentos no son válidos.
            ValueError: Si el nombre está vacío o la capacidad no es un entero positivo (> 0).
        """
        # Validación defensiva del nombre
        if not isinstance(nombre, str):
            raise TypeError(f"El nombre del evento debe ser una cadena (str), recibido: {type(nombre).__name__}")
        
        nombre_limpio = nombre.strip()
        if not nombre_limpio:
            raise ValueError("El nombre del evento no puede estar vacío.")

        # Validación de la capacidad máxima
        if not isinstance(capacidad_maxima, int) or isinstance(capacidad_maxima, bool):
            raise TypeError(f"La capacidad máxima debe ser un número entero (int), recibido: {type(capacidad_maxima).__name__}")
        
        if capacidad_maxima <= 0:
            raise ValueError(f"La capacidad máxima debe ser un entero estrictamente positivo (> 0), recibido: {capacidad_maxima}")

        self._nombre: str = nombre_limpio
        self._capacidad_maxima: int = capacidad_maxima
        # Colección interna protegida: lista para mantener el orden cronológico de registro
        self._asistentes: list[str] = []

    @property
    def nombre(self) -> str:
        """Retorna el nombre del evento."""
        return self._nombre

    @property
    def capacidad_maxima(self) -> int:
        """Retorna la capacidad máxima del evento."""
        return self._capacidad_maxima

    @property
    def asistentes(self) -> Tuple[str, ...]:
        """Retorna una vista inmutable (tupla) de los asistentes registrados.

        Protege la colección interna contra modificaciones externas directas.
        """
        return tuple(self._asistentes)

    def reservar(self, persona: str) -> None:
        """Inscribe a una persona en el evento si hay disponibilidad y no está duplicada.

        Args:
            persona: Nombre de la persona a registrar (cadena no vacía).

        Raises:
            TypeError: Si 'persona' no es de tipo str.
            ValueError: Si 'persona' está vacía o ya se encuentra inscrita.
            OverflowError: Si se ha alcanzado la capacidad máxima del evento.
        """
        if not isinstance(persona, str):
            raise TypeError(f"El nombre de la persona debe ser str, recibido: {type(persona).__name__}")
        
        persona_limpia = persona.strip()
        if not persona_limpia:
            raise ValueError("El nombre de la persona no puede estar vacío.")

        # Regla 1: Una persona no puede reservar dos veces
        if persona_limpia in self._asistentes:
            raise ValueError(f"La persona '{persona_limpia}' ya tiene una reserva activa en el evento.")

        # Regla 2: No pueden superarse las plazas disponibles
        if len(self._asistentes) >= self._capacidad_maxima:
            raise OverflowError(f"No hay plazas disponibles. Aforo completo ({self._capacidad_maxima}/{self._capacidad_maxima}).")

        self._asistentes.append(persona_limpia)

    def cancelar(self, persona: str) -> None:
        """Cancela la reserva de una persona previamente inscrita.

        Args:
            persona: Nombre de la persona cuya reserva se desea cancelar.

        Raises:
            TypeError: Si 'persona' no es de tipo str.
            ValueError: Si la persona no está inscrita en el evento.
        """
        if not isinstance(persona, str):
            raise TypeError(f"El nombre de la persona debe ser str, recibido: {type(persona).__name__}")
        
        persona_limpia = persona.strip()
        
        # Regla 3: No se puede cancelar una reserva que no existe
        if persona_limpia not in self._asistentes:
            raise ValueError(f"No se puede cancelar: '{persona_limpia}' no figura en la lista de reservas.")

        self._asistentes.remove(persona_limpia)

    def plazas_disponibles(self) -> int:
        """Calcula el número de plazas libres restantes en el evento.

        Returns:
            int: Plazas disponibles actualmente.
        """
        return self._capacidad_maxima - len(self._asistentes)

    # Alias en catalán según requisitos bilingües del PDF
    places_disponibles = plazas_disponibles

    def __len__(self) -> int:
        """Permite obtener el número de inscritos usando len(evento).

        Returns:
            int: Número actual de personas registradas.
        """
        return len(self._asistentes)

    def __str__(self) -> str:
        """Representación legible del evento."""
        return (f"Evento '{self._nombre}' ({len(self)}/{self._capacidad_maxima} plazas ocupadas, "
                f"{self.plazas_disponibles()} disponibles)")

    def __repr__(self) -> str:
        """Representación técnica del objeto."""
        return f"Evento(nombre={self._nombre!r}, capacidad_maxima={self._capacidad_maxima!r}, inscritos={len(self)})"


# Alias para soporte en catalán
Esdeveniment = Evento


if __name__ == "__main__":
    print("=" * 60)
    print("DEMOSTRACIÓN COMPLETA - EJERCICIO 2: RESERVA DE PLAZAS")
    print("=" * 60)

    # 1. Creación de un evento con aforo para 2 personas
    conferencia = Evento("Taller Python POO", capacidad_maxima=2)
    print(f"Evento creado: {conferencia}")
    print(f"Plazas disponibles iniciales: {conferencia.plazas_disponibles()}")
    print(f"len(conferencia) inicial: {len(conferencia)}")
    assert conferencia.plazas_disponibles() == 2
    assert len(conferencia) == 0

    # 2. Reservas exitosas
    print("\n--- Reservas exitosas ---")
    conferencia.reservar("Laura")
    print(f"Reserva para Laura. Asistentes: {conferencia.asistentes}, Plazas libres: {conferencia.plazas_disponibles()}")
    assert len(conferencia) == 1
    assert conferencia.plazas_disponibles() == 1

    conferencia.reservar("Carlos")
    print(f"Reserva para Carlos. Asistentes: {conferencia.asistentes}, Plazas libres: {conferencia.plazas_disponibles()}")
    assert len(conferencia) == 2
    assert conferencia.plazas_disponibles() == 0
    print("[OK] Reservas exitosas validadas.")

    # 3. Caso límite: Intento de reserva duplicada
    print("\n--- Intento de reserva duplicada ---")
    try:
        conferencia.reservar("Laura")
        raise AssertionError("Fallo: Debería haber impedido la reserva duplicada de Laura.")
    except ValueError as e:
        print(f"[OK] Capturado intento duplicado correctamente: {e}")

    # 4. Caso límite: Intento de superar el aforo
    print("\n--- Intento de superar aforo máximo ---")
    try:
        conferencia.reservar("Marta")
        raise AssertionError("Fallo: Debería haber impedido superar el aforo.")
    except OverflowError as e:
        print(f"[OK] Capturado exceso de aforo correctamente: {e}")

    # 5. Cancelación exitosa y liberación de plaza
    print("\n--- Cancelación y nueva reserva ---")
    conferencia.cancelar("Laura")
    print(f"Laura canceló su plaza. len(conferencia) = {len(conferencia)}, Plazas libres = {conferencia.plazas_disponibles()}")
    assert len(conferencia) == 1
    assert conferencia.plazas_disponibles() == 1

    # Ahora Marta sí puede reservar
    conferencia.reservar("Marta")
    print(f"Marta se ha reservado con éxito. Asistentes: {conferencia.asistentes}")
    assert "Marta" in conferencia.asistentes
    assert "Laura" not in conferencia.asistentes
    print("[OK] Cancelación y reasignación validadas.")

    # 6. Caso límite: Cancelar reserva inexistente
    print("\n--- Intento de cancelar reserva inexistente ---")
    try:
        conferencia.cancelar("Pepe")
        raise AssertionError("Fallo: Debería haber lanzado error al cancelar alguien no inscrito.")
    except ValueError as e:
        print(f"[OK] Capturada cancelación inexistente correctamente: {e}")

    # 7. Verificación de encapsulamiento e inmutabilidad externa
    print("\n--- Prueba de Encapsulamiento y Protección de Datos ---")
    lista_asistentes = conferencia.asistentes
    print(f"Propiedad 'asistentes' retornada (tipo {type(lista_asistentes).__name__}): {lista_asistentes}")
    
    # Comprobamos que no se puede mutar directamente
    try:
        # Si fuera tupla, no tiene append; si el usuario intenta asignación dará error
        lista_asistentes.append("Intruso")  # type: ignore[attr-defined]
    except AttributeError:
        print("[OK] Inmutabilidad garantizada: La propiedad 'asistentes' es una tupla y no permite append().")

    assert len(conferencia) == 2, "La lista interna del evento no debe haber sido modificada."
    print("\nTodas las pruebas de la clase Evento pasaron satisfactoriamente.")
