import numpy

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
    def addNext(self, node):
        self.next = node
    
class hashtable:
    def __init__(self,length):
        self.list = numpy.empty(shape=length,dtype=Node)
    def add(self,data):
        if self.contains == True:
            return
        value = hash(data) % (self.list).size
        if (self.list[value] == None):
            self.list[value] = Node(data)
        else:
            temp = Node(data)
            temp.next = self.list[value]
            self.list[value] = temp

    def contains(self,data):
        value = hash(data) % (self.list).size
        node = self.list[value]
        if (node == None):
            return False
        while node != None:
            if node.data == data:
                return True
            node = node.next
        return False

