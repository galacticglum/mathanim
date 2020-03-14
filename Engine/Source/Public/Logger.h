#pragma once

#include <memory>
#include <string>
#include <unordered_map>

#include <spdlog/spdlog.h>
#include <spdlog/fmt/ostr.h>

#include <Utilities/MacroUtilities.h>

#define GLOBAL_LOGGER_IDENTIFIER "Global"
#define DEFAULT_MESSAGE_FORMAT "%^[%T] %n: %v%$"

/**
 * @enum LoggerVerbosity LoggerVerbosity.h
 * @brief The logger levels.
 */
enum class LoggerVerbosity
{
    Off,
    Trace,
    Info,
    Warning,
    Error,
    Fatal
};

/**
 * @class Logger Logger.h
 * @brief Message logging system.
 */
class Logger
{
public:
    /**
     * @brief Initialize the logger.
     * @note This method is automatically called by the Logger before any logging operations; however, the Logger can also be manually initialized.
     * @param defaultMessageFormat The format that a log message defaults to.
     * @param force A boolean value indicating whether or not the Logger should be initialized even if it has already been initialized.
     *              This is useful when Logger settings need to be changed during runtime.
     */
    static void Initialize(const std::string& defaultMessageFormat = DEFAULT_MESSAGE_FORMAT, bool force = false);

    /**
     * @brief Log in the specified @p category.
     * @param category The name of the category to log under.
     * @param verbosity The verbosity of the log message.
     * @param args The message(s) to log.
     */
    template <typename... Args>
    static void Log(const std::string& category, const LoggerVerbosity verbosity, const Args&... args)
    {
        InternalLog(category, verbosity, args...);
    }

    /**
     * @brief Log in the global category.
     * @param verbosity The verbosity of the log message.
     * @param args The messages(s) to log.
     */
    template <typename... Args>
    static void Log(const LoggerVerbosity verbosity, const Args&... args)
    {
        InternalLog(GLOBAL_LOGGER_IDENTIFIER, verbosity, args...);
    }

    /**
     * @brief Adds a category with the specified spdlog::logger instance using the default message format.
     * @param name The name of the category.
     * @param logger An instance of the spdlog::logger.
     */
    static void RegisterCategory(const std::string& name, const std::shared_ptr<spdlog::logger>& logger)
    {
        RegisterCategory(name, logger, m_DefaultMessageFormat);
    }

    /**
     * @brief Adds a category with the specified spdlog::logger instance using a custom message format.
     * @param name The name of the category.
     * @param logger An instance of the spdlog::logger.
     * @param messageFormat The format of all messages logged under this category.
     */
    static void RegisterCategory(const std::string& name, const std::shared_ptr<spdlog::logger>& logger, const std::string& messageFormat);

    /**
     * @brief Gets the global spdlog::logger instance.
     */
    static const std::shared_ptr<spdlog::logger>& GetLogger();

    /**
     * @brief Get a logger instance for the specified @p category.
     * @param category The category of the logger instance to retrieve.
     */
    static const std::shared_ptr<spdlog::logger>& GetLogger(const std::string& category);
private:
    template <typename... Args>
    static void InternalLog(const std::string& category, const LoggerVerbosity verbosity, const Args&... args)
    {
        const std::string verbosityName = s_VerbosityNames.find(verbosity)->second;
        auto level = spdlog::level::from_str(verbosityName);
        GetLogger(category)->log(level, args...);
    }

    static const std::unordered_map <LoggerVerbosity, std::string> s_VerbosityNames;
    static std::unordered_map<std::string, std::shared_ptr<spdlog::logger>> s_Loggers;
    static bool s_IsInitialized;

    static std::string m_DefaultMessageFormat;
};

/**
 * @brief Assert a condition
 * @note Triggers a breakpoint if the condition is false.
 */
#define LOG_CATEGORY_ASSERT(x, category, message, ...) {																	\
	if (!(x))																												\
	{																														\
		Logger::Log(category, LoggerVerbosity::Error, "Assertion Failed: " XSTR(message), __VA_ARGS__);						\
		__debugbreak();																										\
	}																														\
}

 /**
  * @brief Assert a condition without triggering a breakpoint.
  */
#define LOG_CATEGORY_ASSERT_NOBREAK(x, category, message, ...) {															\
	if (!(x))																												\
	{																														\
		Logger::Log(category, LoggerVerbosity::Error, "Assertion Failed: " XSTR(message), __VA_ARGS__);						\
	}																														\
}

  /**
   * @brief Assert a condition.
   * @note Triggers a breakpoint if the condition is false.
   */
#define LOG_ASSERT(x, ...) LOG_CATEGORY_ASSERT(x, GLOBAL_LOGGER_IDENTIFIER, __VA_ARGS__)

   /**
    * @brief Assert a condition without triggering a breakpoint.
    */
#define LOG_ASSERT_NOBREAK(x, ...) LOG_CATEGORY_ASSERT_NOBREAK(x, GLOBAL_LOGGER_IDENTIFIER, __VA_ARGS__)