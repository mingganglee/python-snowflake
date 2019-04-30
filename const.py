# 常量控制,将变量更改成为伪常量, 如果检测到已有常量被第二次赋值则抛出异常
class _const:
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const instance attribute (%s)" % name)

        self.__dict__[name] = value

import sys
sys.modules[__name__] = _const()