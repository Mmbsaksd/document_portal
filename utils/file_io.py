from __future__ import annotations
import re
import uuid
from pathlib import Path
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from typing import Iterable, List
from logger import GLOBAL_LOGGER as log
from exeption.custom_exeption import DocumentPortalExeption


SUPPORT_EXTENTIONS = {".pdf", ".docx", ".txt"}

# ----------------------------- #
# Helpers (file I/O + loading)  #
# ----------------------------- #