from setuptools import setup, Extension
import pybind11
import os

# Detectar la ruta de OpenBLAS (si está instalada en el sistema)
openblas_include = os.environ.get("OPENBLAS_INCLUDE", "/usr/include")
openblas_lib = os.environ.get("OPENBLAS_LIB", "/usr/lib")

ext_modules = [
    Extension(
        "fourier_transform",
        ["fourier_bindings.cpp"],
        include_dirs=[
            "../include",  # Tu directorio de cabeceras
            pybind11.get_include(),  # Incluir pybind11
            openblas_include,  # Ruta a los encabezados de OpenBLAS
            "/usr/local/include/eigen3",  # Ruta a Eigen
        ],
        libraries=["openblas"],  # Vincular con OpenBLAS
        library_dirs=[openblas_lib],  # Ruta a las bibliotecas de OpenBLAS
        language="c++",
        extra_compile_args=[
            "-std=c++17",  # Usar C++17
            "-fopenmp",  # Habilitar OpenMP para paralelismo
            "-O3",  # Optimización para velocidad
            "-ffast-math",  # Habilitar optimizaciones matemáticas agresivas
            "-DEIGEN_USE_BLAS",  
            "-DEIGEN_USE_LAPACKE",
            "-DEIGEN_NO_DEBUG",  # Desactivar las comprobaciones de depuración de Eigen
            "-DEIGEN_NO_STATIC_ASSERT",  # Desactivar las aserciones estáticas de Eigen
            "-DEIGEN_VECTORIZE",  # Habilitar vectorización de Eigen
        ],
        extra_link_args=[
            "-fopenmp",  # Vincular con OpenMP
        ],
    ),
]

setup(
    name="fourier_transform",
    version="0.1",
    author="Lázaro Vargas García",
    description="Bindings de Fourier Transform para Python",
    ext_modules=ext_modules,
    zip_safe=False,
    install_requires=[
        "numpy",  # Requerido para la manipulación de matrices
        "pybind11>=2.6.0",  # Requerido para la vinculación de C++ y Python
    ],
    python_requires=">=3.6",  # Requiere Python 3.6 o superior
)
