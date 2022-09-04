from flask import render_template, redirect, session, request
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_app import app

@app.route('/recipes')
def recipes():
    if 'user_id' not in session:
        return redirect('/')

    active_data = {'id': session['user_id']}
    active_user = User.get_by_id(active_data)
    users_with_recipies = Recipe.get_all_users_with_recipes()
    for user in users_with_recipies:
        print(user.id)

    return render_template('recipes.html', user=active_user, uwr=users_with_recipies)