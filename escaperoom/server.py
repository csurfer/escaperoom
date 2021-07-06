import argparse
from datetime import *
from typing import Any, Optional

from flask import Flask, redirect, render_template, request, make_response

from reader import CampaignReader
from room import Game
import logging

# Flask app.
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Global variable for capturing game details.
GAME: Optional[Game] = None
MAX_PLAY_TIME_MINUTES = 60

@app.route("/", methods=['POST', 'GET'])
def index():
    """Method to render homepage."""
    if request.method == 'GET':
        return render_template(
            "index.html", title=GAME.title, text=GAME.text, images=GAME.images, playtime=MAX_PLAY_TIME_MINUTES,
        )
    elif request.method == 'POST':
        user = request.form['teamname']
        if not user:
            raise
        expireTime = datetime.now() + timedelta(minutes = (MAX_PLAY_TIME_MINUTES + 60))
        response = make_response(redirect("/puzzle/1"))
        response.set_cookie('userID', user, expires=expireTime)
        response.set_cookie('startTime', str(datetime.now()), expires=expireTime)
        return response

def get_puzzle(puzzle_id: str) -> Any:
    """Method to get the puzzle.

    :param puzzle_id: ID of the puzzle.
    """
    if puzzle_id == CampaignReader.STARTING_PUZZLE_KEY:
        teamName = request.cookies.get('userID')
        startTime = request.cookies.get('startTime')
        app.logger.info('Team ' + teamName + ' started at ' + startTime)

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
        start_time = datetime.fromisoformat(request.cookies.get('startTime'))
        team_name = request.cookies.get('userID')
        playing_time = datetime.now() - start_time
        if request.form["answer"].lower() == puzzle.answer.lower():
            if puzzle.next_puzzle == CampaignReader.FINAL_PUZZLE_KEY:
                app.logger.info(team_name + " finished in " + str(playing_time))
                hours, remainder = divmod(playing_time.total_seconds(), 3600)
                minutes, seconds = divmod(remainder, 60)
                return render_template(
                    "winner.html",
                    timetaken=f"{int(round(hours, 0))} hours {int(round(minutes, 0))} minutes {int(round(seconds, 0))} seconds",
                )
            else:
                app.logger.info(team_name + " goes to puzzle " + puzzle.title + " after " + str(playing_time))
                return redirect(f"/puzzle/{puzzle.next_puzzle}")
        elif (playing_time.total_seconds() / 60) > MAX_PLAY_TIME_MINUTES:
            app.logger.info(team_name + " failed after " + str(playing_time))
            hours, remainder = divmod(playing_time.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            return render_template(
                "loser.html",
                timetaken=f"{int(round(hours, 0))} hours {int(round(minutes, 0))} minutes {int(round(seconds, 0))} seconds",
            )
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

if __name__ == '__main__':
    main()
