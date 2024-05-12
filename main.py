from typing import Dict, Callable

from request import *

finished_app: bool = True
isLogin: bool = False


def enterCommand() -> str:
    request: str = input("enter a command : ").lower()
    return request


def login():
    global isLogin
    print("login's trial")
    name: str = input("enter your name : ").lower()
    passwd: str = input("enter your password : ").lower()
    isLogin = connectAsUser(name, passwd)


def logout():
    global finished_app, isLogin
    if isLogin:
        finished_app = False
        disConnect()
        isLogin = False


def createAccount():
    print("creation of an account : ")
    name: str = input("enter a name : ").lower()
    password: str = input("enter a password : ").lower()
    email: str = input("enter a email [Optional] : ").lower()
    addUser(name, password, email)


def removeAdvert():
    global isLogin
    if isLogin:
        advert_id: str = input("enter the id of the advert to remove (the id is "
                               "a number) : ")
        if advert_id.isdigit():
            removeAdvertOfId(int(advert_id))
        else:
            print(f"your input {advert_id} is not a digit ")
    else:
        print("you have to login first before making this command \n")


def publishAdvert():
    if isLogin:
        transaction: str = input(
            "enter a transaction value [e.g: sale, rent] : ").lower()
        location: str = input(
            "enter the location for the advert [e.g: paris] : ").lower()
        price: str = input("enter the price for your advert [e.g: 2000.0] : ")
        categoryId: str = input(
            "enter the category's id of your car (your value "
            "should be "
            "between 1 and 5) : ")
        description: str = input("enter a description for your advert : (less "
                                 "than 50 characters) : ").lower()

        if categoryId.isdigit() and price.isdigit():
            publishTheAdvert(transaction, location, float(price), categoryId,
                             description)
    else:
        print("you have to login first before making this command \n")


def modifyAdvert() -> None:
    global isLogin

    if isLogin:
        advert_id: str = input("enter the id of the advert you want to modify"
                               " (value should be a digit) : ")
        newTransaction: str = input("enter the new transaction value [e.g: "
                                    "sale, rent] : ").lower()
        newLocation: str = input("enter the new location for the advert [e.g: "
                                 "paris] : ").lower()
        newPrice: str = input("enter the new price for your advert [e.g: "
                              "2000.0] : ")
        newDescription: str = input("enter a new description for your advert "
                                    ": (less than 50 characters) : ").lower()

        if newPrice.isdigit() and advert_id.isdigit():
            modifyTheAdvert(id_advert=int(advert_id),
                            newTransaction=newTransaction,
                            newLocation=newLocation,
                            newPrice=float(newPrice),
                            newDescription=newDescription)
    else:
        print(f"you have to connect first before making this command !")


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
}


def analyzeCmd(command: str) -> None:
    try:
        function_to_call: Callable = allCommands.get(command, None)
        if function_to_call:
            function_to_call()
        else:
            print("Command not valid, try again!")
    except Exception as e:
        print(f"An error occurred: {e}")


while finished_app:
    cmd: str = enterCommand()
    analyzeCmd(cmd)
