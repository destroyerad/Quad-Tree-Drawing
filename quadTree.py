import pygame as pg
import random as rand
import sys

class Point:
    def __init__(self,x, y):
        self.x = x
        self.y = y

class Node:
    def __init__(self, tL, bR, data = None, previousNode = None, topLeftNode = None, topRightNode = None, bottomRightNode = None, bottomLeftNode = None):
        self.previousNode = previousNode
        self.next = [topLeftNode, topRightNode, bottomRightNode, bottomLeftNode]
        self.topLeft = tL
        self.bottomRight = bR
        self.data = 0

class QuadTree:
    def __init__(self, width : int, height : int):
        if width != height:
            raise Exception("Dimensions are unequal")
        self.leafNode = Node(Point(0,0), Point(width, height))
        self.width = width
        self.height = height

    def inBoundary(self, position):
        return 0 <= position.x < self.width and 0 <= position.y < self.height

    def updateTree(self, node):
        while node.previousNode != None:
            node = node.previousNode
        self.leafNode = node
        
    def addPosition(self, position, item=0):
        currentNode = self.leafNode
        if not self.inBoundary(position):
            return
        recursion = 0
        while abs(currentNode.bottomRight.x - currentNode.topLeft.x) > 1 and abs(currentNode.bottomRight.y - currentNode.topLeft.y) > 1:
            xAverage = (currentNode.bottomRight.x + currentNode.topLeft.x) / 2
            yAverage = (currentNode.bottomRight.y + currentNode.topLeft.y) / 2
            if xAverage >= position.x: # left
                if yAverage >= position.y: # top
                    if currentNode.next[0] == None:
                        currentNode.next[0] = Node(Point(currentNode.topLeft.x, currentNode.topLeft.y), Point(xAverage, yAverage), None, currentNode)
                    currentNode = currentNode.next[0]
                else: # bottom
                    if currentNode.next[3] == None:
                        currentNode.next[3] = Node(Point(currentNode.topLeft.x, yAverage), Point(xAverage, currentNode.bottomRight.y), None, currentNode)
                    currentNode = currentNode.next[3]
            else: # right
                if yAverage >= position.y: # top
                    if currentNode.next[1] == None:
                        currentNode.next[1] = Node(Point(xAverage, currentNode.topLeft.y), Point(currentNode.bottomRight.x, yAverage), None, currentNode)
                    currentNode = currentNode.next[1]
                else: # bottom
                    if currentNode.next[2] == None:
                        currentNode.next[2] = Node(Point(xAverage, yAverage), Point(currentNode.bottomRight.x, currentNode.bottomRight.y), None, currentNode)
                    currentNode = currentNode.next[2]
        currentNode.data = item
        self.updateTree(currentNode)

    def drawNode(self, screen, node):
        pg.draw.rect(screen, (0, 255, 0), (node.topLeft.x, node.topLeft.y, node.bottomRight.x - node.topLeft.x, node.bottomRight.y - node.topLeft.y), 1)
        for child_node in node.next:
            if child_node is not None:
                self.drawNode(screen, child_node)
    
    def draw(self, screen):
        self.drawNode(screen, self.leafNode)
        

class Main:
    def __init__(self, width, height):
        pg.init()
        self.screen = pg.display.set_mode((width, height))
        self.width, self.height = width, height
        self.clock = pg.time.Clock()
        self.reset()
        
    def reset(self):
        self.quadTree = QuadTree(self.width, self.height)
        for i in range(90):
            self.quadTree.addPosition(Point(rand.randint(0,self.width), rand.randint(0,self.height)),1)
    
    def kill(self):
        pg.quit()
        sys.exit()

    def checkEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.kill()
    
    def run(self):
        while True:
            self.checkEvents()
            self.screen.fill((0,0,0))
            self.quadTree.draw(self.screen)
            pg.display.update()
            self.clock.tick(60)
        
if __name__ == '__main__':
    main = Main(500,500)
    main.run()
