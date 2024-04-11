from pydantic import BaseModel
from typing import Tuple

class MoveRequest(BaseModel):
    player: str
    start: Tuple[int, int]
    end: Tuple[int, int]
    game_id: int

class GameResponse(BaseModel):
    id: int
    current_player: str