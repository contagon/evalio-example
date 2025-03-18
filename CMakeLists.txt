cmake_minimum_required(VERSION 3.15)
project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)

# Enforce C++17 for std::variant amongst others
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
include(FetchContent)

# Use new cmake FindPython
# https://pybind11.readthedocs.io/en/stable/cmake/#new-findpython-mode
set(PYBIND11_FINDPYTHON ON)

# Find pybind either on system, or in the python venv
# find_package(pybind11 CONFIG REQUIRED)
# Alternatively, pull from git
FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG v2.13.6
)
FetchContent_MakeAvailable(pybind11)

# Also need to find eigen
FetchContent_Declare(
    Eigen3
    GIT_REPOSITORY https://gitlab.com/libeigen/eigen.git
    GIT_TAG 3.4.0
    FIND_PACKAGE_ARGS
        NO_MODULE # uses find_package first, git if it fails
)
FetchContent_MakeAvailable(Eigen3)

# Similarly, find evalio on system or from python package
# find_package(evalio REQUIRED)
# Or pull from git
FetchContent_Declare(
    evalio
    GIT_REPOSITORY https://github.com/contagon/evalio.git
    GIT_TAG "python-cmake"
)
FetchContent_MakeAvailable(evalio)

pybind11_add_module(_core MODULE src/CppPipeline.cpp)
target_link_libraries(_core PRIVATE evalio)
install(TARGETS _core DESTINATION ${SKBUILD_PROJECT_NAME})
