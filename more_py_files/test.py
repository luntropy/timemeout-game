import random
import copy

def generate_cards(field_size):
    # 4x5 = 20, 10 unique
    # 4x4 = 16, 8 unique
    # 3x4 = 12, 6 unique

    count_unique_cards = int(field_size / 2)
    print(count_unique_cards)
    list_card_ids = list(range(0, 21))

    random.shuffle(list_card_ids)
    cards = list_card_ids[:count_unique_cards]
    duplicates = copy.copy(cards)

    deck = cards + duplicates
    random.shuffle(deck)

    deck_dictionary = {}
    for card in deck:
        card = str(card)

        if card in deck_dictionary.keys():
            card = card + '-2'

        deck_dictionary[card] = 0

    return deck_dictionary

if __name__ == '__main__':
    cards = generate_cards(20)

    print(cards)
