"""
A few easing functions for easing in various applications. 
All functions must take an input from 0 to 1 and will always output from 0 to 1.
All functions will output 0 with an input of 0 and 1 with an input of 1
"""
# Run imports
import math


# Sinusoidal Easing (Both)
def easeInOutSine(progress: float) -> float:
    """
    Generates a sinusoidal in-out easing
    
    :param progress: The progress [0-1] in which the transition has progressed
    :type progress: float
    
    :returns: The eased progress from [0-1]
    :rtype: float
    """
    
    return -0.5*math.cos(progress * math.pi)+0.5

# Sinusoidal Easing (In)
def easeInSine(progress: float) -> float:
    """
    Generates a sinusoidal in easing
    
    :param progress: The progress [0-1] in which the transition has progressed
    :type progress: float
    
    :returns: The eased progress from [0-1]
    :rtype: float
    """
    
    return -1*math.cos(progress*math.pi/2) + 1

# Sinusoidal Easing (Out)
def easeOutSine(progress: float) -> float:
    """
    Generates a sinusoidal out easing
    
    :param progress: The progress [0-1] in which the transition has progressed
    :type progress: float
    
    :returns: The eased progress from [0-1]
    :rtype: float
    """
    
    return -1*math.cos(math.pi/2*(progress+1))

# Quadratic Easing (Both)
def easeInOutQuad(progress: float) -> float:
    """
    Generates a quadratic in-out easing
    
    :param progress: The progress [0-1] in which the transition has progressed
    :type progress: float
    
    :returns: The eased progress from [0-1]
    :rtype: float
    """
    
    return 2*progress**2 if progress < 0.5 else 1 - ((-2 * progress + 2)**2)/2

# Quadratic Easing (In)
def easeInQuad(progress: float) -> float:
    """
    Generates a quadratic in-out easing
    
    :param progress: The progress [0-1] in which the transition has progressed
    :type progress: float
    
    :returns: The eased progress from [0-1]
    :rtype: float
    """
    
    return progress ** 2

# Quadratic Easing (Out)
def easeOutQuad(progress:int) -> float:
    """
    Generates a quadratic in-out easing
    
    :param progress: The progress [0-1] in which the transition has progressed
    :type progress: float
    
    :returns: The eased progress from [0-1]
    :rtype: float
    """
    
    return 1-(progress-1)**2

# Monomic Easing (In)
def easeInMono(progress:float,degree:int) -> float:
    """
    Generates a monomic in easing with a degree of {degree}
    
    :param progress: The progress [0-1] in which the transition has progressed
    :type progress: float
    
    :returns: The eased progress from [0-1]
    :rtype: float
    """
    
    return progress**degree

# Monomic Easing (In)
def easeOutMono(progress:float,degree:int) -> float:
    """
    Generates a monomic out easing with a degree of {degree}
    
    :param progress: The progress [0-1] in which the transition has progressed
    :type progress: float
    
    :returns: The eased progress from [0-1]
    :rtype: float
    """
    
    return 1-(progress-1)**degree if degree%2==0 else 1+(progress-1)**degree

# Monomic Easing (In-Out)
def easeInOutMono(progress:float,degree:int) -> float:
    """
    Generates a monomic in-out easing with a degree of {degree}
    
    :param progress: The progress [0-1] in which the transition has progressed
    :type progress: float
    
    :returns: The eased progress from [0-1]
    :rtype: float
    """
    
    return 2**(degree-1) * progress ** degree if progress < 0.5 else (1+((2*progress-2)**degree)/2 if degree%2 == 1 else 1-((2*progress-2)**degree)/2)