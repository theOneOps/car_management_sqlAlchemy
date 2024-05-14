import math

from sqlalchemy import and_, func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Query

from population import *
from util import *

type userType = {"id": int, "name": str, "passwd": str}

userConnect: userType = {"id": None, "name": "", "passwd": ""}

Session = sessionmaker(bind=engine)
session = Session()


# some requests on the table User

# Request to register as new user

def addUser(name: str, password: str, email: str = "") -> bool:
    # we instanciate a user with the values of the finction's paramters 
    user = User(username=name, password=password, email=email)
    session.add(user)
    session.commit()
    print("account created successfully !")


# addUser("userOnefst", "thepassword", "userOnefst@gmail.com")
# addUser("userScd", "thepasswordTwo")


def printAllSellers():
    # we make a request to get all users that have publiushed some adverts
    # so we only need the User table and the Advert table
    # so we join the tables and we group bt the user_id to not have duplications name in the results
    results = session.query(User.id_user, func.max(User.username), func.max(Advert.id_advert)). \
        join(Advert, User.id_user == Advert.id_user). \
        group_by(User.id_user).all()

    # if there is some results :
    if results:
        # we print them
        line_format = "| {:<10} | {:<20} | {:<10}"
        print(line_format.format("id_user", "username"))
        print("-" * 50)

        for result in results:
            id_user, username, max_advert_id = result
            print(line_format.format(id_user, username))
    else: # else we print an error's message
        print("No sellers found in the database")

# printAllSellers()


def connectAsUser(name: str, password: str) -> bool:
    global userConnect
    res: bool = False
    try:
        # to connect our user, we need to check if the name and password 
        # he/she gives as input are valid authentification password registered in the database
        result = session.query(User).filter(and_(User.username.like(name),
                                                 User.password.like(
                                                     password))).one()
        # if we find an record :
        if result:
            # we stock it for further requests
            res = True
            userConnect["id"] = result.id_user
            userConnect["name"] = result.username
            userConnect["passwd"] = result.password
            print("conection succeeded \n")
    # unless we found no record
    except NoResultFound: # we return an error message
        print(f"there is no user with name {name} and password {password}")
    return res


# connectAsUser("BobSmith", "safePassword321")


def disConnect():
    global userConnect
    # to disconnect our user, we just nned to get rid of 
    # the user 's value we stock before when he was logged in
    if userConnect["id"] is not None:
        userConnect["id"] = None
        userConnect["name"] = ""
        userConnect["passwd"] = ""
        print("you successfully logout ! \n")


# disConnect()

def printAllCategories():
    # to print all categories, we just make a query on the category's table to get all its records
    results = session.query(Category).all()
    if results:
        # Headers of the results
        print("All categories of cars")
        print("| {:<12} | {:<20}".format("idCategory", "car_category"))
        print("-" * 34)  # line that separate headers from the results

        # Print the results
        for row in results:
            print("{:<12} | {:<20}".format(row.id_category, row.car_category))
    else:
        print("No categories of car to display")


# printAllCategories()

def printAllCars():
    # we only print all cars that were concerned about advertises
    # hence the join between the Advert table and the Car table
    results = session.query(Advert, Car).join(Advert,
                                              Advert.id_advert == Car.id_advert).all()
    if results:
        print("All categories of cars ")
        print(
            "idCar | id_advert | car_model | car_brand | car_state | car_category") # for the headers
        line_format = "| {:<10} | {:<10} | {:<20} | {:<20} | {:<20} | {:<20} "
        print(line_format.format("idCar", "id_advert", "car_model", "car_brand",
                                 "car_state", "car_category"))
        print("-" * 120) # line that separate headers from the results
        for advert, car in results:
            print(line_format.format(car.id_car, car.id_advert, car.model_car,
                                     car.car_brand, car.car_state,
                                     categories_data[
                                         int(advert.id_category) - 1][
                                         str(advert.id_category)]))


# printAllCars()

def publishTheAdvert(transaction: str, location: str, price: float,
                     categoryId: str, description: str = "") -> None:
    global userConnect
    # to publish a 
    if userConnect["id"] is not None:
        if categoryId in categories_keys:

            # to publish an advert, we check if the advert has been created before
            request = session.query(Advert).filter_by(
                transaction=transaction, location=location, price=price,
                id_category=categoryId, description=description,
                id_user=userConnect["id"]).first()
            # if yes, then you just returned an error message
            if request:
                print("An advert with the same price, description, transaction,"
                      "and location already exists.")
            else:
                # else we create the advert
                advert = Advert(transaction=transaction,
                                location=location,
                                price=price,
                                description=description,
                                id_user=userConnect["id"],
                                id_category=int(categoryId))
                session.add(advert)
                session.commit()
                print("advert published successfully !")
        else: # if the category id is not valid, we returned an error message
            print(f"the categoryId {categoryId} doesn't exist"
                  "first, check the list of "
                  "available categories "
                  "of car with "
                  "the command ... before making this command \n")


