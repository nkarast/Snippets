from collections import Counter, defaultdict, OrderedDict

#
#   returns the duplicates
#
def duplicates(lst):
    cnt= Counter(lst)
    return [key for key in cnt.keys() if cnt[key]> 1]

#
#   gets the indices of the duplicates
#
def indices(lst, items= None):
    items, ind= set(lst) if items is None else items, defaultdict(list)
    for i, v in enumerate(lst):
        if v in items: ind[v].append(i)
    return ind

