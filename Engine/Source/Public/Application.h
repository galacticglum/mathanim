#pragma once

#include <memory>
#include <Window.h>

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
private:
    std::unique_ptr<Window> m_Window;
    bool m_IsRunning = true;
};