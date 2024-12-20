import postgresqlite, flask, flask_sqlalchemy, datetime

db = flask_sqlalchemy.SQLAlchemy()

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50), nullable=False)
    team_password = db.Column(db.String(50), nullable=False)
    points = db.Column(db.Integer)
    items_found = db.Column(db.Integer)
    quests_completed = db.Column(db.Integer)

    def to_dict(self):
        return {'id': self.id, 'team_name': self.team_name, 'points': self.points, 'items_found': self.items_found, 'quests_completed': self.quests_completed}

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coordinates = db.Column(db.String)
    quest_id = db.Column(db.Integer, db.ForeignKey('quest.id'))

    def to_dict(self):
        return {'id': self.id, 'coordinates': self.coordinates, 'quest_id': self.quest_id}

class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    reward_points = db.Column(db.Integer)
    description = db.Column(db.String)
    player_takes_part = db.Column(db.Boolean)
    answer = db.Column(db.String)
    completed = db.Column(db.Boolean)
    photo = db.Column(db.String)
    hint = db.Column(db.String)


    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'reward_points': self.reward_points, 'description': self.description, 'player_takes_part': self.player_takes_part, 'answer': self.answer, 'completed': self.completed, 'photo': self.photo, 'hint': self.hint}
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    quest_id = db.Column(db.Integer, db.ForeignKey('quest.id'))

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'description': self.description}

class QuestItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quest_id = db.Column(db.Integer, db.ForeignKey('quest.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))

    def to_dict(self):
        return {'id': self.id, 'quest_id': self.quest_id, 'item_id': self.item_id}


class Inventory(db.Model):
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)

    def to_dict(self):
        return {'player_id' : self.player_id, 'item_id' : self.item_id}