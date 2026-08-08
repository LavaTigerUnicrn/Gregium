class vector2:
    
    x:float
    y:float
    
    def __init__(self,x:float,y:float):
        """
        Makes a new vector
        
        Arguments:
            x:
                The x position of the vector
            y:
                The y position of the vector
        """
        
        self.x = x
        self.y = y
        
    @classmethod
    def from_tuple(cls,instance:tuple):
        
        return cls(instance[0],instance[1])
    
    def __getitem__(self,index:int):

        if index > 1:
            raise IndexError("Vector only has components (x,y)")

        if index == 0:
            return self.x
        return self.y
        
    def __add__(self,other:"vector2") -> "vector2":
        
        return vector2(self.x+other.x,self.y+other.y)
        
    def __mul__(self,times:float) -> "vector2":
        
        return vector2(self.x*times,self.y*times)
        
    def __truediv__(self,times:float) -> "vector2":
        
        return vector2(self.x/times,self.y/times)
        
    def __str__(self):
        
        return f"({self.x},{self.y})"
        
    def __repr__(self):
        
        return f"({self.x},{self.y})"
        
    def distance(self,other:"vector2") -> float:
        """
        Finds absolute distance from other vector
        """
        
        return ((other.x-self.x) ** 2 + (other.y-self.y)**2)**(1/2)
    
    def relative(self,other:"vector2") -> "vector2":
        """
        Finds the relative distance (to 1) to the other vector
        """
        
        x,y = other.x - self.x, other.y - self.y
        magnitude = self.distance(other)
        
        if magnitude == 0:
            return vector2(0,0)
            
        return vector2(x/magnitude,y/magnitude)
        
    def magnitude(self) -> float:
        """
        Gets the hypotenuse of the vector
        """

        return (self.x ** 2 + self.y ** 2) ** (1/2)
    
    def direction(self) -> "vector2":
        """
        Gets the relative values of the direction of the vector (0-1)
        
        (Basically just the unit vector)
        """

        magnitude = self.magnitude()
        if magnitude == 0:
            return vector2(0,0)
        return vector2(self.x/magnitude,self.y/magnitude)