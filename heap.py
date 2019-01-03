import math
class Heap:
    '''
    The class has been made to define a heap


    '''
    a=[]

    def __init__(self,a):
        '''
        OBJECTIVE: To initialize
        Input: A list a
        '''
        #Approach:
        self.a=a

        
    def getParent(self,i):
        if(i>0):
            return(self.a[(i-1)//2])
        else:
            return self.a[0]
    
    def getLeftChild(self,i):
        
        if((2*i+1)<len(self.a)):
            return(self.a[2*i+1])
        else:
            return 0
    def getRightChild(self,i):
        if((2*i+2)<len(self.a)):
            return(self.a[2*i+2])
        else:
            return 0

    def createHeap(self):
        a=self.a
        for i in range(0,(len(a))//2) :
            
            if(self.getLeftChild(i)>self.getRightChild(i)):
                maxn=self.getLeftChild(i)
                maxi=2*i+1
            else:
                maxn=self.getRightChild(i)
                maxi=2*i+2

            if(a[i]>maxn):
                pass
            else:
                t=a[maxi]
                a[maxi]=a[i]
                a[i]=t
                while (a[i]> self.getParent(i)) :

                    t=a[i]
                    a[i]=self.getParent(i)
                    a[(i-1)//2]=t
                    i=(i-1)//2
            

                    
                    
                 
    def print(self):
        print(self.a)

    def topElement(self):
        a=self.a
        a2=a[0]
        a.remove(a[0])
        a.insert(0,a[len(a)-1])
        
        a.pop(len(a)-1)
        
        a=Heap(a)
        self.createHeap()
        return a2

def main():
    aq=Heap([16,40,7,23,18,12,11,24,15,50,22,8,30])
    aq.createHeap()
    print("The heap is")
    aq.print()
    print("The removed element is ")
    print(aq.topElement())
    
    print("The heap is")
    aq.print()





if __name__=="__main__":
    main()
    
