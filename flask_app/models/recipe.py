from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.controllers import users

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.made_on = data['made_on']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
    
    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes;"

        results = connectToMySQL('recipes').query_db(query)
        recipes = []

        for recipe in results:
            recipes.append ( cls(recipe))
        
        return recipes
    
    @classmethod
    def save(cls, data):
        print('--------------------------------------------------------------------------------------------------------------------')
        print(session['user_id'])
        query = "INSERT INTO recipes (name, description, instruction, made_on, under_30, user_id) VALUES (%(name)s, %(description)s, %(instruction)s, %(made_on)s,%(under_30)s, %(user_id)s);"

        return connectToMySQL('recipes').query_db(query, data)
    
    @classmethod
    def get_by_id(cls, data) :
        query = "SELECT * FROM recipes WHERE recipes.id = %(id)s;"
        print(data)
        results = connectToMySQL('recipes').query_db(query, data)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++", results)
        return cls(results[0])

    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instruction = %(instruction)s, made_on = %(made_on)s, under_30 = %(under_30)s, updated_at = NOW() WHERE id = %(id)s;"
        print('``````````````````````````````````````````````````````````````````', query)
        return connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL('recipes').query_db(query, data)

    @staticmethod
    def validate_user(recipe):
        is_valid = True
        if(len(recipe['name'])) < 2:
            flash(" name must be longer than 2 characters", "name")
            is_valid = False
        if(len(recipe['description'])) < 2:
            flash("Description must be longer than 2 characters", "description")
            is_valid = False
        if(len(recipe['instruction'])) < 2:
            flash("instructions must be longer than 2 characters", "instruction")
            is_valid = False
        if(len(recipe['made_on'])) < 2:
            flash("Date must be selected", "made_on")
            is_valid = False
        return is_valid