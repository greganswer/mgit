import json
import os

FILENAME = "mgit.json"
ALLOWED_ATTRIBUTES = ["issue_tracker_api"]


class Config(dict):
    def __getattr__(self, key):
        """ Load the JSON file and get the value. """
        if key not in ALLOWED_ATTRIBUTES:
            raise KeyError(f"'{key}' is not an allowed attribute")

        self.load()
        return self.get(key)

    def __setattr__(self, key, value):
        """
        Set the value and save to the JSON file.

        This also removes the trailing slash from URL values.
        """
        if key not in ALLOWED_ATTRIBUTES:
            raise KeyError(f"'{key}' is not an allowed attribute")

        if "http://" in value or "https://" in value:
            value = value.strip("/")

        self[key] = value
        self.save()

    def load(self, force=False):
        """ Lazy load data from the JSON file. """
        if not self.get("issue_tracker_api") or force:
            with open(FILENAME) as infile:
                data = json.load(infile)
                for key in ALLOWED_ATTRIBUTES:
                    self[key] = data[key]

    def save(self):
        """ Save data to the JSON file. """
        with open(FILENAME, "w") as outfile:
            json.dump(self, outfile)

    # Issue tracker values

    @property
    def issue_tracker(self) -> str:
        """ Get the name of the issue tracker provider. """
        if self.issue_tracker_is_github:
            return "GitHub"

        return ""

    @property
    def issue_tracker_is_github(self) -> bool:
        return "github.com" in self.issue_tracker_api


def loaded() -> bool:
    return os.path.isfile(FILENAME)
