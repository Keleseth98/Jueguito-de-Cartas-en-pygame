import json

class EnemyDatabase:
    def __init__(self, path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.enemies = data.get("enemies", {})

    def get(self, enemy_id):
        enemy = self.enemies.get(enemy_id)

        if enemy is None:
            raise ValueError(f"❌ Enemigo '{enemy_id}' no existe en el JSON")

        return enemy

    def get_all_ids(self):
        return list(self.enemies.keys())