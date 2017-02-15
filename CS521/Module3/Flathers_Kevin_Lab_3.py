class Parent:
	greeting = "Hi, I'm a parent object."
	
class ChildA(Parent):
	greeting = "Hi, I am a child object."
	
class ChildB(Parent):
	pass
	

parent = Parent
child_a = ChildA
child_b = ChildB

# Print greeting to console
print("Using solely the greeting instance")
print(parent.greeting)
print(child_a.greeting)
print(child_b.greeting)

# Print greeting to console using __str__()
print("\nUsing the __str__() attribute...")
print(parent.__str__(parent.greeting))
print(child_a.__str__(child_a.greeting))
print(child_b.__str__(child_b.greeting))
