"""
battle.py

This is the core "paradigm showcase" of the project: a coroutine-based
turn loop, implemented as a Python generator.

Why a generator/coroutine here?
--------------------------------
In an imperative language without coroutine support (e.g. plain C), you'd
typically model "wait for the player, then resume the fight logic" using
an explicit state machine: a variable tracking whose turn it is, a switch
statement, and manual bookkeeping of what happens next. It works, but the
control flow is scattered and harder to follow.

A Python generator lets us write the battle as a single, linear function
that reads top-to-bottom like a story ("player acts, then enemy acts,
then check if anyone died, repeat") even though execution is actually
suspended and resumed across multiple calls from main.py. The `yield`
statement pauses the function and hands control back to the caller,
preserving all local state (whose turn, current HP, etc.) automatically --
we don't have to store any of that ourselves.

This function is a generator (a coroutine, in the loose Python sense)
because it contains `yield`. Each call to `next()` or `.send()` resumes it
exactly where it left off.
"""


def battle_loop(player, enemy):
    """
    A generator that drives a full battle between `player` and `enemy`.

    It yields a dict describing what just happened after every action so
    the caller (main.py) can display it, and expects to be sent the index
    of the move to use via `.send(move_index)` whenever it's a turn that
    requires a choice (only the player's turn requires outside input;
    the enemy chooses its own move automatically).
    """
    turn_count = 0

    yield {"type": "battle_start", "message": f"{player.name} vs {enemy.name}!"}

    while player.is_alive() and enemy.is_alive():
        turn_count += 1

        # Determine turn order by speed each round (faster character goes first)
        if player.speed >= enemy.speed:
            order = [(player, enemy, True), (enemy, player, False)]
        else:
            order = [(enemy, player, False), (player, enemy, True)]

        for actor, target, is_player in order:
            if not actor.is_alive() or not target.is_alive():
                continue

            # Apply status effects (poison, stun, etc.) at the start of the turn
            status_messages, skip_turn = actor.apply_status_effects()
            for msg in status_messages:
                yield {"type": "status", "message": msg}

            if not actor.is_alive():
                break

            if skip_turn:
                yield {"type": "turn_skipped", "message": f"{actor.name}'s turn is skipped."}
                continue

            if is_player:
                # Pause here and wait for the caller to send a move index
                move_index = yield {
                    "type": "player_turn",
                    "message": f"{actor.name}'s turn. Choose a move.",
                    "moves": [m.__name__ for m in actor.moves],
                }
                move = actor.moves[move_index]
            else:
                # Very simple AI: pick a random move
                import random
                move = random.choice(actor.moves)

            result_message = move(actor, target)
            yield {
                "type": "action_result",
                "message": result_message,
                "actor_hp": actor.hp,
                "target_hp": target.hp,
            }

            if not target.is_alive():
                break

    winner = player if player.is_alive() else enemy
    yield {"type": "battle_over", "message": f"{winner.name} wins the battle!", "winner": winner.name}
