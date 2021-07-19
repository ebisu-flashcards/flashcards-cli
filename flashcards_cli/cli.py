# from prompt_toolkit import prompt
# from prompt_toolkit.history import FileHistory
# from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
# from prompt_toolkit.completion import Completer, Completion
# import click
# from fuzzyfinder import fuzzyfinder
# #from pygments.lexers.sql import SqlLexer


# SQLKeywords = ['select', 'from', 'insert', 'update', 'delete', 'drop']


# class SQLCompleter(Completer):

#     def get_completions(self, document, complete_event):
#         word_before_cursor = document.get_word_before_cursor(WORD=True)
#         matches = fuzzyfinder(word_before_cursor, SQLKeywords)
#         for m in matches:
#             yield Completion(m, start_position=-len(word_before_cursor))


# while 1:
#     user_input = prompt(u'>',
#                         history=FileHistory('history.txt'),
#                         auto_suggest=AutoSuggestFromHistory(),
#                         completer=SQLCompleter(),
#                         )
#     click.echo_via_pager(user_input)




from PyInquirer import prompt
#from examples import custom_style_2
#from prompt_toolkit.validation import Validator, ValidationError


# class NumberValidator(Validator):

#     def validate(self, document):
#         try:
#             int(document.text)
#         except ValueError:
#             raise ValidationError(message="Please enter a number",
#                                   cursor_position=len(document.text))

from typing import Any, Mapping

import click

from flashcards_core.database import SessionLocal
from flashcards_core.database.decks import Deck
from flashcards_core.database.cards import Card
from flashcards_core.schedulers import get_scheduler, get_available_schedulers


class Study:
    """
    Creates a study session by initializing an algorithm
    engine to process the cards once they're studied.

    This is more of a convenience class than an API, as all
    engines should be stateless.
    """

    def __init__(self, deck_id: int):
        self.deck = Deck.get_one(object_id=deck_id)
        self.scheduler = get_scheduler(self.deck.algorithm)

    def next_card(self) -> Card:
        """
        Returns the next card to be studied.
        :returns: a database Card object.
        """
        return self.scheduler.next_card_to_review()

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
        self.scheduler.process_test_result(card_id=card_id, result=result)


def study(db):
    decks = Deck.get_all(db=db)
    if not decks:
        click.echo("You have no decks! Use \"Edit my collection\" to create one.")
        return

    answers = prompt([
        {
            'type': "list",
            "name": "deck",
            "message": "Enter the deck you want to study:",
            'choices': [deck.name for deck in Deck.get_all(db=db)]
            #"validate": NumberValidator,
            #"filter": lambda val: int(val)
        }
    ])
        # {
        #     'type': "input",
        #     "name": "b",
        #     "message": "Enter the second number",
        #     #"validate": NumberValidator,
        #     "filter": lambda val: int(val)
        # }
    click.echo("Soon!")


def edit(db):
    answers = prompt([
        {
            'type': "list",
            "name": "deck",
            "message": "Which deck do you want to edit?",
            'choices': [d.name for d in Deck.get_all(db=db)] + ["+ Create new deck"]
            #"validate": NumberValidator,
            #"filter": lambda val: int(val)
        }])

    deck: Deck
    if answers["deck"] == "+ Create new deck":
        deck = create_deck(db)
    else:
        deck = Deck.get_by_name(db=db, name=answers["deck"])

    answers = prompt([
        {
            'type': "list",
            "name": "operation",
            "message": "What do you want to do to this deck?",
            'choices': ["Update deck details", "Delete deck", "Edit cards"]
        }])

    if answers["operation"] == "Update deck details":
        deck = update_deck(db, deck)

    elif answers["operation"] == "Delete deck":
        Deck.delete(db=db, object_id=deck.id)
        click.echo("Deck deleted!")

    elif answers["operation"] == "Edit cards":
        edit_cards(db, deck)

    else:
        raise ValueError("Answer not understood.")


def create_deck(db):
    answers = prompt([
        {
            'type': "input",
            "name": "name",
            "message": "Deck Name:"
        },
        {
            'type': "input",
            "name": "description",
            "message": "Deck Description:"
        },
        {
            'type': "list",
            "name": "algorithm",
            "message": "Which SRS algorithm you want to use for studying?",
            'choices': get_available_schedulers()
        },
        {
            'type': "input",
            "name": "params",
            "message": "Any extra parameters (JSON format)?",
            "default": "{}"
        }
    ])
    deck = Deck.create(db=db,
                name=answers['name'],
                description=answers["description"],
                algorithm=answers["algorithm"],
                parameters=answers["params"] or "{}",
                state=None)
    click.echo("New deck created!")
    return deck


def update_deck(db, deck):
    answers = prompt([
        {
            'type': "input",
            "name": "name",
            "message": "Deck Name:",
            "default": deck.name
        },
        {
            'type': "input",
            "name": "description",
            "message": "Deck Description:",
            "default": deck.description
        },
        {
            'type': "list",
            "name": "algorithm",
            "message": "Which SRS algorithm you want to use for studying?",
            'choices': get_available_schedulers(),
            "default": deck.algorithm

        },
        {
            'type': "input",
            "name": "params",
            "message": "Any extra parameters (JSON format)?",
            "default": deck.parameters
        }
    ])
    deck = Deck.update(db=db,
                        object_id=deck.id,
                        name=answers['name'],
                        description=answers["description"],
                        algorithm=answers["algorithm"],
                        parameters=answers["params"] or "{}",
                        state=None)
    click.echo("Deck updated!")
    return deck


def edit_cards(db, deck):
    click.echo("Soon!")


def main():
    db = SessionLocal()
    click.echo("****************************")
    click.echo(" Welcome to Flashcards CLI! ")
    click.echo("****************************")
    while True:
        answers = prompt([
            {
                'type': 'list',
                'name': 'choose_operation',
                'message': 'What do you want to do?',
                'choices': ["Study", "Edit my collections", "Quit"]
            }
        ])
        if answers.get("choose_operation") == "Study":
            study(db)
        elif answers.get("choose_operation") == "Edit my collections":
            edit(db)
        elif answers.get("choose_operation") == "Quit":
            click.echo("Bye bye!")
            return
        else:
            click.echo("Please choose \"Study\", \"Edit my collections\" or \"Quit\":")


if __name__ == "__main__":
    main()
