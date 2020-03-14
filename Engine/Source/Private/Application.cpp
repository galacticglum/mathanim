#include <Application.h>
#include <Core.h>
#include <Events/Event.h>

Application::Application()
{
    m_Window = std::unique_ptr<Window>(Window::Create());
    m_Window->SetEventCallback(BIND_EVENT(Application::OnEvent));
}

Application::~Application() = default;

void Application::Run()
{
    while (m_IsRunning)
    {
        m_Window->OnUpdate();
    }
}

void Application::OnEvent(Event& event)
{
    EventDispather dispatcher(event);
    dispatcher.Dispatch<WindowClosedEvent>(BIND_EVENT(Application::OnWindowClose));

    Logger::Log(LoggerVerbosity::Trace, event);
}

bool Application::OnWindowClose(WindowClosedEvent& event)
{
    m_IsRunning = false;
    return true;
}