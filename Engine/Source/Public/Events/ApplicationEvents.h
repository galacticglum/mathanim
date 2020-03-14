#pragma once

#include <sstream>
#include <Events/Event.h>

/**
 * @class WindowResizedEvent ApplicationEvents.h
 * @brief Raised whenever the window is resized.
 */
class WindowResizedEvent : public Event
{
public:
	/**
	 * Initialize a new WindowResizeEvent given a @p width and @p height.
	 */
	WindowResizedEvent(const uint32_t width, const uint32_t height) : m_Width(width), m_Height(height)
	{
	}

	/**
	 * @brief Get the width.
	 */
	uint32_t GetWidth() const { return m_Width; }

	/**
	 * @brief Get the height.
	 */
	uint32_t GetHeight() const { return m_Height; }

	/**
	 * @brief Convert this WindowResizeEvent to its string representation.
	 */
	std::string ToString() const override
	{
		std::stringstream stream;
		stream << "WindowResizeEvent: " << m_Width << ", " << m_Height;
		return stream.str();
	}

	EVENT_CLASS_TYPE(WindowResized)
	EVENT_CLASS_CATEGORY(Application)
private:
	uint32_t m_Width;
	uint32_t m_Height;
};

/**
 * @class WindowClosedEvent ApplicationEvents.h
 * @brief Raised whenever the window is closed.
 */
class WindowClosedEvent : public Event
{
public:
	WindowClosedEvent() = default;

	EVENT_CLASS_TYPE(WindowClosed)
	EVENT_CLASS_CATEGORY(Application)
};