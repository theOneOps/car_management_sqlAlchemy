import math

from sqlalchemy import and_
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

def addUser(name: str, password: str, email: str = "")->bool:
    user = User(username=name, password=password, email=email)
    session.add(user)
    session.commit()
    print("account created successfully !")



# addUser("userOnefst", "thepassword", "userOnefst@gmail.com")
# addUser("userScd", "thepasswordTwo")


def printAllUsers():
    results = session.query(User).all()
    for row in results:
        print(f"{row.id_user} {row.username} {row.password}\n")


# printAllUsers()


def connectAsUser(name: str, password: str) -> bool:
    global userConnect
    res: bool = False
    try:
        result = session.query(User).filter(and_(User.username.like(name),
                                                 User.password.like(
                                                     password))).one()
        if result:
            res = True
            userConnect["id"] = result.id_user
            userConnect["name"] = result.username
            userConnect["passwd"] = result.password
            print("conection succeeded \n")

            print("the global user values \n")
            print(
                f"userid -> {userConnect["id"]} username -> {userConnect["name"]}  "
                f"password-> {userConnect["passwd"]} \n")

    except NoResultFound:
        print(f"there is no user with name {name} and password {password}")
    return res


# connectAsUser("BobSmith", "safePassword321")


def disConnect():
    global userConnect
    if userConnect["id"] is not None:
        userConnect["id"] = None
        userConnect["name"] = ""
        userConnect["passwd"] = ""
        print("you successfully logout ! \n")


# disConnect()

def printAllCategories():
    results = session.query(Category).all()
    print("All categories of cars ")
    print("idCategory  |  car_category")
    for row in results:
        print(f"{row.id_category}  |  {row.car_category} \n")


# printAllCategories()

def printAllCars():
    results = session.query(Car).all()
    print("All categories of cars ")
    print("idCar | id_advert | car_model | car_brand | car_state")
    for row in results:
        print(f"{row.id_car} | {row.id_advert} | {row.model_car} | "
              f" {row.car_brand} | {row.car_state} \n")


# printAllCars()

def publishTheAdvert(transaction: str, location: str, price: float,
                  categoryId: str, description: str = "") -> None:
    global userConnect
    if userConnect["id"] is not None:
        if categoryId in categories_keys:

            # we check if the advert has been created before
            request = session.query(Advert).filter_by(
                transaction=transaction, location=location, price=price,
                id_category=categoryId, description=description,
                id_user=userConnect["id"]).first()

            if request:
                print("An advert with the same price, description, transaction,"
                      "and location already exists.")
            else:
                advert = Advert(transaction=transaction, location=location,
                                price=price,
                                description=description,
                                id_user=userConnect["id"],
                                id_category=int(categoryId))
                session.add(advert)
                session.commit()
                print("advert published successfully !")
        else:
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

        results = (session.query(Advert, User).join(User,
                                                    Advert.id_user == User.id_user)
                   .filter(User.id_user == userConnect["id"])
                   .all())
        print(f"All of my adverties in details \n")
        for advert, user in results:
            print(f" id_advert -> {advert.id_advert}"
                  f" transaction -> {advert.transaction} "
                  f" location -> {advert.location}"
                  f" price -> {advert.price}"
                  f" description -> {advert.description}"
                  f" category -> "
                  f"{categories_data[int(advert.id_category) - 1][str(advert.id_category)]}"
                  f"\n")
    else:
        print(f"To see your advertises, you need to be connect first to "
              f"execute this request")
        print(f"if you don't have account, create one with the command ...")


# printAllMyAdvertises()


