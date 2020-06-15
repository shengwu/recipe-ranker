from collections import defaultdict
from typing import List

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from sqlalchemy.orm import raiseload


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

# MODELS
# ------

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
    recipes = db.relationship('Recipe', backref='category', order_by='Recipe.votes.desc()', lazy='joined')

    def __repr__(self):
        return '<Category %r>' % self.name


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    url = db.Column(db.Text, unique=True)
    votes = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Recipe %r>' % self.url


def recipe_param_errors(recipe_params: dict) -> List[str]:
    errors = []
    allowed_params = ('category_id', 'url')
    required_params = ('category_id', 'url')
    if len(recipe_params.keys() - allowed_params) > 0:
        errors.append('params not allowed: ' + str(recipe_params.keys() - allowed_params))
    if len(required_params - recipe_params.keys()) > 0:
        errors.append('missing required params: ' + str(required_params - recipe_params.keys()))
    return errors


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


# ROUTES
# ------

@app.route('/recipe/upvote/<int:recipe_id>', methods=['POST'])
def upvote_recipe(recipe_id):
    pass


@app.route('/recipes', methods=['PUT'])
def new_recipe():
    recipe_params = request.get_json()
    if recipe_params is None:
        return jsonify({'error': 'could not parse params as json'}), 400
    errors = recipe_param_errors(recipe_params) 
    if errors != [] :
        return jsonify({'errors': errors}), 400
    db.session.add(Recipe(**recipe_params))
    db.session.commit()
    return 'ok'


@app.route('/category/<category_name>', methods=['PUT'])
def new_category(category_name):
    db.session.add(Category(name=category_name))
    db.session.commit()
    return 'ok'


@app.route('/category/<category_name>', methods=['GET'])
def top_recipes_in_category(category_name):
    category = Category.query.where(name=category_name).first()
    if category is None:
        return jsonify({'error': 'category {} not found'.format(category)}), 404
    return jsonify({'recipes': [object_as_dict(recipe) for recipe in category.recipes]})


@app.route('/', methods=['GET'])
def homepage():
    return jsonify({
        'categories': [
            {
                **object_as_dict(category),
                **{'recipes': [object_as_dict(recipe) for recipe in category.recipes]},
            } for category in Category.query.all()
        ],
    })




# MISC
# ----

if __name__ == '__main__':
    app.run()
