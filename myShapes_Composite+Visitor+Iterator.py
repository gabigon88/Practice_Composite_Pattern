#抽象類別+抽象方法就等於物件導向中的interface
#必須實現interface中的所有函數，否則會編譯錯誤
from __future__ import annotations
from abc import ABCMeta, abstractmethod
from math import pi
import collections.abc

class Visitor(metaclass=ABCMeta): #Visitor
    @abstractmethod
    def visitShapeComposite(self, shapeComposite: ShapeComposite):
        pass

    @abstractmethod
    def visitCircle(self, circle: Circle):
        pass

    @abstractmethod
    def visitRectangle(self, rectangle: Rectangle):
        pass

    @abstractmethod
    def visitTriangle(self, triangle: Triangle):
        pass

class InfoVisitor(Visitor): #Visitor
    def visitShapeComposite(self, shapeComposite: ShapeComposite):
        for shape in shapeComposite: # Iterator pattern
            shape.accept(self)

    def visitCircle(self, circle: Circle):
        print("Circle: radius is %.2f" %circle.radius)

    def visitRectangle(self, rectangle: Rectangle):
        print("Rectangle: width is %.2f, height is %.2f" %(rectangle.width, rectangle.height))

    def visitTriangle(self, triangle: Triangle):
        print("Triangle: base is %.2f, height is %.2f" %(triangle.base, triangle.height))

class Shape(metaclass=ABCMeta): #Component+Visitorable
    @abstractmethod
    def printSelf(self):
        pass

    def is_composite(self) -> bool:
        return False

    @abstractmethod
    def accept(self, visitor: Visitor):
        pass

class ShapeCompositeIterator(collections.abc.Iterator): #Iterator
    def __init__(self, shapeSet: set):
            self._shapeSet = shapeSet
            self.length = len(shapeSet)
            self.index = -1

    def __next__(self):
        self.index = self.index + 1
        if self.index == self.length:
            raise StopIteration
        return self._shapeSet.pop()

class ShapeComposite(Shape, collections.abc.Iterable): #Composite+Visitorable+Iterable
    def __init__(self):
        self._children = set()

    def __iter__(self):
        return ShapeCompositeIterator(self._children)

    def printSelf(self, layer: int = 0):
        print("ShapeComposite:")
        for child in self._children:
            print('  ' * layer + '└─', end="")
            if (child.is_composite()):
                child.printSelf(layer+1)
            else:
                child.printSelf()
    
    def is_composite(self) -> bool:
        return True

    def add(self, component):
        self._children.add(component)

    def remove(self, component):
        self._children.discard(component)
    
    def accept(self, visitor: Visitor):
        visitor.visitShapeComposite(self)

class Circle(Shape): #Leaf+Visitorable
    def __init__(self, _radius=3):
        self.radius = _radius

    def printSelf(self):
        print("Circle: area is %.3f" %self.area())

    def area(self):
        return self.radius * self.radius * pi
    
    def accept(self, visitor):
        visitor.visitCircle(self)

class Rectangle(Shape): #Leaf+Visitorable
    def __init__(self, _width=3, _height=5):
        self.width = _width
        self.height = _height

    def printSelf(self):
        print("Rectangle: area is %.3f" %self.area())
    
    def area(self):
        return self.width * self.height
    
    def accept(self, visitor):
        visitor.visitRectangle(self)
    
class Triangle(Shape): #Leaf+Visitorable
    def __init__(self, _base=3, _height=5):
        self.base = _base
        self.height = _height

    def printSelf(self):
        print("Triangle: area is %.3f" %self.area())
    
    def area(self):
        return self.base * self.height / 2
    
    def accept(self, visitor):
        visitor.visitTriangle(self)

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

infoVisitor = InfoVisitor()
allShapes.accept(infoVisitor)