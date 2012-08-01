from queryset_iterator import queryset_iterator
from mock import Mock
import unittest

VERBOSITY = 2

#todo: refactor and clean-up everything
def get_filter_side_effect(result_set):
    def _get_filter_side_effect_inner(pk__in):
        filter_mock = Mock()
        filter_mock.iterator.side_effect = get_iterator_side_effect(result_set, pk__in)
        return filter_mock

    return _get_filter_side_effect_inner


def get_iterator_side_effect(result_set, pk__in):
    pk_dict = dict((result['pk'], result) for result in result_set)
    def _get_iterator_side_effect_inner():
        for pk in pk__in:
            yield pk_dict[pk]

    return _get_iterator_side_effect_inner


def get_queryset_mock(result_set):
    queryset_mock = Mock()
    iterator_results = (result['pk'] for result in result_set)
    values_list = queryset_mock.values_list.return_value
    distinct = values_list.distinct.return_value
    distinct.iterator.return_value = iterator_results
    queryset_mock.filter.side_effect = get_filter_side_effect(result_set)
    return queryset_mock


#todo: nice programmatic way to test data sets.
#todo: some fixtures
class QuerySetIteratorTest(unittest.TestCase):
    def setUp(self):
        self.result_set = [{ 'pk' : i, 'info' : 'item number %d' % i }
                           for i in xrange(1, 1000)]

    def test_return_values_correct(self):
        #todo: do this with different sets
        queryset_mock = get_queryset_mock(self.result_set)
        test_results_iterator = queryset_iterator(queryset_mock, batchsize = 5)
        full_results = [result for result in test_results_iterator]
        self.assertEqual(full_results, self.result_set)

    def test_retrieves_in_batches(self):
        #todo: do this with different batch sizes
        queryset_mock = get_queryset_mock(self.result_set)
        test_results_iterator = queryset_iterator(queryset_mock, batchsize = 1)
        #todo: refactor and abstract this
        first_pk = test_results_iterator.next()['pk']
        mock_calls = queryset_mock.filter.mock_calls
        self.assertEqual(len(mock_calls), 1)
        self.assertEqual(str(mock_calls[-1]), 'call(pk__in=[%d])' % first_pk)
        second_pk = test_results_iterator.next()['pk']
        mock_calls = queryset_mock.filter.mock_calls
        self.assertEqual(len(mock_calls), 2)
        self.assertEqual(str(mock_calls[-1]), 'call(pk__in=[%d])' % second_pk)

    def test_gc_collect_at_end_of_batch(self):
        self.skipTest('Not Implemented Yet')


def main():
    test_loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(test_loader.loadTestsFromTestCase(QuerySetIteratorTest))
    test_runner = unittest.TextTestRunner(verbosity = VERBOSITY)
    test_runner.run(suite)


if __name__ == '__main__':
    main()
