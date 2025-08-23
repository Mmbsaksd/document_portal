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
def generate_session_id(prefix: str = "session")-> str:
    ist = ZoneInfo("Asia/Kolkata")
    return f"{prefix}_{datetime.now(ist).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

def save_uploaded_files(uploaded_files:Iterable, target_dir:Path)->List[Path]:
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        saved:List[Path] = []

        for uf in uploaded_files:
            name = getattr(uf,"name","file")
            ext = Path(name).suffix.lower()
            if ext not in SUPPORT_EXTENTIONS:
                log.warning("Unsupported file skipped", filename=name)
                continue
            safe_name = re.sub(r'[^a-zA-Z0-9_\-]','_', Path(name).stem).lower()
            fname = f"{safe_name}_{uuid.uuid4().hex[:6]}{ext}"
            fname = f"{uuid.uuid4().hex[:8]}{ext}"
            out = target_dir/fname
            with open(out,"wb") as f:
                if hasattr(uf,"read"):
                    f.write(uf.read())

                else:
                    f.write(uf.getbuffer())
            saved.append(out)
            log.info("File saved for the ingestion", uploaded = name, asved_as = str(out))
        return saved
    except Exception as e:
        log.error("Failed to save uploaded files", error=str(e), dir=str(target_dir))
        raise DocumentPortalExeption("Failed to save uploaded files", e) from e
