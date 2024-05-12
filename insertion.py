from population import *
from util import *

# Création d'une session

session = Session()

# some users' data

# Insertion of user data
for user_data in users_data:
    user = User(username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'])
    session.add(user)

# we commit the session to save the data in the database
session.commit()

# Insertion of category data
count: int = 1
for category_data in categories_data:
    category = Category(car_category=category_data[f'{count}'])
    session.add(category)
    count += 1

# we commit the session to save the data in the database
session.commit()

# Insertion of offer data
for offer_data in offers_data:
    offer = Offer(state_offer=offer_data['state_offer'],
                  price_proposed=offer_data['price_proposed'])
    session.add(offer)

# we commit the session to save the data in the database
session.commit()

# Insertion of advert data
for advert_data in adverts_data:
    advert = Advert(transaction=advert_data['transaction'],
                    location=advert_data['location'],
                    price=advert_data['price'],
                    description=advert_data['description'],
                    id_category=advert_data['id_category'],
                    id_user=advert_data['id_user'])
    session.add(advert)

# we commit the session to save the data in the database
session.commit()

# Insertion of car data

for car_data in cars_data:
    car = Car(model_car=car_data['model_car'], car_brand=car_data['car_brand'],
              car_state=car_data['car_state'], id_advert=car_data['id_advert'])
    session.add(car)

# we commit the session to save the data in the database
session.commit()

# Insertion of propose_offer data

for propose_offer_data in proposed_offers_data:
    propose_offer = ProposeOffer(id_user=propose_offer_data['id_user'],
                                 id_offer=propose_offer_data['id_offer'],
                                 id_advert=propose_offer_data['id_advert'])
    session.add(propose_offer)

# we commit the session to save the data in the database
session.commit()

# We close the session
session.close()
