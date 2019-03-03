b = None
class Foo:
	def mes(self):
		global b
		b = "fee"

f = Foo()
f.mes()

print b