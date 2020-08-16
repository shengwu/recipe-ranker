from collections import defaultdict
import datetime
from typing import List

from flask import Flask, jsonify, request
from flask_cors import CORS # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from sqlalchemy import inspect
from sqlalchemy.orm import raiseload


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# MODELS
# ------

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
    recipes = db.relationship('Recipe', backref='category', order_by='Recipe.votes.desc()', lazy='joined')

    def __repr__(self):
        return '<Category %r>' % self.name

    def render_dict(self):
        return {
            **object_as_dict(self),
            **{'recipes': [recipe.render_dict() for recipe in self.recipes]},
        }

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    url = db.Column(db.Text, unique=True)
    votes = db.Column(db.Integer, default=0)
    comments = db.relationship('Comment', backref='recipe', order_by='Comment.posted_at', lazy='joined')

    def __repr__(self):
        return '<Recipe %r>' % self.url

    def render_dict(self):
        return {
            **object_as_dict(self),
            **{'comments': [comment.render_dict() for comment in self.comments]},
        }

    @staticmethod
    def param_errors(recipe_params: dict) -> List[str]:
        errors = []
        allowed_params = ('category_id', 'url')
        required_params = ('category_id', 'url')
        if len(recipe_params.keys() - allowed_params) > 0:
            errors.append('params not allowed: ' + str(recipe_params.keys() - allowed_params))
        if len(required_params - recipe_params.keys()) > 0:
            errors.append('missing required params: ' + str(required_params - recipe_params.keys()))
        return errors



class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    text = db.Column(db.Text)
    posted_at = db.Column(db.DateTime)

    def __repr__(self):
        return '<Comment %r>' % self.url

    def render_dict(self):
        return object_as_dict(self)

    @staticmethod
    def param_errors(comment_params: dict) -> List[str]:
        errors = []
        allowed_params = ('recipe_id', 'text')
        required_params = ('recipe_id', 'text')
        if len(comment_params.keys() - allowed_params) > 0:
            errors.append('params not allowed: ' + str(comment_params.keys() - allowed_params))
        if len(required_params - comment_params.keys()) > 0:
            errors.append('missing required params: ' + str(required_params - comment_params.keys()))
        return errors


def object_as_dict(obj: db.Model) -> dict:
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}







# ROUTES
# ------

@app.route('/comments', methods=['POST'])
def new_comment():
    comment_params = request.get_json()
    if comment_params is None:
        return jsonify({'error': 'could not parse params as json'}), 400
    errors = Comment.param_errors(comment_params) 
    if errors != [] :
        return jsonify({'errors': errors}), 400
    # have to save as UTC for sqlite3
    db.session.add(Comment(**{**comment_params, 'posted_at': datetime.datetime.utcnow()}))
    db.session.commit()
    return 'ok'


@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = Recipe.query.filter(Recipe.id == recipe_id).one()
    if recipe is None:
        return jsonify({'error': 'recipe with id {} not found'.format(recipe_id)}), 404
    return jsonify({'recipe': recipe.render_dict()})


@app.route('/recipe/upvote/<int:recipe_id>', methods=['POST'])
def upvote_recipe(recipe_id):
    # NOTE: unsure if this is thread safe
    # found this: https://stackoverflow.com/questions/2334824/how-to-increase-a-counter-in-sqlalchemy
    # need to read more sqlalchemy documentation
    recipe = Recipe.query.filter(Recipe.id == recipe_id).one()
    if recipe is None:
        db.session.rollback()
        return jsonify({'error': 'recipe with id {} not found'.format(recipe_id)}), 404
    recipe.votes += 1
    db.session.commit()
    return 'ok'


@app.route('/recipes', methods=['PUT'])
def new_recipe():
    recipe_params = request.get_json()
    if recipe_params is None:
        return jsonify({'error': 'could not parse params as json'}), 400
    errors = Recipe.param_errors(recipe_params) 
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


@app.route('/', methods=['GET'])
def homepage():
    return jsonify({
        'categories': [category.render_dict() for category in Category.query.all()],
    })




# MISC
# ----

if __name__ == '__main__':
    app.run()
