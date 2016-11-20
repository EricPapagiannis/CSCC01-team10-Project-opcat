def showlastest(showlastest_marker):
    '''(int) -> NoneType
    Method for showest the lastest 'n' proposed changes
    "showlastest_marker" is passed in as int
    '''

    unpack_changes()
    Changes_datesort = _mergeSort(CHANGES)
    try:
        i = 0
        ret = ""
        while i < showlastest_marker and i < len(Changes_datesort):
            ret += "\nShowing number : " + str(i) + "\n"
            ret += CHANGES[i]
            ret += "\n"
        print(ret)
        print()
    except TypeError:
        print("invalid input, usage: showlatest [int]")

def _mergeSort(change_list):
    '''(List) -> List
    helper method for sifting through the list of proposed change
    objects to sort it by most recent date
    '''
    if len(change_list)>1:
        mid = len(change_list)//2
        lefthalf = change_list[:mid]
        righthalf = change_list[mid:]

        _mergeSort(lefthalf)
        _mergeSort(righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] > righthalf[j]:
                change_list[k]=lefthalf[i]
                i=i+1
            else:
                change_list[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            change_list[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            change_list[k]=righthalf[j]
            j=j+1
            k=k+1
    return change_list
    
