VERBOSITY = 2
DEFAULT_QUERYSET_ARGS = {
    'batchsize': 10,
    'gc_collect': True
}
VALID_TEST_DATA = (
    [{'pk': pk, 'pk_info': str(pk)} for pk in xrange(1, 1000)],
    [{'pk': pk, 'pk_info': str(pk)} for pk in xrange(100, 200)],
    [{'pk': pk, 'pk_info': str(pk)} for pk in xrange(10000, 20000, 50)],
    [{'pk': pk, 'pk_info': str(pk)} for pk in xrange(1, 1000, 2)],
)
VALID_BATCH_SIZES = (5, 10, 20, 40, 80)
VALID_RESULT_SET = VALID_TEST_DATA[0]
LT_EQ_ZERO_TEST_DATA = (0, -1, -2, -3, -4, -5, -100, -9999)
BAD_TYPE_TEST_DATA = ([1], {'2': 3}, 'four', object(), {1, 2}, (3, 4), 1.5)
