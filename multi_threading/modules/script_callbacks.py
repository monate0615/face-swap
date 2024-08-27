from __future__ import annotations

import dataclasses
import inspect
import os
from typing import Optional, Any

from fastapi import FastAPI

from multi_threading.modules import errors, timer