cmake_minimum_required(VERSION 3.15)
project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)

# Enforce C++17 for std::variant amongst others
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
include(FetchContent)

# Find python
find_package(
    Python
    3.11
    REQUIRED
    COMPONENTS Interpreter Development.Module
    OPTIONAL_COMPONENTS Development.SABIModule
)

# Find pybind either on system or in the python venv
find_package(nanobind CONFIG REQUIRED)
# Alternatively, pull from git
# FetchContent_Declare(
#     nanobind
#     GIT_REPOSITORY https://github.com/wjakob/nanobind
#     GIT_TAG v2.7.0
# )
# FetchContent_MakeAvailable(nanobind)

# Also need to find eigen
FetchContent_Declare(
    Eigen3
    GIT_REPOSITORY https://gitlab.com/libeigen/eigen.git
    GIT_TAG 3.4.0
    FIND_PACKAGE_ARGS
        NO_MODULE # uses find_package first, git if it fails
)
FetchContent_MakeAvailable(Eigen3)

# Similarly, find evalio on system or from the evalio python package
find_package(evalio REQUIRED)
# Or pull from git
# FetchContent_Declare(
#     evalio
#     GIT_REPOSITORY https://github.com/contagon/evalio.git
#     GIT_TAG "master"
# )
# FetchContent_MakeAvailable(evalio)

nanobind_add_module(_core src/evalio_example/CppPipeline.cpp)
target_link_libraries(_core PRIVATE evalio)
install(TARGETS _core DESTINATION ${SKBUILD_PROJECT_NAME})
