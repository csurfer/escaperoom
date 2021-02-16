from flask import Flask, redirect, render_template, request

from .reader import CampaignReader

app = Flask(__name__)

GAME = CampaignReader(
    "/home/csurfer/escaperoom/escaperoom/example_campaigns/example_campaign_1.json"
).get_game_from_campaign()


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
    if request.method == "GET":
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
                    return render_template("winner.html")
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
