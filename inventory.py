# inventory.py

class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self, item_name):
        if item_name in self.items:
            self.items[item_name] += 1
        else:
            self.items[item_name] = 1
        print(f"\n[+] Added to inventory: {item_name}")

    def remove_item(self, item_name):
        if item_name in self.items and self.items[item_name] > 0:
            self.items[item_name] -= 1
            if self.items[item_name] == 0:
                del self.items[item_name]
            return True
        return False

    def display(self):
        print("\n--- Your Inventory ---")
        if not self.items:
            print("Empty.")
        else:
            for item, count in self.items.items():
                print(f"- {item}: x{count}")
        print("----------------------")

    def has_ingredients(self, required_list):
        # Creates a copy of current inventory to check
        temp_inv = self.items.copy()
        for item in required_list:
            if item in temp_inv and temp_inv[item] > 0:
                temp_inv[item] -= 1
            else:
                return False
        return True

    def consume_ingredients(self, required_list):
        for item in required_list:
            self.remove_item(item)
