#include <Logger.h>

int main()
{
    Logger::Log(LoggerVerbosity::Off, "You shouldn't see this -_-");
    Logger::Log(LoggerVerbosity::Trace, "Like Hercules Mulligan, I'm here to relay information.");
    Logger::Log(LoggerVerbosity::Info, "Everything is fine.");
    Logger::Log(LoggerVerbosity::Warning, "Don't worry, it's just a warning, but you should still listen.");
    Logger::Log(LoggerVerbosity::Error, "Oh no, an error!");
    Logger::Log(LoggerVerbosity::Fatal, "Oh no, this is a super bad error!!");
}
