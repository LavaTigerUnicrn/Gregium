"""
A few easing functions for easing in various applications. 
All functions must take an input from 0 to 1 and 
will always output from 0 to 1.

* This module can be run for visual tests
"""

# Run imports
import math


# Sinusoidal Easing (Both)
def easeInOutSine(progress: float) -> float:
    """
    Generates a sinusoidal in-out easing, will return a value of 0 to 1 based on current progress

    Arguments:
        progress:
            The progress (0 to 1) in which the transition has progressed
    """

    return -0.5 * math.cos(progress * math.pi) + 0.5


# Sinusoidal Easing (In)
def easeInSine(progress: float) -> float:
    """
    Generates a sinusoidal in easing, will return a value of 0 to 1 based on current progress

    Arguments:
        progress:
            The progress (0 to 1) in which the transition has progressed
    """

    return -1 * math.cos(progress * math.pi / 2) + 1


# Sinusoidal Easing (Out)
def easeOutSine(progress: float) -> float:
    """
    Generates a sinusoidal out easing, will return a value of 0 to 1 based on current progress

    Arguments:
        progress:
            The progress (0 to 1) in which the transition has progressed
    """

    return -1 * math.cos(math.pi / 2 * (progress + 1))


# Quadratic Easing (Both)
def easeInOutQuad(progress: float) -> float:
    """
    Generates a quadratic in-out easing, will return a value of 0 to 1 based on current progress

    Arguments:
        progress:
            The progress (0 to 1) in which the transition has progressed
    """

    return 2 * progress**2 if progress < 0.5 else 1 - ((-2 * progress + 2) ** 2) / 2


# Quadratic Easing (In)
def easeInQuad(progress: float) -> float:
    """
    Generates a quadratic in-out easing, will return a value of 0 to 1 based on current progress

    Arguments:
        progress:
            The progress (0 to 1) in which the transition has progressed
    """

    return progress**2


# Quadratic Easing (Out)
def easeOutQuad(progress: int) -> float:
    """
    Generates a quadratic in-out easing, will return a value of 0 to 1 based on current progress

    Arguments:
        progress:
            The progress (0 to 1) in which the transition has progressed
    """

    return 1 - (progress - 1) ** 2


# Monic Polynomial Easing (In)
def easeInMono(progress: float, degree: int) -> float:
    """
    Generates a monic polynomial in easing with a degree of {degree}, will return a value of 0 to 1 based on current progress

    Arguments:
        progress:
            The progress (0 to 1) in which the transition has progressed
    """

    return progress**degree


# Monic Polynomial Easing (In)
def easeOutMono(progress: float, degree: int) -> float:
    """
    Generates a monic polynomial out easing with a degree of {degree}, will return a value of 0 to 1 based on current progress

    Arguments:
        progress:
            The progress (0 to 1) in which the transition has progressed
    """

    return (
        1 - (progress - 1) ** degree
        if degree % 2 == 0
        else 1 + (progress - 1) ** degree
    )


# Monic Polynomial Easing (In-Out)
def easeInOutMono(progress: float, degree: int) -> float:
    """
    Generates a monic polynomial in-out easing with a degree of {degree}, will return a value of 0 to 1 based on current progress

    Arguments:
        progress:
            The progress (0 to 1) in which the transition has progressed
    """

    return (
        2 ** (degree - 1) * progress**degree
        if progress < 0.5
        else (
            1 + ((2 * progress - 2) ** degree) / 2
            if degree % 2 == 1
            else 1 - ((2 * progress - 2) ** degree) / 2
        )
    )
