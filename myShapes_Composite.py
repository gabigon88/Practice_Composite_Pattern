#抽象類別+抽象方法就等於物件導向中的interface
#必須實現interface中的所有函數，否則會編譯錯誤
from abc import ABCMeta, abstractmethod
from math import pi

class Shape(metaclass=ABCMeta): #Component
    @abstractmethod
    def printSelf(self):
        pass

    def is_composite(self) -> bool:
        return False

class ShapeComposite(Shape): #Composite
    def __init__(self):
        self._children = set()

    def printSelf(self, layer: int = 0):
        print("ShapeComposite: ")
        for child in self._children:
            print('  ' * layer + '└─', end="")
            if (child.is_composite()):

                child.printSelf(layer+1)
            else:
                child.printSelf()

    def is_composite(self) -> bool:
        return True

    def add(self, component: Shape):
        self._children.add(component)

    def remove(self, component: Shape):
        self._children.discard(component)

class Circle(Shape): #Leaf
    def __init__(self, _radius=3):
        self.radius = _radius

    def printSelf(self):
        print("Circle: area is %.3f" %self.area())

    def area(self):
        return self.radius * self.radius * pi

class Rectangle(Shape): #Leaf
    def __init__(self, _width=3, _height=5):
        self.width = _width
        self.height = _height

    def printSelf(self):
        print("Rectangle: area is %.3f" %self.area())
    
    def area(self):
        return self.width * self.height

class Triangle(Shape): #Leaf
    def __init__(self, _base=3, _height=5):
        self.base = _base
        self.height = _height

    def printSelf(self):
        print("Triangle: area is %.3f" %self.area())
    
    def area(self):
        return self.base * self.height / 2

#-----------執行測試-----------
circle1 = Circle()

rectangle1 = Rectangle()
rectangle2 = Rectangle(5, 7)
rectangleList = ShapeComposite()
rectangleList.add(rectangle1)
rectangleList.add(rectangle2)

triangle1 = Triangle()
triangle2 = Triangle(6, 8)
triangleList1 = ShapeComposite()
triangleList2 = ShapeComposite()
triangleList1.add(triangle1)
triangleList1.add(triangleList2)
triangleList2.add(triangle2)

allShapes = ShapeComposite()
allShapes.add(circle1)
allShapes.add(rectangleList)
allShapes.add(triangleList1)
allShapes.printSelf()