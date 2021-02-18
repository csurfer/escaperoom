from copy import deepcopy
from json import loads
from os import path
from typing import Any, Dict
from unittest.mock import mock_open, patch

import pytest
from jsonschema import ValidationError

from escaperoom.reader import CampaignReader


@pytest.fixture
def schema() -> Dict[str, Any]:
    here = path.abspath(path.dirname(__file__))
    schema_path = path.join(here, "..", "..", "escaperoom", "config.schema")
    with open(schema_path, "r") as f:
        return loads(f.read())


@pytest.fixture
def valid_json() -> Dict[str, Any]:
    return {
        "story": {"title": "s", "text": "s", "images": ["https://testserver/ted.gif"]},
        "puzzles": [
            {
                "title": "t1",
                "text": "t1",
                "images": ["https://testserver/over.jpg", "/path/to/freedom.jpg"],
                "hints": ["h1", "h2"],
                "answer": "a1",
            },
            {
                "title": "t2",
                "text": "t2",
                "images": ["https://testserver/la.jpg", "/path/to/escape.jpg"],
                "hints": ["h1"],
                "answer": "a2",
            },
        ],
    }


@pytest.fixture
def valid_json_empty_images_and_hints() -> Dict[str, Any]:
    return {
        "story": {"title": "s", "text": "s", "images": []},
        "puzzles": [
            {"title": "t1", "text": "t1", "images": [], "hints": [], "answer": "a1"}
        ],
    }


def validation(load_file_patch, campaign_dict, schema_dict) -> None:
    # Campaign gets loaded before schema.
    load_file_patch.side_effect = [campaign_dict, schema_dict]
    CampaignReader("test_file").validate()


@patch("escaperoom.reader.CampaignReader._load_file")
def test_validate_success(load_file_patch, valid_json, schema) -> None:
    validation(load_file_patch, valid_json, schema)


@patch("escaperoom.reader.CampaignReader._load_file")
def test_validate_success_empty_image_and_hint_list(
    load_file_patch, valid_json_empty_images_and_hints, schema
) -> None:
    validation(load_file_patch, valid_json_empty_images_and_hints, schema)


@patch("escaperoom.reader.CampaignReader._load_file")
def test_validate_failure(load_file_patch, valid_json, schema) -> None:
    # Top level key deletion test.
    for key in ["story", "puzzles"]:
        dc = deepcopy(valid_json)
        del dc[key]
        with pytest.raises(ValidationError):
            validation(load_file_patch, dc, schema)
    # Story key deletion test.
    for key in ["title", "text", "images"]:
        dc = deepcopy(valid_json)
        del dc["story"][key]
        with pytest.raises(ValidationError):
            validation(load_file_patch, dc, schema)
    # Puzzle key deletion test.
    for key in ["title", "text", "images", "hints", "answer"]:
        dc = deepcopy(valid_json)
        del dc["puzzles"][0][key]
        with pytest.raises(ValidationError):
            validation(load_file_patch, dc, schema)
