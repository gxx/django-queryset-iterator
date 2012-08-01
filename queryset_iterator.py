"""
Contains the queryset_iterator function.
This function is useful for iterating over large querysets with Django.
"""
import gc


def queryset_iterator(queryset, batchsize=500, gc_collect=True):
    """
    Obtain a generator that can be used to iterator
    over the queryset in batches.
    Keyword Arguments:
    queryset -- The queryset to iterate over in batches.
    batchsize -- The batch size used to process the queryset. Defaults to 500.
    gc_collect -- Whether to garbage collect between batches. Defaults to True.
    """
    # Acquire a distinct iterator of the primary keys within the queryset.
    # This will be maintained in memory (or a temporary table) within the
    # database and iterated over, i.e. we will not copy and store results.
    iterator = queryset.values_list('pk', flat=True).distinct().iterator()
    # Begin main logic loop. Will loop until iterator is exhausted.
    while True:
        try:
            pk_buffer = []
            buffer_len = 0
            # Consume queryset iterator until batch is reached or the
            # iterator has been exhausted.
            while buffer_len < batchsize:
                pk_buffer.append(iterator.next())
                buffer_len += 1
        except StopIteration:
            # Break out of the loop once the queryset
            # iterator has been consumed.
            break
        finally:
            # Use the original queryset to obtain the proper results.
            # Once again using an iterator to keep memory footprint low.
            for result in queryset.filter(pk__in=pk_buffer).iterator():
                yield result

            if gc_collect:
                # Perform a garbage collection to reduce the memory used.
                # Iterating over large datasets can be quite costly on memory.
                gc.collect()
