# %%
import math
import numpy as np
import pytest
import time, sys
import random
import secrets
import requests
from requests.models import Response
import json
import textwrap

# %%

# Introduction, Get to Know
def introduction():
    print("Hello, and welcome to Free Think")
    for i in range(7):
        sys.stdout.write("   ")
        x = i % 4
        sys.stdout.write('\r' + "." * x )
        time.sleep(0.2)
        sys.stdout.flush()
    print("My name is Claud")
    time.sleep(1)
    print("")
    name = input("What is your name? ")
    print("")
    time.sleep(1.5)
    print(f"Welcome {name.capitalize()}, it is so good to have you here.")
    print("")   

# %%

# Do you have a favorite Animal
def animal():
    animals = ["cat", "dog", "turtle", "bird", "fish", "chicken"]
    r_animal = secrets.choice(animals)
    time.sleep(1)
    print()
    while True:
        a = input("Do you like animals? \nYes or No : ").lower()
        if a == "yes":
            print("")
            time.sleep(1)
            print("Oh good, I am glad to hear that")
            time.sleep(1)
            print(f"I like animals as well, especially {r_animal}s. ")
            print("")
            break
        elif a == "no":
            print("")
            time.sleep(1)
            print("Me neither, they are alot of work")
            time.sleep(1)
            print(f"But, if I did like animals, I would like {r_animal}s. ")
            print("")
            break
    

# %%

# Where would you like to travel
def travel():
    print()
    foods = ["Pyramids", "Great Wall of China", "Machu Pichu", "Grand Canyon", "Rome", "Yellowstone"]
    random1 = secrets.choice(foods)
    random2 = secrets.choice(foods)

    if random1 == random2:
        random2 = secrets.choice(foods)

    while True:
        try:
            print("")
            location = int(input(f"Would you rather visit (1): {random1} or (2): {random2}? (number): "))
            if location == 1:
                time.sleep(1.5)
                print("I want to go there too!")
                print("")
                break
            elif location == 2:
                time.sleep(1.5)
                print("Interesting Choice.")
                print("")
                break
            else:
                print("Please pick either 1 or 2")            
        except ValueError:
            print("That was no valid number.  Try again...")
            print("")
                
# %%

# Guess how fast this animal can swim.
def speed():
    fish = {"Sailfish": 68, "Swordfish": 60, "Marlin": 50, "Pilot Whale": 47, "Flying Fish": 35, "Killer Whale":34}
    entry_list = list(fish.items())
    random_entry = random.choice(entry_list)
    attempts = 0
    time.sleep(1.5)
    print("Oh, I have another fun game! \n Let's see if you can guess how fast this animal swims underwater.")
    time.sleep(1.5)
    print(f'Guess how fast a {random_entry[0]} can move in water (mph): ')
    while True:
        try:
            guess = input("What is your guess?: ")
            guess = float(guess)
            attempts = attempts + 1
            if guess == random_entry[1]:
                if attempts <= 5 and attempts >1:
                    print(f"Wow!, you are good, it took only {attempts} guess!")
                    print("")
                    break
                elif attempts == 1:
                    print("Great Job, you got it in 1 Try!")
                    print("")
                    break
                else:
                    print(f"Well done, you got it in {attempts} attempts.")
                break
            elif guess > random_entry[1]:
                print("Slower")
            elif guess < random_entry[1]:
                print("Faster")
        except ValueError:
            print("That was no valid number.  Try again...")
    
    time.sleep(2)

# %%

