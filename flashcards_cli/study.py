from typing import Any, Mapping

import click
from PyInquirer import prompt

from flashcards_core.database import Session
from flashcards_core.database.decks import Deck


def study(db: Session):
    decks = Deck.get_all(db=db)
    if not decks:
        click.echo('You have no decks! Use "Edit my collection" to create one.')
        return

    answers = prompt(
        [
            {
                "type": "list",
                "name": "deck",
                "message": "Enter the deck you want to study:",
                "choices": [deck.name for deck in Deck.get_all(db=db)]
                # "validate": NumberValidator,
                # "filter": lambda val: int(val)
            }
        ]
    )
    # {
    #     'type': "input",
    #     "name": "b",
    #     "message": "Enter the second number",
    #     #"validate": NumberValidator,
    #     "filter": lambda val: int(val)
    # }
    click.echo("Soon!")
