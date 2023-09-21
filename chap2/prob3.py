user_name = input("Hi. What's your name? ")
user_old = input("And how old are you? ")
user_weigh = input("Okay, last question. How many pounds do you weigh? ")
print("")
user_old = int(user_old)
dog_old = str(user_old / 7)
print("Did you know that you're just "+ dog_old + "in dog years?")
print("")
user_age = int(user_old)
age_day = user_age * 365
age_second = age_day * 24 * 60 * 60
age_second = str(age_second)
print("But you're also over " + age_second + " seconds old.")
print("")
print("If a small child were trying to ger your attention, your name would become :")
name_res = user_name * 5
print(name_res)
print("")
user_weigh = int(user_weigh)
moon = user_weigh / 6
sun = user_weigh * 27.1
moon = str(moon)
sun = str(sun)
print("Did you know that on the moon you would weigh only " + moon + "pounds?")
print("But on the sun, you'd weigh " + sun + "(but, ah... not for long).")
