#pragma once

/**
 * @class RenderContext RenderContext.h
 * @brief Platform-independent render context interface.
 */
class RenderContext
{
public:
	/**
	 * @brief Dispose of this RenderContext.
	 */
	virtual ~RenderContext() = default;
	/**
	 * @brief Initialize this RenderContext.
	 */
	virtual void Initialize() = 0;

	/**
	 * @brief Swap frame buffers.
	 */
	virtual void SwapBuffers() = 0;
};