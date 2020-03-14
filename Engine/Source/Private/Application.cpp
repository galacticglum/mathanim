#include <Application.h>
#include <Common.h>
#include <Events/Event.h>

Application* Application::s_Instance = nullptr;

Application::Application()
{
    // Ensure that there is only application instance
    LOG_CATEGORY_ASSERT(!s_Instance, "Engine", "Application already exists!");
    s_Instance = this;

    // Create and initialize the window
    m_Window = std::unique_ptr<Window>(Window::Create());
    m_Window->SetEventCallback(BIND_EVENT(Application::OnEvent));

    glGenVertexArrays(1, &m_VertexArray);
    glBindVertexArray(m_VertexArray);

    glGenBuffers(1, &m_VertexBuffer);
    glBindBuffer(GL_ARRAY_BUFFER, m_VertexBuffer);

    float vertices[9] = {
        -0.5f, -0.5f, 0.0f,
        0.5f, -0.5f, 0.0f,
        0.0f, 0.5f, 0.0f
    };

    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

    glEnableVertexAttribArray(0);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), nullptr);

    glGenBuffers(1, &m_IndexBuffer);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, m_IndexBuffer);

    GLuint indices[3] = {
        0, 1, 2
    };

    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);
}

Application::~Application() = default;

void Application::Run() const
{
    while (m_IsRunning)
    {
        glClearColor(0.1f, 0.1f, 0.1f, 1);
        glClear(GL_COLOR_BUFFER_BIT);

        glBindVertexArray(m_VertexArray);
        glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, nullptr);

        // Update the window
        m_Window->OnUpdate();
    }
}

void Application::OnEvent(Event& event)
{
    EventDispather dispatcher(event);
    dispatcher.Dispatch<WindowClosedEvent>(BIND_EVENT(Application::OnWindowClose));
}

bool Application::OnWindowClose(WindowClosedEvent& event)
{
    m_IsRunning = false;
    return true;
}