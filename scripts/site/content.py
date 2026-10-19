"""All page copy, keyed by page id and language."""
from content_home import HOME
from content_hub import HUB
from content_editor import EDITOR
from content_tools import TOOLS
from content_tools2 import TOOLS2
from content_tools3 import TOOLS3
from content_tools4 import TOOLS4
from content_tools5 import TOOLS5

CONTENT = {"home": HOME, "tools": HUB, **EDITOR, **TOOLS, **TOOLS2, **TOOLS3, **TOOLS4, **TOOLS5}
