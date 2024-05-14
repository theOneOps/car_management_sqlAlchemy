from typing import Dict, Callable

from request import *

finished_app: bool = True
isLogin: bool = False

# function to get a user's input

def enterCommand() -> str:
    request: str = input("enter a command : ").lower()
    return request

# function to ask user to login
def login():
    global isLogin
    print("login's trial")
    name: str = input("enter your name : ").lower()
    passwd: str = input("enter your password : ").lower()
    isLogin = connectAsUser(name, passwd)

# function to disconnect the user
def logout():
    global isLogin
    if isLogin:
        disConnect()
        isLogin = False

# function to create an account
def createAccount():
    print("creation of an account : ")
    name: str = input("enter a name : ").lower()
    if name != "":
        password: str = input("enter a password : ").lower()
        if password != "":
            email: str = input("enter a email [Optional] : ").lower()
            addUser(name, password, email)
        else:
            print("password should not be empty !")
    else:
        print("name should not be empty !")

# function to remove an advert
def removeAdvert():
    global isLogin
    if isLogin:
        advert_id: str = input(
            "enter the id of the advert to remove (the id is "
            "a number)\n[before removing, check your available advertises with "
            "the command 'printmyadvertises' to see their id : ")
        if advert_id.isdigit():
            removeAdvertOfId(int(advert_id))
        else:
            print(f"your input {advert_id} is not a digit ")
    else:
        print("you have to login first before making this command \n")

# function to publish an advert
def publishAdvert():
    if isLogin:
        transaction: str = input(
            "enter a transaction value [e.g: sale, rent] : ").lower()
        if transaction != "":
            location: str = input(
                "enter the location for the advert [e.g: paris] : ").lower()
            if location != "":
                price: str = input(
                    "enter the price for your advert [e.g: 2000] : ")
                if price != "" and price.isdigit():
                    categoryId: str = input(
                        "enter the category's id of your car (your value "
                        "should be "
                        "between 1 and 5) : ")
                    if (categoryId != "" and categoryId.isdigit() and
                            categoryId in ["1", "2", "3", "4", "5"]):
                        description: str = input(
                            "enter a description for your advert : (less "
                            "than 50 characters) : ").lower()

                        publishTheAdvert(transaction, location, float(price),
                                         categoryId,
                                         description)
                    else:
                        print("category's id should be a digit between 1 and 5")
                else:
                    print("price should be a digit !")
            else:
                print("location should not be empty !")

        else:
            print("the transaction should not be empty !")
    else:
        print("you have to login first before making this command \n")

# function to modify an advert
def modifyAdvert() -> None:
    global isLogin

    if isLogin:
        advert_id: str = input("enter the id of the advert you want to modify"
                               " (value should be a digit) \n"
                               "[check your available "
                               "advertises with the command '' to see their id]  : ")
        if advert_id != "":
            newTransaction: str = input("enter the new transaction value [e.g: "
                                        "sale, rent] : ").lower()
            if newTransaction != "":
                newLocation: str = input(
                    "enter the new location for the advert [e.g: "
                    "paris] : ").lower()
                if newLocation != "":
                    newPrice: str = input(
                        "enter the new price for your advert [e.g: "
                        "2000] : ")
                    if newPrice.isdigit():
                        newDescription: str = input(
                            "enter a new description for your advert "
                            ": (less than 50 characters) : ").lower()
                        modifyTheAdvert(id_advert=int(advert_id),
                                        newTransaction=newTransaction,
                                        newLocation=newLocation,
                                        newPrice=float(newPrice),
                                        newDescription=newDescription)
                    else:
                        print("price should be a digit !")
                else:
                    print("location should not be empty !")
            else:
                print("the transaction should not be empty !")
        else:
            print("the advert_id should be a digit !")
    else:
        print(f"you have to connect first before making this command !")

