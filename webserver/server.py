
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python3 server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@34.74.246.148/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@34.74.246.148/proj1part2"
#
DATABASEURI = "postgresql://njd2135:9081@34.74.246.148/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: https://flask.palletsprojects.com/en/2.0.x/quickstart/?highlight=routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  return render_template("index.html")
@app.route('/index')
def indexProper():
  return render_template("index.html")


#

# This is an example of a different path.  You can see it at:

# 

#     localhost:8111/another

#

# Notice that the function name is another() rather than index()

# The functions for each app.route need to have different names

#
@app.route('/fishStuff')

def fishStuff():

  return render_template("fishStuff.html", )



@app.route('/another')

def another():

    return render_template("another.html")



# Example of adding new data to the database

@app.route('/add', methods=['POST'])

def add():

  name = request.form['name']

  g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)

  return redirect('/')





@app.route('/add_friend', methods=['POST'])

def add_friend():

    fssn = request.form['personal_fssn']

    friend_fssn = request.form['friend_fssn']
    try:
      g.conn.execute("INSERT INTO friend_to(fssn, fssn_friend) VALUES (%s, %s), (%s, %s)", fssn, friend_fssn, friend_fssn, fssn)
    except: 
      context = dict(friending_message = "Improper message")
      return render_template("suggestedFriends.html", **context)
    context = dict(friending_message = "successfully friended!")
    return render_template("suggestedFriends.html", **context)



@app.route('/view_fish_profile', methods=['POST'])

def view_fish_profile():
  fssn =  request.form['name']


  try:
    cursor = g.conn.execute("SELECT f.name FROM fish f WHERE f. fssn='" + str(fssn) + "'")
  except:
    return render_template('badInput.html')
  account_name = ''
  
  for result in cursor:

    account_name = result['name']

  cursor.close()


  cursor = g.conn.execute("SELECT f2.name FROM fish f1, fish f2, friend_to ft WHERE f1.fssn = '" + str(fssn) +"' AND ft.fssn = f1.fssn AND f2.fssn = ft.fssn_friend")

  friend_names = []

  for result in cursor:

    friend_names.append(result['name'])  # can also be accessed using result[0]

  cursor.close()


  cursor = g.conn.execute("SELECT f2.name FROM fish f1, fish f2, family_to ft WHERE f1.fssn = '" + str(fssn) +"' AND ft.fssn = f1.fssn AND f2.fssn = ft.fssn_family")

  family_names = []

  for result in cursor:

    family_names.append(result['name'])  # can also be accessed using result[0]

  cursor.close()

  predator_names = []
  cursor = g.conn.execute("SELECT f2.name FROM fish f1, fish f2, eaten_by pt WHERE f1.fssn = '" + str(fssn) +"' AND pt.fssn_prey = f1.fssn AND f2.fssn = pt.fssn_predator")

  for result in cursor:

    predator_names.append(result['name'])  # can also be accessed using result[0]

    cursor.close()
    

  

  cursor = g.conn.execute("SELECT f2.name FROM fish f1, fish f2, eaten_by pt WHERE f1.fssn = '" + str(fssn) +"' AND pt.fssn_predator = f1.fssn AND f2.fssn = pt.fssn_prey")

  prey_names = []

  for result in cursor:

    prey_names.append(result['name'])  # can also be accessed using result[0]

  cursor.close()

  

  cursor = g.conn.execute("SELECT f2.name FROM fish f1, fish f2, acquaintance_to acqt WHERE f1.fssn = '" + str(fssn) +"' AND acqt.fssn = f1.fssn AND f2.fssn = acqt.fssn_acquaintance")

  acquaintance_names = []

  for result in cursor:

    acquaintance_names.append(result['name'])

  cursor.close()


  cursor = g.conn.execute("SELECT o.name FROM fish f, owner o, belongs_to bt WHERE f.fssn = '" + str(fssn) +"' AND bt.ssn = o.ssn AND f.fssn = bt.fssn")

  owner_names = []

  for result in cursor:

    owner_names.append(result['name'])

  cursor.close()
  





  cursor = g.conn.execute("SELECT o.type FROM origin o, fish f WHERE f.fssn = '" + str(fssn) +"' AND o.origin_id = f.origin_id")

  origin_names = []

  for result in cursor:

    origin_names.append(result['type'])

  cursor.close()





  cursor = g.conn.execute("SELECT li.tank_id, li.aq_id FROM lives_in li WHERE li.fssn = '" + str(fssn) +"'")

  tank_name = ''

  aquarium_id = '' 

  for result in cursor:

    tank_name = result['tank_id']

    aquarium_id = result['aq_id']

  cursor.close()


  cursor = g.conn.execute("SELECT a.address, a.city, a.state_province, a.country, a.zip FROM aquarium a WHERE a.aq_id = '" + str(aquarium_id) +"'")

  address = ''

  city = ''

  state_province = ''

  country = ''

  ZIP = ''

  for result in cursor:

    address = result['address']

    city = result['city']

    state_province = result['state_province']

    country = result['country']

    ZIP = result['zip']

  aquarium_name = address + ", " + city + ", " + state_province + ", " + country + ", " + str(ZIP)

  cursor.close()



  context = dict(account_name = account_name, friend_data = friend_names, family_data = family_names, predator_data = predator_names, acquaintance_data =  acquaintance_names, owner_data = owner_names, origin_data = origin_names, prey_data = prey_names, aquarium_data = aquarium_name, tank_data = tank_name)




  return render_template("fishInfo.html", **context)

