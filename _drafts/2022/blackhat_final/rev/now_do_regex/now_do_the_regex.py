#!/usr/local/bin/python
import re

def login(usr):
    if re.match("(\w)\\1+([a-z]){7}[0-9]+@[(?i)(B)][^A-G,^I-Z,^a-z0-9]\.MEE{0}A", usr):
        print(open("flag.txt", "r").read())
        return True
    else:
        return False

def main():
    print("Log into the system to claim the flag!!")
    
    while True:
        usr = input()

        if login(usr):
            break

        print("Wrong user")        

if __name__ == "__main__":
    main()