# function to search an Advert on multiple criterias
def searchAdvertOn():
    transaction: str = input(
        "enter a transaction value [e.g: sale, rent] : ").lower()
    location: str = input(
        "enter the location for the advert [e.g: paris] : ").lower()
    price: str = input("enter the price for your advert [e.g: 2000] : ")
    cmp: str = input(
        "enter a comparison value: (there is only 4 values available: \n"
        "[equals] for same price\n,"
        "[inf] for price less than the value you have entered for the price\n, "
        "[infEquals] for price less or equals than the value you have entered for the price\n,"
        "[sup] for price greater than the value you have entered for the price\n,"
        "[supEquals] for price greater ou equals than the value you have entered for the price : ").lower()

    categoryId: str = input(
        "enter the category's id of your car (your value "
        "should be "
        "between 1 and 5) : ")
    description: str = input("enter a description for your advert : (less "
                             "than 50 characters) : ").lower()
    id_user: str = input("enter the id of the user  : ")

    thePrice: float = math.inf
    theUser: int = math.inf
    if transaction != "" or transaction == "":
        if cmp == "":
            cmp = "equals"
        if cmp in ["inf", "equals", "infequals", "supequals", "sup"]:
            if location != "" or location == "":
                if price != "" and price.isdigit():
                    thePrice = float(price)
                if (categoryId in categories_keys) or categoryId == "":
                    if id_user.isdigit():
                        theUser = int(id_user)
                    findAdvertBaseOnCriterias(transaction=transaction,
                                              location=location,
                                              price=thePrice,
                                              id_category=categoryId,
                                              description=description,
                                              cmp=cmp,
                                              id_user=theUser)
                    # print(transaction, location, price, categoryId, description,
                    #       cmp, id_user)

# function to get the history of offers made by user
def printAllOffersImade():
    if isLogin:
        printAllOffersIHaveMade()
    else:
        print("you have to login first before making this command \n")

# function to answer to an offer
def answerOffer():
    if isLogin:
        offer_id = input("Enter the offer Id "
                         "\n [first check all offers you "
                         "have received with : 'printofferonmyadvert to "
                         "see offer's id ']: ")
        if offer_id.isdigit():
            my_answer = input("Enter the answer for that offer \n"
                              "[there is only 3 available answers :\n"
                              "'pending' (the default value of the offer"
                              " if there is an offer) \n,"
                              "'accepted' for accepting the offer\n,"
                              "'refused' for refusing the offer : ").lower()

            if my_answer in ["pending", "refused", "accepted"]:
                answerOfferOfId(int(offer_id), my_answer)
            else:
                print("your answer is not a valid value ! \n")
        else:
            print("your offer_id's value is not a digit ! \n")


    else:
        print("you have to login first before making this command \n")


# function to make and send offer for an advert
def makeOfferOnAdvert():
    if isLogin:
        advert_id: str = input("Enter the advert Id : ")
        if advert_id.isdigit():
            my_price = input("Enter your proposed price for that ")
            if my_price.isdigit():
                makeOfferForAdvert(id_advert=int(advert_id),
                                   price=float(my_price))
            else:
                print("your price is not a digit ! ")
        else:
            print("your advert_id's value is not a digit ! ")
    else:
        print("you should log in first before making this command ! \n")

# function to quit app
def quitApp():
    global finished_app
    if isLogin:
        disConnect()
    finished_app = False

