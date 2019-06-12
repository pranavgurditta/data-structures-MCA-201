import random,pickle

class Record:
    '''
    Objective: To represent a record entity
    '''
    count = 1 
    
    def __init__(self):
        '''
        Objective: To instantiate a Record object
        Input:
            self: Implicit parameter
            key: key value for the record
          others: other information 
        '''
        self.key = Record.count + 10000
        Record.count +=1
        self.others = str(self.key)*random.randint(50,250)

    def __str__(self):
        '''
        Objective: To override string function
        Input:
            self: Implicit parameter
        Return: STring representation of object
        '''
        return str(self.key)+":"+self.others

    def getKey(self):
        '''
        Objective: To return key value of a record
        Input:
            self: Implicit paramter
        Return: Key value
        '''
        return self.key

if __name__=="__main__":
    f1 = open("Records.txt",'wb')
    f2 = open("Index.txt",'wb')

    threshold=5000000
    n = int(input("Enter the number of records to be created:"))
    for i in range(0,n):
        r = Record()
        offset = f1.tell()
        pickle.dump(r,f1)
        pickle.dump((r.getKey(),offset+threshold),f2)
        #print(f1.tell(),f2.tell())    

    f1.close()
    f2.close()

    f1 = open("Records.txt",'rb')
    f2 = open("Index.txt",'rb')
    k = int(input("Enter the key value of record to be accessed:"))
    k = k - 10001
    f2.seek(14*k)
    tup=pickle.load(f2)
    f1.seek(int(tup[1])-threshold)
    print(pickle.load(f1))
