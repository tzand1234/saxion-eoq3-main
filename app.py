import flask, postgresqlite, random
from flask import render_template, request, flash, redirect, url_for, session
import secrets
from model import Player, Location, Quest, Item,  QuestItem ,Inventory, db


app = flask.Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = postgresqlite.get_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex(16)
db.init_app(app)

# Set user_id on request if user is logged in, or else set it to None.
@app.before_request
def check_authentication():
    if "user_id" in session:
        user = session["user_id"]
    else:
        request.user_id = None

@app.before_first_request
def create_tables():
    """Function to create database tables before the first request is handled.

    Note: This function is called only once, before the first request is handled.
    """
    with app.app_context():
        # Create all the tables defined in the database models
        db.create_all()

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("home.html")

@app.route("/create", methods=['GET', 'POST'])
def create_team():
    # If a new customer is being created, handle the POST request
    if request.method == "POST":
        # Get the customer name from the form data
        team_name = request.form.get("team_name")

        # Check if the team_name is already in the system or if it's empty
        team = Player.query.filter_by(team_name=team_name).first()
        team_password = request.form.get("team_password")
        if team:
            if team_password == team.team_password:
                # Redirect to the team_dashboard page after processing the form data
                session['user_id'] = team.id
                return redirect(url_for("team_dashboard", team_name=team_name))
            else:
                # Show an error message if the team password is incorrect
                flash("Invalid team password. Please try again.")
                return render_template("create_team.html")
        else:
            # If the customer name is valid, add a new customer to the database
            new_player = Player(team_name=team_name,team_password=team_password, points=0, items_found=0, quests_completed=0)
            db.session.add(new_player)
            db.session.commit()
            session['user_id'] = new_player.id
        # Redirect to the quest_location.html page after processing the form data
        return redirect(url_for("team_dashboard", team_name=team_name))

    # Show the main page with the list of customers and their invoices, as well as a form to add a new customer
    return render_template("create_team.html")



@app.route("/change_password", methods=['GET', 'POST'])
def change_password():
    # If a password change is being requested, handle the POST request
    if request.method == "POST":
        # Get the team name and new password from the form data
        team_name = request.form.get("team_name")
        new_password = request.form.get("new_password")

        # Find the team with the given name and update its password
        team = Player.query.filter_by(team_name=team_name).first()
        if team:
            if team.team_password == new_password:
                flash("Do not use your old password.")
                return render_template("change_password.html")

            team.team_password = new_password
            db.session.commit()

            # Set the user_id session variable and redirect to team_dashboard
            session['user_id'] = team.id
            return redirect(url_for("team_dashboard", team_name=team_name))
        else:
            # Show an error message if the team name is invalid
            flash("Invalid team name. Please try again.")
            return render_template("change_password.html")

    # Show the change_password.html page with the form to change the team password
    return render_template("change_password.html")

# Sign out user
@app.route("/signout", methods=["GET"])
def signout():
    session.pop('user_id', None)
    return redirect(url_for("index"))


@app.route("/<team_name>/dashboard", methods=['GET', 'POST'])
def team_dashboard(team_name):
    if 'user_id' not in session:
        return redirect('/')
    player = Player.query.filter_by(team_name=team_name).first()
    high_scores = Player.query.order_by(Player.points.asc()).all()

    return render_template("team_dashboard.html", player=player, high_scores=high_scores)

@app.route("/<team_name>/quest", methods=['GET', 'POST'])
def quest(team_name):
    if 'user_id' not in session:
        return redirect('/')
    
    new_quest1 = Quest(title='Twice the Number', reward_points=50, description="I am a number. If you add me to myself, and then add 10, you'll get 30. What number am I?", player_takes_part=False, answer='10', completed=False, photo='dictective.jpg', hint='the suspect has a tattoo on their arm.')

    new_quest2 = Quest(title='What am I?', reward_points=100, description='I am taken from a mine, and shut up in a wooden case, from which I am never released, and yet I am used by almost every person. What am I?', player_takes_part=False, answer='pencil', completed=False, photo='dictective.jpg', hint=" the suspects is a fan of the Assassin's Creed video game series.")

    new_quest3 = Quest(title='Hidden Message', reward_points=75, description='I am a word that starts with a letter "T." I am filled with "T," and end with a letter "T." What am I?', player_takes_part=False, answer='teapot', completed=False, photo='dictective-photo.jpg', hint=' the suspect enjoys going for walks.')

    new_quest4 = Quest(title='The More You Take...', reward_points=100, description='The more you take, the more you leave behind. What am I?', player_takes_part=False, answer='footsteps', completed=False, photo='dictective.jpg', hint='the suspect wears glasses.')

    new_quest5 = Quest(title='Alive Without Breath', reward_points=75, description='I am alive without breath, as cold as death. I am never thirsty, but always drinking. What am I?', player_takes_part=False, answer='fish', completed=False, photo='dictective.jpg', hint='the suspect is a bit of a neat freak and likes to keep his workspace very organized.')

    db.session.add(new_quest1)
    db.session.add(new_quest2)
    db.session.add(new_quest3)
    db.session.add(new_quest4)
    db.session.add(new_quest5)
    db.session.commit()

    quests = Quest.query.all()
    random_quest = random.choice(quests)

    player = Player.query.filter_by(team_name=team_name).first()
    return render_template("quest_location.html", quest=random_quest, player=player)

@app.route("/<team_name>/solve_murder", methods=['GET', 'POST'])
def solve_murder(team_name):
    if 'user_id' not in session:
        return redirect('/')
    return render_template("solve_murder.html", team_name=team_name)

@app.route("/<team_name>/inventory", methods=['GET', 'POST'])
def inventory():
    if 'user_id' not in session:
        return redirect('/')
    return render_template("inventory.html")

@app.route('/directions', methods=['POST'])
def directions():
    origin = request.form['origin']
    destination = request.form['destination']
    url = 'https://maps.googleapis.com/maps/api/directions/json'
    params = {'origin': origin, 'destination': destination, 'key': API_KEY}
    response = requests.get(url, params=params)
    directions = response.json()['routes'][0]['legs'][0]['steps']
    return render_template('directions.html', directions=directions)


# if __name__ == '__main__':
#     app.run(debug=True)