from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user_model import User
from flask_app.models import recipes_model


class Recipe:
    def __init__(self,data):
        self.id=data['id']
        self.name=data['name']
        self.time=data['time']
        self.description=data['description']
        self.instructions=data['instructions']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.user_id=data['user_id']

    @classmethod
    def create(cls,data):
        query = "INSERT INTO recipes (name, time, description, instructions, user_id) VALUES (%(name)s, %(time)s, %(description)s, %(instructions)s, %(user_id)s)"
        return connectToMySQL('recipes').query_db(query, data)
    
    @classmethod
    def get_recipe_by_id(cls,data):
        query='SELECT * FROM recipes WHERE id=%(id)s'
        results=connectToMySQL('recipes').query_db(query,data)

        if results:
            return cls(results[0])
        else:
            return False

    @classmethod
    def update(cls, data):
        query="UPDATE recipes SET name=%(name)s, time=%(time)s, description=%(description)s, instructions=%(instructions)s, updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL('recipes').query_db(query,data)

    @classmethod
    def delete(cls,data):
        query='DELETE FROM recipes WHERE id=%(id)s'
        return connectToMySQL('recipes').query_db(query,data)

    @classmethod
    def get_recipes_with_users(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id=users.id;"
        results=connectToMySQL('recipes').query_db(query)

        if (results):

            recipes=[]

            for result in results:
                recipes.append(result)
            return recipes

    @classmethod
    def validate(cls,data):
        if len(data["description"]) < 1:
            flash("Your description must not be blank!")
            return False
        return True

    @classmethod
    def get_recipe_by_user(cls, data):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id=users.id WHERE recipes.id=%(id)s;"
        results=connectToMySQL('recipes').query_db(query, data)

        if (results):

            recipes=[]

            for result in results:
                recipes.append(result)
            return recipes