# Remove equal adjacent elements
#
# Example input: [1, 2, 2, 3]
# Example output: [1, 2, 3]
def remove_adjacent(lst):
    lst0=[]
    i=0
    lst0.insert(0,lst[0])
    for k in lst:
        if lst0[i]!=k:
            lst0.insert(len(lst0),k)
            i+=1
    return lst0

# Merge two sorted lists in one sorted list in linear time
#
# Example input: [2, 4, 6], [1, 3, 5]
# Example output: [1, 2, 3, 4, 5, 6]
def linear_merge(lst1, lst2):
    i1=0
    i2=0
    lst=[]
    while ((i2<len(lst2))and(i1<len(lst1))):
        if lst2[i2]<lst1[i1]:
            lst.insert(len(lst), lst2[i2])
            i2=i2+1
        else:
            lst.insert(len(lst), lst1[i1])
            i1=i1+1
    if i2<len(lst2):
        for i in range(len(lst2)-i2):
            lst.insert(len(lst), lst2[i+i2])
    
    if i1<len(lst1):
        for i in range(len(lst1)-i1):
            lst.insert(len(lst), lst1[i+i1])
   
    return lst
