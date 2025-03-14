#!/usr/bin/env python3
import ctypes
import ast
import string

members = dir(ctypes)
ob = ctypes.c_int(0)

def get_member():
    member = input("member: ")
    assert all(x in string.ascii_letters + "._" for x in member)
    return eval(f"ctypes.{member}")

def menu():
    print("1. Call ctypes function")
    print("2. Assign object value")
    print("3. Print object value")

    option = int(input("Option: "))
    assert 0 < option < 4
    return option

while True:
    option = menu()
    
    match option:
        case 1:
            fun = get_member()
            ob = fun(ob)
            print("result: ", ob)
        case 2:
            ob.value = ast.literal_eval(input("ob.value: "))
        case 3:
            print("ob.value =", ob.value)