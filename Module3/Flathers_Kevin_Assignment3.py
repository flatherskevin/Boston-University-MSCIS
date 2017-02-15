"""
Author: Kevin Flathers
Last Edited: 02/06/2017
Date Created: 02/01/2017
Course: CS521


This is a simple implementation of python objects. A super class, Pet,
is defined, and subclasses and methods are further created and implemented.
Proper inheritance, polymorphism, and mixin class usage is performed throughout.
"""


class Pet:  # Include Jumper mixin class

    # Create two variables kind and color; assign values
    # Generic pets will be black and have a kind of 'Pet'
    kind = 'pet'
    color = 'black'

    # Give the option to initialize an owner for the pet. Default is simply: Default Owner
    def __init__(self, name, owner='Default Owner'):

        # In the constructor, initialize the pets name
        self.name = name
        self.owner = owner

    def do_tricks(self):

        # Print the name of the pet and that it is doing tricks
        print("{name} is doing tricks!".format( name=self.name))
        # Call the speak method
        self.speak()
        # Call the jump method
        self.jump()

    def speak(self):

        pass

    def jump(self):

        pass


class Jumper:

    # This is a mixin class for jump

    def jump(self):

        # Create jump method that prints that a Pet is jumping and the pets name
        print("{name} is jumping!".format(name=self.name))


class Dog(Pet):  # You will need to inherit for this to work

    # Change kind to canine
    kind = 'canine'

    def __str__(self):

        # Print the name and description of dog
        print("{name} is a {color} {kind}".format(name=self.name, color=self.color, kind=self.kind))

    def __call__(self, action):

        try:
            if action is 'Rollover':
                # Rollover action prints the name of the dog and that it is rolling over
                print("{name} is rolling over!".format(name=self.name))
            elif action is 'Owner':
                # Owner action returns the name of the owner
                return self.owner
            else:
                raise PetError("This action does not exist. Try using 'Owner' or 'Rollover'")
        except PetError as err:
            print("""
                {error}
                was raised with
                {name}, {color}, {kind}
            """.format(error=err, name=self.name, color=self.color, kind=self.kind))


class BigDog(Dog):  # You will need to inherit for this to work

    # Change the color to tan
    color = 'tan'

    def __str__(self):

        # Print the name and description of BigDog
        print("{name} is a {color} {kind}".format(name=self.name, color=self.color, kind=self.kind))

    def speak(self):

        # Print dogs name and what it says
        print("{name} says, '*BARK* I'm a big dog *BARK*'".format(name=self.name))


class SmallDog(Dog):  # You will need to inherit for this to work

    # Change the color to brindle
    color = 'brindle'

    def __str__(self):

        # Print the name and description of SmallDog
        print("{name} is a {color} {kind}".format(name=self.name, color=self.color, kind=self.kind))

    def speak(self):

        # Print dogs name and what it says
        print("{name} says, '*BARK* I'm a small dog *BARK*'".format(name=self.name))


class Cat(Pet):  # You will need to inherit for this to work

    # Change the kind to feline
    kind = 'feline'

    def __str__(self):

        # Print the name and description of cat
        print("{name} is a {color} {kind}".format(name=self.name, color=self.color, kind=self.kind))

    def speak(self):

        # Print cats name and what it says
        print("{name} says, '*MEOW* I'm a cat *MEOW*'".format(name=self.name))

    def climb(self):

        # Prints the name of the cat and that it is climbing
        print("{name} is climbing!".format(name=self.name))


class HouseCat(Cat):  # You will need to inherit for this to work

    # Change the color to white
    color = 'white'

    def __str__(self):

        # Print the name and description of cat
        print("{name} is a {color} {kind}".format(name=self.name, color=self.color, kind=self.kind))

    def speak(self):

        # Print cats name and what it says
        print("{name} says, '*MEOW* I'm a house cat *MEOW*'".format(name=self.name))


class PetError(Exception):
    pass

###########################################

# EXERCISE YOUR CODE

#    1. Instantiate each class(except jumper)

pet = Pet('Brandy', owner='Kevin')
dog = Dog('Scotch', owner='Kevin')
big_dog = BigDog('Jameson', owner='Kevin')
small_dog = SmallDog('Lager', owner='Kevin')
cat = Cat('Whiskey', owner='Kevin')
house_cat = HouseCat('Pinot Noir', owner='Kevin')

#    2. Create a list of the instantiated objects
pet_list = [pet, dog, big_dog, small_dog, cat, house_cat]

#    3. Loop through the objects
for animal in pet_list:

    # 4. Print __str__
    print(animal.__str__())
    # 5. print the kind of pet
    print(animal.kind)
    # 6. Print the Color of the pet
    print(animal.color)
    # 7. Have the pet do tricks
    animal.do_tricks()

    # 8. if applicable, print rollover action and the owners name
    if animal.kind == 'canine':
        animal.__call__('Rollover')
        print("{owner} is the owner of {name}".format(owner=animal.__call__('Owner'), name=animal.name))
    # 9. If applicable, have the pet climb
    if animal.kind == 'feline':
        animal.climb()
    # 10. To separate each pet print underscores
    print("\n_______________________________________________\n")