def printAllAdvertisesOf(username: str) -> None:
    global userConnect
    if userConnect["id"] is not None:
        results = session.query(Advert, User).join(User, Advert.id_user ==
                                                   User.id_user).filter(
            User.username == username)
        print(f"the advertises made by the user {username} \n")
        if results:
            print(f"there are {results.count()} results \n")
            for advert, user in results:
                print(f" id_advert -> {advert.id_advert}"
                      f" transaction -> {advert.transaction} "
                      f" location -> {advert.location}"
                      f" price -> {advert.price}"
                      f" description -> {advert.description}"
                      f" category -> "
                      f""
                      f"{categories_data[int(advert.id_category) - 1][str(advert.id_category)]}"
                      f"\n")
        else:
            print(f"The username '{username}' you enter is not registered "
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
            result = session.query(Advert, User).join(User, Advert.id_user ==
                                                      User.id_user).filter(
                and_(User.id_user == userConnect["id"], Advert.id_advert ==
                     id_advert)).one()
            if result:
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
        except NoResultFound:
            print(f"you don't have advert of id {id_advert}")


# modifyTheAdvert(3, "rent", "Paris", 12000.0, "I have changed it !")


def removeAdvertOfId(id_advert: Integer) -> None:
    global userConnect

    try:
        result = session.query(Advert, User).join(User, Advert.id_user ==
                                                  User.id_user).filter(
            and_(User.id_user == userConnect["id"], Advert.id_advert ==
                 id_advert)).one()
        if result:
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
    results = Query(Advert, session)
    if transaction != "":
        results = results.filter(Advert.transaction == transaction)

    if location != "":
        results = results.filter(Advert.location == location)

    if price != math.inf:
        if cmp == "equals":
            results = results.filter(Advert.price == price)
        elif cmp == "inf":
            results = results.filter(Advert.price < price)
        elif cmp == "infEquals":
            results = results.filter(Advert.price <= price)
        elif cmp == "supEquals":
            results = results.filter(Advert.price >= price)
        elif cmp == "sup":
            results = results.filter(Advert.price > price)
        else:
            print("I don't recognize that value of cmp for this research !")

    if description != "":
        results = results.filter(Advert.description == description)

    if id_user != math.inf:
        results = results.filter(Advert.id_user == id_user)

    if id_category != "":
        results = results.filter(Advert.id_category == int(id_category))

    if (transaction == "" and location == "" and price == math.inf and
            description == "" and id_user == math.inf
            and id_category != ""):
        results = Query(Advert, session).all()
    else:
        results = results.all()

    if results:
        header = "{:<10} | {:<15} | {:<15} | {:<15} | {:<10} | {}"
        print(header.format("id_user", "id_category", "transaction", "location",
                            "price", "description"))
        print("-" * 90)  # Ajoute une ligne de séparation

        for row in results:
            # Utilisation de format pour aligner les colonnes
            line = "{:<10} | {:<15} | {:<15} | {:<15} | {:<10.2f} | {}"
            print(line.format(row.id_user, row.id_category, row.transaction,
                              row.location, row.price, row.description))
    else:
        print("there is no records found for your research !")


# findAdvertBaseOnCriterias(transaction="sale")


def makeOfferForAdvert(id_advert: int, price: float) -> None:
    global userConnect
    if userConnect["id"] is not None:
        request = session.query(Offer, ProposeOffer).join(
            ProposeOffer, Offer.id_offer == ProposeOffer.id_offer
        ).filter(
            and_(and_(Offer.price_proposed == price, ProposeOffer.id_advert ==
                      id_advert),
                 ProposeOffer.id_user == userConnect["id"])).first()

        if request:
            print(
                f"You have already make an offer for the advert of id {id_advert}")

        else:
            offer = Offer(state_offer="pending", price_proposed=price)
            session.add(offer)
            session.commit()
            the_propose_offer = ProposeOffer(id_user=userConnect["id"],
                                             id_offer=offer.id_offer,
                                             id_advert=id_advert)

            session.add(the_propose_offer)
            session.commit()

            print(f"offer successfully made for the advert of id {id_advert} ")


# makeOfferForAdvert(4, 20000)


def printAllOffersIMade() -> None:
    global userConnect
    if userConnect["id"] is not None:
        results = session.query(Offer, ProposeOffer, Advert) \
            .join(ProposeOffer, Offer.id_offer == ProposeOffer.id_offer) \
            .join(Advert, Advert.id_advert == ProposeOffer.id_advert) \
            .filter(ProposeOffer.id_user == userConnect["id"]) \
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
        print("you need to login first before executing this command !")


# printAllOffersIMade()


def printOffersOnMyAdvertOfId(id_advert: int = math.inf,
                              state_offer: str = "", printUsers: bool = False,
                              printAdverts: bool = False) -> \
        None:
    results = session.query(ProposeOffer, Offer, Advert, User).join(
        Offer, Offer.id_offer == ProposeOffer.id_offer
    ).join(Advert, Advert.id_advert == ProposeOffer.id_advert).join(
        User.id_user == ProposeOffer.id_user)

    if id_advert != math.inf:
        results = results.filter(Advert.id_advert == id_advert)

    if state_offer != "":
        results = results.filter(Offer.state_offer == state_offer)

    results = results.all()

    for proposeOffer, offer, advert, user in results:
        if printUsers:
            print(f"user_id {user.id_user} offerUserName : {user.username}")

        print(f"offer_id {offer.id_offer} state_offer {offer.state_offer} "
              f"price_proposed {offer.price_proposed}")

        if printAdverts:
            print(f"transaction {advert.transaction} location "
                  f"{advert.location} price {advert.price} "
                  f"description {advert.description}")

        print("\n")


def answerOffer(id_offer: int, answer: str):
    try:
        offer = session.query(Offer).filter(
            Offer.id_offer == id_offer).one_or_none()

        if offer and offer.state_offer == "pending":
            offer.state_offer = answer
            session.commit()
            print("Offer updated successfully.")
        else:
            print(f"No pending offer found with the specified ID {id_offer}.")
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()


# answerOffer(id_offer=10, answer="refused")

# We close the session
session.close()
