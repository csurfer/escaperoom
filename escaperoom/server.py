import argparse
import datetime
from typing import Any, Optional

from flask import Flask, redirect, render_template, request

from .reader import CampaignReader
from .room import Game

# Flask app.
app = Flask(__name__)

# Global variable for capturing game details.
GAME: Optional[Game] = None
# Global variable for capturing total time.
EPOCH: datetime.datetime = datetime.datetime(1970, 1, 1)
START_TIME: datetime.datetime = EPOCH


@app.route("/")
def index():
    """Method to render homepage."""
    return render_template(
        "index.html", title=GAME.title, text=GAME.text, images=GAME.images,
    )


def get_puzzle(puzzle_id: str) -> Any:
    """Method to get the puzzle.

    :param puzzle_id: ID of the puzzle.
    """
    global START_TIME
    if puzzle_id == CampaignReader.STARTING_PUZZLE_KEY and START_TIME == EPOCH:
        START_TIME = datetime.datetime.now()

    if GAME and puzzle_id in GAME.puzzles:
        puzzle = GAME.puzzles[puzzle_id]
        return render_template(
            "puzzle.html",
            title=puzzle.title,
            text=puzzle.text,
            images=puzzle.images,
            hints=puzzle.hints,
        )
    else:
        return redirect("/404")


def submit_answer(puzzle_id: str) -> Any:
    """Method to submit answer to the puzzle.

    :param puzzle_id: ID of the puzzle.
    """
    if GAME and puzzle_id in GAME.puzzles:
        puzzle = GAME.puzzles[puzzle_id]
        if request.form["answer"].lower() == puzzle.answer.lower():
            if puzzle.next_puzzle == CampaignReader.FINAL_PUZZLE_KEY:
                seconds = int((datetime.datetime.now() - START_TIME).total_seconds())
                minutes = seconds // 60
                seconds = seconds % 60
                hours = minutes // 60
                minutes = minutes % 60
                return render_template(
                    "winner.html",
                    timetaken=f"{hours} hours {minutes} minutes {seconds} seconds",
                )
            else:
                return redirect(f"/puzzle/{puzzle.next_puzzle}")
        else:
            return render_template(
                "puzzle.html",
                title=puzzle.title,
                text=puzzle.text,
                images=puzzle.images,
                hints=puzzle.hints,
            )
    else:
        return redirect("/404")


@app.route("/puzzle/<puzzle_id>", methods=["GET", "POST"])
def riddler(puzzle_id: str) -> Any:
    """Method to render the puzzles."""
    if request.method == "GET":
        return get_puzzle(puzzle_id)
    elif request.method == "POST":
        return submit_answer(puzzle_id)


def main():
    # Create command line parser.
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    # Create validation command parser.
    validator = subparsers.add_parser("validate")
    validator.add_argument("jsonfile", help="JSON file with escaperoom config")

    # Create run command parser.
    runner = subparsers.add_parser("run")
    runner.add_argument("jsonfile", help="JSON file with escaperoom config")
    runner.add_argument("--host", type=str, default="127.0.0.1")
    runner.add_argument("--port", type=int, default=5000)

    # Parse command line arguments.
    arguments = parser.parse_args()

    if arguments.command == "validate":
        CampaignReader(arguments.jsonfile)

    if arguments.command == "run":
        # Set game configuration.
        global GAME
        GAME = CampaignReader(arguments.jsonfile).get_game_from_campaign()

        # Run flask app.
        app.run(host=arguments.host, port=arguments.port)
