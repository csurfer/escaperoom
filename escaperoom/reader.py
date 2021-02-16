from dataclasses import dataclass
from json import load, loads
from os import path
from typing import Any, Dict, List
from uuid import uuid4

import jsonschema


@dataclass
class Puzzle:
    title: str
    text: str
    images: List[str]
    hints: List[str]
    answer: str
    next_puzzle: str


class CampaignReader:
    STARTING_PUZZLE_KEY = "1"
    FINAL_PUZZLE_KEY = "end"

    # Common keys.
    TITLE_KEY = "title"
    TEXT_KEY = "text"
    IMAGES_KEY = "images"

    # Story keys.
    STORY_KEY = "story"

    # List of puzzles key
    PUZZLES_KEY = "puzzles"

    # Key in each puzzles.
    PUZZLE_HINTS_KEY = "hints"
    PUZZLE_ANSWER_KEY = "answer"

    def __init__(self, campaign_file):
        self.campaign = None
        with open(campaign_file, "r") as f:
            self.campaign = loads(f.read())

        self.schema = None
        here = path.abspath(path.dirname(__file__))
        with open(path.join(here, "config.schema"), "r") as f:
            self.schema = loads(f.read())

        # Validate the campaign.
        self.validate()

    def validate(self):
        """Method to validate the provided campaign."""
        jsonschema.validate(self.campaign, self.schema)

    def get_game_from_campaign(self) -> Dict[str, Any]:
        """Method to procure game setup from campaign."""
        game = {
            CampaignReader.TITLE_KEY: self.campaign[CampaignReader.STORY_KEY][
                CampaignReader.TITLE_KEY
            ],
            CampaignReader.TEXT_KEY: self.campaign[CampaignReader.STORY_KEY][
                CampaignReader.TEXT_KEY
            ],
            CampaignReader.IMAGES_KEY: self.campaign[CampaignReader.STORY_KEY][
                CampaignReader.IMAGES_KEY
            ],
        }

        next_key = CampaignReader.STARTING_PUZZLE_KEY
        total_steps = len(self.campaign[CampaignReader.PUZZLES_KEY])

        for i, puzzle in enumerate(self.campaign[CampaignReader.PUZZLES_KEY]):
            key = next_key
            next_key = str(uuid4())
            game[key] = Puzzle(
                title=puzzle[CampaignReader.TITLE_KEY],
                text=puzzle[CampaignReader.TEXT_KEY],
                images=puzzle[CampaignReader.IMAGES_KEY],
                hints=puzzle[CampaignReader.PUZZLE_HINTS_KEY],
                answer=puzzle[CampaignReader.PUZZLE_ANSWER_KEY],
                next_puzzle=CampaignReader.FINAL_PUZZLE_KEY
                if i == total_steps - 1
                else next_key,
            )

        return game
