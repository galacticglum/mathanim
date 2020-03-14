macro(ternary var boolean value1 value2)
    set(${var} $<${${boolean}}:${value1}>$<$<NOT:${${boolean}}>:${value2}>)
endmacro(ternary)

macro(CONFIG_NAME var)
    set(${var} $<$<CONFIG:Debug>:Debug>$<$<CONFIG:Release>:Release>)
endmacro(CONFIG_NAME)

CONFIG_NAME(_config)
cmake_minimum_required(VERSION 3.6)

# Setup the base project
project(Mathanim)

option(BUILD_ENGINE "Generate engine project" ON)
option(BUILD_SAMPLES "Generate samples project" ON)

# We need a CMAKE_DIR with some code to find external dependencies
SET(Mathanim_CMAKE_DIR "${Mathanim_SOURCE_DIR}/CMake")
SET(Mathanim_Engine_DEPEND_DIR "${Mathanim_SOURCE_DIR}/Engine/Dependencies")

if(BUILD_ENGINE)
    add_subdirectory(${CMAKE_SOURCE_DIR}/Engine)
endif()

if(BUILD_SAMPLES)
    add_subdirectory(${CMAKE_SOURCE_DIR}/Samples)
endif()

if (MSVC)
    set_property(DIRECTORY PROPERTY VS_STARTUP_PROJECT Samples)
endif (MSVC)