from kkcards import Ribbons, FlowerViewing, FourBrightsWithRainman
from copy import copy
import unittest as ut

# Test Ribbons, PoetryRibbons, BlueRibbons, tally_points
TEST_COLL1 = ['Matsu no Tan', 'Ume no Tan', 'Sakura no Tan', 'Botan no Tan', 'Kiku no Tan', 'Momiji no Tan']

# Test FourBrightsWithRainmain, FlowerViewing
TEST_COLL2 = ['Matsu ni Tsuru', 'Sakura ni Maku', 'Kiri ni Ho-oh', 'Kiku ni Sakazuki', 'Yanagi ni Ono no Toufuu',
              'Susuki ni Tsuki']


class TestFlowerViewing(ut.TestCase):
    def test_collect(self):
        # Ensure cards not collected if not in "required" list
        yaku = FlowerViewing()
        yaku.collect(TEST_COLL1)
        self.assertEqual(yaku.collected, [], 'Expect empty list')

    def test_complete(self):
        # Ensure yaku not complete if "collected" and "required" list not equal
        yaku = FlowerViewing()
        yaku.collected = copy(TEST_COLL2)
        self.assertFalse(yaku.complete, 'Expect False')

        # Ensure correct number of cards collected and yaku is complete
        yaku.collected = []
        yaku.collect(TEST_COLL2)
        self.assertTrue(yaku.complete, 'Expect True')
        self.assertEqual(yaku.count, 2, 'Expect 2')
        self.assertFalse(yaku.remaining, f'Expect empty list, remaining={yaku.remaining}')


class TestFourBrightsWithRainman(ut.TestCase):
    def test_complete(self):
        # Ensure yaku not complete with more than four brights
        yaku = FourBrightsWithRainman()
        yaku.collect(TEST_COLL2)
        self.assertFalse(yaku.complete, 'Expect False')

        # Ensure yaku not complete without required card
        yaku = FourBrightsWithRainman()
        yaku.collect(TEST_COLL2)
        yaku.collected.remove('Yanagi ni Ono no Toufuu')
        self.assertFalse(yaku.complete, 'Expect False')

        # Ensure yaku can be complete
        yaku = FourBrightsWithRainman()
        yaku.collect(TEST_COLL2)
        yaku.collected.remove('Susuki ni Tsuki')
        self.assertTrue(yaku.complete, 'Expect True')


class TestRibbons(ut.TestCase):
    def test_tally_points(self):
        # Ensure extra points added to value and original value remains set
        yaku = Ribbons()
        yaku.collect(TEST_COLL1)
        pts = yaku.tally_points()
        self.assertEqual(yaku.value, 5, 'Expect 5')
        self.assertEqual(pts, 6, 'Expect 6')

        # Ensure 0 returned if not complete and value remains set
        yaku = Ribbons()
        yaku.collect(TEST_COLL2)
        pts = yaku.tally_points()
        self.assertFalse(yaku.complete, 'Expect False')
        self.assertEqual(yaku.value, 5, 'Expect 5')
        self.assertEqual(pts, 0, 'Expect 0')


if __name__ == '__main__':
    ut.main()
