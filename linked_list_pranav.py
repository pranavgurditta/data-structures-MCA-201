class Node:
    
    '''
    Objective: To represent a linked list node
    '''

    def __init__(self,value):

        '''
        Objective: To instantiate a class object
        Input:
             self: Implicit object of class Node
            value: Value at the node
        Return Value: None
        '''

        self.data = value
        self.next = None

    def __str__(self):

        '''
        Objective: To override the string function
        Input:
             self: Implicit object of class Node
        Return Value: String
        '''

        return str(self.data)

class LinkedList:

    '''
    Objective: To represent a linked list
    '''

    def __init__(self):

        '''
        Objective: To instantiate a class object
        Input:
             self: Implicit object of class LinkedList
        Return Value: None
        '''

        self.head = None


    def insertAtBeg(self,value):

        '''
        Objective: To add a node at the begining of a linked list
        Input:
            self: Implicit object of class LinkedList
            value: Value to be inserted
        Return Value: None
        '''

        temp = Node(value)
        temp.next = self.head
        self.head = temp


    def insertAtEnd(self,temp,value):

        '''
        Objective: To add a node at the begining of a linked list
        Input:
            self: Implicit object of class LinkedList
            value: Value to be inserted
            temp : Current node
        Return Value: None
        '''

        #Approach: Recurssively
        if temp == None:
            self.head = Node(value)
        elif temp.next == None:
            temp.next = Node(value)
        else:
            return self.insertAtEnd(temp.next,value)


    def insertSorted(self,temp,value):

        '''
        Objective: To add a node in a sorted linked list
        Input:
            self: Implicit object of class LinkedList
            value: Value to be inserted
            temp : Current node
        Return Value: None
        '''

        #Approach: Recurssively
        if temp == None:
            self.head = Node(value)
        elif temp == self.head and  value < temp.data:
            newNode = Node(value)
            newNode.next = temp
            self.head = newNode
        elif temp.next == None:
            if temp.data < value:
                temp.next = Node(value)
            else:
                self.insertAtBeg(value)
        elif temp.next.data > value:
            node = Node(value)
            node.next = temp.next
            temp.next = node
        else:
            return self.insertSorted(temp.next,value)
   

    def deleteFromBeg(self):
        
        '''
        Objective: To delete a node from the begining of a linked list
        Input:
            self: Implicit object of class LinkedList
        Return Value: Value of node deleted
        '''

        if self.head == None:
            print("List is already empty")
        else:
            temp = self.head
            self.head = self.head.next
            temp.next = None
            return temp.data


    def deleteValue(self,value):

        '''
        Objective: To delete a node from a linked list
        Input:
            self: Implicit object of class LinkedList
            value: Value to be deleted
        Return Value: None
        '''

        if self.head == None:
            print("Value not found")
        elif self.head.data == value:
            print("Deleted successfully")
            self.deleteFromBeg()
        else:
            parent = self.head
            temp = parent.next
            while temp != None:
                if temp.data == value:
                    parent.next = temp.next
                    temp.next = None
                    print("Deleted successfully")
                    return
                else:
                    parent = temp
                    temp = temp.next
            print("Value not found")

    def __str__(self):
        '''
        Objective: To override the string function
        Input:
             self: Implicit object of class LinkedList
        Return Value: String
        '''
        if self.head == None:
            return "List is empty"
        else:
            temp = self.head
            msg = "List is: "
            while temp != None:
                msg += str(temp.data)+" "
                temp = temp.next
            return msg
        
if __name__ == "__main__":
    lst=LinkedList()
    while True:
        print("Press 1 to insert at the beginning")
        print("Press 2 to  Insert at the end")
        print("Press 3 to Insert in a sorted linked list")
        print("Pres  4 to Delete from beginning")
        print("Press 5 to Delete a value")
        print("Press 6 to  Print linked list")
        print("Press 7 to Exit")
        print("Enter your choice:",end="")
        ch = input()
        if ch.isdigit()== False:
            print("Invalid input")
            break
        ch =int(ch)
        if ch==1:
            print("\nEnter the value to be inserted:",end="")
            lst.insertAtBeg(int(input()))
        elif ch==2:
            print("\nEnter the value to be inserted:",end="")
            lst.insertAtEnd(lst.head,int(input()))
        elif ch==3:
            print("\nEnter the value to be inserted:",end="")
            lst.insertSorted(lst.head,int(input()))
        elif ch==4:
            elt = lst.deleteFromBeg()
            if elt != None:
                print("Element deleted:",elt)
        elif ch==5:
            print("\nEnter the value to be deleted:",end="")
            lst.deleteValue(int(input()))
        elif ch==6:
            print(lst)
        else:
            if ch!=7:
                print("Invalid input")
            break
        print("**********************************************************\n")
        
            
        