# What is your horoscope
def horoscope():
    print("While you are here, lets check out your horoscope.")
    while True:
        try:
            day = int(input("Input date of birth: "))
            if day > 31:
                print("That isn' possible, try again")
                day = int(input("Input date of birth: "))
            break
        except ValueError:
            print("That was no valid number.  Try again...")
    while True:
        month = str(input("Input month of birth (e.g. march, july etc): "))
        month= month.lower()
        if month != "december" and month !="january" and month!="february" and month !="march" and month !="april" and month !="may" and month !="june" and month !="july" and month !="august" and month !="september" and month !="october" and month !="november":
            print("That is not a possible month try again")
        else:
            break
    month = month.lower()   
    if month == 'december':
        astro_sign = 'Sagittarius' if (day < 22) else 'capricorn'
    elif month == 'january':
        astro_sign = 'Capricorn' if (day < 20) else 'aquarius'
    elif month == 'february':
        astro_sign = 'Aquarius' if (day < 19) else 'pisces'
    elif month == 'march':
        astro_sign = 'Pisces' if (day < 21) else 'aries'
    elif month == 'april':
        astro_sign = 'Aries' if (day < 20) else 'taurus'
    elif month == 'may':
        astro_sign = 'Taurus' if (day < 21) else 'gemini'
    elif month == 'june':
        astro_sign = 'Gemini' if (day < 21) else 'cancer'
    elif month == 'july':
        astro_sign = 'Cancer' if (day < 23) else 'leo'
    elif month == 'august':
        astro_sign = 'Leo' if (day < 23) else 'virgo'
    elif month == 'september':
        astro_sign = 'Virgo' if (day < 23) else 'libra'
    elif month == 'october':
        astro_sign = 'Libra' if (day < 23) else 'scorpio'
    elif month == 'november':
        astro_sign = 'scorpio' if (day < 22) else 'sagittarius'
    else:
        print("not an option")
    print("Your Astrological sign is :",astro_sign)
    for i in range(4):
        sys.stdout.write("   ")
        x = i % 4
        sys.stdout.write('\r' + ".." * x )
        time.sleep(1)
        sys.stdout.flush()
    response = requests.get(f'http://horoscope-api.herokuapp.com/horoscope/today/{astro_sign}')
    scope =response.json()
    dedented_text = textwrap.dedent(scope["horoscope"]).strip()
    print("")
    print (textwrap.fill(dedented_text, width=60))
    print(" \n ")
    time.sleep(4)

# %%

# Temperatures from our the Nation
def temperature():
    places = {"Rigby": {"Latitude": 43.6724, "Longitude" :-111.915}, 
    "Billings": {"Latitude":45.80694, "Longitude" :-108.54222}, 
    "Lancaster": {"Latitude":34.6868,"Longitude" : -118.1542},
    #"Phoenix": {"Latitude":33.4484,"Longitude" : -112.0740},
    "Portland": {"Latitude":45.5051,"Longitude" : -122.6750}}
    where = None

    while where != "done":
        where = (input("Where would you like to know the weather about?" 
        "\n Your options are: \n 1. Rigby \n 2. Billings \n 3. Lancaster \n 4. Portland \n 5. Or type done to leave \n(Write your location): "))
        # I changed the line above by taking out Pheonix. It was number 4 before.
        where = where.capitalize()
        if where == "Done":
            where = str("Done")
            break

        elif where == "Rigby" or where =="Billings" or where =="Lancaster" or where =="Pheonix" or where =="Portland":

            latitude = places[where]["Latitude"]
            longitude = places[where]["Longitude"]
            url = (f"https://api.weather.gov/points/{latitude},{longitude}/forecast")
            try1 = requests.get(url)
            try2 = try1.json()
            for i in range(5):
                sys.stdout.write("   ")
                x = i % 4
                sys.stdout.write('\r' + "." * x )
                time.sleep(1)
                sys.stdout.flush()
            print("")
            temp = (try2["properties"]["periods"][0]["temperature"])
            print(f"The Temperature outside is currently {temp} degrees")
            print(" ")
            again = str(input("Would you like to search again? (y/n): "))
            if again == 'y':
                pass
            elif again =='n':
                print("Okay, have a nice day")
                break
            else:
                print("That is not a possible response")
        
        elif where != ("Rigby" or "Billings" or "Lancaster" or "Pheonix" or "Portland"):
            print("")
            print("Not Valid Response")
            print("")

# %%

