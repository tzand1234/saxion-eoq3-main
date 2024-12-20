def create_quest(quest_values):
    new_quest = Quest(**quest_values)
    db.session.add(new_quest)
    db.session.commit()
    return new_quest


# Create quests
quest = {'title' : '', 'reward_points': 0, 'description' : '', 'players_takes_part' : False, 'answer': '', 'completed': False, 'photo' : ''}
quest = {'title' : '', 'reward_points': 0, 'description' : '', 'players_takes_part' : False, 'answer': '', 'completed': False, 'photo' : ''}
quest = {'title' : '', 'reward_points': 0, 'description' : '', 'players_takes_part' : False, 'answer': '', 'completed': False, 'photo' : ''}
quest = {'title' : '', 'reward_points': 0, 'description' : '', 'players_takes_part' : False, 'answer': '', 'completed': False, 'photo' : ''}
quest = {'title' : '', 'reward_points': 0, 'description' : '', 'players_takes_part' : False, 'answer': '', 'completed': False, 'photo' : ''}
quest = {'title' : '', 'reward_points': 0, 'description' : '', 'players_takes_part' : False, 'answer': '', 'completed': False, 'photo' : ''}
quest = {'title' : '', 'reward_points': 0, 'description' : '', 'players_takes_part' : False, 'answer': '', 'completed': False, 'photo' : ''}


create_quest(quest1)
create_quest(quest2) #etc...



def create_item(name, description, quest_id):
    new_item = Item(name=name, description=description, quest_id=quest_id)
    db.session.add(new_item)
    db.session.commit()


create_item('', '', 0)
create_item('', '', 0)
create_item('', '', 0)
create_item('', '', 0)
create_item('', '', 0)


def create_location(coordinates, quest_id):
    new_location = Location(coordinates=coordinates, quest_id=quest_id)
    db.session.add(new_location)
    db.session.commit()


create_location("12.345, 67.890", 1)
create_location("12.345, 67.890", 1)
create_location("12.345, 67.890", 1)


