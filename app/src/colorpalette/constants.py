import numpy as np
import os
import sys

constantsPath = os.path.join(
    os.path.dirname(sys.modules['__main__'].__file__),
    'app',
    'src',
    'colorpalette',
    'constants'
)

WEBSAFE_PALETTE = np.load(f"{constantsPath}/websafe.npy")
