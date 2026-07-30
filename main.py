"""
main.py

Command-line entry point. Sets up two characters, drives the battle_loop
generator from battle.py, and handles all user input/output.
"""

from characters import Warrior, Mage, Rogue
from battle import battle_loop


CLASS_OPTIONS = {
    "1": ("Warrior", Warrior),
    "2": ("Mage", Mage),
    "3": ("Rogue", Rogue),
}


def choose_character(prompt_label):
    print(f"\nChoose a class for {prompt_label}:")
    for key, (name, _) in CLASS_OPTIONS.items():
        print(f"  {key}. {name}")

    choice = input("Enter number: ").strip()
    while choice not in CLASS_OPTIONS:
        choice = input("Invalid choice. Enter number: ").strip()

    class_name, class_type = CLASS_OPTIONS[choice]
    char_name = input(f"Name your {class_name}: ").strip() or class_name
    return class_type(char_name)


def choose_move(character):
    print(f"\n{character.name}'s moves:")
    for i, move in enumerate(character.moves):
        print(f"  {i}. {move.__name__.replace('_', ' ').title()}")

    choice = input("Choose a move number: ").strip()
    while not choice.isdigit() or int(choice) not in range(len(character.moves)):
        choice = input("Invalid move. Choose a move number: ").strip()

    return int(choice)


def run_battle(player, enemy):
    gen = battle_loop(player, enemy)

    # Prime the generator and process events until it's exhausted
    event = next(gen)

    while True:
        print(f"\n>> {event['message']}")

        if event["type"] == "battle_over":
            break

        if event["type"] == "player_turn":
            move_index = choose_move(player)
            try:
                event = gen.send(move_index)
            except StopIteration:
                break
        else:
            if event["type"] == "action_result":
                print(f"   ({event['actor_hp']} HP left on actor, {event['target_hp']} HP left on target)")
            try:
                event = next(gen)
            except StopIteration:
                break


def main():
    print("=" * 50)
    print("  CS3003 Battle Game -- Coroutine-Based Turn Loop")
    print("=" * 50)

    player = choose_character("Player")
    enemy = choose_character("Enemy")

    run_battle(player, enemy)

    print("\nThanks for playing!")


if __name__ == "__main__":
    main()
