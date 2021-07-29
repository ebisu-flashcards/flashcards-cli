import click
from PyInquirer import prompt
from sqlalchemy.orm import Session

from flashcards_core.schedulers import get_scheduler_for_deck
from flashcards_core.database import Deck


def study(session: Session):

    decks = Deck.get_all(session=session)
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

    deck = Deck.get_by_name(session=session, name=answers["deck"])
    scheduler = get_scheduler_for_deck(session=session, deck=deck)

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
            scheduler.process_test_result(card, True)
            click.echo(" ** Correct! **")
        else:
            scheduler.process_test_result(card, False)
            click.echo(f" __ Wrong! The answer was {card.answer.value} __")
