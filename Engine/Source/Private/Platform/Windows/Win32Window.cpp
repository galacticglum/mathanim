#include <Platform/Windows/Win32Window.h>
#include <Window.h>
#include <Logger.h>
#include <Events/ApplicationEvents.h> 
#include <Platform/OpenGL/OpenGLContext.h> 

static bool s_IsGLFWInitialized = false;

static void GLFWErrorCallback(const int error, const char* description)
{
    Logger::Log("Graphics", LoggerVerbosity::Error, "GLFW Error ({0}): {1}", error, description);
}

Window* Window::Create(const WindowProperties& props)
{
    return new Win32Window(props);
}

Win32Window::Win32Window(const WindowProperties& props) : m_Window(nullptr)
{
    Initialize(props);
}

Win32Window::~Win32Window()
{
    Shutdown();
}

void Win32Window::OnUpdate() const
{
    glfwPollEvents();
    m_RenderContext->SwapBuffers();
}

void Win32Window::ToggleVSync(const bool enabled)
{
    glfwSwapInterval(enabled ? 1 : 0);
    m_Data.IsVSyncEnabled = enabled;
}

void Win32Window::Initialize(const WindowProperties& props)
{
    m_Data.Title = props.Title;
    m_Data.Width = props.Width;
    m_Data.Height = props.Height;

    Logger::Log("Graphics", LoggerVerbosity::Info, "Create window \"{}\" ({} x {})", props.Title, props.Width, props.Height);
    if (!s_IsGLFWInitialized)
    {
        const int success = glfwInit();
        LOG_CATEGORY_ASSERT(success, "Graphics", "Could not initialize GLFW!");
        glfwSetErrorCallback(GLFWErrorCallback);
        s_IsGLFWInitialized = success;
    }

    m_Window = glfwCreateWindow(static_cast<int>(props.Width), static_cast<int>(props.Height), m_Data.Title.c_str(), nullptr, nullptr);
    m_RenderContext = new OpenGLContext(m_Window);
    m_RenderContext->Initialize();

    glfwSetWindowUserPointer(m_Window, &m_Data);
    ToggleVSync(true);

    // Initialize events
    glfwSetWindowSizeCallback(m_Window, [](GLFWwindow* window, const int width, const int height)
    {
        WindowData& data = *static_cast<WindowData*>(glfwGetWindowUserPointer(window));

        // Update window data
        data.Width = width;
        data.Height = height;

        // Create and dispatch event
        WindowResizedEvent resizeEvent(width, height);
        data.Handler(resizeEvent);
    });

    glfwSetWindowCloseCallback(m_Window, [](GLFWwindow* window)
    {
        WindowData& data = *static_cast<WindowData*>(glfwGetWindowUserPointer(window));
        WindowClosedEvent closeEvent;
        data.Handler(closeEvent);
    });
}

void Win32Window::Shutdown() const
{
    glfwDestroyWindow(m_Window);
}