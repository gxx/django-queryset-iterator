"""
Contains the queryset_iterator function.
This function is useful for iterating over large querysets with Django.
"""
import gc


GC_COLLECT_BATCH = 1
GC_COLLECT_END = 2


def queryset_iterator(queryset, batchsize=500, gc_collect=GC_COLLECT_BATCH):
    """
    Obtain a generator that can be used to iterator
    over the queryset in batches.
    Keyword Arguments:
    queryset -- The queryset to iterate over in batches.
    batchsize -- The batch size used to process the queryset. Defaults to 500.
    gc_collect -- Whether to garbage collect between batches. Defaults to True.
    """
    if batchsize < 1:
        raise ValueError('Batch size must be above 0')

    if not isinstance(batchsize, int):
        raise TypeError('batchsize must be an integer')

    # Acquire a distinct iterator of the primary keys within the queryset.
    # This will be maintained in memory (or a temporary table) within the
    # database and iterated over, i.e. we will not copy and store results.
    iterator = queryset.values_list('pk', flat=True).distinct().iterator()
    # Begin main logic loop. Will loop until iterator is exhausted.
    while True:
        pk_buffer = []
        try:
            # Consume queryset iterator until batch is reached or the
            # iterator has been exhausted.
            while len(pk_buffer) < batchsize:
                pk_buffer.append(iterator.next())
        except StopIteration:
            # Break out of the loop once the queryset has been consumed.
            break
        finally:
            # Use the original queryset to obtain the proper results.
            # Once again using an iterator to keep memory footprint low.
            for result in queryset.filter(pk__in=pk_buffer).iterator():
                yield result

            if gc_collect == GC_COLLECT_BATCH and pk_buffer:
                # Perform a garbage collection to reduce the memory used.
                # Iterating over large datasets can be quite costly on memory.
                gc.collect()

    if gc_collect == GC_COLLECT_END:
        # Perform a garbage collection to reduce the memory used.
        gc.collect()
