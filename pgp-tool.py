import argparse
from classes import *

# Call function for chosen tool
def call_function(option):
    if option == 1:
        Message.encrypt()
    elif option == 2:
        Message.decrypt()
    elif option == 3:
        List.list()
    elif option == 4:
        Keys.gen_key()
    elif option == 5:
        Keys.del_key()
    elif option == 6:
        Keys.import_pubkey()
    elif option == 7:
        Keys.show_pubkey()
    elif option == 8:
        Keys.show_privkey()
    elif option == 9:
        Keys.sign_key()
    elif option == 10:
        Keys.edit_key()
    else:
        print("Invalid option")

# Show CLI and get function to use
def start():
    CLI.banner()
    CLI.show_options()
    option = CLI.select_option()
    call_function(option)
    again = str(input("Do you want to do something else (y/n): "))
    if again == "y":
        start()
    elif again == "n":
        exit
    else:
        print("Invalid option")

start()


