import random
answer = random.randint(1, 100)
count = 0
print("\t\t\tWelcome to 'Guess My Number'!\n\nI'm thinking of a number between 1 and 100.\nTry to guess it in as few attempts as possible\n\n")
while True:
    user_guess = int(input("Take a guess: "))
    count += 1
    if user_guess < answer:
        print("Higher...")
    elif user_guess > answer:
        print("Lower...")
    else:
        print(f"You guessed it! The number was {answer}")
        print(f"And it only took you {count} tries!")
        break