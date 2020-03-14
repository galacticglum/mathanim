#pragma once

#include <memory>
#include <Window.h>
#include <Events/Event.h> 
#include <Events/ApplicationEvents.h> 

/**
 * @class Application Application.h
 * @brief The main application.
 */
class Application
{
public:
    Application();
    virtual ~Application();
    void Run();

    void OnEvent(Event& event);
private:
    bool OnWindowClose(WindowClosedEvent& event);

    std::unique_ptr<Window> m_Window;
    bool m_IsRunning = true;
};