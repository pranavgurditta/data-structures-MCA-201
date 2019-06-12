# Python program for implementation of heap Sort 

def right(n):
        '''
        Objective: Returns the index of right child
        Input:
        n: index of parent

        Return: Index of right child
        '''
        #Approach: Right child is present at position 2n+2

        return 2*n+2
    

def left(n):
        '''
         Objective: Returns the index of left child
         Input:
              n: index of parent
         Return: Index of left child
        '''
        #Approach: Left child is present at position 2n+1

        return 2*n+1

    
def parent(n):
        '''
         Objective: Returns the index of parent
         Input:
         n: index of child
         Return: Index of parent
        '''
        #Approach: Parent is present at position n/2

        if n%2==0:
            return n//2-1
        return n//2


def heapify(arr, n, i):
    '''
    Objective: To heapify subtree rooted at i
    Input:
    arr: array represntation of elements to be sorted
    n: total number of elements to be sorted
    i: index of root
        Return: None
        '''
    largest = i # Initialize largest as root 
    l = left(i)  # left = 2*i + 1 
    r = right(i)     # right = 2*i + 2 

    # See if left child of root exists and is 
    # greater than root 
    if l < n and arr[i] < arr[l]: 
        largest = l 

    # See if right child of root exists and is 
    # greater than root 
    if r < n and arr[largest] < arr[r]: 
        largest = r 

    # Change root, if needed 
    if largest != i: 
        arr[i],arr[largest] = arr[largest],arr[i] # swap 

    # Heapify the root. 
        heapify(arr, n, largest) 

# The main function to sort an array of given size 
def heapSort(arr):
    '''
        Objective: To build heap
        Input:
           arr: array to store the max heap elements
        Return: None
        '''
    n = len(arr)

    # Build a maxheap. 
    for i in range(n, -1, -1): 
	    heapify(arr, n, i)

    # One by one extract elements 
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0) 

# Driver code to test above
def main():
        arr = [ 41, 11, 33, 25, 16, 71] 
        heapSort(arr) 
        n = len(arr) 
        print ("Sorted array is") 
        for i in range(n):
            print ("%d" %arr[i])


if __name__=="__main__":
    main()