# publishTheAdvert("sale", "tours", 21000.0, "2")
#
# publishTheAdvert("sale", "tours", 21000.0, "2")


def printAllMyAdvertises() -> None:
    global userConnect
    if userConnect["id"] is not None:
        # to print all of my advertises, we make a query to get all advertises where the id_user from the Advert table is the user 'logged in'
        results = (session.query(Advert, User).join(User,
                                                    Advert.id_user == User.id_user)
                   .filter(User.id_user == userConnect["id"])
                   .all())
        if results:# if we have some results, we print them
            print("All of my advertisements in details\n")
            header = "{:<12} | {:<12} | {:<12} | {:<12} | {:<14} | {}"
            print(header.format("id_advert", "transaction", "location",
                                "price", "category", "description"))
            print("-" * 110)  # Ligne de séparation

            for advert, user in results:
                category_id = int(advert.id_category) - 1
                category_name = categories_data[category_id][
                    str(advert.id_category)]

                line = "{:<12} | {:<12} | {:<12} | {:<12.2f} | {:<14} | {}"
                print(line.format(advert.id_advert, advert.transaction,
                                  advert.location, advert.price,
                                  category_name, advert.description))
        else: # else there is no advertises for that user 'logged in'
            print("you don't have any advertises ! ")
    else: # unless, you 'are not logged in, the nyou should be logged in
        print(f"To see your advertises, you need to be connect first to "
              f"execute this request")
        print(f"if you don't have account, create one with the command "
              f" 'createAccount' ")


# printAllMyAdvertises()


def printAllAdvertisesOf(username: str) -> None:
    global userConnect
    if userConnect["id"] is not None:
        # we print all advertises of a username given in parameter
        results = session.query(Advert, User).join(User, Advert.id_user ==
                                                   User.id_user).filter(
            User.username == username)
        print(f"the advertises made by the user {username} \n")
        if results: # if there are some results, we print them
            count = len(results)
            print(f"There are {count} results\n")
            header = "{:<12} | {:<12} | {:<12} | {:<12} | {:<15} | {}"
            print(header.format("id_advert", "transaction", "location", "price",
                                "category", "description"))
            print("-" * 90)  # Ligne de séparation

            for advert, user in results:
                category_id = int(advert.id_category) - 1
                category_name = categories_data[category_id][
                    str(advert.id_category)]

                # Affichage détaillé de chaque annonce
                line = "{:<12} | {:<12} | {:<12} | {:<12.2f} | {:<15} | {}"
                print(line.format(advert.id_advert, advert.transaction,
                                  advert.location, advert.price,
                                  advert.description, category_name))
        else:# unless, there is no user with that name who publish before or just existed
            print(f"The username '{username}' you enter doesn't exist or doesn't have advertises"
                  f"on the "
                  f"\application")
    else:
        print("you need to connect first ! \n")


# printAllAdvertisesOf("BobSmith")


def modifyTheAdvert(id_advert: int, newTransaction: str, newLocation: str,
                    newPrice: float, newDescription: str) -> None:
    global userConnect
    
    if userConnect["id"] is not None:
        try:
            # to modify an advert, we firdt check if the advert with the id 
            # given in parameter existed and is the user's own
            result = session.query(Advert, User).join(User, Advert.id_user ==
                                                      User.id_user).filter(
                and_(User.id_user == userConnect["id"], Advert.id_advert ==
                     id_advert)).one()
            # if we found a result
            if result:
                # then we search it and we modify it
                session.query(Advert).filter(
                    Advert.id_advert == id_advert).update({
                    Advert.price: newPrice,
                    Advert.description: newDescription,
                    Advert.transaction: newTransaction,
                    Advert.location: newLocation
                })
                session.commit()
                print(
                    f"you have successfully changed one of your advert of id_advert"
                    f" {id_advert}")
        except NoResultFound: # unless there is no advert found for us
            print(f"you don't have advert of id {id_advert}")


# modifyTheAdvert(3, "rent", "Paris", 12000.0, "I have changed it !")


def removeAdvertOfId(id_advert: Integer) -> None:
    global userConnect
    try:
        # to remove an advert, we need to check if the advert_id is one of us,
        # and if it's really existed
        result = session.query(Advert, User).join(User, Advert.id_user ==
                                                  User.id_user).filter(
            and_(User.id_user == userConnect["id"], Advert.id_advert ==
                 id_advert)).one()
        # if there is a result
        if result:
            # we found it, and removed it from the database
            request = session.get(Advert, id_advert)
            session.delete(request)
            session.commit()
            print(
                f"you have successfully removed one of your advert of id_advert"
                f" {id_advert}")
    except NoResultFound:
        print(f"you don't have advert of id {id_advert}")


