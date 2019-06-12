from Record_pranav import *
from BTreeNode import *
blockSize = 4


class BPlus:

    def __init__(self):
        '''
        Objective : To define constructor of BPlus

        Input Parameter:
                  self : Implicit object

        Return Value : None
        '''

        self.nodes = 0
        self.records = 0
        self.nodeAddress = []
        self.Data_File_create()
    

    def Data_File_create(self):
        '''
        Objective : To create a index file for B+ tree

        Input Parameter:
                  self : Implicit object

        Return Value : None
        '''
        
        f1 = open('IndexFile.txt','wb')
        root = Node(self.nodes)

        self.nodeAddress.insert(self.nodes,f1.tell())
        
        pickle.dump(root,f1)

        f1.close()

    def splitLeaf(self,node):
        '''
        Objective : To split the leaf node

        Input Paramter :
                  self : Implicit Object
                  node : Node to be split
        '''

        # Calculate the mid index
        f1 = open('IndexFile.txt','rb+')

        f1.seek(self.nodeAddress[-1])

        pickle.load(f1)

        endOffset = f1.tell()
        
        mid = blockSize//2

        # If it's the root that is being split up then create parent
        if node.parent == None:
            self.nodes += 1
            parent = Node(self.nodes)
            parent.ptrs[0] = node.nodeNo
            node.parent = parent.nodeNo

            #Write the parent at the end
            self.nodeAddress.append(endOffset)
            f1.seek(endOffset)
            pickle.dump(parent,f1)
            endOffset = f1.tell()
            
            #Change the rootPos info as well
            f1.seek(0)
            rootPos = pickle.load(f1)
            rootPos.keys[0] = (parent.nodeNo,None)
            self.rewriteFile(rootPos)
            
                
        # Create the right neighbour 
        self.nodes += 1
        newNode = Node(self.nodes)
        newNode.parent = node.parent

        # Because by that time node will have one extra key
        for i in range(mid,blockSize+1):
            newNode.keys[i-mid] = node.keys[i]
            node.keys[i] = (None,None)

        node.keys.pop()
        # Connect the two leaf nodes
        newNode.ptrs[0] = node.ptrs[0]
        node.ptrs[0] = newNode.nodeNo

        '''Write these nodes to the file'''

        # Rewrite the updated node
        self.rewriteFile(node)
        self.rewriteFile(newNode)
        
        f1.close()
        
        
        #Send the middle key to the parent
        self.updateParent(newNode.keys[0],node)    


    def updateParent(self,record,left):

        '''
        Objective : To update the parent after splitting

        Input Parameter:
                  self : Implicit Object
                record : Mid-key tuple
                  left : Left part of the spiltted node
        '''
        
        f1 = open('IndexFile.txt','rb+')

        # Seek parent of the node
        parentIndex = left.parent
        f1.seek(self.nodeAddress[parentIndex])
        parent = pickle.load(f1)
            
        index = blockSize
        
        for i in range(blockSize):
            if parent.keys[i][0] == None or record[0] < parent.keys[i][0] :
                index = i
                break

        # Update the parent node
        #       - Correct the Keys
        #       - Correct the Ptrs
        
        parent.keys.insert(index,record)
        parent.ptrs.insert(index+1,left.ptrs[0])


        # If the parent was already full, then split the external node
        if parent.keys[blockSize][0] != None:
            self.splitExternal(parent)

        # Write this back to the file
        else:
            parent.ptrs.pop()
            parent.keys.pop()
            self.rewriteFile(parent)
        f1.close()

        
    def splitExternal(self,node):

        '''
        Objective : To split the external node

        Input Paramter :
                  self : Implicit Object
                  node : Node to be split        
        '''
        
        f1 = open('IndexFile.txt','rb+')

        #Find the end of the file
        f1.seek(self.nodeAddress[-1])
        pickle.load(f1)
        endOffset = f1.tell()
        
        mid = blockSize//2

        # If parent is none, i.e. we are splitting root node
        
        if node.parent == None:
            self.nodes += 1
            parent = Node(self.nodes)
            parent.ptrs[0] = node.nodeNo
            node.parent = parent.nodeNo

            #Write the parent at the end
            self.nodeAddress.append(endOffset)
            f1.seek(endOffset)
            pickle.dump(parent,f1)
            endOffset = f1.tell()
            
            #Change the rootPos info as well
            f1.seek(0)
            rootPos = pickle.load(f1)
            rootPos.keys[0] = (parent.nodeNo,None)
            self.rewriteFile(rootPos)
        
        # Create the right neighbour 
        self.nodes += 1
        newNode = Node(self.nodes)
        newNode.parent = node.parent

        # Because by that time node will have one extra key
        for i in range(mid):
            newNode.keys[i] = node.keys[i+mid+1]
            newNode.ptrs[i] = node.ptrs[i+mid+1]
            node.keys[i+mid+1] = (None,None)
            node.ptrs[i+mid+1] = None
                        
        newNode.ptrs[mid] = node.ptrs[-1]
        # Store mid key
        
        mid_key = node.keys[mid]
        node.keys[mid] = (None,None)

        node.keys.pop()
        if len(node.ptrs) > blockSize + 1:
            node.ptrs.pop()
        
        '''Write these nodes to the file'''

        # Reach to the node Address in file
        self.rewriteFile(node)
        
        # Write new node at the end of file
        self.rewriteFile(newNode)
        

        #Update parents of their respective child
        for i in range(mid+1):
            # If the ptr is None
            try:
                childAddress = self.nodeAddress[newNode.ptrs[i]]
                f1.seek(childAddress)
                child = pickle.load(f1)
                child.parent = newNode.nodeNo
                self.rewriteFile(child)
            except TypeError:
                print(newNode,newNode.nodeNo)
            

        # Just to pass the right child node no
        node.ptrs[0] = newNode.nodeNo
        f1.close()
        
        # Update parent
        self.updateParent(mid_key,node)
        
            
    def rewriteFile(self,node):
        '''
        Objective : To rewrite file whole file after the given node

        Input Parameter:
                  self : Implicit object
                  node : Updated node after which the file has to be re-writen
                  
        '''

        f1 = open('IndexFile.txt','rb+')
        f2 = open('TempFile.txt','wb+')

        # If appending to the file, then seek the ptr to the end 
        try:
            f1.seek(self.nodeAddress[node.nodeNo+1])
            length = len(self.nodeAddress)
            self.nodeAddress = self.nodeAddress[:node.nodeNo+1]
        except IndexError:

            f1.seek(self.nodeAddress[-1])
            if len(self.nodeAddress)-1 != node.nodeNo:
                pickle.load(f1)
                self.nodeAddress.append(f1.tell())
            pickle.dump(node,f1)
            f1.close()
            return

        
        
        # Else write all nodes below it to a new file 
        i = node.nodeNo+1
        while i<length:
            try:
                pickle.dump(pickle.load(f1),f2)
                i+=1
            except EOFError:
                break

        # Then write the node to the apt position 
        f1.seek(self.nodeAddress[node.nodeNo])
        pickle.dump(node,f1)

        f2.seek(0)

        # Append all the records and update the addresses
        while True:
            prev = f1.tell()
            try:
                pickle.dump(pickle.load(f2),f1)
                self.nodeAddress.append(prev)
            except EOFError:
                break

        f1.close()
        f2.close()
        
        
    def insertRecord(self,record):
        '''
        Objective : To insert a record into B+ tree

        Input Parameter:
                  self : Implicit object
                record : Record type object

        Return Value : None
        '''
        
        self.records += 1
        f1 = open('IndexFile.txt','rb+')
        
        # Case 1: Inserting to an Empty B Plus Tree

        if self.records == 1 :

            rootPos = pickle.load(f1)                
            rootPos.keys[0] = (1,None)

            self.nodes += 1

            #Creating root node
            node = Node(self.nodes)
            node.keys[0] = (record.getKey(), self.records)
            node.parent = None

            f1.seek(self.nodeAddress[rootPos.nodeNo])
            pickle.dump(rootPos,f1)
            
            self.nodeAddress.insert(self.nodes,f1.tell())
            pickle.dump(node,f1)
            
            f1.close()
    
            
        else:

            #Gives information about the node number of root
            rootPos = pickle.load(f1).keys[0][0]

            #Retrieve the root node
            f1.seek(self.nodeAddress[rootPos])
            root = pickle.load(f1)

            # Case 2: Only one node that is not full

            if root.keys[-1][0] == None and root.ptrs[0] == None:
            
                
                for i in range(blockSize):
                    if root.keys[i][0]==None or record.getKey() < root.keys[i][0] :
                        index = i
                        break

                root.keys.insert(index,(record.getKey(),self.records))
                root.keys.pop()

                f1.seek(self.nodeAddress[root.nodeNo])
                pickle.dump(root,f1)

            # Case 3: Normal insert
            else:

                temp = root
                eltKey = record.getKey()
                while temp.ptrs[1]!=None:
                    nextNode = None
                    
                    if eltKey < temp.keys[0][0]:
                        #Get to lower level
                        nextNode = temp.ptrs[0] 

                    else:
                        
                        for i in range(blockSize-1):
                            if temp.keys[i+1][0] == None:
                                nextNode = temp.ptrs[i+1]
                                break
                            
                            elif temp.keys[i][0] < eltKey and temp.keys[i+1][0] >= eltKey:
                                nextNode = temp.ptrs[i+1]
                                break

                    if nextNode == None:
                        nextNode = temp.ptrs[-1]

                    f1.seek(self.nodeAddress[nextNode])
                    
                    temp = pickle.load(f1)

                index = blockSize
                
                # Find the correct index for insertion
                for i in range(blockSize):
                    if temp.keys[i][0]== None or record.getKey() < temp.keys[i][0] :
                        index = i
                        break

                # Check if we need to spilt the node or not
                if temp.keys[-1][0] == None:
                    temp.keys.insert(index,(record.getKey(),self.records))
                    temp.keys.pop()
                    self.rewriteFile(temp)
                    f1.close()
                    
                else:
                    temp.keys.insert(index,(record.getKey(),self.records))
                    self.splitLeaf(temp)