def Are_we_there_yet():
    print("Let's say you are going on a trip, and want to know how long your travel is going to be.")
    print("")
    distance = float(input("How far away is your location? (miles): "))
    mph = float(input("And what is your miles per hour?: "))
    value = round(distance / mph,2)
    print("")
    for i in range(5):
        sys.stdout.write("   ")
        x = i % 4
        sys.stdout.write('\r' + "." * x )
        time.sleep(1)
        sys.stdout.flush()
    print(f"The trip will take you about {value} hours")


# %%
def shopping():
    next = None
    shop_list = {}
    print("Okay, time to go shopping. ")
    while True:
        try:
            next = int(input("Would you like to \n(1). Add \n(2). Receipt \n(3). Check-Out \n(4). Leave Store \n(Type number): "))
            print("")
            if next == 1:
                item = str(input("What would like to put in the cart? "))
                cost = float(input("And how much does it cost?: "))
                cost = round(cost,2)
                if cost > 100:
                    print("")
                    sure = str(input("Are you sure this item is over $100.00 (y/n): "))
                    if sure.lower() == "y":
                        shop_list[item] = cost
                        tot = shop_list.values()
                        total = sum(tot)
                    elif sure.lower() == "n":
                        cost = float(input("And how much does it cost?: "))
                        cost = round(cost,2)
                        shop_list[item] = cost
                        tot = shop_list.values()
                        total = sum(tot)
                    else:
                        print("Sorry, I don't understand")
                shop_list[item] = cost
                tot = shop_list.values()
                total = sum(tot)
                print("")
            elif next == 2:
                print("")
                tot = shop_list.values()
                total = round(sum(tot),2)
                print ("{:<10} {:<10}".format('ITEM', 'COST'))
                for item, cost in shop_list.items():
                    print('{:<10} ${:<10}'.format(item, cost))
                print("- - - - - - - - - -")
                print('{:<10} ${:<20}'.format(("Total"),total))
                print("")
            elif next == 3:
                total = round(total, 2)
                print(f"It looks like your total today will be ${total}")
                item_list = list(shop_list.items())
                sale = random.choice(item_list)
                time.sleep(1.2)
                print("")
                print(f"Has anyone told you that there is a sale on -{sale[0]}- today?")
                time.sleep(1.5)
                number = random.randint(2,4)
                discounts = [15, 20, 25, 30, 35]
                the_dis = (random.choice(discounts))
                new_product_price = round((sale[1] * (the_dis/100)) + sale[1] * (number -1),2)
                print("Today you can get {} {}'s for deal of buy {} get one {} percent off. \nThe new total for this product would be ${} instead of ${}".format(number, sale[0], number - 1, the_dis, new_product_price, (sale[1] * number)))
                time.sleep(3)
                accept = str(input("Would you like to accept this discount? (y/n): ")).lower()
                while True:
                    if accept == 'y':
                        print("Okay, lets get that switched")
                        time.sleep(1)
                        shop_list[f"{sale[0]}"] = new_product_price
                        print("")
                        print ("{:<10} {:<10}".format('ITEM', 'COST'))
                        for item, cost in shop_list.items():
                            print('{:<10} ${:<10}'.format(item, cost))
                        print("- - - - - - - - - -")
                        print('{:<10} ${:<20}'.format(("Total"),total))
                        print("")
                        time.sleep(1.2)
                        tot = shop_list.values()
                        total = round(sum(tot),2)
                        print(f'Your new total will be ${total}')
                        print("Thank you for shopping with us today :) ")
                        break
                    elif accept == 'n':
                        print(f"Okay, then your total will be ${total}")
                    else:
                        print("ERROR, either y or n")
                break

            elif next == 4:
                empty=(len(shop_list.keys()))
                if empty == 0:
                    print("Okay, have a nice day")
                    break
                else:
                    time.sleep(1.2)
                    print("Excuse me, you have an item in your cart, you need to pay first.")
                    print("")
                    time.sleep(1)
            else:
                print("Not an option")
        except ValueError:
            print("")
            print("- - - - - - -")
            print("ERROR: Must be a number from the option list")
            print("- - - - - - -")
            print("")
    pass


# %%

introduction()
animal()
speed()
horoscope()
travel()
temperature()
shopping()



# %%
#temperature()
# %%
