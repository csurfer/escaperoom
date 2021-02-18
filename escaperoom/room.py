from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Puzzle:
    """Class with individual puzzle/page details."""

    title: str
    text: str
    images: List[str]
    hints: List[str]
    answer: str
    next_puzzle: str


@dataclass
class Game:
    """Class with overall escape room details."""

    # Story elements.
    title: str
    text: str
    images: List[str]

    # Dictionary of puzzles.
    puzzles: Dict[str, Puzzle]
