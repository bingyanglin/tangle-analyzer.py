# utils_test.py
from unittest import TestCase, main
from tangleanalyzer import (
    AddressFilter,
    BundleFilter,
    ObsoleteTagFilter,
    TagFilter,
    TransactionHashFilter
)
from . import (
    transaction_and_hash,
    address_correct,
    address_wrong,
    bundle_correct,
    bundle_wrong,
    obsolete_tag_correct,
    obsolete_tag_wrong,
    tag_correct,
    tag_wrong,
    transaction_hash_correct,
    transaction_hash_wrong
)


class FilterTestCase(TestCase):

    def test_filter_in_set(self):
        set_tuple = (address_correct, bundle_correct,
                     obsolete_tag_correct, tag_correct, transaction_hash_correct)

        filter_tuple = (AddressFilter, BundleFilter,
                        ObsoleteTagFilter, TagFilter, TransactionHashFilter)

        for s, f in zip(set_tuple, filter_tuple):
            filter_to_test = f(set(s)).make_filter()
            self.assertEqual(True, filter_to_test(transaction_and_hash))

    def test_filter_not_in_set(self):
        set_tuple = (address_wrong, bundle_wrong,
                     obsolete_tag_wrong, tag_wrong, transaction_hash_wrong)

        filter_tuple = (AddressFilter, BundleFilter,
                        ObsoleteTagFilter, TagFilter, TransactionHashFilter)

        for s, f in zip(set_tuple, filter_tuple):
            filter_to_test = f(set(s)).make_filter()
            self.assertEqual(False, filter_to_test(transaction_and_hash))


if __name__ == '__main__':
    main()
