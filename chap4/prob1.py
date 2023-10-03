import random
mood = random.randint(0, 2)
if mood == 0:
    print(":)")
elif mood == 1:
    print(":|")
elif mood == 2:
    print(":(")
else:
    print("Illegal mood value!")
