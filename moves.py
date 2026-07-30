"""
moves.py

Defines the moves each character can use, plus a StatusEffect class
for lingering effects like poison or stun.

Design note: moves are implemented as plain functions that take
(actor, target) and return a message string describing what happened.
This is a light touch of the functional paradigm layered on top of the
OOP character system -- moves don't hold state themselves, they just
transform the actor/target based on their arguments.
"""

import random


class StatusEffect:
    """A status effect applied to a character, e.g. poison or stun."""

    def __init__(self, name, duration, on_tick=None):
        self.name = name
        self.duration = duration
        # on_tick is a function(character) -> message string, applied each turn
        self.on_tick = on_tick

    def tick(self, character):
        self.duration -= 1
        skip_turn = False
        message = f"{character.name} is affected by {self.name}."

        if self.name == "Poison":
            dmg = 5
            character.hp = max(0, character.hp - dmg)
            message = f"{character.name} takes {dmg} poison damage."
        elif self.name == "Stun":
            skip_turn = True
            message = f"{character.name} is stunned and can't move!"

        return {"message": message, "skip_turn": skip_turn}


# ---------------------------------------------------------------------------
# Warrior moves
# ---------------------------------------------------------------------------

def slash(actor, target):
    dmg = target.take_damage(actor.attack)
    return f"{actor.name} slashes {target.name} for {dmg} damage."


def power_strike(actor, target):
    dmg = target.take_damage(int(actor.attack * 1.5))
    return f"{actor.name} unleashes a Power Strike on {target.name} for {dmg} damage!"


def defend(actor, target):
    actor.defense += 5
    return f"{actor.name} braces and raises their defense."
    
def berserk(actor, target):
    self_damage = int(actor.max_hp * 0.1)
    actor.hp = max(1, actor.hp - self_damage)
    dmg = target.take_damage(int(actor.attack * 2))
    return f"{actor.name} goes berserk, dealing {dmg} damage but taking {self_damage} recoil damage!"


# ---------------------------------------------------------------------------
# Mage moves
# ---------------------------------------------------------------------------

def fireball(actor, target):
    dmg = target.take_damage(actor.attack)
    return f"{actor.name} hurls a fireball at {target.name} for {dmg} damage!"


def heal_spell(actor, target):
    healed = actor.heal(15)
    return f"{actor.name} casts a healing spell, restoring {healed} HP."


def poison_bolt(actor, target):
    dmg = target.take_damage(int(actor.attack * 0.6))
    target.add_status_effect(StatusEffect("Poison", duration=3))
    return f"{actor.name} hits {target.name} with a Poison Bolt for {dmg} damage and poisons them!"


# ---------------------------------------------------------------------------
# Rogue moves
# ---------------------------------------------------------------------------

def stab(actor, target):
    dmg = target.take_damage(actor.attack)
    return f"{actor.name} stabs {target.name} for {dmg} damage."


def quick_strike(actor, target):
    dmg = target.take_damage(int(actor.attack * 0.7))
    return f"{actor.name} lands a Quick Strike on {target.name} for {dmg} damage."


def stunning_blow(actor, target):
    dmg = target.take_damage(int(actor.attack * 0.5))
    if random.random() < 0.5:
        target.add_status_effect(StatusEffect("Stun", duration=1))
        return f"{actor.name} stuns {target.name} with a blow for {dmg} damage!"
    return f"{actor.name} strikes {target.name} for {dmg} damage, but they resist the stun."
