from __future__ import annotations

from datetime import datetime

from rich.text import Text

from ..widget import Widget
from ..reactive import Reactive, watch


class HeaderIcon(Widget):
    """Display an 'icon' on the left of the header."""

    DEFAULT_CSS = """
    HeaderIcon {
        dock: left;
        padding: 0 1;
        width: 8;
        content-align: left middle;
    }
    """
    icon = Reactive("⭘")

    def render(self):
        return self.icon


class HeaderClock(Widget):
    """Display a clock on the right of the header."""

    DEFAULT_CSS = """
    HeaderClock {
        dock: right;
        width: 10;
        padding: 0 1;
        background: $secondary-background-lighten-1;
        color: $text;
        text-opacity: 85%;
        content-align: center middle;
    }
    """

    def on_mount(self) -> None:
        self.set_interval(1, callback=self.refresh, name=f"update header clock")

    def render(self):
        return Text(datetime.now().time().strftime("%X"))


class HeaderTitle(Widget):
    """Display the title / subtitle in the header."""

    DEFAULT_CSS = """
    HeaderTitle {
        content-align: center middle;
        width: 100%;
        margin-right: 10;
    }
    """

    text: Reactive[str] = Reactive("")
    sub_text = Reactive("")

    def render(self) -> Text:
        text = Text(self.text, no_wrap=True, overflow="ellipsis")
        if self.sub_text:
            text.append(" — ")
            text.append(self.sub_text, "dim")
        return text


class Header(Widget):
    """A header widget with icon and clock.

    Args:
        show_clock (bool, optional): True if the clock should be shown on the right of the header.
    """

    DEFAULT_CSS = """
    Header {
        dock: top;
        width: 100%;
        background: $secondary-background;
        color: $text;
        height: 1;
    }
    Header.-tall {
        height: 3;
    }
    """

    tall = Reactive(True)

    DEFAULT_CLASSES = "-tall"

    def __init__(
        self,
        show_clock: bool = False,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ):
        super().__init__(name=name, id=id, classes=classes)
        self.show_clock = show_clock

    def compose(self):
        yield HeaderIcon()
        yield HeaderTitle()
        if self.show_clock:
            yield HeaderClock()

    def watch_tall(self, tall: bool) -> None:
        self.set_class(tall, "-tall")

    def on_click(self):
        self.toggle_class("-tall")

    def on_mount(self) -> None:
        def set_title(title: str) -> None:
            self.query_one(HeaderTitle).text = title

        def set_sub_title(sub_title: str) -> None:
            self.query_one(HeaderTitle).sub_text = sub_title

        watch(self.app, "title", set_title)
        watch(self.app, "sub_title", set_sub_title)
