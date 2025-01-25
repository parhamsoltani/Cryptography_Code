class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
def point_addition(P1, P2, p, a):
    if P1.x == P2.x and P1.y == P2.y:
        return point_doubling(P1, p, a)
    
    if P1.x == None:
        return P2
    if P2.x == None:
        return P1
        
    # Calculate lambda = (y2-y1)/(x2-x1) mod p
    try:
        lambda_val = ((P2.y - P1.y) * pow(P2.x - P1.x, -1, p)) % p
    except:
        return Point(None, None)  # Point at infinity
        
    # Calculate x3 = lambda^2 - x1 - x2 mod p
    x3 = (lambda_val**2 - P1.x - P2.x) % p
    
    # Calculate y3 = lambda(x1-x3) - y1 mod p
    y3 = (lambda_val * (P1.x - x3) - P1.y) % p
    
    return Point(x3, y3)

def point_doubling(P, p, a):
    if P.x == None:
        return Point(None, None)
    
    # Calculate lambda = (3x^2 + a)/(2y) mod p
    try:
        lambda_val = ((3 * P.x**2 + a) * pow(2 * P.y, -1, p)) % p
    except:
        return Point(None, None)  # Point at infinity
        
    # Calculate x3 = lambda^2 - 2x mod p
    x3 = (lambda_val**2 - 2*P.x) % p
    
    # Calculate y3 = lambda(x-x3) - y mod p
    y3 = (lambda_val * (P.x - x3) - P.y) % p
    
    return Point(x3, y3)

def main():
    # Get curve parameters
    print("Enter elliptic curve parameters:")
    p = int(input("Enter prime modulus p: "))
    a = int(input("Enter coefficient a: "))
    b = int(input("Enter coefficient b: "))
    
    # Get first point
    print("\nEnter first point coordinates:")
    x1 = int(input("x1: "))
    y1 = int(input("y1: "))
    P1 = Point(x1, y1)
    
    # Get second point
    print("\nEnter second point coordinates:")
    x2 = int(input("x2: "))
    y2 = int(input("y2: "))
    P2 = Point(x2, y2)
    
    # Perform point addition
    P3 = point_addition(P1, P2, p, a)
    print("\nPoint Addition Result:")
    print(f"P1 + P2 = ({P3.x}, {P3.y})")
    
    # Perform point doubling
    P4 = point_doubling(P1, p, a)
    print("\nPoint Doubling Result:")
    print(f"2P1 = ({P4.x}, {P4.y})")

if __name__ == "__main__":
    main()