@app.route('/addressDirectory')
def addressDirectory():
  return render_template("addressDirectory.html")

@app.route('/address_directory', methods=['POST'])
def view_fish_directory():

  warning_message = ""
  name = ""
  street_address = ""
  city = ""
  state_province = ""
  country = ""
  zip_code = ""


  fssn = request.form['fssn']
  try:
    cursor = g.conn.execute("SELECT F.name, A.address, A.city, A.state_province, A.country, A.zip FROM fish F, lives_in L, aquarium A WHERE F.fssn = '" + str(fssn) + "' AND F.fssn = L.fssn AND L.aq_id = A.aq_id")
  except:
    return render_template("badInput.html")

  for result in cursor:
    name = result['name']
    street_address = result['address']
    city = result['city']
    state_province = result['state_province']
    country = result['country']
    zip_code = result['zip']

  cursor.close()
  context = dict(warning_message=warning_message, name=name, street_address=street_address, city=city, state_province=state_province, country=country, zip_code=zip_code)

  return render_template("addressDirectory.html", **context)

@app.route('/bestOwners')
def bestOwners():
  return render_template("bestOwners.html")

@app.route('/best_owners_in_country', methods=['POST'])
def view_best_owners_in_country():
  country = request.form['country']
  try:
    cursor = g.conn.execute("SELECT O.name FROM owner O, belongs_to B, lives_in L, aquarium A WHERE O.ssn = B.ssn AND B.fssn = L.fssn AND L.aq_id = A.aq_id AND A.country = '" + str(country) +"' AND O.rating > (SELECT AVG(O.rating) FROM owner O, belongs_to B, lives_in L, aquarium A WHERE O.ssn = B.ssn AND B.fssn = L.fssn AND L.aq_id = A.aq_id AND A.country = '" + str(country) +"' )")
  except:
    return render_template("badInput.html")
  owner_names = []
  for result in cursor:
    owner_names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()
  context = dict(owner_names=owner_names)

  return render_template("bestOwners.html", **context)

@app.route('/tanksInSameAquarium')
def tanksInSameAquarium():
  return render_template("tanksinSameAquarium.html")

@app.route('/tanks_in_same_aquarium', methods=['POST'])
def view_tanks_in_same_aquarium():
  fssn = request.form['fssn']
  try:
    cursor = g.conn.execute("SELECT DISTINCT T.tank_id, T.fish_count, T.size, T.rating FROM lives_in L, tank_exists_in T, fish F WHERE F.fssn = '" + str(fssn) + "' AND F.fssn = L.fssn AND L.aq_id = T.aq_id")
  except:
    return render_template("badInput.html")
  tanks = []
  for result in cursor:
    tanks.append(result)
  cursor.close()
  context = dict(tanks=tanks)

  return render_template("tanksInSameAquarium.html", **context)

@app.route('/suggestedFriends')
def suggestedFriends():
  return render_template("suggestedFriends.html")

@app.route('/suggested_friends', methods=['POST'])
def view_suggested_friends():
    fssn = request.form['fssn']
    try:
      cursor = g.conn.execute("SELECT F2.fssn_friend FROM friend_to F1, friend_to F2 WHERE F1.fssn = '" + str(fssn) +"' AND F1.fssn_friend = F2.fssn EXCEPT SELECT F1.fssn_friend FROM friend_to F1 WHERE F1.fssn = '" + str(fssn) +"'")
    except:
      return render_template("badInput.html")
    
    suggested_friends = []
    
    for result in cursor:
      suggested_friends.append(result['fssn_friend'])  # can also be accessed using result[0]
    cursor.close()
    context = dict(suggested_friends = suggested_friends)

    return render_template("suggestedFriends.html", **context)


if __name__ == "__main__":

  import click



  @click.command()

  @click.option('--debug', is_flag=True)

  @click.option('--threaded', is_flag=True)

  @click.argument('HOST', default='0.0.0.0')

  @click.argument('PORT', default=8111, type=int)

  def run(debug, threaded, host, port):

    """

    This function handles command line parameters.

    Run the server using:



        python3 server.py



    Show the help text using:



        python3 server.py --help



    """



    HOST, PORT = host, port

    print("running on %s:%d" % (HOST, PORT))

    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)



  run()
