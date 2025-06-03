# SnSm: Surrogate models for Sn

SnSm es una biblioteca C++ (con bindings para Python) para trabajar las representaciones de Sn generadas por las familias YKR, YSR y YOR. 
También permite calcular, dada una función, su transformada de Fourier y transformada inversa.

---

## Características

- **Rational**: Clase para números racionales con operaciones aritméticas exactas.
- **FourierTransform**: Implementación de la transformada de Fourier para funciones sobre grupos simétricos, soportando coeficientes `double` y racionales.
- **Irrep**: Representaciones irreducibles del grupo simétrico, con evaluación y acceso a matrices asociadas.
- **Bindings Python**: Acceso a toda algunas funcionalidades desde Python usando `pybind11`.

---

## C++

## Instalación

### Requisitos
- Linux (soporte principal y probado)
- C++17
- CMake ≥ 3.10
- Eigen3
- OpenBLAS

### Comandos para instalación

```bash
git clone https://github.com/lvargasgarcia/SnSm.git
cd SnSm
sudo chmod 700 install.sh
sudo ./install.sh

```
Esto moverá los archivos *.h a /usr/local/include/

Para que el script funcione, es necesario tener instalado eigen en /usr/local/include/eigen3

## Compilación manual eficiente (C++)

Si deseas compilar manualmente un archivo C++ usando los flags de máxima eficiencia recomendados para Eigen y OpenBLAS, utiliza los siguientes flags:

- `-static`  
- `-O3`  
- `-I /usr/local/include/eigen3`  
- `-funroll-loops`  
- `-ffast-math`  
- `-flto`  
- `-fopenmp`  
- `-lopenblas`  
- `-mavx`  
- `-mavx2`  
- `-mfma`  
- `-msse4.1`  
- `-msse4.2`  
- `-DEIGEN_NO_DEBUG`  
- `-DEIGEN_USE_BLAS`  
- `-DEIGEN_USE_LAPACKE`  
- `-DEIGEN_VECTORIZE`  
- `-DEIGEN_VECTORIZE_SSE2`  
- `-DEIGEN_VECTORIZE_SSE3`  
- `-DEIGEN_VECTORIZE_SSSE3`  
- `-DEIGEN_VECTORIZE_SSE4_1`  
- `-DEIGEN_VECTORIZE_SSE4_2`  
- `-DEIGEN_VECTORIZE_AVX`  
- `-DEIGEN_VECTORIZE_FMA`  
- `-DEIGEN_VECTORIZE_AVX2`  
- `-DEIGEN_UNROLLING_LIMIT=100`  

Ejemplo de compilación:

```bash
g++ [FLAGS] experiment.cpp -o experiment
```

## Clases principales

## Rational

Representa números racionales, las clases Irrep y FourierTransform usan esta clase si hacen cálculos con números racionales 
(para las familias YKR e YSR).

## Irrep 

La clase `Irrep<T>` implementa representaciones irreducibles del grupo simétrico para un tipo de dato genérico `T` (`double` o `Rational`). 
Utiliza Eigen para el manejo eficiente de matrices dispersas y densas.
partition: Vector de enteros que define la partición asociada a la representación irreducible.
mode: Cadena de texto que indica el modo de construcción de las matrices ("YKR", "YSR", etc.).
Comportamiento:
El constructor inicializa la representación irreducible para la partición y modo dados, calcula las matrices asociadas y determina la dimensión de la representación (d_lambda).

## Constructor

```cpp
Irrep(std::vector<int> partition, std::string mode)
```

### Atributos principales:
- partition (std::vector<int>): Partición asociada a la representación.
- n (int): Número total de elementos (suma de la partición).
- mode (std::string): Modo de construcción de la representación.
- d_lambda (int): Dimensión de la representación irreducible.
- matrices (std::vector<Eigen::SparseMatrix<T>>): Matrices asociadas a cada transposición adyacente de Sn.
### Método principal
```cpp
Eigen::SparseMatrix<T> evaluate(std::vector<int> pi)
```
- pi: Vector de enteros que representa una permutación del grupo simétrico.
#### Descripción:
- Evalúa la representación irreducible sobre la permutación pi y la devuelve en formato disperso.

## FourierTransform

La clase `FourierTransform<T>` implementa la transformada de Fourier y su inversa para funciones sobre el grupo simétrico, utilizando representaciones irreducibles y álgebra lineal eficiente con Eigen. Es genérica en el tipo `T` (por ejemplo, `double` o `Rational`).

---

## Constructor

```cpp
FourierTransform(int n, std::map<int, T> f, std::string mode, int nthreads)
```

