import os
import sys
import config.settings

# Creating a settings object corresponding to env
APP_ENV = os.environ.get('APP_ENV', 'Dev')
_current = getattr(
    sys.modules['config.settings'],
    '{0}Config'.format(APP_ENV)
)()

# Copying attributes to module
for atr in [f for f in dir(_current) if '__' not in f]:
    # environment override
    val = os.environ.get(atr, getattr(_current, atr))
    setattr(sys.modules[__name__], atr, val)


def as_dict():
    res = {}
    for atr in [f for f in dir(config) if '__' not in f]:
        val = getattr(config, atr)
        res[atr] = val
    return res
