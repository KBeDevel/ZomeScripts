import sys
from decimal import Decimal

def get_value(value):
	phi = Decimal((1 + 5**(1/2))/2)

	up_value = Decimal(value) * phi
	down_value = Decimal(value) / phi

	return { float(up_value), float(down_value) }

if __name__ == "__main__":
	print(get_value(sys.argv[1]))
