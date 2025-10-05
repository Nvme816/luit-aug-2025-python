print(1+1)
print(105+10)

number = 1
print(number)
print(type(number))

number = "hello"
print(number)
print(type(number))


#section 3 using variables

first_number = 1+1 
print(first_number)
second_number = 105+10
print(second_number)
total = first_number + second_number
print(total)


#section 4 numbers in python

print(2 * 6 * 8)
print(2 / 4)
# float (decimal)
print(type(0.5))
# int (whole number)
print(type(4 * 6))
# modulus (remainder)
print(5 % 3)
print(10 % 2)
print(7.5 % 5)
#pemdas
print(2 * 5 - 1)
print(2 * ( 5 - 1))


#project 1 health potion part 1 and 2
import random
health = 50
difficulty = random.randint(1,3)
potion_health = random.randint(25,50) // difficulty

#project 1 health potion part 2

health = health + potion_health
if difficulty == 1:
    print("Easy mode selected")
elif difficulty == 2:
    print("Medium mode selected")
else:
    print("Hard mode selected")
print(health)

number = round(2.1)
print(number)
numnber = round(1.5)
print(number)
import math
number = math.floor(1.5)
print(number)
number = math.ceil(2.1)
print(number)
number = math.pi
print(number)


#section 5 how to use strings
print("Hello World")
print(type("Hello World"))
message = 'John said to me "I will see you later"'
print(message)

hello = "Hello World!"
print(hello)
#part 2 collecting data template

#ask user for name
name = input("What is your name?: ")
#ask user for age
age = input("What is your age?: ")
#ask user for city
location = input("What city are you located in?: ")
#ask user what they enjoy
hobby = input("What do you most enjoy doing?: ")
#create output text/string formatting
string = "Your name is {} and you are {} years old. You live in {} and your favorite hobby is {}"
output = string.format(name, age, location, hobby)
A = "part" #variable A
B = 1 #variable B
A + str(B) #variables combined
print(A + str(B))
print("{} - {}".format(A,B)) #same as line 94 with - sign
print("{}{}".format(A,B)) #same as line 95 and 94
print("{1} - {0}".format(A,B)) #same as line 96 numbers count up from 0 so A = 0
#print output to screen
print(output)
#rules of prompting: Task, Reference, Context, Evaluation, Iteration


