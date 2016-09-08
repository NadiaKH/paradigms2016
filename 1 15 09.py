# Remove equal adjacent elements
#
# Example input: [1, 2, 2, 3]
# Example output: [1, 2, 3]
def remove_adjacent(lst):
    i=int
    i=1
    while i<len(lst):
        if lst[i-1]==lst[i]:
            del lst[i-1]
        else:
            i=i+1
    return lst

# Merge two sorted lists in one sorted list in linear time
#
# Example input: [2, 4, 6], [1, 3, 5]
# Example output: [1, 2, 3, 4, 5, 6]
def linear_merge(lst1, lst2):
    i=0
    while (len(lst1)>0) and (i<len(lst2)):
       if lst2[i]>lst1[0]:
           lst2.insert(i,lst1[0])
           del lst1[0]
           i=i+1
       else:
           i=i+1
    if len(lst1)>0:
        lst2.extend(lst1)
    return lst2
