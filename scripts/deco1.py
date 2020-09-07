import math

from decorators import *


@do_twice
def return_greting(name):
    print("Creaing greeting")
    return f"Hi {name}"


print(return_greting("Kitty"))


@slow_down
def countdown(from_number):
    if from_number < 1:
        print("Liftoff!")
    else:
        print(from_number)
        countdown(from_number - 1)


math.factorial = debug(math.factorial)


def approximate_e(terms=18):
    return sum(1 / math.factorial(n) for n in range(terms))


@timer
def waste_some_time(num_times):
    for _ in range(num_times):
        sum([i ** 2 for i in range(10000)])


class TimeWaster:
    @debug
    def __init__(self, max_num):
        self.max_num = max_num

    @timer
    def waste_time(self, num_times):
        for _ in range(num_times):
            sum([i ** 2 for i in range(self.max_num)])


@timer
class TimeWaster2:
    def __init__(self, max_num):
        self.max_num = max_num

    def waste_time(self, num_times):
        for _ in range(num_times):
            sum([i ** 2 for i in range(self.max_num)])


@debug
@do_twice
def greet2(name):
    print(f"Hello {name}")


@repeat(num_times=4)
def greet(name):
    print(f"Hello {name}")


@repeat
def say_whee2():
    print("Whee!")


@count_calls
def say_whee3():
    print("Whee!")


@CountCalls
def say_whee4():
    print("Whee!")


@slowdown(rate=2)
def countdown2(from_number):
    if from_number < 1:
        print("Liftoff!")
    else:
        print(from_number)
        countdown(from_number - 1)


@set_unit("cm^3")
def volume(radius, height):
    return math.pi * radius ** 2 * height


@use_unit("meters per second")
def average_speed(distance, duration):
    return distance / duration


@swap_func_args({"dog": "cat"})
def hello_kitty(cat="meow"):
    print(f"Cat says {cat}")


waste_some_time(999)
approximate_e(5)
countdown(3)
tw = TimeWaster(1000)
tw.waste_time(999)
tw = TimeWaster(1000)
greet2("Eva")
say_whee2()
say_whee3()
say_whee3()
print(f"{say_whee3.count_calls} is count_calls")
counter = Counter()
counter()
counter()
counter()
counter()
counter()
say_whee4()
say_whee4()
say_whee4()
say_whee4()
print(f"{say_whee4.num_calls} is count_calls")
countdown2(3)
volume(3, 5)
print(volume.unit)
bolt = average_speed(100, 9.58)
print(bolt)
print(bolt.to("km per hour"))
print(bolt.to("mph").m)
hello_kitty(dog="meow")
