

def binary_search(list, value):
    print list, value
    mid = int(len(list)/2)
    if len(list) == 1:
        return value == list[0]
    if value < list[mid]:
        return binary_search(list[:mid],value)
    elif value == list[mid]:
        return True
    elif value > list[mid]:
        return binary_search(list[mid:], value)

def insert(list, value):
    print list, value
    if len(list) == 0:
        return [value]
    elif len(list) == 1:
        if value > list[0]:
            return list + [value]
        if value < list[0]:
            return [value] + list
    mid = int(len(list) / 2)
    if value < list[mid]:
        return insert(list[:mid], value) + list[mid:]
    if value > list[mid]:
        return list[:mid] + insert(list[mid:], value)
    else:
        return list



if __name__ == "__main__":
    print "starting inserts"
    l = []
    print insert(l, 1)  # [1]
    print insert(insert(l,1),2)  # [1,2]
    print insert(insert(insert(l, 1), 3), 2)  # [1,2,3]
    print insert(insert(insert(l, 3), 1), 2)  # [1,2,3]
    print insert(insert(insert(insert(insert(insert([1,20,30,40,50], 44),-1),-55),22), 13), 14)
    print "ending inserts"
    # print "starting search"
    # l = [i for i in xrange(1, 10)]
    # assert(binary_search(l, 1))
    # assert(not binary_search(l, -1))
    # assert(not binary_search(l, 23))
    # assert(binary_search(l, 9))
    # print "ending search"
