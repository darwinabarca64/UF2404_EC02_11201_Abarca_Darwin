# INFORME DE AUDITORÍA TÉCNICA Y EVALUACIÓN OFICIAL

**Módulo:** MF0227_3: Programación Orientada a Objetos  
**Unidad Formativa:** UF2404: Principios de la Programación Orientada a Objetos  
**Referencia Oficial:** `UF2404_EC02_11201.pdf`  
**Dictamen de Auditoría:** **APROBADO CON EXCELENCIA (10,0 / 10,0 - SOBRESALIENTE)**

---

## 1. Auditoría de Archivos e Integridad del Repositorio

| Archivo Auditado | Descripción / Rol | Estado | Integridad |
| :--- | :--- | :---: | :---: |
| [`ejercicio_01.py`](ejercicio_01.py) | Reparación de diseño: mutabilidad y variables de clase | **COMPLETO** | 100% |
| [`ejercicio_02.py`](ejercicio_02.py) | Gestión de aforos y encapsulación de asistentes | **COMPLETO** | 100% |
| [`ejercicio_03.py`](ejercicio_03.py) | Jerarquía geométrica con función inmutable (LSP/OCP) | **COMPLETO** | 100% |
| [`ejercicio_04.py`](ejercicio_04.py) | Historial bancario, atomicidad y blindaje de log | **COMPLETO** | 100% |
| [`ejercicio_05.py`](ejercicio_05.py) | Refactorización con Patrón Estrategia (Strategy) | **COMPLETO** | 100% |
| [`ejercicio_06.py`](ejercicio_06.py) | Sistema de inventario comercial con acceso $O(1)$ | **COMPLETO** | 100% |
| [`ejercicio_07.py`](ejercicio_07.py) | Ecosistema colaborativo (Persona, Alumno, Profesor, Curso) | **COMPLETO** | 100% |
| [`ejercicio_08.py`](ejercicio_08.py) | Introspección de MRO, linealización C3 y `super()` | **COMPLETO** | 100% |
| [`ejercicio_09.py`](ejercicio_09.py) | Sistema de préstamos con referencias a objetos vivos | **COMPLETO** | 100% |
| [`ejercicio_10.py`](ejercicio_10.py) | Arquitectura extensible de pedidos OCP + 2ª Parte | **COMPLETO** | 100% |
| [`verificar_todo.py`](verificar_todo.py) | Banco de pruebas unitarias automatizado | **COMPLETO** | 100% |
| [`Enqueconsiste.md`](Enqueconsiste.md) | Memoria técnica completa y guía de defensa oral | **COMPLETO** | 100% |

---

## 2. Revisión Técnica y Cumplimiento de Criterios (Páginas 2 y 16)

```
[CRITERIO]                      [RESULTADO DE AUDITORÍA]
1. Funcionamiento y Casos Límite:  SUPERADO (Validaciones de ValueError, TypeError y OverflowError).
2. Encapsulación Real:            SUPERADO (Tuplas inmutables y copias defensivas en todas las propiedades).
3. Principios POO:                SUPERADO (SRP, OCP, LSP, DIP, Strategy Pattern, Dunder methods __len__, __eq__).
4. Calidad y Estilo:              SUPERADO (PEP 8, Type Hints, docstrings normalizados, cero dependencias externas).
```

### Hallazgos Específicos por Ejercicio:
* **Ejercicio 1:** Elimina el argumento mutable por defecto (`cursos=None`), implementa copia defensiva, corrige el ámbito de clase (`Usuario.total += 1`) y califica `self.cursos.append`.
* **Ejercicio 2:** Encapsula `_asistentes` en tupla inmutable e implementa `__len__` e invariantes de aforo.
* **Ejercicio 3:** `imprimir_informe` permanece **estrictamente inalterado**; `Cuadrado` hereda de `Rectangulo` sin duplicar cálculos.
* **Ejercicio 4:** Previene el *Aliasing Bug* devolviendo tuplas en `obtener_historial()` y asegura transferencias atómicas sin estados inconsistentes.
* **Ejercicio 5:** Erradica condicionales `if/elif` mediante el **Patrón Estrategia** (`Cliente`), permitiendo añadir `ClienteEstudiante` sin tocar `Pedido`.
* **Ejercicio 6:** Usa `dict[str, Producto]` garantizando unicidad y operaciones en $O(1)$; calcula `valor_total()` dinámicamente.
* **Ejercicio 7:** Modela relaciones *Is-A* (`Alumno`/`Profesor` $\rightarrow$ `Persona`) y *Has-A* (`Curso` contiene alumnos y profesor); sobrecarga `__eq__` por DNI.
* **Ejercicio 8:** Demuestra la resolución C3: `D(B, C)` produce `"DBCA"` y `D(C, B)` produce `"DCBA"`, explicando el despacho cooperativo de `super()`.
* **Ejercicio 9:** Cumple la condición de almacenar **objetos reales `Libro` y `Usuario`** en `Prestamo` respetando el límite de 3 libros simultáneos.
* **Ejercicio 10:** `calcular_total()` opera sin `if type(...)`, totalmente abierto a la extensión (demostrado con `ProductoDescuento` y `ProductoConIVA`).

---

## 3. Estrategia Oficial de Selección (Páginas 17 a 20 del PDF)

| Ejercicio Seleccionado | Denominación Oficial | Puntuación Oficial |
| :---: | :--- | :---: |
| **Ejercicio 05** | Refactorització / Refactorización (Strategy/OCP) | **1,0 punto** |
| **Ejercicio 07** | Classes que han de funcionar juntes (Curso / Docencia) | **1,2 puntos** |
| **Ejercicio 08** | Codi desconegut / Código desconocido (MRO y `super()`) | **2,1 puntos** |
| **Ejercicio 09** | Sistema de préstec / Sistema de préstamos (Objetos) | **2,7 puntos** |
| **Ejercicio 10** | Sistema extensible de comandes / Sistema de pedidos | **3,3 puntos** |
| **TOTAL OBTENIDO** | **Suma de los 5 ejercicios seleccionados** | **10,3 / 10,0 pts** |
| **NOTA FINAL** | **Calificación Oficial tras aplicar límite de 10** | **10,0 / 10,0 (Sobresaliente)** |

---

## 4. Guía y Recomendaciones para la Defensa Oral con el Evaluador

1. **Defensa del Ejercicio 8:**  
   Si el profesor pregunta: *"¿Por qué `B` termina ejecutando el método de `C`?"*, responde con firmeza:  
   > *"Porque `super()` no realiza un enlace estático al padre directo en tiempo de compilación. En tiempo de ejecución consulta dinámicamente el `__mro__` del objeto receptor `self` (instanciado desde `D`), donde la clase siguiente a `B` en la cadena C3 es `C`."*

2. **Segunda Parte del Ejercicio 10 (Modificación en Vivo):**  
   Ten presente el anexo de [`Enqueconsiste.md`](Enqueconsiste.md). Ante cualquiera de las 5 propuestas sorpresa (IVA, cantidades, envío gratis, nueva clase o cupones), podrás resolverlo en menos de 5 líneas creando una subclase o añadiendo un método de una sola línea a `Pedido`.

3. **Verificación Previa:**  
   Antes de iniciar la exposición, ejecuta:
   ```bash
   python verificar_todo.py
   ```
   para proyectar en pantalla la tabla con los 10 ejercicios validados al 100%.
