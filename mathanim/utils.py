import functools

def rgetattr(obj, name, *args):
    '''
    A recursive implementatin of the ``getattr`` function that supports "dot" notation.

    :param obj:
        The object whose attribute to get.
    :param name:
        The name of the attribute to get.
    
    '''
    def _getattr(obj, name):
        return getattr(obj, name, *args)

    return functools.reduce(_getattr, [obj] + name.split('.'))

def rsetattr(obj, name, value):
    '''
    A recursive implementatin of the ``setattr`` function that supports "dot" notation.

    :param obj:
        The object whose attribute to set.
    :param name:
        The name of the attribute to set.
    :param value:   
        The value to set the attribute to.

    '''
    
    pre, _, post = name.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, value)
