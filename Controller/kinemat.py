

import numpy as np
import DiscoBotKinematics as dbk

pi = np.pi
pi2 = pi/2
pi4 = pi/4

retval = dbk.findEndEffectorTip(pi2, 1.347, 0.36688, 0.76769)

print retval


dbk.runInverse(30.49, 0.0, 49.06, -0.66)

