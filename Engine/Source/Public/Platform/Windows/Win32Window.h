#pragma once

#include <string>
#include <Window.h>

#include <GLFW/glfw3.h>

class Win32Windows : public Window
{
public:
    explicit Win32Windows(const WindowProperties& props);
    virtual ~Win32Windows();

    void OnUpdate() const override;
    uint32_t GetWidth() const override
    {
        return m_Data.Width;
    }

    uint32_t GetHeight() const override
    {
        return m_Data.Height;
    }

    void ToggleVSync(bool enabled) override;
    bool IsVSyncEnabled() const override
    {
        return m_Data.IsVSyncEnabled;
    }

private:
    virtual void Initialize(const WindowProperties& props);
    virtual void Shutdown();

    GLFWwindow* m_Window;
    struct WindowData
    {
        std::string Title;
        uint32_t Width;
        uint32_t Height;
        bool IsVSyncEnabled;
    } m_Data;
};