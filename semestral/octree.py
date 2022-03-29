import math

def getOctant(color, level = 0):
    if level > 7:
        raise ValueError("Level must be smaller than 8.")
    # level determines which bit to look at
    # if xBit is equal to the bitvalue at the position given by level
    rBit = color[0] >> (7 - level) & 1
    gBit = color[1] >> (7 - level) & 1
    bBit = color[2] >> (7 - level) & 1
    # returns 0bRGB (number 0 - 7)
    return rBit << 2 | gBit << 1 | bBit

class Node:
    def __init__(self):
        self.rgb = None
        self.isParent = False
        self.children = [None for _ in range(8)]
    
    def addColor(self, color, level = 0):
        # node is empty
        if not self.isParent and not self.rgb:
            self.isParent = True
            octant = getOctant(color, level)
            self.children[octant] = Node()
            self.children[octant].rgb = color
            return
        # node has color but no children
        if not self.isParent and self.rgb:       
            self.isParent = True
            thisOctant = getOctant(self.rgb)
            self.children[thisOctant] = Node()
            self.children[thisOctant].addColor(self.rgb, level + 1)
            self.rgb = None
        # node has children
        octant = getOctant(color, level)
        if not self.children[octant]:
            self.children[octant] = Node()
        self.children[octant].addColor(color, level + 1)

    def getAllColors(self):
        colors = []
        if self.rgb:
            colors.append(self.rgb)
        for child in self.children:
            if child:
                colors += child.getAllColors()
        return colors


    def print(self, level = 0):
        if self.rgb:
            print(f"{self.rgb} level: {level - 1} id: {getOctant(self.rgb, level - 1)}")
        for child in self.children:
            if child:
                child.print(level + 1)



def findCandidates(subtree, color, level = 0):                                                                                                             
    if subtree.rgb:
        return [subtree.rgb]

    octant = getOctant(color, level)
    if subtree.children[octant]:
        return findCandidates(subtree.children[octant], color, level + 1)
    
    else:
        return subtree.getAllColors()

def NNS(colorPalette, pixel):
    shortestDistance = float('inf')
    for color in colorPalette:
        distance = math.dist(pixel, color)
        if distance < shortestDistance:
            closestColor = color
            shortestDistance = distance
    return closestColor

class Octree:
    def __init__(self):
        self.root = Node()

    def addColor(self, color):
        self.root.addColor(color)

    def print(self):
        self.root.print()

    def fill(self, palette):
        for color in palette:
            self.addColor(color)

    def findClosest(self, color):
        if color[0] < 0 or color[1] < 0 or color[2] < 0 or color[0] > 255 or color[1] > 255 or color[2] > 255:
            print(color)
        if not self.root.isParent:
            raise ValueError("Not enough colors in this palette.")
        candidates = findCandidates(self.root, color)
        return NNS(candidates, color)
