rizz_list = ["rizz", "sigma", "gyatt", "slay", "glaze"]
print("Welcome to this sanity (rizz) check!")
while True:
    print("\n1. Check rizz")
    print("2. How do i rizz?")
    print("3. Exit")
    choice = input("Enter your choice (1-3)\n> ")
    if choice == "1":
        rizz = input("Enter your rizz\n>")
        if all(r in rizz for r in rizz_list):
            print("OMG you got amazing rizz, here's the flag!")
            print(open("flag.txt", "r").read())
            break
        else:
            print("You have bad rizz!")
    elif choice == "2":
        print("Here is how to rizz:\n")
        print(open(__file__, "r").read())
    elif choice == "3":
        break
