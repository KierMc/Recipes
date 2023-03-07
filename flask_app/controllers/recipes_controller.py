from flask import redirect, render_template, request, session, flash
from flask_app import app
from flask_app.models import recipes_model
from flask_app.models import user_model
from flask_app.config.mysqlconnection import connectToMySQL


@app.route('/dashboard')
def dashboard():
    if not 'id' in session:
        return redirect ('/')



    recipes=recipes_model.Recipe.get_recipes_with_users()

    return render_template("dashboard.html", recipes=recipes)

@app.route('/new_recipe')
def new_recipe():
    if not 'id' in session:
        return redirect ('/')

    return render_template ('new.html')

@app.route('/create_recipe', methods=["POST"])
def create_recipe():

    if not recipes_model.Recipe.validate(request.form):
        return redirect ('/new_recipe')

    data={
        **request.form,
        "user_id":session['id']
    }

    recipes_model.Recipe.create(data)

    return redirect('/dashboard')

@app.route('/edit/<int:recipe_id>')
def edit_recipe(recipe_id):
    if not 'id' in session:
        return redirect ('/')

    data={
        "id":recipe_id
    }

    recipe_to_edit=recipes_model.Recipe.get_recipe_by_id(data)

    return render_template ('edit.html', recipe=recipe_to_edit)

@app.route('/save_recipe/<int:recipe_id>', methods=['POST'])
def save_recipe(recipe_id):

    data={
        "id":recipe_id,
        "name":request.form["name"],
        "time":request.form["time"],
        "description":request.form["description"],
        "instructions":request.form["instructions"]
    }

    recipes_model.Recipe.update(data)
    
    return redirect ('/dashboard')

@app.route('/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    if not 'id' in session:
        return redirect ('/')
        
    data={
        "id":recipe_id
    }

    recipe_to_delete = recipes_model.Recipe.get_recipe_by_id(data)
    print (recipe_to_delete)

    recipes_model.Recipe.delete(data)
    return redirect ('/dashboard')

@app.route('/view/<int:recipe_id>')
def view_recipe(recipe_id):
    if not 'id' in session:
        return redirect ('/')

    data={
        "id":recipe_id
    }
    
    recipe_to_view = recipes_model.Recipe.get_recipe_by_user(data)
    return render_template ('view.html',recipes=recipe_to_view)
