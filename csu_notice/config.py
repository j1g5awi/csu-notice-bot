import json
from pathlib import Path
from typing import Any, Dict, List

from pydantic import BaseModel


class Tag(BaseModel):
    enabled_group: List[int] = []
    latest_head: int = 0


class Config(BaseModel):
    _path: Path = Path() / "data" / "csu_notice" / "config.json"
    api_server: str
    tags: Dict[str, Tag] = {"main": Tag(), "cse": Tag()}

    def __init__(__pydantic_self__, **data: Any) -> None:
        if __pydantic_self__._path.exists():
            super().__init__(
                **json.load(__pydantic_self__._path.open("r", encoding="utf-8"))
            )
            assert __pydantic_self__.api_server
        else:
            super().__init__()
            __pydantic_self__.dump()

    def dump(self):
        self._path.parent.mkdir(parents=True, exist_ok=True)
        json.dump(
            self.dict(),
            self._path.open("w", encoding="utf-8"),
            indent=4,
        )


_config = Config()
