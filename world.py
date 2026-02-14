# world.py
from data import LOCATIONS, NPCS

class World:
    def __init__(self, inventory):
        self.current_location_id = "workshop"
        self.inventory = inventory
        self.flags = {
            "florist_greeted": False,
            "puzzle_solved": False,
            "sage_talked": False
        }

    def get_current_location(self):
        return LOCATIONS[self.current_location_id]

    def move(self, location_id):
        if location_id in self.get_current_location()["connections"]:
            self.current_location_id = location_id
            print(f"\n[MOVING] You walk to the {LOCATIONS[location_id]['name']}.")
            return True
        else:
            print("\nYou can't go there from here.")
            return False

    def interact(self):
        # Find NPC in current location
        npc_id = None
        for nid, data in NPCS.items():
            if data["location"] == self.current_location_id:
                npc_id = nid
                break
        
        if not npc_id:
            print("\nThere's nobody here to talk to.")
            return

        npc = NPCS[npc_id]
        print(f"\n--- {npc['name']} ---")
        
        if npc_id == "sage":
            print(npc["dialogue"])
            if not self.flags["sage_talked"]:
                print(f"The Sage hands you something: {npc['quest_item']}")
                self.inventory.add_item(npc["quest_item"])
                self.flags["sage_talked"] = True
            elif "Care" in self.inventory.items and not "Trust" in self.inventory.items:
                print("\nSage: 'I see you have learned the value of Care. Now, take this 'Trust'. It is the final piece of the foundation.'")
                self.inventory.add_item("Trust")
            else:
                print(f"Hint: {npc['quest_hint']}")

        elif npc_id == "florist":
            print(npc["dialogue"])
            print("1. " + npc["options"]["1"])
            print("2. " + npc["options"]["2"])
            choice = input("\nYour choice (1 or 2): ")
            if choice == "1":
                if not self.flags["florist_greeted"]:
                    print("\nFlorist: 'Oh, an alchemist! Here, take these 'Care' petals and some 'Attention' seeds. They are essential.'")
                    self.inventory.add_item("Care")
                    self.inventory.add_item("Attention")
                    self.flags["florist_greeted"] = True
                else:
                    print("\nFlorist: 'I hope those ingredients help you!'")
            else:
                print("\nFlorist: 'That's very kind of you. Have a lovely day!'")
                self.inventory.add_item("Communication")

        elif npc_id == "trickster":
            print(npc["dialogue"])
            if not self.flags["puzzle_solved"]:
                print(f"\nPuzzle: {npc['puzzle']}")
                answer = input("Your answer: ").lower().strip()
                if answer == "keyboard":
                    print("\nTrickster: 'Correct! You have a quick mind. Take this 'Humor' and a bit of 'Passion'!'")
                    self.inventory.add_item("Humor")
                    self.inventory.add_item("Passion")
                    self.flags["puzzle_solved"] = True
                else:
                    print("\nTrickster: 'Nope! Not even close. Try again later!'")
                    print("He laughs and throws a 'Conflict' stone at you.")
                    self.inventory.add_item("Conflict")
            else:
                print("\nTrickster: 'You already solved my riddle! Go play with your tubes and potions.'")

    def describe_location(self):
        loc = self.get_current_location()
        print(f"\n========================================")
        print(f" LOCATION: {loc['name']}")
        print(f"========================================")
        print(loc["description"])
        
        print("\nYou can see paths leading to:")
        for conn in loc["connections"]:
            print(f"- {LOCATIONS[conn]['name']} ({conn})")
        
        # Check for NPCs
        for nid, data in NPCS.items():
            if data["location"] == self.current_location_id:
                print(f"\n[!] {data['name']} is here.")
