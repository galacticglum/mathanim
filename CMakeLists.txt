cmake_minimum_required(VERSION 2.6)

project(Mathanim)

# add the -c and -Wall flags
if(MSVC)
	add_definitions(
		-c
		-W4
	)
else()
	add_definitions(
		-c
		-Wall
	)
endif()

if ( CMAKE_BUILD_TYPE STREQUAL "" )
	# CMake defaults to leaving CMAKE_BUILD_TYPE empty. This screws up
	# differentiation between debug and release builds.
	set(
		CMAKE_BUILD_TYPE
			"Debug"
		CACHE STRING
			"Choose the type of build, options are: None (CMAKE_CXX_FLAGS or CMAKE_C_FLAGS used) \"Debug\" \"Release\" \"RelWithDebInfo\" \"MinSizeRel\"."
		FORCE
	)
endif ( CMAKE_BUILD_TYPE STREQUAL "" )

if ( CMAKE_BUILD_TYPE STREQUAL "Release" )
add_definitions( -O2 )
endif ( CMAKE_BUILD_TYPE STREQUAL "Release" )

# Lets LOAD up our headers for the core project
file(GLOB_RECURSE CORE_HDRS
	${Mathanim_SOURCE_DIR}/Source/Core/Public/*.h
)

# Lets LOAD up our sources for the core project
file(GLOB_RECURSE CORE_SRCS
	${Mathanim_SOURCE_DIR}/Source/Core/Private/*.cpp
	${Mathanim_SOURCE_DIR}/Source/Core/Private/*.c
)

# Define the executable
add_executable(Core ${CORE_HDRS} ${CORE_SRCS})

# We need a CMAKE_DIR with some code to find external dependencies
SET(Mathanim_CMAKE_DIR "${Mathanim_SOURCE_DIR}/cmake")

#######################################
# LOOK for the packages that we need! #
#######################################

# OpenGL
find_package(OpenGL REQUIRED)

# GLEW
INCLUDE(${Mathanim_CMAKE_DIR}/FindGLEW.cmake)

# GLFW
INCLUDE(${Mathanim_CMAKE_DIR}/FindGLFW.cmake)

# Define the include DIRs
include_directories(
	${Mathanim_SOURCE_DIR}/Source
	${OPENGL_INCLUDE_DIRS}
    ${GLEW_INCLUDE_DIRS}
    ${GLFW_INCLUDE_DIRS}
)

# Define the link libraries
target_link_libraries( Core
	${OPENGL_LIBRARIES}
    ${GLEW_LIBRARIES}
    ${GLFW_LIBRARIES}
)

if(WIN32)
	string(REPLACE "/" "\\" source_path_windows "${Mathanim_SOURCE_DIR}/Content")
	string(REPLACE "/" "\\" build_path_windows "${Mathanim_BINARY_DIR}/Content")
	execute_process(COMMAND cmd.exe /c mklink /J "${build_path_windows}" "${source_path_windows}" RESULT_VARIABLE exitcode)
else()
	execute_process(COMMAND ${CMAKE_COMMAND} -E create_symlink ${Mathanim_SOURCE_DIR}/Content ${Mathanim_BINARY_DIR}/Content RESULT_VARIABLE exitcode)
endif()

if(NOT ${exitcode} EQUAL 0)
	MESSAGE("SYMLINKING FAILED: ${exitcode}")
	MESSAGE("FALLING BACK TO COPYING")
endif()

#Copy file if the build resource folder contains an older version. This is ignored when the symlink was succesful because the files are already the newest version.
file(GLOB_RECURSE RES RELATIVE ${Mathanim_SOURCE_DIR}/Content/ ${Mathanim_SOURCE_DIR}/Content/*.*)
foreach(file IN LISTS RES)
	configure_file(${Mathanim_SOURCE_DIR}/Content/${file} ${Mathanim_BINARY_DIR}/Content/${file} COPYONLY)
endforeach()

#Create virtual folders to make it look nicer in VS
if(MSVC_IDE)
	foreach(source IN LISTS SRCS HDRS)
		get_filename_component(source_path "${source}" PATH)
		string(REPLACE "${Mathanim_SOURCE_DIR}" "" relative_source_path "${source_path}")
		string(REPLACE "/" "\\" source_path_msvc "${relative_source_path}")
		source_group("${source_path_msvc}" FILES "${source}")
	endforeach()
endif()
