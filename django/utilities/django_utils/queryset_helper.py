'''
queryset_iterator and queryset_list_iterator from:
https://gist.github.com/897894
'''

def queryset_iterator(queryset, chunksize=1000):
    """
    Iterate over a Django Queryset ordered by the primary key
    
    This method loads a maximum of chunksize (default: 1000) rows in it's
    memory at the same time while django normally would load all rows in it's
    memory. Using the iterator() method only causes it to not preload all the
    classes.
    
    Note that the implementation of the iterator does not support ordered query sets.
    
    Usage:
    
    my_queryset = queryset_iterator( MyItem.objects.all() )
    for item in my_queryset:
        item.do_something()
    
    """
    last_pk = queryset.order_by('-pk')[0].pk
    queryset = queryset.order_by('pk')
    pk = queryset[0].pk
    while pk < last_pk:
        for row in queryset.filter(pk__gt=pk)[:chunksize]:
            pk = row.pk
            yield row
        gc.collect()


def queryset_list_iterator(queryset, listsize=10000, chunksize=1000):
    """
    Iterate over a Django Queryset ordered by the primary key and return a
    list of model objects of the size 'listsize'.
    This method loads a maximum of chunksize (default: 1000) rows in it's memory
    at the same time while django normally would load all rows in it's memory.
    In contrast to the queryset_iterator, it doesn't return each row on its own,
    but returns a list of listsize (default: 10000) rows at a time.
    
    Note that the implementation of the iterator does not support ordered query sets.
    """
    it = queryset_iterator(queryset, chunksize)
    i = 0
    row_list = []
    for row in it:
        i += 1
        row_list.append(row)
        if i >= listsize:
            yield row_list
            i = 0
            row_list = []