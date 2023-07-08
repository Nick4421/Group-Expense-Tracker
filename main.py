from expense import expense as exp

# inst = exp("Nick", ["Nick", "Jack", "Max", "Zack"], 40)
# inst.print_expense()

active = True

while active:
    choice = input("(e)xpense or (q)uit ")
    if choice == "e" or choice == "expense":
        print("Adding expense")
    elif choice == "q" or choice == "quit":
        print("Quit")
        active = False
    else:
        print("Invalid choice")