- n: Número de elementos del grupo simétrico (Sn).
- f: Mapa que asocia a cada permutación (codificada como entero) un valor de tipo T (la función sobre la que se aplica la transformada).
- mode: Cadena que indica el modo de construcción de las representaciones ("YKR", "YSR", etc.).
- nthreads: Número de hilos a usar para el cálculo paralelo (debe ser divisor de n!).
### Comportamiento:

- Inicializa la estructura de datos para todas las particiones de n, crea las representaciones irreducibles asociadas y prepara los coeficientes y vectores necesarios para la transformada y su inversa.

Atributos principales
- n (int): Número de elementos.
- nfact (int): Factorial de n (n!).
- mode (std::string): Modo de construcción de las representaciones.
- partitions (std::vector<std::vector<int>>): Todas las particiones de n.
- coefficients (std::map<int, Matrix>): Coeficientes de la transformada de Fourier para cada partición.
- irreps (std::map<int, Irrep<T>>): Representaciones irreducibles asociadas a cada partición.
- f (std::map<int, T>): Función original sobre el grupo simétrico.
- invFT (std::map<int, T>): Resultado de la transformada inversa.
- num__threads (int): Número de hilos usados en los cálculos.

### Métodos principales
```cpp
void build_coefficients()
```
Calcula los coeficientes de la transformada de Fourier para cada partición usando las representaciones irreducibles y la función f. Utiliza paralelización con OpenMP.

```cpp
void inverse_fourier_transform()
```
Calcula la transformada inversa de Fourier, reconstruyendo la función original a partir de los coeficientes y las representaciones. Utiliza paralelización con OpenMP.
```cpp
T inverseFT(int pi, int order)
```
Devuelve el valor de la función reconstruida (transformada inversa) para la permutación codificada como pi y el orden dado. Esto es, 
se realiza el cálculo de la transformada inversa usando únicamente los coeficientes con orden igual o menor que ```order```

```cpp
void set_coefficient(std::vector<std::vector<T>> &coef, std::vector<int> partition)
```

Permite establecer manualmente la matriz de coeficientes para una partición dada.


## API para python

El módulo `fourier_transform` proporciona acceso desde Python a las clases y algoritmos principales de la biblioteca C++ 
para trabajar con transformadas de Fourier y representaciones del grupo simétrico.

## Instalación

### Requisitos

- Los necesarios para instalar la biblioteca C++
- Python 3.10.4 o superior (versiones inferiores no han sido probadas).

### Comandos para instalación

Con un entorno virtual activo, ejecutar los siguientes comandos:

```bash
cd SnSm
cd python
pip install .
```

---

## Clases principales

### Rational

Representa un número racional exacto.

**Constructores:**
- `Rational(numerator: int, denominator: int)`
- `Rational(value: float)`

**Atributos:**
- `numerator`: numerador (int)
- `denominator`: denominador (int)

**Métodos:**
- `to_double()`: Devuelve el valor como float.
- Operadores aritméticos: `+`, `-`, `*`, `/`, `==`

### FourierTransform_double

Transformada de Fourier para funciones sobre el grupo simétrico con coeficientes `double`.

**Constructor:**
- `FourierTransform_double(n: int, f: dict[int, float], mode: str, nthreads: int)`

**Atributos:**
- `coefficients`: diccionario de matrices de coeficientes (por partición)
- `irreps`: diccionario de representaciones irreducibles (por partición)
- `f`: función original (diccionario)
- `invFT`: resultado de la transformada inversa (diccionario)

**Métodos:**
- `build_coefficients()`: Calcula los coeficientes de la transformada.
- `inverse_fourier_transform()`: Calcula la transformada inversa.
- `inverseFT(pi: int, order: int)`: Devuelve el valor reconstruido para una permutación y orden.
- `set_coefficient(coef: list[list[float]], partition: list[int])`: Establece manualmente los coeficientes.

### FourierTransform_double

Análogo a lo anterior pero usando coma flotante.

### Irrep_double

Representación irreducible del grupo simétrico con coeficientes `double`.

**Constructor:**
- `Irrep_double(partition: list[int], mode: str)`

**Atributos:**
- `partition`: partición asociada (lista de enteros)
- `n`: número de elementos (int)
- `mode`: modo de construcción (str)
- `d_lambda`: dimensión de la representación (int)
- `matrices`: matrices asociadas (lista de matrices dispersas)

**Métodos:**
- `evaluate(pi: list[int]) -> numpy.ndarray`: Evalúa la representación para una permutación. Devuelve la matriz correspondiente como un array de NumPy.

