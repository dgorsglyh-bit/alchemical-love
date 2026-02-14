# main.py
"""
Heart Alchemist (Алхимик Сердец)
A Valentine's Day themed text-quest and alchemy simulator.
"""
import os
from inventory import Inventory
from alchemy_lab import AlchemyLab
from world import World

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    inventory = Inventory()
    lab = AlchemyLab(inventory)
    world = World(inventory)
    
    print("****************************************")
    print("*         HEART ALCHEMIST              *")
    print("*       (Алхимик Сердец)               *")
    print("****************************************")
    print("\nWelcome, Apprentice Alchemist.")
    print("Your goal is to create the potion of 'True Love'.")
    print("Explore the world, collect ingredients, and mix them in your workshop.")
    input("\nPress Enter to begin...")

    while True:
        clear_screen()
        world.describe_location()
        
        print("\n--- Actions ---")
        print("1. Talk to someone")
        print("2. Move to another location")
        print("3. Open Inventory")
        if world.current_location_id == "workshop":
            print("4. Use Alchemy Lab")
        print("Q. Quit Game")
        
        choice = input("\nWhat will you do? ").upper().strip()
        
        if choice == "1":
            world.interact()
            input("\nPress Enter to continue...")
        
        elif choice == "2":
            print("\nWhere do you want to go?")
            loc = world.get_current_location()
            for i, conn in enumerate(loc["connections"], 1):
                from data import LOCATIONS
                print(f"{i}. {LOCATIONS[conn]['name']} ({conn})")
            
            dest = input("Enter destination ID: ").lower().strip()
            world.move(dest)
            input("\nPress Enter to continue...")

        elif choice == "3":
            inventory.display()
            input("\nPress Enter to continue...")

        elif choice == "4" and world.current_location_id == "workshop":
            result = lab.mix()
            if result == "True Love":
                print("\n****************************************")
                print("*       CONGRATULATIONS!               *")
                print("*    You have found True Love!         *")
                print("****************************************")
                print("\nYou have completed your apprenticeship.")
                input("\nPress Enter to end the game...")
                break
            input("\nPress Enter to continue...")

        elif choice == "Q":
            print("\nThanks for playing!")
            break
        
        else:
            print("\nInvalid action.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
