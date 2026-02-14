# data.py

INGREDIENTS = {
    "Sincerity": "✨ A pure, glowing crystal of absolute truth.",
    "Communication": "🪶 A soft, humming feather that vibrates when held.",
    "Interest": "⚙️ A small, curious gear that never stops turning.",
    "Humor": "✨ A jar of sparkling dust that makes you want to giggle.",
    "Conflict": "🪨 A jagged, cold stone that occasionally sparks.",
    "Care": "🌸 A warm, velvet-like petal that radiates comfort.",
    "Attention": "🔍 A lens that makes everything look clearer.",
    "Trust": "🔗 A sturdy, unbreakable chain link made of light.",
    "Passion": "🔥 A flickering flame that doesn't burn the hand.",
    "Support": "🛡️ A small, indestructible shield of kindness.",
    "Patience": "⏳ A vial of slow-flowing, golden sand.",
    "Respect": "👑 A crown-shaped seal of mutual recognition."
}

RECIPES = {
    "Strong Friendship": {
        "ingredients": ["Communication", "Communication", "Interest", "Humor"],
        "description": "A stable and reliable bond that stands the test of time."
    },
    "Controversial Partnership": {
        "ingredients": ["Sincerity", "Conflict", "Conflict"],
        "description": "Honest but filled with constant struggles."
    },
    "Stable Bond": {
        "ingredients": ["Trust", "Respect", "Support"],
        "description": "A foundation of mutual strength and kindness."
    },
    "Deep Devotion": {
        "ingredients": ["Care", "Respect", "Patience", "Support"],
        "description": "A love that grows stronger with every passing day."
    },
    "True Love": {
        "ingredients": ["Sincerity", "Care", "Trust", "Attention"],
        "description": "The ultimate elixir. Deep, selfless, and eternal."
    },
    "Stormy Romance": {
        "ingredients": ["Passion", "Conflict", "Humor"],
        "description": "Exciting and volatile. A rollercoaster of emotions."
    }
}

LOCATIONS = {
    "workshop": {
        "name": "Alchemist's Workshop",
        "description": "Your cozy laboratory. Shelves are filled with empty vials and strange apparatuses. One large cauldron sits in the center.",
        "connections": ["market", "park"]
    },
    "market": {
        "name": "Market of Feelings",
        "description": "A bustling plaza where abstract concepts are traded like spices. The air smells of hope and lavender.",
        "connections": ["workshop"]
    },
    "park": {
        "name": "Park of Forgotten Encounters",
        "description": "A quiet, misty park with stone benches and ancient trees. It feels peaceful yet slightly melancholic.",
        "connections": ["workshop"]
    }
}

NPCS = {
    "sage": {
        "name": "Old Sage",
        "location": "workshop",
        "dialogue": "Greetings, apprentice. To find 'True Love', one must look beyond the surface. Care and Trust are the foundation.",
        "quest_item": "Sincerity",
        "quest_hint": "Have you spoken to the Florist yet? They understand 'Care'."
    },
    "florist": {
        "name": "Shy Florist",
        "location": "market",
        "dialogue": "Oh! Hello. These flowers require so much... well, care. Are you here for the festival?",
        "options": {
            "1": "Yes, I'm looking for ingredients.",
            "2": "I just like your flowers."
        }
    },
    "trickster": {
        "name": "Playful Trickster",
        "location": "park",
        "dialogue": "Life is too serious! Don't you think? A bit of Humor—or a little Conflict—keeps things interesting!",
        "puzzle": "I have keys but no locks. I have a space but no room. You can enter, but never leave. What am I?"
    }
}
