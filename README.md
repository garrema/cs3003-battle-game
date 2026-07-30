# CS3003 Battle Game

A turn-based battle game built in Python for CS3003 (Programming Languages,
Summer 2026). The project demonstrates two paradigm concepts from the
course: **object-oriented design** (character class hierarchy) and
**coroutines** (the turn loop, implemented as a Python generator).

## How to Run

Requires Python 3.8+.

```bash
python3 main.py
```

You'll be prompted to choose a class (Warrior, Mage, or Rogue) and a name
for both the player and the enemy, then the battle plays out turn by turn
in the terminal.

## Project Structure

```
battle-game/
├── characters.py   # Character class hierarchy (OOP)
├── moves.py        # Move functions and StatusEffect class
├── battle.py        # Coroutine-based turn loop (generator)
├── main.py         # CLI entry point
└── README.md
```

## Design Decisions & Course Connections

### Object-Oriented Programming (`characters.py`)

- `Character` is a base class holding shared state (HP, attack, defense,
  speed, status effects) and shared behavior (`take_damage`, `heal`,
  `apply_status_effects`).
- `Warrior`, `Mage`, and `Rogue` **inherit** from `Character` and each
  define their own move set in their constructor, this is **polymorphism**:
  the battle loop calls `actor.moves` and `move(actor, target)` without
  needing to know which subclass it's dealing with.
- HP/stat mutation happens only through methods (`take_damage`, `heal`),
  not by reaching in and setting `self.hp` directly from outside the
  class, a simple form of **encapsulation**.

### Coroutines (`battle.py`)

This is the core paradigm showcase. `battle_loop()` is a Python generator
(a function containing `yield`), which acts as a coroutine: it can pause
mid-execution, hand control back to the caller, and resume later exactly
where it left off with all of its local variables (whose turn it is,
current round, etc.) preserved automatically.

This matters because it changes *how* the control flow is expressed:

- **Without coroutines** (e.g., in C), interleaving "player does something,
  wait for input, enemy does something automatically" would typically
  require an explicit state machine, a variable tracking the current
  phase, checked with `switch`/`if` statements scattered across the game
  loop, with all "waiting" state manually saved into structs.
- **With coroutines**, `battle_loop()` is written as a single, linear
  function that reads top-to-bottom like the actual sequence of events in
  a battle. The `yield` statement is the only concession to the fact that
  execution is actually suspended and resumed across multiple calls from
  `main.py`.

`main.py` drives the generator using `next()` to advance automatically
(e.g., after the enemy's AI turn) and `.send(move_index)` to resume the
generator *with a value* when the player has chosen a move and this is what
makes it a true two-way coroutine rather than a simple generator that only
produces values.

### Status Effects

Poison and Stun (in `moves.py`) are implemented as objects with a
`duration` and a `tick()` method, applied at the start of each turn via
`Character.apply_status_effects()`. This shows the turn loop handling
state that persists *across* multiple yields/resumes, a good example of
why preserving local state automatically (a coroutine's core feature) is
useful here.

## Challenges Encountered

- Getting `.send()` semantics right took some trial and error as the first
  value sent into a freshly-started generator is discarded, so the
  generator has to be "primed" with an initial `next()` call before you
  can `.send()` anything meaningful into it.
- Balancing turn order by speed while also supporting stun (which can
  skip a turn entirely) required checking `is_alive()` and re-checking
  status effects at multiple points in the loop, rather than assuming a
  fixed two-actions-per-round structure.

## Possible Extensions

- Multiplayer (network) support
- Enemy AI that's minimax-style instead of random
- A party system (more than one character per side, turn order by speed
  across the whole party)
- Persisting battle history/logs to a file

## Author

Monish Siddardha garre
