from decimal import Decimal

from textual import events, on
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.css.query import NoMatches
from textual.reactive import var
from textual.binding import Binding
from textual.widgets import Button, Digits, Footer, Label, Tabs, TabbedContent, TabPane, Header, Input

from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import fnmatch
import json
import time
import os
import random
import re


class ToolApp(App):

    CSS_PATH = "styles.css"

    numbers = var("0")
    show_ac = var(True)
    left = var(Decimal("0"))
    right = var(Decimal("0"))
    value = var("")
    operator = var("plus")

    BINDINGS = [
        Binding(key="d", action="toggle_dark", description="Toggle dark mode"),
        Binding(
            key="question_mark",
            action="help",
            description="Show help screen",
            key_display="?",
        ),
        Binding(key="delete", action="delete", description="Delete the thing"),
        Binding(key="j", action="down", description="Scroll down", show=False),
    ]

    NAME_MAP = {
        "asterisk": "multiply",
        "slash": "divide",
        "underscore": "plus-minus",
        "full_stop": "point",
        "plus_minus_sign": "plus-minus",
        "percent_sign": "percent",
        "equals_sign": "equals",
        "minus": "minus",
        "plus": "plus",
    }

    CSS = """
        Tabs {
        dock: top;
        }
        Screen {
            align: center middle;
        }
        Label {
            margin:1 1;
            width: 100%;
            height: 100%;
            background: $panel;
            border: tall $primary;
            content-align: center middle;
        }

        Screen {
            overflow: auto;
        }

        #calculator {
            layout: grid;
            grid-size: 4;
            grid-gutter: 1 2;
            grid-columns: 1fr;
            grid-rows: 2fr 1fr 1fr 1fr 1fr 1fr;
            margin: 1 2;
            min-height: 25;
            min-width: 26;
            height: 100%;
        }

        Button {
            width: 100%;
            height: 100%;
            
        }

        Button:hover {
            background: $primary-lighten-2;
            border: none; 
        }

        #minus:hover, #plus:hover, #divide:hover, #multiply:hover, #equals:hover {
            background: #eaa73c !important;
            border: none; 
        }

        #numbers {
            column-span: 4;
            padding: 0 1;
            height: 100%;
            background: $primary-lighten-2;
            color: $text;
            content-align: center middle;
            text-align: right;
        }

        #number-0 {
            column-span: 2;
        }

    """

    def on_mount(self) -> None:
        """Focus the tabs when the app starts."""
        self.query_one(Tabs).focus()

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        """Handle TabActivated message sent by Tabs."""
        label = self.query_one(Label)
        if event.tab is None:
            label.visible = False
        else:
            label.visible = True
            label.update(event.tab.label)


    def watch_numbers(self, value: str) -> None:
        self.query_one("#numbers", Digits).update(value)

    def compute_show_ac(self) -> bool:
        return self.value in ("", "0") and self.numbers == "0"

    def watch_show_ac(self, show_ac: bool) -> None:
        self.query_one("#c").display = not show_ac
        self.query_one("#ac").display = show_ac

    def compose(self) -> ComposeResult:

        with TabbedContent(id="tabs"):
            with TabPane("Calculator"):
                with Container(id="calculator"):
                    yield Digits(id="numbers")
                    yield Button("AC", id="ac", variant="primary")
                    yield Button("C", id="c", variant="primary")
                    yield Button("+/-", id="plus-minus", variant="primary")
                    yield Button("%", id="percent", variant="primary")
                    yield Button("÷", id="divide", variant="warning")
                    yield Button("7", id="number-7", classes="number")
                    yield Button("8", id="number-8", classes="number")
                    yield Button("9", id="number-9", classes="number")
                    yield Button("×", id="multiply", variant="warning")
                    yield Button("4", id="number-4", classes="number")
                    yield Button("5", id="number-5", classes="number")
                    yield Button("6", id="number-6", classes="number")
                    yield Button("-", id="minus", variant="warning")
                    yield Button("1", id="number-1", classes="number")
                    yield Button("2", id="number-2", classes="number")
                    yield Button("3", id="number-3", classes="number")
                    yield Button("+", id="plus", variant="warning")
                    yield Button("0", id="number-0", classes="number")
                    yield Button(".", id="point")
                    yield Button("=", id="equals", variant="warning")
            with TabPane("Analizer"):
                with Container(id="analizer__container"):
                    with Container(id="container__buttons"):
                        yield Button("Analyze text", id="btn__analize__text", variant="default")
                        yield Button("Analyze File", id="btn__analizer__file", variant="primary")
                        yield Button("Graph", id="btn__graph__result", variant="success")
                    with Container(id="container__analize__text"):
                        yield Label("Enter the text to analyze: ", id="label__analize__text")
                        yield Input(placeholder="First Name")
            with TabPane("Pass_Generator"):
                with Container(id="pass-generator"):
                    yield Button("Pass", id="passgenerator", variant="success")
            with TabPane("Speech"):
                with Container(id="speech"):
                    yield Button("Speech", id="speecher", variant="success")
            with TabPane("Alarm"):
                with Container(id="alarm"):
                    yield Button("Alarm", id="alarm", variant="success")
            
        yield Header()
        yield Footer()

    @on(Button.Pressed, '#btn__analize__text')
    def analize_text(self, event: Button.Pressed) -> None:
        self.query_one("#container__buttons").display = False

        self.query_one("#container__analize__text").display = True

    
    def on_key(self, event: events.Key) -> None:
        def press(button_id: str) -> None:
            try:
                self.query_one(f"#{button_id}", Button).press()
            except NoMatches:
                pass

        key = event.key
        if key.isdecimal():
            press(f"number-{key}")
        elif key == "c":
            press("c")
            press("ac")
        else:
            button_id = self.NAME_MAP.get(key)
            if button_id is not None:
                press(self.NAME_MAP.get(key, key))

    @on(Button.Pressed, ".number")
    def number_pressed(self, event: Button.Pressed) -> None:
        assert event.button.id is not None
        number = event.button.id.partition("-")[-1]
        self.numbers = self.value = self.value.lstrip("0") + number

    @on(Button.Pressed, "#plus-minus")
    def plus_minus_pressed(self) -> None:
        self.numbers = self.value = str(Decimal(self.value or "0") * -1)

    @on(Button.Pressed, "#percent")
    def percent_pressed(self) -> None:
        self.numbers = self.value = str(Decimal(self.value or "0") / Decimal(100))

    @on(Button.Pressed, "#point")
    def pressed_point(self) -> None:
        if "." not in self.value:
            self.numbers = self.value = (self.value or "0") + "."

    @on(Button.Pressed, "#ac")
    def pressed_ac(self) -> None:
        self.value = ""
        self.left = self.right = Decimal(0)
        self.operator = "plus"
        self.numbers = "0"

    @on(Button.Pressed, "#c")
    def pressed_c(self) -> None:
        self.value = ""
        self.numbers = "0"

    def _do_math(self) -> None:
        try:
            if self.operator == "plus":
                self.left += self.right
            elif self.operator == "minus":
                self.left -= self.right
            elif self.operator == "divide":
                self.left /= self.right
            elif self.operator == "multiply":
                self.left *= self.right
            self.numbers = str(self.left)
            self.value = ""
        except Exception:
            self.numbers = "Error"

    @on(Button.Pressed, "#plus,#minus,#divide,#multiply")
    def pressed_op(self, event: Button.Pressed) -> None:
        self.right = Decimal(self.value or "0")
        self._do_math()
        assert event.button.id is not None
        self.operator = event.button.id

    @on(Button.Pressed, "#equals")
    def pressed_equals(self) -> None:
        if self.value:
            self.right = Decimal(self.value)
        self._do_math()
    
    def action_toggle_dark(self) -> None:
        self.dark = not self.dark


if __name__ == "__main__":
    ToolApp().run()