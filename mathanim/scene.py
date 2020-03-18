import cairo

class SceneSettings:
    '''
    The settings of a Scene.

    '''
    
    def __init__(self, width, height, fps):
        '''
        Initializes SceneSettings.

        :param width:
            The width of the scene's reference frame.
        :param height:
            The height of the scene's reference frame.
        :param fps:
            The frames per second of the scene.
        
        '''
        self.width = width
        self.height = height
        self.fps = fps

# HDTV (1080p at 30 frames per second) scene preset.
SceneSettings.HDTV = SceneSettings(1920, 1080, 30)

class Scene:
    def __init__(self, settings=SceneSettings.HDTV):
        self.settings = settings

    def __enter__(self):
        print('scene entered')

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print('scene exited')