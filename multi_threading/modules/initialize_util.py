import json
import os
import signal
import sys
import re

from multi_threading.modules.timer import startup_timer

def fix_torch_version():
    import torch

    if '.dev' in torch.__version__ or '+git' in torch.__version__:
        torch.__long_version__ = torch.__version__
        torch.__version__ = re.search(r'[\d.]+[\d]', torch.__version__).group(0)

def fix_pytorch_lightning():
    if 'pytorch_lightning.utilities.distributed' not in sys.modules:
        import pytorch_lightning
        print("Pytorch_lightning.distributed not found, attempting pytorch_lightning.rank_zero")
        sys.modules["pytorch_lightning.utilities.distributed"] = pytorch_lightning.utilities.rank_zero

def fix_asyncio_event_loop_policy():
    import asyncio

    if sys.platform == 'win32' and hasattr(asyncio, 'WindowsSelectorEventLoopPolicy'):
        _BasePolicy = asyncio.WindowsSelectorEventLoopPolicy
    else:
        _BasePolicy = asyncio.DefaultEventLoopPolicy

    class AnyThreadEventLoopPolicy(_BasePolicy):
        def get_event_loop(self) -> asyncio.AbstractEventLoop:
            try:
                return super().get_event_loop()
            except (RuntimeError, AssertionError):
                loop = self.new_event_loop()
                self.set_event_loop(loop)
                return loop
            
    asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())

def restore_config_state_file():
    pass