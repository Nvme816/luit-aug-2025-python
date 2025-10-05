import random
roll = random.randint(1,6)

guess = int(input('Guess the dice roll:\n'))
if guess == roll:
    print("Correct! They rolled a " + str(roll))
else:
    print("Wrong! They rolled a " + str(roll))


acronyms = {"LOL": "laugh out loud", "IDK": "I don't know", "TBH": " to be honest"}
sentence = "IDK" + ' what happend ' + "TBH"
translation = acronyms.get("IDK") + ' what happened' + acronyms.get("TBH") 

print('sentence:', sentence)
print ('translation:', translation)