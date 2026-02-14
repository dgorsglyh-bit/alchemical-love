# alchemy_lab.py
from data import RECIPES

class AlchemyLab:
    def __init__(self, inventory):
        self.inventory = inventory

    def mix(self):
        if not self.inventory.items:
            print("\nYou have nothing to mix!")
            return

        print("\n--- Alchemy Lab ---")
        self.inventory.display()
        print("\nAvailable Recipes (partial hints):")
        for name in RECIPES:
            print(f"- {name}")
        
        choice = input("\nWhich potion do you want to attempt to brew? (Enter name or 'cancel'): ").title().strip()
        
        if choice == "Cancel":
            return

        if choice in RECIPES:
            recipe = RECIPES[choice]
            if self.inventory.has_ingredients(recipe['ingredients']):
                print(f"\n[SUCCESS] You carefully mix the ingredients...")
                print(f"You have created: {choice}!")
                print(f"Description: {recipe['description']}")
                self.inventory.consume_ingredients(recipe['ingredients'])
                return choice
            else:
                print(f"\n[FAILURE] You lack the necessary ingredients for {choice}.")
                print(f"Required: {', '.join(recipe['ingredients'])}")
        else:
            print("\nThat doesn't look like a known recipe.")
        
        return None
