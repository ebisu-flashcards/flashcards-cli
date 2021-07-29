import sys
import click
from time import sleep
from PyInquirer import prompt

from flashcards_core.database import init_db

from flashcards_cli.study import study
from flashcards_cli.edit import edit


def main():
    """
    Main CLI menu. Creates the initial DB connection
    through a flashcards-core's init_db() call.
    """
    session = init_db()()
    click.echo("\n****************************")
    click.echo(" Welcome to Flashcards CLI! ")
    click.echo("****************************\n")
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
            study(session)
        elif answers.get("choose_operation") == "Edit my collections":
            edit(session)
        elif answers.get("choose_operation") == "Quit":
            click.echo("Bye bye!")
            return
        else:
            click.echo("Bye bye!")
            sleep(1)
            sys.exit(0)


if __name__ == "__main__":
    main()
