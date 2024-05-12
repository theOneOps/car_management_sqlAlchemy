

users_data = [
    {"username": "AliceMartin", "email": "alice.martin@example.com",
     "password": "password123"},
    {"username": "BobSmith", "email": "bob.smith@example.com",
     "password": "safePassword321"},
    {"username": "CharlieBrown", "email": "charlie.brown@example.com",
     "password": "mySecurePass456"},
    {"username": "DavidWilson", "email": "david.wilson@example.com",
     "password": "pass789Secure"},
    {"username": "EvaGreen", "email": "eva.green@example.com",
     "password": "greenPass234"},
    {"username": "FionaClark", "email": "fiona.clark@example.com",
     "password": "clarkPass987"},
    {"username": "GeorgeHall", "email": "george.hall@example.com",
     "password": "hallPass654"},
    {"username": "HelenAllen", "email": "helen.allen@example.com",
     "password": "allen123Password"},
    {"username": "IvanMorris", "email": "ivan.morris@example.com",
     "password": "morris321Pass"},
    {"username": "JuliaHarris", "email": "julia.harris@example.com",
     "password": "juliaSecure456"}
]

# Example of category data
categories_keys = ["1", "2", "3", "4", "5"]

categories_data = [
    {"1": "SUV"},
    {"2": "Sedan"},
    {"3": "Convertible"},
    {"4": "Hatchback"},
    {"5": "Coupe"}
]

# Example of offer data

offers_data = [
    {"state_offer": "pending", "price_proposed": 1000.0},
    {"state_offer": "accepted", "price_proposed": 1500.0},
    {"state_offer": "refused", "price_proposed": 900.0},
    {"state_offer": "pending", "price_proposed": 800.0},
    {"state_offer": "accepted", "price_proposed": 2000.0},
    {"state_offer": "refused", "price_proposed": 1200.0},
    {"state_offer": "pending", "price_proposed": 700.0},
    {"state_offer": "accepted", "price_proposed": 1800.0},
    {"state_offer": "refused", "price_proposed": 1100.0},
    {"state_offer": "pending", "price_proposed": 600.0}
]


# Example of advert data

adverts_data = [
    {"transaction": "sale", "location": "Paris", "price": 30000.0,
     "description": "Nice car", "id_category": 1, "id_user": 1},
    {"transaction": "rent", "location": "Lyon", "price": 10000.0,
     "description": "great car", "id_category": 2, "id_user": 1},
    {"transaction": "sale", "location": "Marseille", "price": 35000.0,
     "description": "it's unbelievable !", "id_category": 3, "id_user": 2},
    {"transaction": "sale", "location": "Toulouse", "price": 30000.0,
     "description": "One word : convenient !", "id_category": 3, "id_user": 2},
    {"transaction": "rent", "location": "Nice", "price": 25000.0,
     "description": "really cheapest one !", "id_category": 4, "id_user": 3},
    {"transaction": "sale", "location": "Bordeaux", "price": 40000.0,
     "description": "Nice Hatch ! right ? ", "id_category": 4, "id_user": 3},
    {"transaction": "sale", "location": "Lille", "price": 65000.0,
     "description": "black suv to point out !", "id_category": 1, "id_user": 3},
    {"transaction": "rent", "location": "Strasbourg", "price": 20000.0,
     "description": "relevant car ! ", "id_category": 2, "id_user": 4},
    {"transaction": "sale", "location": "Rennes", "price": 40000.0,
     "description": "a true transformer car, right ?", "id_category": 3,
     "id_user": 1},
    {"transaction": "rent", "location": "Nantes", "price": 5000.0,
     "description": "Convenient", "id_category": 5, "id_user": 2}
]

# Example of car data

cars_data = [
    {"model_car": "X5", "car_brand": "BMW", "car_state": "used", "id_advert":
        1},
    {"model_car": "Cayenne", "car_brand": "Porsche", "car_state": "new",
     "id_advert": 2},
    {"model_car": "A3", "car_brand": "Audi", "car_state": "new",
     "id_advert": 3},
    {"model_car": "A4", "car_brand": "Audi", "car_state": "used", "id_advert":
        4},
    {"model_car": "Golf", "car_brand": "Volkswagen", "car_state": "new",
     "id_advert": 5},
    {"model_car": "Civic", "car_brand": "Honda", "car_state": "new",
     "id_advert": 6},
    {"model_car": "Q7", "car_brand": "Audi", "car_state": "used", "id_advert":
        7},
    {"model_car": "A6", "car_brand": "Audi", "car_state": "used", "id_advert":
        8},
    {"model_car": "Clio", "car_brand": "Renault", "car_state": "new",
     "id_advert": 9},
    {"model_car": "C4", "car_brand": "Citroen", "car_state": "used",
     "id_advert": 10}
]


# Example of propose_offer data

proposed_offers_data = [
    {"id_user": 5, "id_offer": 1, "id_advert": 1},
    {"id_user": 5, "id_offer": 2, "id_advert": 2},
    {"id_user": 7, "id_offer": 4, "id_advert": 4},
    {"id_user": 7, "id_offer": 5, "id_advert": 5},
    {"id_user": 8, "id_offer": 6, "id_advert": 6},
    {"id_user": 9, "id_offer": 7, "id_advert": 7},
    {"id_user": 10, "id_offer": 8, "id_advert": 8},
    {"id_user": 1, "id_offer": 9, "id_advert": 9},
    {"id_user": 2, "id_offer": 10, "id_advert": 10},
    {"id_user": 3, "id_offer": 4, "id_advert": 1},
    {"id_user": 4, "id_offer": 5, "id_advert": 5},
    {"id_user": 5, "id_offer": 6, "id_advert": 6},
    {"id_user": 1, "id_offer": 7, "id_advert": 10},
]