# removeAdvertOfId(10)


def findAdvertBaseOnCriterias(transaction: str = "", location: str = "",
                              price: float = math.inf,
                              cmp: str = "equals",
                              description: str = "",
                              id_category: str = "",
                              id_user: int = math.inf) -> None:
    # we first initialize the query
    results = Query(Advert, session)
    if transaction != "": # if there is a value of transaction, we make some filter based on it
        results = results.filter(Advert.transaction == transaction)

    if location != "": # if there is a value of location, we make some filter based on it
        results = results.filter(Advert.location == location)

    if price != math.inf:
        if cmp == "equals": # if cmp is '=', then we filter the advert based on the equals price given in parameters
            results = results.filter(Advert.price == price)
        elif cmp == "inf": # if cmp is '<', then we filter the advert based on the lower price given in parameters
            results = results.filter(Advert.price < price)
        elif cmp == "infEquals": # if cmp is '<=', then we filter the advert based on the equals or lower price given in parameters
            results = results.filter(Advert.price <= price)
        elif cmp == "supEquals": # if cmp is '>=', then we filter the advert based on the equals or upper price given in parameters
            results = results.filter(Advert.price >= price)
        elif cmp == "sup":# if cmp is '>', then we filter the advert based on the upper price given in parameters
            results = results.filter(Advert.price > price)
        else: # that sign of cmp is not recognized !
            print("I don't recognize that value of cmp for this research !")

    if description != "": # if there is a value of description, we make some filter based on it
        results = results.filter(Advert.description == description)

    if id_user != math.inf: # if there is a value of user's id, we make some filter based on it
        results = results.filter(Advert.id_user == id_user)

    if id_category != "": # if there is a value of category_id, we make some filter based on it
        results = results.filter(Advert.id_category == int(id_category))

    if (transaction == "" and location == "" and price == math.inf and
            description == "" and id_user == math.inf
            and id_category != ""): # if all attributs are empty, then e get all records of the table
        results = Query(Advert, session).all()
    else:
        results = results.all() # unless we make request based on the filters we worked on before

    if results: # if there is some results
        header = "{:<10} | {:<15} | {:<15} | {:<15} | {:<10} | {}"
        print(header.format("id_user", "id_category", "transaction", "location",
                            "price", "description"))
        print("-" * 90)  # line that separates headers from the results

        for row in results:
            # we initialize the format to print the results 
            line = "{:<10} | {:<15} | {:<15} | {:<15} | {:<10.2f} | {}"
            print(line.format(row.id_user, row.id_category, row.transaction,
                              row.location, row.price, row.description))
    else:
        print("there is no records found for your research !")


# findAdvertBaseOnCriterias()


def makeOfferForAdvert(id_advert: int, price: float) -> None:
    global userConnect
    if userConnect["id"] is not None:
        try:
            # to make an offer, we first check if the advert 
            # with the id given in parameters really existed
            advertExists = session.query(Advert).filter(Advert.id_advert ==
                                                        id_advert).one()
            # if we find an advert, we check if it's the user 'logged in' own
            myadvert = session.query(Advert).filter(and_(Advert.id_user ==
                                                    userConnect["id"],
                                                         Advert.id_advert == id_advert
                                                         )).first()
            if myadvert: # if yes, then we can't make offer on our own advertises
                print("this advert is yours, you can make offer on your own "
                      "advert !")
            else: # if not, we make query to get the advert
                request = session.query(Offer, ProposeOffer, Advert).join(
                    ProposeOffer, Offer.id_offer == ProposeOffer.id_offer
                ).join(
                    Advert, Advert.id_advert == ProposeOffer.id_advert
                ).filter(
                    
                    Offer.price_proposed == price,  # advert with the concerned price
                    ProposeOffer.id_advert == id_advert,
                    # id of the concerned advert

                    # Additional conditions
                    # the user who proposed the offer is me # basically I can't make the same offer again !
                    ProposeOffer.id_user == userConnect["id"], 
                    Advert.id_user != userConnect["id"] 
                    # the advert's creator should not be the connected user who made the advert
                ).first()

                if request: # if we found an offer, then we have already made an offer,
                    # like that before with the same lement of offers
                    print(
                        f"You have already make an offer for the advert of id {id_advert}")

                else: # we haven't made that kind of offer before
                    offer = Offer(state_offer="pending", price_proposed=price)
                    session.add(offer)
                    session.commit()
                    the_propose_offer = ProposeOffer(id_user=userConnect["id"],
                                                     id_offer=offer.id_offer,
                                                     id_advert=id_advert)

                    session.add(the_propose_offer)
                    session.commit()

                    print(
                        f"offer successfully made for the advert of id {id_advert} ")
        except NoResultFound:
            print(f"an advert with the id {id_advert} doesn't exist in the "
                  f"database")


