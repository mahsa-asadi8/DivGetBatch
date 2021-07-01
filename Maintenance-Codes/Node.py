class Node:

    def __init__(self,parent, level, id):
        self.parent = parent
        self.level = level
        self.id = id
        self.numberOfElement = 0
        self.numberOfChildren = 0
        self.children = []
        self.elementIds = []

    def setChildren(self,children):
        self.children.append(children)
        self.numberOfChildren = self.numberOfChildren + 1

    def insertElement(self,item):
        self.elements.append(item)
        self.numberOfElement =  self.numberOfElement + 1

    def setAllElements(self,elements):
        self.elements = elements