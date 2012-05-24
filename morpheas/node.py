debug050512_0851 = False #got error testing test_Menu: is needed! L23
#File "C:\BlenderSVN\cmake_all3\bin\2.63\scripts\addons\Ephestos\morpheas\node.py", line 18, in remove_child
#    self.children.remove(node)
#ValueError: list.remove(x): x not in list

class Node(object):

    def __init__(self, name = 'node'):
        self.parent = None
        self.children = []
        self.name = name

    def __repr__(self):
        return 'aNode(' + self.name + ')'

    #Node accessing:

    def add_child(self, node):
        self.children.append(node)
        node.parent = self

    def remove_child(self, node):
        if debug050512_0851:
            print("node.py remove_child; node =  ", node) 
        self.children.remove(node)
        node.parent = None

    #Node functions:

    def get_root(self):
        if self.parent == None:
            return self
        else:
            return self.parent.get_root()

    def get_depth(self):
        if self.parent == None:
            return 0
        else:
            return self.parent.get_depth() + 1

    def get_all_children(self):
        "includes myself"
        result = [self]
        for child in self.children:
            result.extend(child.get_all_children())
        return result

    def get_all_leafs(self):
        result = []
        for element in self.get_all_children():
            if element.children == []:
                result.append(element)
        return(result)

    def get_all_parents(self):
        "includes myself"
        result = [self]
        if self.parent != None:
            result.extend(self.parent.get_all_parents())
        return result

    def get_siblings(self):
        result = []
        for element in self.parent.children:
            if element is not self:
                result.append(element)
        return result

    def get_parent_of_class(self, aClass):
        "answer the first of my parents which is an instance of aClass"
        for element in self.all_parents():
            if isinstance(element, aClass):
                return element
        return None

    def get_child_of_class(self, aClass):
        "answer the first of my children which is an instance of aClass"
        for element in self.all_children():
            if isinstance(element, aClass):
                return element
        return None

