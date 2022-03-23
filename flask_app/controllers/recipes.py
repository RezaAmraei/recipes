
from flask import render_template, redirect, session, request, flash, Flask
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_app import app

@app.route('/create/recipe')
def create_recipe():
    if  not session.get("user_name"):
        return redirect('/')
    
    
    return render_template('create-rec.html')

@app.route('/created/recipe', methods = ['POST'])
def created_recipe():
    if  not session.get("user_name"):
        return redirect('/')
    if not Recipe.validate_user(request.form):
        return redirect('/create/recipe')
    data = {
        "name" : request.form['name'],
        "description" : request.form['description'],
        "instruction" : request.form['instruction'],
        "made_on" : request.form['made_on'],
        "under_30" : request.form['under_30'],
        "user_id" : session['user_id']
    }
    Recipe.save(data)
    return redirect('/home')

@app.route('/view/instructions/<int:id>')
def view_instructions(id):
    if  not session.get("user_name"):
        return redirect('/')
    data = {
        'id' : id
    }
    instructions = Recipe.get_by_id(data)
    return render_template('instructions.html', instructions = instructions)

@app.route('/edit/recipe/<int:id>')
def edit_recipe(id):
    if  not session.get("user_name"):
        return redirect('/')
    data = {
        'id' : id
    }
    recipe = Recipe.get_by_id(data)
    return render_template('edit.html', recipe = recipe)

@app.route('/update/recipe/<int:id>', methods = ['POST'])
def update_recipe(id):
    if  not session.get("user_name"):
        return redirect('/')
    data = {
        **request.form,
        'id' : id
    }
    Recipe.update_recipe(data)
    return redirect('/home')

@app.route('/delete/<int:id>')
def delete_recipe(id):
    if  not session.get("user_name"):
        return redirect('/')
    data = {
        'id': id
    }
    Recipe.delete_recipe(data)
    return redirect('/home')