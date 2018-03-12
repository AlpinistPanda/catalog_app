from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, User, CategoryItem

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create first user -- Admin
User1 = User(name="Ozgun Balaban", email="ozgunbalaban@somemail.com")
session.add(User1)
session.commit()

# First Category -- football
category1 = Category(user_id=1, name="Football")

session.add(category1)
session.commit()

# Some Items for Football category

item1 = CategoryItem(user_id=1, title="Shin Guards", description="It protects your shins",
                     category=category1)

session.add(item1)
session.commit()

item2 = CategoryItem(user_id=1, title="Keeper Gloves",
                description="For keepers this is crucial",
                category=category1)

session.add(item2)
session.commit()

item3 = CategoryItem(user_id=1, title="Football",
                description="Without football you cannot play this game",
                category=category1)

session.add(item3)
session.commit()

# Second Category -- Rock Climbing
category2 = Category(user_id=1, name="Rock Climbing")

session.add(category2)
session.commit()

# Some Items for Rock Climbing category

item4 = CategoryItem(user_id=1, title="Harness",
                description="This one will save your life if you fall",
                category=category2)

session.add(item4)
session.commit()

item5 = CategoryItem(user_id=1, title="Quick Draw",
                description="To keep your rope attached to the bolts",
                category=category2)

session.add(item5)
session.commit()

# Third Category -- Rock Climbing
category3 = Category(user_id=1, name="Wind Surfing")

session.add(category3)
session.commit()

# Some Items for Wind Surfing category

item6 = CategoryItem(user_id=1, title="Sail",
                description="I need my sail to get moving with the wind",
                category=category3)

session.add(item6)
session.commit()

item7 = CategoryItem(user_id=1, title="Board",
                description="This boards are bigger than surf boards",
                category=category3)

session.add(item7)
session.commit()

print "added catalog items!"
