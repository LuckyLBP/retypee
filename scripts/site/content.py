"""All page copy, keyed by page id and language."""
from content_home import HOME
from content_hub import HUB
from content_editor import EDITOR
from content_tools import TOOLS

CONTENT = {"home": HOME, "tools": HUB, **EDITOR, **TOOLS}
