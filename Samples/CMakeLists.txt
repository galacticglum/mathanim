# add the -c and -Wall flags
if(MSVC)
	add_definitions(
		-c
	)
else()
	add_definitions(
		-c
		-Wall
	)
endif()

add_definitions( -D_CRT_SECURE_NO_WARNINGS )

file(GLOB_RECURSE Samples_HDRS
	${Mathanim_SOURCE_DIR}/Samples/Source/*.h
)

file(GLOB_RECURSE Samples_SRCS
	${Mathanim_SOURCE_DIR}/Samples/Source/*.cpp
	${Mathanim_SOURCE_DIR}/Samples/Source/*.c
)

include_directories(${Mathanim_SOURCE_DIR}/Samples/Source/Public)

# Define the executable
add_executable(Samples ${Samples_HDRS} ${Samples_SRCS})
target_compile_definitions(Samples PUBLIC 
	"$<$<CONFIG:Release>:O2>" 
	"$<$<CONFIG:Release>:NDEBUG>"
)

target_compile_options(Samples PUBLIC
	"$<$<CONFIG:Release>:-w>"
	"$<$<CONFIG:Debug>:-W4>"
)

# GLAD
INCLUDE(${Mathanim_CMAKE_DIR}/FindGLAD.cmake)

# GLFW
INCLUDE(${Mathanim_CMAKE_DIR}/FindGLFW.cmake)

# spdlog
INCLUDE(${Mathanim_CMAKE_DIR}/FindSPDLOG.cmake)

# imgui
INCLUDE(${Mathanim_CMAKE_DIR}/FindImGui.cmake)

# Define the include DIRs
include_directories(
	${Mathanim_SOURCE_DIR}/Engine/Source/Public
	${OPENGL_INCLUDE_DIRS}
	${GLFW_INCLUDE_DIRS}
	${GLAD_INCLUDE_DIRS}
	${SPDLOG_INCLUDE_DIRS}
	${ImGui_INCLUDE_DIRS}
)

target_link_libraries( Samples Engine )

# Set the output directory for Samples to make managing directories easier
set (Samples_OUT_DIR "${CMAKE_CURRENT_BINARY_DIR}/bin")
set_target_properties( Samples PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${Samples_OUT_DIR})

set_property(TARGET Samples PROPERTY CXX_STANDARD 17)
set_property(TARGET Samples PROPERTY CXX_STANDARD_REQUIRED ON)

# Copy content to output directory
add_custom_command(TARGET Samples PRE_BUILD
				   COMMAND ${CMAKE_COMMAND} -E copy_directory
				   ${Mathanim_SOURCE_DIR}/Samples/Content $<TARGET_FILE_DIR:Samples>/Content)

# Copy binaries to output directory...
# Find all dependencies that have a bin folder...
include(${Mathanim_CMAKE_DIR}/utils.cmake)
SUBDIRLIST(DEPENDENCY_DIRS ${Mathanim_Engine_DEPEND_DIR})
foreach(dependency_name ${DEPENDENCY_DIRS})
	# check if there is a bin directory
	if(EXISTS "${Mathanim_Engine_DEPEND_DIR}/${dependency_name}/bin")
		# there is a bin directory which means that we should copy this dependency
		add_custom_command(TARGET Samples PRE_BUILD
						   COMMAND ${CMAKE_COMMAND} -E copy_directory
						   "${Mathanim_Engine_DEPEND_DIR}/${dependency_name}/bin/${_config}/$<$<EQUAL:4,${CMAKE_SIZEOF_VOID_P}>:Win32>$<$<EQUAL:8,${CMAKE_SIZEOF_VOID_P}>:x64>" $<TARGET_FILE_DIR:Samples>)
	endif()
endforeach()

# Set the working directory
file( WRITE "${CMAKE_CURRENT_BINARY_DIR}/Samples.vcxproj.user" 
    "<?xml version=\"1.0\" encoding=\"utf-8\"?>     \
    <Project ToolsVersion=\"4.0\" xmlns=\"http://schemas.microsoft.com/developer/msbuild/2003\">
    <PropertyGroup Condition=\"'$(Configuration)|$(Platform)'=='Debug|x64'\">
        <LocalDebuggerWorkingDirectory>$(OutDir)</LocalDebuggerWorkingDirectory>
        <DebuggerFlavor>WindowsLocalDebugger</DebuggerFlavor>
    </PropertyGroup>
    <PropertyGroup Condition=\"'$(Configuration)|$(Platform)'=='Release|x64'\">
        <LocalDebuggerWorkingDirectory>$(OutDir)</LocalDebuggerWorkingDirectory>
        <DebuggerFlavor>WindowsLocalDebugger</DebuggerFlavor>
    </PropertyGroup>
	</Project>"
)

# Create virtual folders to make it look nicer in VS
if(MSVC_IDE)
	foreach(source IN LISTS Samples_SRCS Samples_HDRS)
		get_filename_component(source_path "${source}" PATH)
		string(REPLACE "${Mathanim_SOURCE_DIR}" "" relative_source_path "${source_path}")
		string(REPLACE "/" "\\" source_path_msvc "${relative_source_path}")
		string(REPLACE "Samples\\Source\\" "" actual_source_path_msvc "${source_path_msvc}")
		source_group("${actual_source_path_msvc}" FILES "${source}")
	endforeach()
endif()