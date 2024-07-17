from Map import Map
from Particles import Particles


#Init map
myMap = Map()
myMap.init(10,10)
#Init Particles
particles = Particles()
'''
Arguments:
1st: MAP
2nd: number of rabbits
3rd: number of wolves
4th: Number of max iterations
'''
particles.init(myMap, 900, 100, 5000)
#Let the game begins
particles.lifeCycle()
