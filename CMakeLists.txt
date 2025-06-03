cmake_minimum_required(VERSION 3.10)
project(SnSm VERSION 1.0.0 LANGUAGES CXX)

# Configuración de compilación
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Flags de compilación para optimización y rendimiento
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -funroll-loops -ffast-math -flto -fopenmp")
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -fopenmp -static -lopenblas")

# Buscar Eigen utilizando el archivo de firma
find_path(EIGEN3_INCLUDE_DIR
    NAMES signature_of_eigen3_matrix_library
    PATHS /usr/include/eigen3 /usr/local/include/eigen3
    DOC "Ruta al directorio de Eigen3"
)

# Verificar si se encontró Eigen
if(EIGEN3_INCLUDE_DIR)
    message(STATUS "Eigen encontrado en: ${EIGEN3_INCLUDE_DIR}")
else()
    message(FATAL_ERROR "Eigen no encontrado. Por favor, instala Eigen o especifica su ruta.")
endif()

# Crear la biblioteca
add_library(SnSm INTERFACE)

# Configurar rutas de inclusión para la instalación
target_include_directories(SnSm INTERFACE
    $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
    ${EIGEN3_INCLUDE_DIR}
)

# Configurar opciones de compilación y bibliotecas necesarias
target_compile_options(SnSm INTERFACE -O3 -funroll-loops -ffast-math -flto -fopenmp)
target_link_libraries(SnSm INTERFACE -lopenblas -fopenmp)

# Exportar la configuración de la biblioteca
install(TARGETS SnSm EXPORT SnSmConfig)
install(EXPORT SnSmConfig
    FILE SnSmConfig.cmake
    DESTINATION lib/cmake/SnSm
)

# Instalar los archivos de cabecera
install(DIRECTORY include/ DESTINATION include)