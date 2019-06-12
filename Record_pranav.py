import numpy
import random,pickle


class Record_Pranav:
    '''
    A class to represent the record.
    '''

    def __init__(self,key,others):
        '''
        Objective: This has been done for object intialisation of class Record_Pranav
        Input :    key: The key attribute of the record.
                   others: The other or non-key attribute of the record. 
        '''
        self.key = key
        self.others =others

    def __str__(self):
        '''
        Objective: Gives a string representation of the object of Record_Pranav class
        Input :    self : It is an implicit object of class Record_Pranav
        RETURN :   String representation of the given record.
        '''
        return ' KEY- '+str(self.key) + ' OTHERS- '+str(self.others)

    def getKey(record_object):
        '''
        Objective:   To get the key attribute of the given record.
        Input:       record_object :An object of class Record_Pranav
        Return:      record_object's key attribute
        '''
        return record_object.key



def Data_File_create(no):
    '''
    Objective : To create a data file of given no. of records.
    INPUT :
        number : Number of records.
    RETURN : None
    '''
    threshold = 45454
    all_Keys = random.sample(range(1,(no)*10),no)
    with open('DF.txt','wb') as DF:
        for key in all_Keys:
            key = numpy.int64(key)
            others = str(key+threshold) *2
            pickle.dump(Record_Pranav(key,others),DF)
    Record_Position_File()


def Record_Position_File():
    '''
    OBJECTIVE : To create a data position file which contains a list of starting positions of all the records in the data file.
    INPUT : None
    RETURN : None
    '''
    dataPosList = []
    
    with open('Record_Position_File.txt','wb') as Record_Pos_File:
        with open('DF.txt','rb') as DF:
            while True:
                s=DF.tell()
                pickle.dump(s,Record_Pos_File)
                dataPosList.append(s)
                try:
                    pickle.load(DF)
                except:
                    break

    with open('Record_Position_File.txt','rb') as Pos:
         with open('DF.txt','rb') as DF:
             i=1
             while True:
                 try:
                     t =pickle.load(Pos)
                     
                     print("Record "+str(i)+" Position "+str(t))
                     DF.seek(t)
                     print(pickle.load(DF))
                     i=i+1
                 except:
                     break






if __name__ == "__main__":

    n = int(input("Enter the number of records to be written:"))

    Data_File_create(n)
    f1 = open('DF.txt','rb')
    f2 = open('Record_Position_File.txt','rb')
    n=int(input("Enter the record to search"))-1
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


