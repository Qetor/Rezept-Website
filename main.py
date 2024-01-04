import os, magic
from flask import Flask, jsonify, render_template, send_from_directory, request, url_for, redirect, Blueprint
from dotenv import load_dotenv

load_dotenv()
RECIPE_DIR = os.getenv('RECIPE_DIR')
SUBPATH = os.getenv('SUBPATH')

if not os.path.exists(RECIPE_DIR):
    os.mkdir(RECIPE_DIR)

main = Blueprint('main', __name__, template_folder='templates', static_folder='static', static_url_path='assets')

def get_recipes_list():
    recipes = []
    
    for filename in os.listdir(RECIPE_DIR):
        recipes.append(filename)

    recipes.sort()

    return recipes

@main.route('/')
def root():
    recipes = get_recipes_list()
    return render_template("index.html", recipes=recipes)

@main.route('/search')
def search():
    query = request.args['q']
    
    lower_query = query.lower()

    recipes = [recipe.lower() for recipe in get_recipes_list() if lower_query in recipe]
    
    return render_template("index.html", recipes=recipes, query=query)

@main.route('/bye')
def bye_bye():
    return jsonify({"message": "cya"})

@main.route('/new', methods=["POST", "GET"])
def new_recipe():
    if request.method == "GET":
        return render_template("create.html")
    
    file = request.files.get('image')
    if not file:
        return jsonify({"message": "No file provided!"})
    
    file.save(os.path.join(RECIPE_DIR, request.form['title']))

    return redirect(url_for("root"), 302)
    

@main.route('/delete/<name>')
def delete_recipe(name):
    filepath = os.path.join(RECIPE_DIR, name)
    os.remove(filepath)

    return redirect(url_for("root"), 302)

@main.route('/recipe/<name>')
def get_recipe(name):
    filepath = os.path.join(RECIPE_DIR, name)
    if not os.path.exists(filepath):
        return jsonify({"message": "Recipe doesn't exist!"})

    return render_template("recipe.html", name=name)

@main.route('/files/<name>')
def download_file(name):
    mime = magic.from_file(os.path.join(RECIPE_DIR, name), mime=True)
    return send_from_directory(RECIPE_DIR, name), {'Content-Type': mime}

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = RECIPE_DIR
app.register_blueprint(main, url_prefix=SUBPATH)
 
if __name__ == '__main__':
    app.run(port=8080)

