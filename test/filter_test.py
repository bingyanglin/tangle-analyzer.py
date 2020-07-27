# utils_test.py
from unittest import TestCase, main
from tangleanalyzer import (
    AddressFilter,
    BranchTransactionHashFilter,
    BundleFilter,
    NonceFilter,
    ObsoleteTagFilter,
    SignatureMessageFragmentFilter,
    TagFilter,
    TimeFilter,
    TransactionHashFilter,
    TrunkTransactionHashFilter,
    ValueFilter
)
from . import (
    transaction_and_hash,
    address_correct,
    address_wrong,
    branch_correct,
    branch_wrong,
    bundle_correct,
    bundle_wrong,
    nonce_correct,
    nonce_wrong,
    obsolete_tag_correct,
    obsolete_tag_wrong,
    signature_correct,
    signature_wrong,
    tag_correct,
    tag_wrong,
    transaction_hash_correct,
    transaction_hash_wrong,
    trunk_correct,
    trunk_wrong
)

from tangleanalyzer.common.const import *


class FilterTestCase(TestCase):

    def test_filter_in_set(self):
        set_tuple = (address_correct, branch_correct, bundle_correct,
                     nonce_correct, obsolete_tag_correct, signature_correct,
                     tag_correct, transaction_hash_correct, trunk_correct)

        filter_tuple = (AddressFilter, BranchTransactionHashFilter, BundleFilter,
                        NonceFilter, ObsoleteTagFilter, SignatureMessageFragmentFilter,
                        TagFilter, TransactionHashFilter, TrunkTransactionHashFilter)

        for s, f in zip(set_tuple, filter_tuple):
            filter_to_test = f(set(s)).make_filter()
            self.assertEqual(True, filter_to_test(transaction_and_hash))

    def test_filter_not_in_set(self):
        set_tuple = (address_wrong, branch_wrong, bundle_wrong,
                     nonce_wrong, obsolete_tag_wrong, signature_wrong,
                     tag_wrong, transaction_hash_wrong, trunk_wrong)

        filter_tuple = (AddressFilter, BranchTransactionHashFilter, BundleFilter,
                        NonceFilter, ObsoleteTagFilter, SignatureMessageFragmentFilter,
                        TagFilter, TransactionHashFilter, TrunkTransactionHashFilter)

        for s, f in zip(set_tuple, filter_tuple):
            filter_to_test = f(set(s)).make_filter()
            self.assertEqual(False, filter_to_test(transaction_and_hash))

    def test_value_R_filter(self):
        min, max = (-3, 3)
        filter_to_test = ValueFilter(min, max).make_filter('R')
        self.assertEqual(True, filter_to_test(transaction_and_hash))

    def test_value_m_filter(self):
        min, max = (-3, None)
        filter_to_test = ValueFilter(min, max).make_filter('m')
        self.assertEqual(True, filter_to_test(transaction_and_hash))

    def test_value_M_filter(self):
        min, max = (None, 3)
        filter_to_test = ValueFilter(min, max).make_filter('M')
        self.assertEqual(True, filter_to_test(transaction_and_hash))

    def test_value_E_filter(self):
        min, max = (0, None)
        filter_to_test = ValueFilter(min, max).make_filter('E')
        self.assertEqual(True, filter_to_test(transaction_and_hash))

    def test_value_RE_filter(self):
        min, max = (0, 3)
        filter_to_test = ValueFilter(min, max).make_filter('RE')
        self.assertEqual(True, filter_to_test(transaction_and_hash))

    def test_value_mE_filter(self):
        min, max = (0, 3)
        filter_to_test = ValueFilter(min, max).make_filter('mE')
        self.assertEqual(True, filter_to_test(transaction_and_hash))

    def test_value_ME_filter(self):
        min, max = (-3, -1)
        filter_to_test = ValueFilter(min, max).make_filter('ME')
        self.assertEqual(False, filter_to_test(transaction_and_hash))


if __name__ == '__main__':
    main()
