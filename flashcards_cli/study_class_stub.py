from typing import Any, Mapping

from flashcards_core.database.decks import Deck
from flashcards_core.database.cards import Card
from flashcards_core.spaced_repetition.engines import (
    BaseAlgorithmEngine,
    get_algorithm_engine,
)


class Study:
    """
    Creates a study session by initializing an algorithm
    engine to process the cards once they're studied.

    This is more of a convenience class than an API, as all
    engines should be stateless.
    """

    def __init__(self, deck_id: int):
        self.deck = Deck.get_one(object_id=deck_id)
        self.engine = get_algorithm_engine(self.deck.algorithm_id)

    def next_card(self) -> Card:
        """
        Returns the next card to be studied.
        :returns: a database Card object.
        """
        return self.engine.next_card_to_review()

    def save_result(self, card_id: int, result: Mapping[str, Any]) -> None:
        """
        Saves the results of a test.

        :param card_id: Card reviewed
        :param result: the content of the form of the user, as a dictionary.
            Passed to the algorihtm as a series of arg=value.
        :returns: Nothing.
        :raises Card.DoesNotExist if the card does not exist in this deck
        :raises Deck.DoesNotExist if the deck does not exist for this user
        """
        self.engine.process_test_result(card_id=card_id, result=result)
