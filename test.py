from queryset_iterator import queryset_iterator
from mock import Mock
import unittest


VERBOSITY = 2


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


class QuerySetIteratorTest(unittest.TestCase):
    def test_return_values_corrent(self):
        result_set = [{ 'pk' : i, 'info' : 'item number %d' % i }
                        for i in xrange(1, 1000)]
        queryset_mock = Mock()
        iterator_results = (result['pk'] for result in result_set)
        values_list = queryset_mock.values_list.return_value
        distinct = values_list.distinct.return_value
        distinct.iterator.return_value = iterator_results
#        values_list_iterator = distinct.iterator.return_value
#        values_list_iterator.return_value = iterator_results
        queryset_mock.filter.side_effect = get_filter_side_effect(result_set)
        test_results_iterator = queryset_iterator(queryset_mock, batchsize = 5)
        full_results = [result for result in test_results_iterator]
        self.assertEqual(full_results, result_set)


def main():
    test_loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(test_loader.loadTestsFromTestCase(QuerySetIteratorTest))
    test_runner = unittest.TextTestRunner(verbosity = VERBOSITY)
    test_runner.run(suite)


if __name__ == '__main__':
    main()
