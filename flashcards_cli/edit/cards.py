from typing import Optional

import click
from PyInquirer import prompt
from sqlalchemy.orm import Session

from flashcards_core.database import Deck, Card, Fact


def edit_cards(session: Session, deck: Deck):
    """
    Prompt for the Edit Cards menu.
    Lets the user select the cards they want to edit, or add new ones.

    :param session: a SQLAlchemy Session object
    """
    # When a suboperation is done, reshow this menu
    while True:
        answers = prompt(
            [
                {
                    "type": "list",
                    "name": "card",
                    "message": "Select the card you want to edit:",
                    "choices": ["< Back", "+ New Card"]
                    + [
                        f"{c.id}: {c.question.value} | {c.answer.value}"
                        for c in deck.cards
                    ],
                }
            ]
        )

        # Happens in case of Ctrl+C
        if not answers.get("card"):
            return

        deck: Deck
        if answers["card"] == "+ New Card":
            card = create_card(session, deck)
        elif answers["card"] == "< Back":
            return
        else:
            card_id = answers["card"].split(":")[0]
            card = Card.get_one(session=session, object_id=card_id)

        # Happens in case of Ctrl+C during any of the sub-operations (creation, update...)
        if not card:
            edit_cards(session, deck)
            return

        answers = prompt(
            [
                {
                    "type": "list",
                    "name": "operation",
                    "message": "What do you want to do to this card?",
                    "choices": [
                        "Modify",
                        "Delete",
                        "< Back",
                    ],
                }
            ]
        )

        if not answers.get("operation") or answers["operation"] == "< Back":
            edit_cards(session, deck)

        elif answers["operation"] == "Modify":
            update_card(session, card)

        elif answers["operation"] == "Delete":
            delete_card(session, card)


def create_card(session: Session, deck: Deck) -> None:
    """
    Created a new deck with the information gathered,
    and gives some feesessionack to the user.

    :param session: a SQLAlchemy Session object
    :returns: None. This is is intended, because in this way you won't
        get the "What to do with this card?" menu but go directly back.
    """
    answers = prompt(
        [
            {"type": "input", "name": "question", "message": "Question:"},
            {"type": "input", "name": "answer", "message": "Answer:"},
        ]
    )

    # This happens in case of a Ctrl+C during the above questions
    if not answers.get("question") or not answers.get("answer"):
        click.echo("Card creation stopped: no card was created.")
        return

    question = Fact.create(
        session=session, value=answers["question"], format="plaintext"
    )
    answer = Fact.create(session=session, value=answers["answer"], format="plaintext")
    Card.create(
        session=session, deck_id=deck.id, question_id=question.id, answer_id=answer.id
    )
    click.echo("New card created!")


def update_card(session: Session, card: Card) -> Optional[Card]:
    """
    Updates the given card with the information gathered,
    and gives some feesessionack to the user.

    :param session: a SQLAlchemy Session object
    :param deck: the Deck model object the card belongs to
    :param card: the Card model object to modify
    """
    answers = prompt(
        [
            {
                "type": "input",
                "name": "question",
                "message": "Question:",
                "default": card.question.value,
            },
            {
                "type": "input",
                "name": "answer",
                "message": "Answer:",
                "default": card.answer.value,
            },
        ]
    )

    # This happens in case of a Ctrl+C during the above questions
    if not answers.get("question") or not answers.get("answer"):
        click.echo("Card update stopped.")
        return

    Fact.update(
        session=session,
        object_id=card.question.id,
        value=answers["question"],
        format="plaintext",
    )
    Fact.update(
        session=session,
        object_id=card.answer.id,
        value=answers["answer"],
        format="plaintext",
    )

    click.echo("Card updated!")
    return card


def delete_card(session: Session, card: Card) -> None:
    """
    Deletes the given card and gives some feesessionack to the user.

    :param session: a SQLAlchemy Session object
    :param card: the Card model object to delete
    """
    answers = prompt(
        [
            {
                "type": "confirm",
                "name": "confirm",
                "message": "Are you really sure you want to delete this card?",
                "default": False,
            }
        ]
    )
    if answers["confirm"]:
        Card.delete(session=session, object_id=card.id)
        click.echo("Card deleted!")
    else:
        click.echo("The card was NOT deleted.")
