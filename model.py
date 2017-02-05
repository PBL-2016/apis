import chainer
from chainer import Chain
import chainer.functions as F
import chainer.links as L

class PBLLogi(Chain):
    def __init__(self):
        super(PBLLogi, self).__init__(
            l1=L.Linear(8,5),
        )
    
    def __call__(self, x, y):
        return F.mean_squared_error(self.fwd(x), y)
    
    def fwd(self, x):
        return F.softmax(self.l1(x))