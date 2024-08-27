from __future__ import annotations

import configparser
import dataclasses
import os
import threading
import re

from multi_threading.modules import shared, errors