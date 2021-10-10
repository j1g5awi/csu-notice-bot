import json
from pathlib import Path
from typing import Any, Dict, List

from pydantic import BaseModel, Field


class Filter(BaseModel):
    from_: List[str] = Field(alias="from")
    keyword: List[str]


class Group(BaseModel):
    subscribe: List[str]
    limit: int
    filter: Filter
    filter_out: Filter


class Config(BaseModel):
    _path: Path = Path() / "data" / "csu_notice" / "config.json"
    api_server: str = ""
    tag: Dict[str, int] = {"main": 0, "cse": 0}
    group: Dict[str, Group] = {}

    def __init__(self, **data: Any) -> None:
        if self._path.exists():
            super().__init__(**json.load(self._path.open("r", encoding="utf-8")))
            assert self.api_server
        else:
            super().__init__()
            self.dump()

    def dump(self):
        self._path.parent.mkdir(parents=True, exist_ok=True)
        json.dump(
            self.dict(by_alias=True),
            self._path.open("w", encoding="utf-8"),
            ensure_ascii=False,
            indent=4,
        )


_config = Config()
