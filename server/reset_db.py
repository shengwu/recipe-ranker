from app import db, Category, Recipe

db.drop_all()
db.create_all()
db.session.add(Category(name='Chocolate chip cookies'))
db.session.commit()

categories = Category.query.all()
assert len(categories) == 1
chocolate_chip_cookie_category = categories[0]

db.session.add(Recipe(
    category_id=chocolate_chip_cookie_category.id,
    url='https://sallysbakingaddiction.com/chocolate-chip-cookies/',
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
