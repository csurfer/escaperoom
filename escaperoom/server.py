import argparse
import datetime

from flask import Flask, redirect, render_template, request

from .reader import CampaignReader

app = Flask(__name__)

GAME = None
START_TIME = None


@app.route("/")
def index():
    return render_template(
        "index.html",
        title=GAME[CampaignReader.TITLE_KEY],
        text=GAME[CampaignReader.TEXT_KEY],
        images=GAME[CampaignReader.IMAGES_KEY],
    )


@app.route("/puzzle/<puzzle_id>", methods=["GET", "POST"])
def riddler(puzzle_id):
    global START_TIME

    if request.method == "GET":
        if puzzle_id == CampaignReader.STARTING_PUZZLE_KEY and START_TIME is None:
            START_TIME = datetime.datetime.now()

        if puzzle_id in GAME:
            puzzle = GAME[puzzle_id]
            return render_template(
                "puzzle.html",
                title=puzzle.title,
                text=puzzle.text,
                images=puzzle.images,
                hints=puzzle.hints,
            )
        else:
            redirect("/404")
    elif request.method == "POST":
        if puzzle_id in GAME:
            puzzle = GAME[puzzle_id]
            if request.form["answer"].lower() == puzzle.answer.lower():
                if puzzle.next_puzzle == CampaignReader.FINAL_PUZZLE_KEY:
                    seconds = int(
                        (datetime.datetime.now() - START_TIME).total_seconds()
                    )
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


def main():
    global GAME

    # Create command line parser.
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    # Create validation command parser.
    validation = subparsers.add_parser("validation")
    validation.add_argument("jsonfile", help="JSON file with escaperoom config")

    # Create run command parser.
    runner = subparsers.add_parser("run")
    runner.add_argument("jsonfile", help="JSON file with escaperoom config")
    runner.add_argument("--host", type=str, default="127.0.0.1")
    runner.add_argument("--port", type=int, default=5000)

    # Parse command line arguments.
    arguments = parser.parse_args()

    if arguments.command == "validation":
        CampaignReader(arguments.jsonfile)

    if arguments.command == "run":
        # Set game configuration.
        GAME = CampaignReader(arguments.jsonfile).get_game_from_campaign()

        # Run flask app.
        app.run(host=arguments.host, port=arguments.port)
