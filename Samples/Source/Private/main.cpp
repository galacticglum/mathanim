#include <Logger.h>
#include <Application.h>

class SampleApplication : public Application
{
public:
	SampleApplication()
	{
	}

	~SampleApplication()
	{
		
	}
};

/**
 * Entry point for the sample application.
 */
int main(int argc, char** argv)
{
    // Test logging
    Logger::Log(LoggerVerbosity::Off, "You shouldn't see this -_-");
    Logger::Log(LoggerVerbosity::Trace, "Like Hercules Mulligan, I'm here to relay information.");
    Logger::Log(LoggerVerbosity::Info, "Everything is fine.");
    Logger::Log(LoggerVerbosity::Warning, "Don't worry, it's just a warning, but you should still listen.");
    Logger::Log(LoggerVerbosity::Error, "Oh no, an error!");
    Logger::Log(LoggerVerbosity::Fatal, "Oh no, this is a super bad error!!");

    // Create and start sample application
	SampleApplication* sampleApplication = new SampleApplication();
    sampleApplication->Run();
	delete sampleApplication;
}