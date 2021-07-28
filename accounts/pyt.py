
def dec_a(func): #here func refers to dec_b.wrap_b
	print("inside decorator A")
	def wrap_a(*args, **kwargs):
		print("inside wrapper A")
		return func(*args, **kwargs) #calls dec_b.wrap_b
	return wrap_a



def dec_b(func): #here func refers to my_func
	print("inside decorator B")
	def wrap_b(*args, **kwargs):
		print("inside wrapper B")
		return func(*args, **kwargs) #calls my_func
	return wrap_b


@dec_a
@dec_b
def my_func():
	print("Inside function")

my_func()

"""
inside decorator B
inside decorator A
inside wrapper A
inside wrapper B
Inside function

"""