def search(key):

    '''
    Objective : Search a record whose key value is given and then display n records
    Input Paramaters:
               self : Implicit object
                key : Key of the record to be searched
            
    Return Value : None
    '''

    f1 = open('IndexFile.txt','rb')
    f2 = open('IndexPos.txt','rb')
    nodeAddress = pickle.load(f2)
    f2.close()

    f1.seek(nodeAddress[0])
    
    rootPos = pickle.load(f1).keys[0][0]
    
    
    # Reach to the root
    f1.seek(nodeAddress[rootPos])
    root = pickle.load(f1)
    
    temp = root
    
    while temp.ptrs[1]!=None:
        nextNode = None
        
        if key < temp.keys[0][0]:
            #Get to lower level
            nextNode = temp.ptrs[0] 

        else:
            
            for i in range(blockSize-1):

                if temp.keys[i+1][0] == None:
                    nextNode = temp.ptrs[i+1]
                    break
                
                elif temp.keys[i][0] <= key and temp.keys[i+1][0] > key:
                    #print("In")
                    nextNode = temp.ptrs[i+1]
                    break

        if nextNode == None:
            nextNode = temp.ptrs[-1]

        f1.seek(nodeAddress[nextNode])
        
        temp = pickle.load(f1)
    #print(temp,nextNode) 

    recordNo = 0
    index = 0
    for i in range(4):
        if key == temp.keys[i][0]:
            recordNo = temp.keys[i][1]
            index = i
            break

    if recordNo == 0:
        print('Not Found')

    else:

        f1 = open('DF.txt','rb')
        f2 = open('Record_Position_File.txt','rb')
        n=recordNo-1
        print("The record is")
        print("")
        i=0
        while True:
            try:
                t =pickle.load(f2)
                if(i==n):
                    print("Record "+str(int(i+1))+" Position "+str(t))
                    f1.seek(t)
                    print(pickle.load(f1))
                i=i+1
            except:
                break


if __name__=="__main__":

    b = None
    
    Data_File_create(int(input("Enter the number of records you want to create:")))
    print("Record file and position file created..")

    n = int(input("Enter the number of records you want to add in B+ tree:"))
    b = BPlus()
    f1 = open('DF.txt','rb')
    for i in range(n):
        obj = pickle.load(f1)
        print("Inserting Key:",obj.getKey())
        b.insertRecord(obj)
    f1.close()
            
    f2 = open('IndexPos.txt','wb')
    pickle.dump(b.nodeAddress,f2)
    f2.close()

    print("Index file and index position file created..")

    f1 = open('IndexFile.txt','rb')
    n = 0
    for i in b.nodeAddress:
        print("\nNODE "+ str(n)+":")    
        f1.seek(i)
        print(pickle.load(f1))
        n += 1
    n = int(input('Enter the key to begin with searching a key :'))
    search(n)
    
