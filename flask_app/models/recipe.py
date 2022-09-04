from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User


class Recipe:
    def __init__(self, data:dict) -> None:
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        self.instructions = data.get('instructions')
        self.date_cooked = data.get('date_cooked')
        self.under_30 = data.get('under_30')
        self.user_id = data.get('user_id')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')

    def __repr__(self):
        return f'<Recipe: {self.name}> Created by {self.user_id}'

    @classmethod
    def get_all_users_with_recipes(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON user_id = users.id;"
        results = connectToMySQL('recipes').query_db(query)
        users = []

        for row in results:
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }

            user = User(user_data)

            recipe_data = {
                'id': row['id'],
                'name': row['name'],
                'description': row['description'],
                'instructions': row['instructions'],
                'date_cooked': row['date_cooked'],
                'under_30': row['under_30'],
                'user_id': row['user_id'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }

            user.recipes.append(Recipe(recipe_data))
            users.append(user)

        return users