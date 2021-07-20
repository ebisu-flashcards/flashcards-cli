import sys
import click
from PyInquirer import prompt

from flashcards_core.database import SessionLocal

from flashcards_cli.study import study
from flashcards_cli.edit import edit


def main():
    """
    Main CLI menu. Creates the initial DB connection
    through a flashcards-core's SessionLocal() call.
    """
    db = SessionLocal()
    click.echo("****************************")
    click.echo(" Welcome to Flashcards CLI! ")
    click.echo("****************************")
    while True:
        answers = prompt(
            [
                {
                    "type": "list",
                    "name": "choose_operation",
                    "message": "What do you want to do?",
                    "choices": ["Study", "Edit my collections", "Quit"],
                }
            ]
        )
        if answers.get("choose_operation") == "Study":
            study(db)
        elif answers.get("choose_operation") == "Edit my collections":
            edit(db)
        elif answers.get("choose_operation") == "Quit":
            click.echo("Bye bye!")
            return
        else:
            click.echo("Bye bye!")
            sys.exit(0)


if __name__ == "__main__":
    main()
