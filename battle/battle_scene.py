

ENCOUNTER_TOWN_SLIMES = [
    {"name": "Slime",  "hp": 80,  "atk": 10, "def": 3,  "exp": 20, "gold": 5},
    {"name": "Slime",  "hp": 80,  "atk": 10, "def": 3,  "exp": 20, "gold": 5},
    {"name": "Slime",  "hp": 80,  "atk": 10, "def": 3,  "exp": 20, "gold": 5},
]

ENCOUNTER_FOREST_MONSTERS = [
    {"name": "Mushroom", "hp": 120, "atk": 15, "def": 5,  "exp": 35, "gold": 8},
    {"name": "Mushroom", "hp": 120, "atk": 15, "def": 5,  "exp": 35, "gold": 8},
]

ENCOUNTER_RUINS_TRAP = [
    {"name": "Stone Golem", "hp": 200, "atk": 20, "def": 12, "exp": 60, "gold": 15},
    {"name": "Stone Golem", "hp": 200, "atk": 20, "def": 12, "exp": 60, "gold": 15},
    {"name": "Stone Golem", "hp": 200, "atk": 20, "def": 12, "exp": 60, "gold": 15},
]

ENCOUNTER_VILLAGE_MONSTERS = [
    {"name": "Goblin",  "hp": 90,  "atk": 14, "def": 4,  "exp": 30, "gold": 7},
    {"name": "Goblin",  "hp": 90,  "atk": 14, "def": 4,  "exp": 30, "gold": 7},
    {"name": "Goblin",  "hp": 90,  "atk": 14, "def": 4,  "exp": 30, "gold": 7},
    {"name": "Orc",     "hp": 180, "atk": 22, "def": 10, "exp": 70, "gold": 20},
]

ENCOUNTER_CASTLE_DUNGEON = [
    {"name": "Dark Knight", "hp": 250, "atk": 28, "def": 15, "exp": 100, "gold": 30},
    {"name": "Dark Knight", "hp": 250, "atk": 28, "def": 15, "exp": 100, "gold": 30},
]

ENCOUNTER_DEMON_KING = [
    {
        "name": "Demon King",
        "hp": 9999,
        "atk": 80,
        "def": 40,
        "exp": 9999,
        "gold": 0,
        "is_boss": True,
        "phases": 2,
    },
]


def start_battle_scene(game, enemies: list, return_scene_class, context: dict = None):
    raise NotImplementedError(
        "[HINT] start_battle_scene() belum diimplementasi.\n"
        "Buat kelas BattleScene di battle/battle_scene.py, "
        "lalu ganti fungsi ini dengan game.replace_scene(BattleScene(...))."
    )

