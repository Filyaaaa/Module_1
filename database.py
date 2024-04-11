import aiomysql

# MySQL connection details
DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "chess_games"

async def get_connection():
    return await aiomysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME
    )

async def create_game():
    async with get_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("INSERT INTO games (current_player) VALUES ('white')")
            await conn.commit()
            game_id = cursor.lastrowid
    return game_id

async def make_move(game_id, current_player):
    async with get_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("UPDATE games SET current_player = %s WHERE id = %s", (current_player, game_id))
            await conn.commit()
    return {"current_player": current_player}

async def end_game(game_id):
    async with get_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("DELETE FROM games WHERE id = %s", (game_id,))
            await conn.commit()

async def get_game(game_id):
    async with get_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT id, current_player FROM games WHERE id = %s", (game_id,))
            result = await cursor.fetchone()
    if result:
        return {"id": result[0], "current_player": result[1]}
    else:
        return None

def get_initial_board():
    return [
        ['7 ', '7♜', '7♞', '7♝', '7♛', '7♚', '7♝', '7♞', '7♜'],
        ['6♟', '6♟', '6♟', '6♟', '6♟', '6♟', '6♟', '6♟'],
        [' 0', ' 1', ' 2', ' 3', ' 4', ' 5', ' 6', ' 7'],
    ]
