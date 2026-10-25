import os
import calendar
from datetime import datetime, date

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.core.window import Window

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup

from PIL import Image, ImageDraw, ImageFont


# ==================================================
# SETTINGS
# ==================================================

Window.clearcolor = (0.94, 0.95, 0.97, 1)
Window.softinput_mode = "resize"

APP_TITLE = "ORDER SLIP MAKER"

IMAGE_WIDTH = 1200
MARGIN = 60

FONT_TITLE_SIZE = 54
FONT_LABEL_SIZE = 32
FONT_TEXT_SIZE = 30
FONT_SMALL_SIZE = 26


# ==================================================
# FONT HELPER
# ==================================================

def get_font(size, bold=False):

    if bold:
        font_paths = [
            "/system/fonts/Roboto-Bold.ttf",
            "/system/fonts/DroidSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
    else:
        font_paths = [
            "/system/fonts/Roboto-Regular.ttf",
            "/system/fonts/DroidSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]

    for path in font_paths:
        try:
            if os.path.exists(path):
                return ImageFont.truetype(path, size=size)
        except Exception:
            pass

    return ImageFont.load_default()


# ==================================================
# IMAGE GENERATOR
# ==================================================

def create_order_slip(data, items, output_path):

    width = IMAGE_WIDTH
    margin = MARGIN
    right = width - margin

    font_title = get_font(FONT_TITLE_SIZE, True)
    font_label = get_font(FONT_LABEL_SIZE, True)
    font_text = get_font(FONT_TEXT_SIZE)
    font_small = get_font(FONT_SMALL_SIZE)

    black = (0, 0, 0)
    gray = (170, 170, 170)

    details = [
        ("Ordered By", data["ordered_by"]),
        ("Address", data["address"]),
        ("Via", data["via"]),
        ("Date", data["date"]),
        ("Salesman", data["salesman"]),
    ]

    if data["order_type"] == "Wais Misis":
        details.append(
            ("WM Account Number", data["account_number"])
        )

    elif data["order_type"] == "Wholesale":
        details.append(
            ("WS Account Number", data["account_number"])
        )

    detail_height = 72
    table_header_height = 75
    row_height = 75
    signature_height = 150

    height = (
        180
        + len(details) * detail_height
        + table_header_height
        + max(len(items), 5) * row_height
        + signature_height
    )

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Outer border
    draw.rectangle(
        (15, 15, width - 15, height - 15),
        outline=black,
        width=4
    )

    # Title
    title = "ORDER SLIP"
    bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = bbox[2] - bbox[0]

    draw.text(
        ((width - title_width) // 2, 40),
        title,
        fill=black,
        font=font_title
    )

    draw.line(
        (margin, 120, right, 120),
        fill=black,
        width=3
    )

    y = 145

    # Order type
    draw.text(
        (margin, y),
        "ORDER TYPE:",
        fill=black,
        font=font_label
    )

    draw.text(
        (330, y + 2),
        data["order_type"],
        fill=black,
        font=font_text
    )

    y += 70

    # Details
    for label, value in details:

        draw.text(
            (margin, y),
            label + ":",
            fill=black,
            font=font_label
        )

        label_width = draw.textbbox(
            (0, 0),
            label + ":",
            font=font_label
        )[2]

        value_x = margin + label_width + 18
        max_width = right - value_x - 10

        value = str(value)
        words = value.split()

        lines = []
        current_line = ""

        for word in words:

            test_line = (
                current_line + " " + word
            ).strip()

            test_width = draw.textbbox(
                (0, 0),
                test_line,
                font=font_text
            )[2]

            if test_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)

                current_line = word

        if current_line:
            lines.append(current_line)

        if not lines:
            lines = [""]

        for line_index, line in enumerate(lines):

            draw.text(
                (
                    value_x,
                    y + line_index * 38
                ),
                line,
                fill=black,
                font=font_text
            )

        actual_height = max(
            detail_height,
            len(lines) * 42 + 20
        )

        y += actual_height

        draw.line(
            (margin, y - 8, right, y - 8),
            fill=gray,
            width=1
        )

    y += 15

    # Table header
    table_left = margin
    table_right = right
    quantity_divider = margin + 210

    draw.rectangle(
        (
            table_left,
            y,
            table_right,
            y + table_header_height
        ),
        outline=black,
        width=3
    )

    draw.text(
        (margin + 15, y + 18),
        "QUANTITY",
        fill=black,
        font=font_label
    )

    draw.text(
        (quantity_divider + 15, y + 18),
        "ARTICLE / DESCRIPTION",
        fill=black,
        font=font_label
    )

    draw.line(
        (
            quantity_divider,
            y,
            quantity_divider,
            y + table_header_height
        ),
        fill=black,
        width=3
    )

    y += table_header_height

    # Item rows
    row_count = max(len(items), 5)

    for index in range(row_count):

        draw.rectangle(
            (
                table_left,
                y,
                table_right,
                y + row_height
            ),
            outline=black,
            width=2
        )

        draw.line(
            (
                quantity_divider,
                y,
                quantity_divider,
                y + row_height
            ),
            fill=black,
            width=2
        )

        if index < len(items):

            quantity = str(items[index]["quantity"])
            article = str(items[index]["article"])

            draw.text(
                (margin + 15, y + 18),
                quantity,
                fill=black,
                font=font_text
            )

            article_x = quantity_divider + 15
            article_max_width = right - article_x - 10

            words = article.split()
            lines = []
            current_line = ""

            for word in words:

                test_line = (
                    current_line + " " + word
                ).strip()

                text_width = draw.textbbox(
                    (0, 0),
                    test_line,
                    font=font_text
                )[2]

                if text_width <= article_max_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)

                    current_line = word

            if current_line:
                lines.append(current_line)

            if lines:
                draw.text(
                    (article_x, y + 18),
                    lines[0],
                    fill=black,
                    font=font_text
                )

        y += row_height

    # Signature section
    y += 55

    draw.line(
        (margin, y, margin + 390, y),
        fill=black,
        width=2
    )

    draw.text(
        (margin + 35, y + 12),
        "Received / Prepared By",
        fill=black,
        font=font_small
    )

    draw.line(
        (right - 390, y, right, y),
        fill=black,
        width=2
    )

    draw.text(
        (right - 320, y + 12),
        "Authorized Signature",
        fill=black,
        font=font_small
    )

    output_folder = os.path.dirname(output_path)

    if output_folder:
        os.makedirs(output_folder, exist_ok=True)

    image.save(output_path, "PNG")

    return output_path


# ==================================================
# APPLICATION
# ==================================================

class OrderSlipApp(App):

    def build(self):

        self.title = APP_TITLE
        self.items = []
        self.inputs = {}

        scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=dp(6)
        )

        self.main_scroll = scroll

        self.root_layout = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(12),
            size_hint_y=None
        )

        self.root_layout.bind(
            minimum_height=self.root_layout.setter("height")
        )

        scroll.add_widget(self.root_layout)

        # Title
        self.root_layout.add_widget(
            Label(
                text="[b]ORDER SLIP MAKER[/b]",
                markup=True,
                font_size=sp(28),
                color=(0.05, 0.15, 0.30, 1),
                size_hint_y=None,
                height=dp(55)
            )
        )

        # Order type
        self.add_label("Order Type")

        self.order_type = Spinner(
            text="Retail",
            values=("Retail", "Wais Misis", "Wholesale"),
            size_hint_y=None,
            height=dp(58),
            font_size=sp(22),
            background_normal="",
            background_color=(0.85, 0.90, 0.98, 1),
            color=(0, 0, 0, 1)
        )

        self.order_type.bind(
            text=self.on_order_type_changed
        )

        self.root_layout.add_widget(self.order_type)

        # Conditional account number
        self.account_label = self.make_label(
            "WM Account Number"
        )

        self.account_input = self.make_input(
            "Enter account number"
        )

        self.account_label.height = 0
        self.account_input.height = 0

        self.account_label.opacity = 0
        self.account_input.opacity = 0

        self.account_label.disabled = True
        self.account_input.disabled = True

        self.root_layout.add_widget(self.account_label)
        self.root_layout.add_widget(self.account_input)

        # Standard fields
        fields = [
            ("Ordered By", "ordered_by"),
            ("Address", "address"),
            ("Via", "via"),
            ("Salesman", "salesman"),
        ]

        for label, key in fields:

            self.add_label(label)

            field = self.make_input(
                "Enter " + label
            )

            self.inputs[key] = field
            self.root_layout.add_widget(field)

        # Date picker
        self.add_label("Date")

        self.date_button = Button(
            text=date.today().strftime("%m/%d/%Y"),
            font_size=sp(22),
            size_hint_y=None,
            height=dp(58),
            background_normal="",
            background_color=(0.85, 0.90, 0.98, 1),
            color=(0, 0, 0, 1)
        )

        self.date_button.bind(
            on_release=self.open_date_picker
        )

        self.root_layout.add_widget(self.date_button)

        # Items section
        self.add_label("Items")

        header = GridLayout(
            cols=2,
            spacing=dp(8),
            size_hint_y=None,
            height=dp(45)
        )

        header.add_widget(
            Label(
                text="[b]Quantity[/b]",
                markup=True,
                font_size=sp(18),
                color=(0, 0, 0, 1)
            )
        )

        header.add_widget(
            Label(
                text="[b]Article / Description[/b]",
                markup=True,
                font_size=sp(18),
                color=(0, 0, 0, 1)
            )
        )

        self.root_layout.add_widget(header)

        self.items_layout = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            size_hint_y=None
        )

        self.items_layout.bind(
            minimum_height=self.items_layout.setter("height")
        )

        self.root_layout.add_widget(self.items_layout)

        self.add_item_row()

        # Add item button
        add_button = Button(
            text="+ ADD ITEM",
            font_size=sp(20),
            bold=True,
            size_hint_y=None,
            height=dp(58),
            background_normal="",
            background_color=(0.15, 0.55, 0.30, 1)
        )

        add_button.bind(
            on_release=lambda instance: self.add_item_row()
        )

        self.root_layout.add_widget(add_button)

        # Export button
        export_button = Button(
            text="SAVE ORDER SLIP AS IMAGE",
            font_size=sp(20),
            bold=True,
            size_hint_y=None,
            height=dp(65),
            background_normal="",
            background_color=(0.10, 0.35, 0.75, 1)
        )

        export_button.bind(
            on_release=lambda instance: self.export_image()
        )

        self.root_layout.add_widget(export_button)

        self.root_layout.add_widget(
            Label(
                text="PNG Image • Large Text • Offline Form",
                font_size=sp(16),
                color=(0.25, 0.25, 0.25, 1),
                size_hint_y=None,
                height=dp(40)
            )
        )

        return scroll

    # --------------------------------------------------
    # FORM HELPERS
    # --------------------------------------------------

    def make_label(self, text):

        label = Label(
            text=text,
            font_size=sp(21),
            bold=True,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(38),
            halign="left",
            valign="middle"
        )

        label.bind(
            size=lambda widget, value:
            setattr(widget, "text_size", value)
        )

        return label

    def add_label(self, text):

        self.root_layout.add_widget(
            self.make_label(text)
        )

    def make_input(self, hint):

        field = TextInput(
            hint_text=hint,
            multiline=False,
            font_size=sp(20),
            size_hint_y=None,
            height=dp(58),
            padding=(dp(12), dp(14)),
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            cursor_color=(0, 0, 0, 1)
        )

        field.bind(
            focus=self.on_input_focus
        )

        return field

    # --------------------------------------------------
    # KEYBOARD ADJUSTMENT
    # --------------------------------------------------

    def on_input_focus(self, widget, focused):

        if focused:
            Clock.schedule_once(
                lambda dt: self.show_focused_input(widget),
                0.25
            )

    def show_focused_input(self, widget):

        try:
            self.main_scroll.scroll_to(
                widget,
                padding=dp(180),
                animate=True
            )
        except Exception:
            pass

    # --------------------------------------------------
    # ORDER TYPE
    # --------------------------------------------------

    def on_order_type_changed(self, spinner, text):

        if text == "Retail":

            self.account_label.text = "WM Account Number"

            self.account_label.height = 0
            self.account_input.height = 0

            self.account_label.opacity = 0
            self.account_input.opacity = 0

            self.account_label.disabled = True
            self.account_input.disabled = True

            self.account_input.text = ""

        else:

            if text == "Wais Misis":
                self.account_label.text = "WM Account Number"
            else:
                self.account_label.text = "WS Account Number"

            self.account_label.height = dp(38)
            self.account_input.height = dp(58)

            self.account_label.opacity = 1
            self.account_input.opacity = 1

            self.account_label.disabled = False
            self.account_input.disabled = False

    # --------------------------------------------------
    # DATE PICKER - MONTH AND YEAR DROPDOWNS
    # --------------------------------------------------

    def open_date_picker(self, instance):

        month_names = [
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ]

        # Use the date currently shown in the button.
        try:
            current_date = datetime.strptime(
                self.date_button.text,
                "%m/%d/%Y"
            ).date()
        except ValueError:
            current_date = date.today()

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=dp(10)
        )

        # Month and year dropdowns
        selectors = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=dp(8)
        )

        month_spinner = Spinner(
            text=month_names[current_date.month - 1],
            values=month_names,
            font_size=sp(18)
        )

        year_spinner = Spinner(
            text=str(current_date.year),
            values=tuple(
                str(year)
                for year in range(
                    current_date.year - 10,
                    current_date.year + 11
                )
            ),
            font_size=sp(18)
        )

        selectors.add_widget(month_spinner)
        selectors.add_widget(year_spinner)

        content.add_widget(selectors)

        # Calendar grid
        calendar_grid = GridLayout(
            cols=7,
            spacing=dp(4),
            size_hint_y=None
        )

        calendar_grid.bind(
            minimum_height=calendar_grid.setter("height")
        )

        content.add_widget(calendar_grid)

        popup = Popup(
            title="SELECT DATE",
            content=content,
            size_hint=(0.96, 0.80)
        )

        def select_date(day, month, year):

            self.date_button.text = (
                f"{month:02d}/{day:02d}/{year}"
            )

            popup.dismiss()

        def draw_calendar(*args):

            calendar_grid.clear_widgets()

            month = month_names.index(
                month_spinner.text
            ) + 1

            year = int(year_spinner.text)

            # Weekday headings
            weekdays = [
                "Mon", "Tue", "Wed", "Thu",
                "Fri", "Sat", "Sun"
            ]

            for weekday in weekdays:

                calendar_grid.add_widget(
                    Label(
                        text=weekday,
                        font_size=sp(14),
                        bold=True,
                        color=(0, 0, 0, 1),
                        size_hint_y=None,
                        height=dp(32)
                    )
                )

            # Correct number of days, including leap years
            weeks = calendar.monthcalendar(year, month)

            for week in weeks:

                for day in week:

                    if day == 0:

                        calendar_grid.add_widget(
                            Label(
                                text="",
                                size_hint_y=None,
                                height=dp(44)
                            )
                        )

                    else:

                        is_current_date = (
                            day == current_date.day
                            and month == current_date.month
                            and year == current_date.year
                        )

                        button = Button(
                            text=str(day),
                            font_size=sp(18),
                            size_hint_y=None,
                            height=dp(44),
                            background_normal="",
                            background_color=(
                                (0.20, 0.48, 0.80, 1)
                                if is_current_date
                                else (0.88, 0.92, 0.98, 1)
                            ),
                            color=(0, 0, 0, 1)
                        )

                        button.bind(
                            on_release=lambda btn,
                            d=day,
                            m=month,
                            y=year:
                            select_date(d, m, y)
                        )

                        calendar_grid.add_widget(button)

        month_spinner.bind(
            text=draw_calendar
        )

        year_spinner.bind(
            text=draw_calendar
        )

        draw_calendar()
        popup.open()

    # --------------------------------------------------
    # ITEMS
    # --------------------------------------------------

    def add_item_row(self):

        row = GridLayout(
            cols=2,
            spacing=dp(8),
            size_hint_y=None,
            height=dp(58)
        )

        quantity_input = TextInput(
            hint_text="Quantity",
            multiline=False,
            input_filter="int",
            font_size=sp(20),
            size_hint_y=None,
            height=dp(58),
            padding=(dp(10), dp(14)),
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )

        article_input = TextInput(
            hint_text="Article / Description",
            multiline=False,
            font_size=sp(20),
            size_hint_y=None,
            height=dp(58),
            padding=(dp(10), dp(14)),
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )

        quantity_input.bind(
            focus=self.on_input_focus
        )

        article_input.bind(
            focus=self.on_input_focus
        )

        row.add_widget(quantity_input)
        row.add_widget(article_input)

        self.items_layout.add_widget(row)

        self.items.append({
            "quantity_input": quantity_input,
            "article_input": article_input
        })

    # --------------------------------------------------
    # EXPORT IMAGE
    # --------------------------------------------------

    def export_image(self):

        order_type = self.order_type.text

        account_number = ""

        if order_type != "Retail":
            account_number = self.account_input.text.strip()

            if not account_number:
                self.show_message(
                    "Missing Account Number",
                    "Please enter the account number."
                )
                return

        items = []

        for item in self.items:

            quantity = item["quantity_input"].text.strip()
            article = item["article_input"].text.strip()

            if quantity or article:

                items.append({
                    "quantity": quantity,
                    "article": article
                })

        if not items:
            self.show_message(
                "Missing Items",
                "Please enter at least one item."
            )
            return

        data = {
            "order_type": order_type,
            "account_number": account_number,
            "ordered_by": self.inputs["ordered_by"].text.strip(),
            "address": self.inputs["address"].text.strip(),
            "via": self.inputs["via"].text.strip(),
            "salesman": self.inputs["salesman"].text.strip(),
            "date": self.date_button.text
        }

        try:

            if hasattr(self, "user_data_dir"):
                preferred_folder = (
                    "/storage/emulated/0/Pictures/OrderSlipMaker"
                )

                try:
                    os.makedirs(
                        preferred_folder,
                        exist_ok=True
                    )

                    test_path = os.path.join(
                        preferred_folder,
                        ".permission_test"
                    )

                    with open(test_path, "w") as test_file:
                        test_file.write("test")

                    os.remove(test_path)

                    output_folder = preferred_folder

                except Exception:
                    output_folder = os.path.join(
                        self.user_data_dir,
                        "OrderSlipMaker"
                    )

                    os.makedirs(
                        output_folder,
                        exist_ok=True
                    )

            else:
                output_folder = os.path.join(
                    os.getcwd(),
                    "OrderSlipMaker"
                )

                os.makedirs(
                    output_folder,
                    exist_ok=True
                )

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            filename = f"OrderSlip_{timestamp}.png"

            output_path = os.path.join(
                output_folder,
                filename
            )

            create_order_slip(
                data,
                items,
                output_path
            )

            self.show_message(
                "Saved Successfully",
                "Order slip saved successfully!\n\n"
                + output_path
            )

        except Exception as error:

            self.show_message(
                "Save Error",
                str(error)
            )

    # --------------------------------------------------
    # MESSAGE POPUP
    # --------------------------------------------------

    def show_message(self, title, message):

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(12)
        )

        message_label = Label(
            text=message,
            font_size=sp(16),
            halign="center",
            valign="middle"
        )

        message_label.bind(
            size=lambda widget, value:
            setattr(widget, "text_size", value)
        )

        close_button = Button(
            text="OK",
            font_size=sp(18),
            size_hint_y=None,
            height=dp(48)
        )

        content.add_widget(message_label)
        content.add_widget(close_button)

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.92, 0.45),
            auto_dismiss=False
        )

        close_button.bind(
            on_release=popup.dismiss
        )

        popup.open()


# ==================================================
# RUN APPLICATION
# ==================================================

if __name__ == "__main__":
    OrderSlipApp().run()