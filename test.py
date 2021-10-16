class Child:
	parentObj = None
	def __init__(self, parentObj):
		self.parentObj = parentObj
		print("I'm a child")
		parentObj.countUP()
		print(parentObj.no)
class Parent:
	no = 0
	def __init__(self):
		print("I'm a parent")
		child1 = Child(self)
		child2 = Child(self)
		child3 = Child(self)
		child4 = Child(self)
	def countUP(self):
		self.no += 1
		print("now, no is ", self.no)
		


parent = Parent()
