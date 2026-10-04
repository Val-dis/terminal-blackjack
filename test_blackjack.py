import unittest
from blackjack import Deck, hand_value, is_blackjack, settle, dealer_play


class BlackjackTests(unittest.TestCase):
    def test_hand_values(self):
        self.assertEqual(hand_value([("K", "S"), ("7", "H")]), 17)
        self.assertEqual(hand_value([("A", "S"), ("K", "H")]), 21)
        self.assertEqual(hand_value([("A", "S"), ("A", "H"), ("9", "D")]), 21)
        self.assertEqual(hand_value([("K", "S"), ("Q", "H"), ("5", "D")]), 25)

    def test_blackjack_detection(self):
        self.assertTrue(is_blackjack([("A", "S"), ("K", "H")]))
        self.assertFalse(is_blackjack([("7", "S"), ("7", "H"), ("7", "D")]))

    def test_settle(self):
        bj = [("A", "S"), ("K", "H")]
        twenty = [("K", "S"), ("Q", "H")]
        bust = [("K", "S"), ("Q", "H"), ("5", "D")]
        self.assertEqual(settle(bj, twenty, 100), 150)
        self.assertEqual(settle(bust, twenty, 100), -100)
        self.assertEqual(settle(twenty, bust, 100), 100)
        self.assertEqual(settle(twenty, twenty, 100), 0)
        self.assertEqual(settle(bj, bj, 100), 0)

    def test_dealer_stops_at_17(self):
        deck = Deck()
        hand = dealer_play(deck, [("5", "S"), ("3", "H")])
        self.assertGreaterEqual(hand_value(hand), 17)

    def test_deck_has_52_unique_cards(self):
        deck = Deck()
        self.assertEqual(len(set(deck.cards)), 52)


if __name__ == "__main__":
    unittest.main()
