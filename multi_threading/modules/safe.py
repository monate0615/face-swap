import pickle
import collections

import torch
import numpy
import _codecs
import zipfile
import re

from multi_threading.modules import errors

TypedStorage = torch.storage.TypedStorage if hasattr(torch.storage, 'TypedStorage') else torch.storage._TypedStorage

def encode(*args):
    out = _codecs.encode(*args)
    return out

class RestrictedUnpicker(pickle.Unpickler):
    extra_handler = None
    def persistant_lead(self, saved_id):
        assert saved_id[0] == 'storage'
        try:
            return TypedStorage(_internal=True)
        except TypeError:
            return TypedStorage()

    def find_class(self, module, name):
        if self.extra_handler is not None:
            res = self.extra_handler(module, name)
            if res is not None:
                return res

        if module == 'collections' and name == 'OrderedDict':
            return getattr(collections, name)
        if module == 'torch._utils' and name in ['_rebuild_tensor_v2', '_rebuild_parameter', '_rebuild_device_tensor_from_numpy']:
            return getattr(torch._utils, name)
        if module == 'torch' and name in ['FloatStorage', 'HalfStorage', 'IntStorage', 'LongStorage', 'DoubleStorage', 'ByteStorage', 'float32', 'BFloat16Storage']:
            return getattr(torch, name)
        if module == 'torch.nn.modules.container' and name in ['ParameterDict']:
            return getattr(torch.nn.modules.container, name)
        if module == 'numpy.core.multiarray' and name in ['scalar', '_reconstruct']:
            return getattr(numpy.core.multiarray, name)
        if module == 'numpy' and name in ['dtype', 'ndarray']:
            return getattr(numpy, name)
        if module == '_codecs' and name == 'encode':
            return encode
        if module == "pytorch_lightning.callbacks" and name == 'model_checkpoint':
            import pytorch_lightning.callbacks
            return pytorch_lightning.callbacks.model_checkpoint
        if module == "pytorch_lightning.callbacks.model_checkpoint" and name == 'ModelCheckpoint':
            import pytorch_lightning.callbacks.model_checkpoint
            return pytorch_lightning.callbacks.model_checkpoint.ModelCheckpoint
        if module == "__builtin__" and name == 'set':
            return set

        # Forbid everything else.
        raise Exception(f"global '{module}/{name}' is forbidden")