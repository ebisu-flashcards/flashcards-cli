import click
from PyInquirer import prompt
from sqlalchemy.orm import Session

from flashcards_core.schedulers import get_scheduler_for_deck
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
                "choices": [deck.name for deck in decks] + ["< Back"],
            }
        ]
    )

    # Happens in case of Ctrl+C
    if not answers.get("deck") or answers["deck"] == "< Back":
        return

    deck = Deck.get_by_name(db=db, name=answers["deck"])
    scheduler = get_scheduler_for_deck(db=db, deck=deck)

    reviewed_cards = 0
    while True:

        reviewed_cards += 1
        card = scheduler.next_card()
        click.echo(f"\n Card #{reviewed_cards} -------------------")
        answer = prompt(
            [
                {
                    "type": "input",
                    "name": "answer",
                    "message": f"Q: {card.question.value}",
                }
            ]
        )

        if not answer.get("answer"):
            click.echo("\n----------")
            click.echo(" Bye bye!")
            click.echo("----------\n")
            return

        if answer["answer"] == card.answer.value:
            click.echo(" ** Correct! **")
        else:
            click.echo(f" __ Wrong! The answer was {card.answer.value} __")
