def average(lst):
    return sum(lst)/(len(lst) or 1)


def averages_row(mat):
    lst = []
    for row in mat or []:
        lst.append(average(row))
    return lst


def find_min_pos(mat):
    min_i = None
    min_j = None
    min_val = None
    for i, row in enumerate(mat) or []:
        for j, elem in enumerate(row) or []:
            if (min_val is None) or (elem < min_val):
                min_i = i
                min_j = j
                min_val = mat[i][j]
    return (min_i, min_j)


def unique(lst):
    set_uniq = set(lst)
    lst_uniq = []
    for i, elem in enumerate(lst) or []:
        if elem in set_uniq:
            set_uniq.remove(elem)
            lst_uniq.append(elem)
    return lst_uniq
