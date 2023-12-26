# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import os
from flask import Flask, jsonify, render_template, send_from_directory, request, url_for, redirect

recipe_dir = "/home/elian/recipes/"
if not os.path.exists(recipe_dir):
    os.mkdir(recipe_dir)

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = recipe_dir

def get_recipes_list():
    recipes = []
    
    for filename in os.listdir(recipe_dir):
        recipes.append(filename)

    recipes.sort()

    return recipes

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def root():
    recipes = get_recipes_list()
    return render_template("index.html", recipes=recipes)

@app.route('/bye')
def bye_bye():
    return jsonify({"message": "cya"})

@app.route('/new', methods=["POST"])
def new_recipe():
    file = request.files.get('image')
    if not file:
        return jsonify({"message": "No file provided!"})
    
    file.save(os.path.join(recipe_dir, request.form['title']))

    return redirect(url_for("root"), 302)
    

@app.route('/delete/<name>')
def delete_recipe(name):
    filepath = os.path.join(recipe_dir, name)
    os.remove(filepath)

    return redirect(url_for("root"), 302)

@app.route('/recipe/<name>')
def get_recipe(name):
    filepath = os.path.join(recipe_dir, name)
    if not os.path.exists(filepath):
        return jsonify({"message": "Recipe doesn't exist!"})

    return render_template("recipe.html", name=name)

@app.route('/files/<name>')
def download_file(name):
    return send_from_directory(recipe_dir, name)
 
# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(port=8080)

