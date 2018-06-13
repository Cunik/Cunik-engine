import sys
sys.path.append('..')

import api.models.cunik as C

cfg = C.CunikConfig(
)

cu = C.Cunik(cfg)
input('waiting')
cu.start()
input('started')
cu.stop()
input('stopped')