# function to get  help to use this app
def help(cmd: str = ""):
    if cmd == "":
        print("User Functionalities for Car Sales Application:")
        print('you can type help "name of the command" to see its description ')
        print(
            "- Login: Enter 'login' to log in with your username and password.")
        print("- Logout: Enter 'logout' to log out from the application.")
        print(
            "- Create Account: Enter 'createAccount' to create a new account.")
        print(
            "- Display Car Categories: Enter 'printAllCategories' to view "
            "all available car categories.")
        print(
            "- Display All of my Advertisements: Enter 'printMyAdvertises' to "
            "see "
            "all advertisements on the application.")
        print(
            "- Display All Sellers: Enter 'printAllSellers' to view "
            "all sellers except yourself.")
        print(
            "- Display All Cars: Enter 'printAllCars' to see "
            "all available cars with their categories.")
        print(
            "- Modify Advertisement: Enter 'modifyAdvert' to update"
            " an existing advertisement.")
        print(
            "- Search Advertisement: Enter 'searchAdvertOn' to "
            "search for specific advertisements, or to print all advertises if "
            "there is no criterias")
        print(
            "- Make Offer on Advertisement: Enter 'makeOfferOnAdvert' "
            "to place an offer on an advertisement.")
        print(
            "- Display Offers Made: Enter 'printAllOffersIMade'"
            " to view all offers you've made.")
        print(
            "- Answer Offers: Enter 'answerOffer' to accept or reject"
            " offers from other users.")
        print(
            "Print offers you have received from others users : "
            "Enter 'printOfferOnMyAdvert'.")
    else:
        if cmd in command_descriptions.keys():
            print(command_descriptions[cmd])
        else:
            print(f"the command {cmd} doesn't have documentation\n"
                  f"it's not a valid command !")

#function to analyze command
def analyzeCmd(command: str) -> None:
    try:
        cmds = command.split()
        main_cmd: str = cmds[0]
        function_to_call: Callable = allCommands.get(main_cmd, None)
        if function_to_call:
            if len(cmds) > 1:
                function_to_call(cmds[1])
            else:
                function_to_call()
        else:
            print("Command not valid, try again!")
    except Exception as e:
        print(f"An error occurred: {e}")


#function to start the app
def startApp():
    analyzeCmd("help")
    while finished_app:
        cmd: str = enterCommand()
        analyzeCmd(cmd)


#function to get all offer on my advert
def printOfferOnMyAdvert():
    if isLogin:
        theId: int = math.inf
        id_advert: str = input("enter a value's id of one of your advert : ")
        if id_advert.isdigit():
            theId = int(id_advert)
        state_offer: str = input(
            "enter a state of the offer you're searching : \n"
            "the valid values are between ['pending', "
            "'refused',"
            "'accepted'] or nothing : ")
        if (state_offer in ['pending', 'refused',
                            'accepted']) or state_offer == "":
            printOffersOnMyAdvertOfId(theId, state_offer)
        else:
            print("state_offer should be in ['pending', 'refused','accepted']")
    else:
        print("you need to be connect before making this command !")

#list of all commands and the proper functions they called
allCommands: Dict[str, Callable[[], None]] = {
    "login": login,
    "logout": logout,
    "createaccount": createAccount,
    "printallcars": printAllCars,
    "printallcategories": printAllCategories,
    "printmyadvertises": printAllMyAdvertises,
    "removeadvert": removeAdvert,
    "publish": publishAdvert,
    "modifyadvert": modifyAdvert,
    "searchadverton": searchAdvertOn,
    "printalloffersimade": printAllOffersImade,
    "answeroffer": answerOffer,
    "printallsellers": printAllSellers,
    "quit": quitApp,
    "makeofferonadvert": makeOfferOnAdvert,
    "help": help,
    "printofferonmyadvert": printOfferOnMyAdvert,
    "printalladvertisesofseller": printAllAdvertisesOf,
}

#list of help when use the command "help <command>"
command_descriptions = {
    "login": "Log in with your username and password.",
    "logout": "Log out from the application.",
    "createaccount": "Create a new account.",
    "printallcategories": "Display all available car categories.",
    "printmyadvertises": "Display all my advertisements on the application.",
    "printallsellers": "Display all sellers on the platform, including"
                       " you if you have published some adnvertises",
    "printallcars": "Display all available cars with their respective categories.",
    "modifyadvert": "Modify an existing advertisement.",
    "searchadverton": "Search for advertisements based on specific criteria "
                      "or print all advertises if there is no criterias",
    "makeofferonadvert": "Place an offer on a specific advertisement.",
    "printalloffersimade": "Display all offers you've made.",
    "answeroffer": "Accept or reject offers from other users.",
    "printofferonmyadvert": "Print All offers i have received on my advertises."
}
