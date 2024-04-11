from fastapi import FastAPI, HTTPException
from chess_board import Board
from database import create_game, make_move, end_game, get_game, get_initial_board
from models import MoveRequest

app = FastAPI()

@app.post("/start_game/")
def start_game():
    game_id = create_game()
    return {"message": "Game started", "game_id": game_id}

@app.post("/move/")
def move(move: MoveRequest):
    game = get_game(move.game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    if game["current_player"] != move.player:
        raise HTTPException(status_code=400, detail="It's not your turn")

    board = Board()
    if not board.is_valid_move(move.start, move.end):
        raise HTTPException(status_code=400, detail="Invalid move")

    board.move_piece(move.start, move.end)
    updated_game = make_move(move.game_id, "black" if game["current_player"] == "white" else "white")
    return {"message": "Move made", "game_id": move.game_id, "current_player": updated_game["current_player"]}

@app.post("/end_game/")
def end_game(game_id: int):
    end_game(game_id)
    return {"message": "Game ended"}

@app.get("/get_board/{game_id}")
def get_board(game_id: int):
    game = get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    board = Board()
    serialized_board = board.serialize_board()
    return serialized_board

@app.get("/initial_board/")
def get_initial_board():
    initial_board = get_initial_board()
    return initial_board

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    print('Hi')
    uvicorn.run(app, host="localhost", port=3000)
