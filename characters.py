"""
characters.py

Defines the Character class hierarchy for the battle game.
This is the Object-Oriented layer of the project:
    - Encapsulation: stats are stored as instance attributes and modified
      through methods rather than being freely manipulated elsewhere.
    - Inheritance: Warrior and Mage both inherit shared behavior from
      the Character base class.
    - Polymorphism: each subclass defines its own list of moves and can
      override methods (like take_damage) if it needs special behavior.
"""


class Character:
    """Base class for any creature/player that can fight in a battle."""

    def __init__(self, name, hp, attack, defense, speed):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.status_effects = []  # list of StatusEffect objects (see moves.py)
        self.moves = []  # filled in by subclasses

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        """Reduce HP by amount, factoring in defense. Never drops below 0."""
        actual_damage = max(1, amount - self.defense)  # always deal at least 1
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage

    def heal(self, amount):
        """Restore HP, capped at max_hp."""
        healed = min(amount, self.max_hp - self.hp)
        self.hp += healed
        return healed

    def apply_status_effects(self):
        """
        Called at the start of each of this character's turns.
        Applies (and ticks down) any active status effects like poison or stun.
        Returns a list of message strings describing what happened, and
        a bool indicating whether this character's turn should be skipped
        (e.g., if stunned).
        """
        messages = []
        skip_turn = False
        remaining_effects = []

        for effect in self.status_effects:
            result = effect.tick(self)
            messages.append(result["message"])
            if result.get("skip_turn"):
                skip_turn = True
            if effect.duration > 0:
                remaining_effects.append(effect)

        self.status_effects = remaining_effects
        return messages, skip_turn

    def add_status_effect(self, effect):
        self.status_effects.append(effect)

    def __str__(self):
        return f"{self.name} (HP: {self.hp}/{self.max_hp})"


class Warrior(Character):
    """A tanky melee fighter: high attack/defense, low speed."""

    def __init__(self, name):
        super().__init__(name, hp=120, attack=18, defense=8, speed=5)
        # Import here to avoid circular imports between characters.py and moves.py
        from moves import slash, power_strike, defend, berserk

        self.moves = [slash, power_strike, defend, berserk]

class Mage(Character):
    """A fragile spellcaster: high attack via magic, low defense, high speed."""

    def __init__(self, name):
        super().__init__(name, hp=80, attack=22, defense=3, speed=9)
        from moves import fireball, heal_spell, poison_bolt

        self.moves = [fireball, heal_spell, poison_bolt]


class Rogue(Character):
    """A fast, evasive attacker with a stun move. Optional third class."""

    def __init__(self, name):
        super().__init__(name, hp=90, attack=16, defense=5, speed=14)
        from moves import stab, quick_strike, stunning_blow

        self.moves = [stab, quick_strike, stunning_blow]

class Cleric(Character):
    """A support-focused healer: strong healing, low attack, moderate defense."""

    def __init__(self, name):
        super().__init__(name, hp=100, attack=10, defense=6, speed=7)
        from moves import smite, greater_heal, blessing

        self.moves = [smite, greater_heal, blessing]
