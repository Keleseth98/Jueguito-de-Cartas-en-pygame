class EnemyFactory:
    def __init__(self, card_factory, enemy_db):
        self.card_factory = card_factory
        self.enemy_db = enemy_db

    def create(self, enemy_id):
        data = self.enemy_db.get(enemy_id)

        # Crear deck
        deck = [
            self.card_factory.create(card_id)
            for card_id in data["deck"]
        ]

        from core.character import Character

        # 🔥 FIX: pasar image_path desde el JSON para que el enemigo
        # use su imagen propia en vez de assets/heroes/enemy.png genérico
        enemy = Character(
            name=data["name"],
            deck=deck,
            is_player=False,
            image_path=data.get("image")
        )

        # starting_hp del JSON puede diferir de 5 si en el futuro se quiere customizar
        # pero con el sistema actual todos empiezan en 5 y escalan por turnos
        if "starting_hp" in data:
            enemy.hp = data["starting_hp"]
            enemy.max_hp = data["starting_hp"]

        return enemy, data