# makeOfferForAdvert(4, 20000)


def printAllOffersIHaveMade() -> None:
    global userConnect
    if userConnect["id"] is not None:
        results = session.query(Offer, ProposeOffer, Advert) \
            .join(ProposeOffer, Offer.id_offer == ProposeOffer.id_offer) \
            .join(Advert, Advert.id_advert == ProposeOffer.id_advert) \
            .filter(and_(ProposeOffer.id_user == userConnect["id"]),
                    Advert.id_user != userConnect["id"]) \
            .all()

        if results:
            # Define the header format and print the header
            header_format = (
                "{:<10} | {:<10} | {:<10} | {:<10} | {:<15} | {:<20} | {"
                ":<15} | {}")
            print(header_format.format("id_offer", "state_offer", "my price",
                                       "id_advert",
                                       "transaction", "price of the advert",
                                       "location", "description"))
            print("-" * 110)  # Print a separator line for better clarity

            # Iterate through the results and format each row
            for offer, proposeoffer, advert in results:
                row_format = (
                    "{:<10} | {:<10} | {:<10.2f} | {:<10} | {:<15} | {"
                    ":<20.2f} | {:<15} | {}")
                print(row_format.format(
                    offer.id_offer,
                    offer.state_offer,
                    offer.price_proposed,
                    advert.id_advert,
                    advert.transaction,
                    advert.price,
                    advert.location,
                    advert.description
                ))
                print()  # Adding a newline for spacing between entries
        else:
            print("You have made no offers !")

    else:
        print("you need to login first before executing this command !")


# printAllOffersIHaveMade()


def printOffersOnMyAdvertOfId(id_advert: int = math.inf,
                              state_offer: str = "") -> None:
    global userConnect

    if userConnect["id"] is not None:

        try:
            if id_advert != math.inf:
                request = session.query(Advert).filter(and_(Advert.id_advert ==
                                                            id_advert,
                                                            Advert.id_user ==
                                                            userConnect[
                                                                "id"])).one()
            else:
                request = session.query(Advert).filter(and_(
                                                            Advert.id_user ==
                                                            userConnect[
                                                                "id"])).one()


            results = session.query(User, ProposeOffer, Offer, Advert) \
                .join(ProposeOffer, ProposeOffer.id_user == User.id_user) \
                .join(Offer, ProposeOffer.id_offer == Offer.id_offer) \
                .join(Advert, ProposeOffer.id_advert == Advert.id_advert) \
                .filter(
                Advert.id_user == userConnect["id"],
                ProposeOffer.id_user != Advert.id_user,
                Advert.id_user == userConnect["id"]
            )

            if id_advert != math.inf:
                results = results.filter(Advert.id_advert == id_advert)

            if state_offer != "":
                results = results.filter(Offer.state_offer == state_offer)

            results = results.all()

            if results:
                for user, proposeoffer, offer, advert in results:
                    print(f"offerUserId {user.id_user} offerUserName :"
                          f" {user.username}")

                    print(
                        f"offer_id {offer.id_offer} state_offer {offer.state_offer} "
                        f"price_proposed {offer.price_proposed}")

                    print(f"transaction {advert.transaction} location "
                          f"{advert.location} price {advert.price} "
                          f"description {advert.description}")

                    print("\n")
            else:
                if id_advert == math.inf:
                    print("there is no offer for your advertises !")
                else:
                    print(
                        f"there is no offer for your advertise of id {id_advert}!")
        except NoResultFound:
            print(f"you don't have advert of id {id_advert}")


def answerOfferOfId(id_offer: int, answer: str):
    global userConnect
    if userConnect["id"] is not None:
        try:
            offer = session.query(Offer).filter(
                Offer.id_offer == id_offer).one_or_none()
            try:
                myOffer = session.query(ProposeOffer).filter(
                    and_(ProposeOffer.id_user == userConnect["id"],
                         ProposeOffer.offer == id_offer)).one()
                if offer and offer.state_offer == "pending":
                    offer.state_offer = answer
                    session.commit()
                    print("Offer updated successfully.")
                else:
                    print(
                        f"No pending offer found with the specified ID {id_offer}.")
            except NoResultFound:
                print("this offer is yours, you can answer your own offer !")
        except NoResultFound:
            print(f"the offer with the id {id_offer} doesn't exist !")
            session.rollback()


# answerOfferOfId(id_offer=10, answer="refused")

# We close the session
session.close()
