import unittest as ut
from kkmain import Deck, Card, CardType, Hand


# class TestCard(ut.TestCase):
#     def test_post_init(self):
#         # Ensure proper assignment of type and value
#         card = Card(name='Botan ni Chou')
#         self.assertEqual(card.value, 6, f'value={card.value}')
#         self.assertIs(card.type, CardType.RIBBON, f'type={card.type}')


class TestDeck(ut.TestCase):
    def test_build(self):
        # Ensure Card object instatiated
        deck = Deck()
        card = deck.cards[0]
        self.assertIsInstance(card, Card)

        # Ensure correct number of Cards created
        self.assertEqual(len(deck.cards), 48, 'Expect 48 cards')

        # Ensure Card names and types properly assigned
        card_name = 'Matsu ni Tsuru'
        names = [card.name for card in deck.cards]
        self.assertTrue(card_name in names)
        self.assertTrue(card.name == card_name, 'Expect True')

    def test_draw_cards(self):
        # Ensure correct number of cards added/removed
        deck = Deck()
        cards = deck.draw_cards(4)
        self.assertEqual(48 - len(cards), deck.remaining, f'cards={cards}, remaining={deck.remaining}')

        # Ensure specified cards removed from deck
        for card in cards:
            self.assertFalse(card in deck.cards, f'card={card}')


class TestHand(ut.TestCase):
    pass


if __name__ == '__main__':
    ut.main()
