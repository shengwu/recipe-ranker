import datetime
from app import db, Category, Recipe, Comment

db.drop_all()
db.create_all()
db.session.add(Category(name='Chocolate chip cookies'))
db.session.commit()

categories = Category.query.all()
assert len(categories) == 1
chocolate_chip_cookie_category = categories[0]

db.session.add(Recipe(
    category_id=chocolate_chip_cookie_category.id,
    url='https://sallysbakingaddiction.com/nutella-chocolate-chip-cookies/',
))
db.session.add(Recipe(
    category_id=chocolate_chip_cookie_category.id,
    url='https://www.verybestbaking.com/recipes/18476/original-nestle-toll-house-chocolate-chip-cookies/',
))
db.session.add(Recipe(
    category_id=chocolate_chip_cookie_category.id,
    url='https://www.epicurious.com/recipes/member/views/americas-test-kitchen-chocolate-chip-cookies-5800472a65f91f073d177abf',
))

db.session.commit()

nutella_recipe = Recipe.query.filter(Recipe.url == 'https://sallysbakingaddiction.com/nutella-chocolate-chip-cookies/').one()
assert nutella_recipe is not None
db.session.add(Comment(text='too much flour', recipe_id=nutella_recipe.id, posted_at=datetime.datetime.now()))
db.session.commit()
