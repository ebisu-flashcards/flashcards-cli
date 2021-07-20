from typing import Optional

import click
from PyInquirer import prompt
from sqlalchemy.orm import Session

from flashcards_core.database.decks import Deck
from flashcards_core.schedulers import get_available_schedulers

from flashcards_cli.edit.cards import edit_cards


def edit_decks(db: Session):
    """
    Prompt for the Edit Collection menu.
    Lets the user select the deck they want to edit, or add new ones.

    :param db: a SQLAlchemy Session object
    """
    answers = prompt(
        [
            {
                "type": "list",
                "name": "deck",
                "message": "Which deck do you want to edit?",
                "choices": [d.name for d in Deck.get_all(db=db)]
                + ["+ Create new deck", "< Back"]
            }
        ]
    )

    # Happens in case of Ctrl+C
    if not answers.get("deck"):
        return

    deck: Deck
    if answers["deck"] == "+ Create new deck":
        deck = create_deck(db)
    elif answers["deck"] == "< Back":
        return
    else:
        deck = Deck.get_by_name(db=db, name=answers["deck"])

    # Happens in case of Ctrl+C during any of the sub-operations (creation, update...)
    if not deck:
        edit_decks(db)
        return

    answers = prompt(
        [
            {
                "type": "list",
                "name": "operation",
                "message": "What do you want to do to this deck?",
                "choices": [
                    "Update deck details",
                    "Delete deck",
                    "Edit cards",
                    "< Back",
                ],
            }
        ]
    )

    if answers["operation"] == "Update deck details":
        deck = update_deck(db, deck)

    elif answers["operation"] == "Delete deck":
        delete_deck(db, deck)

    elif answers["operation"] == "Edit cards":
        edit_cards(db, deck)

    elif answers["operation"] == "< Back":
        edit_decks(db)


def create_deck(db: Session) -> Optional[Deck]:
    """
    Created a new deck with the information gathered,
    and gives some feedback to the user.

    :param db: a SQLAlchemy Session object
    """
    answers = prompt(
        [
            {"type": "input", "name": "name", "message": "Deck Name:"},
            {"type": "input", "name": "desc", "message": "Deck Description:"},
            {
                "type": "list",
                "name": "algorithm",
                "message": "Which SRS algorithm you want to use for studying?",
                "choices": get_available_schedulers(),
            },
            {
                "type": "input",
                "name": "params",
                "message": "Any extra parameters (JSON format)?",
                "default": "{}",
            },
        ]
    )

    # This happens in case of a Ctrl+C during the above questions
    if (
        not answers.get("name")
        or not not answers.get("desc")
        or not answers.get("algorithm")
    ):
        click.echo("Deck creation stopped: no deck was created.")
        return

    deck = Deck.create(
        db=db,
        name=answers["name"],
        description=answers["desc"],
        algorithm=answers["algorithm"],
        parameters=answers["params"] or "{}",
        state=None,
    )
    click.echo("New deck created!")
    return deck


def update_deck(db: Session, deck: Deck) -> Optional[Deck]:
    """
    Updates the given deck with the information gathered,
    and gives some feedback to the user.

    :param db: a SQLAlchemy Session object
    :param deck: the Deck model object to update
    """
    answers = prompt(
        [
            {
                "type": "input",
                "name": "name",
                "message": "Deck Name:",
                "default": deck.name,
            },
            {
                "type": "input",
                "name": "description",
                "message": "Deck Description:",
                "default": deck.description,
            },
            {
                "type": "list",
                "name": "algorithm",
                "message": "Which SRS algorithm you want to use for studying?",
                "choices": get_available_schedulers(),
                "default": deck.algorithm,
            },
            {
                "type": "input",
                "name": "params",
                "message": "Any extra parameters (JSON format)?",
                "default": deck.parameters,
            },
        ]
    )

    # This happens in case of a Ctrl+C during the above questions
    if (
        not answers.get("name")
        or not not answers.get("desc")
        or not answers.get("algorithm")
    ):
        click.echo("Deck update stopped.")
        return

    deck = Deck.update(
        db=db,
        object_id=deck.id,
        name=answers["name"],
        description=answers["description"],
        algorithm=answers["algorithm"],
        parameters=answers["params"] or "{}",
        state=None,
    )
    click.echo("Deck updated!")
    return deck


def delete_deck(db: Session, deck: Deck) -> None:
    """
    Deletes the given deck and gives some feedback to the user.

    :param db: a SQLAlchemy Session object
    :param deck: the Deck model object to delete
    """
    answers = prompt(
        [
            {
                "type": "confirm",
                "name": "confirm",
                "message": f"Are you really sure you want to delete '{deck.name}'? "
                "Its cards won't be deleted.",
                "default": False,
            }
        ]
    )
    if answers["confirm"]:
        Deck.delete(db=db, object_id=deck.id)
        click.echo("Deck deleted!")
    else:
        click.echo("The deck was NOT deleted.")
