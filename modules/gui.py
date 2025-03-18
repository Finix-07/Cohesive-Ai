from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Line, Rectangle
from kivy.core.window import Window
import pandas as pd


# Custom Label with borders and theme handling
class BorderedLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.after:
            self.border_color = Color(0, 0, 0)  # Default: Black border (Light Mode)
            self.border = Line(width=1, rectangle=(self.x, self.y, self.width, self.height))
        self.bind(pos=self.update_border, size=self.update_border)

    def update_border(self, *args):
        self.border.rectangle = (self.x, self.y, self.width, self.height)

    def update_theme(self, bg_color, text_color, border_color):
        self.color = text_color
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*bg_color)  # Background
            Rectangle(pos=self.pos, size=self.size)

        # Update border color
        self.border_color.rgb = border_color
        self.update_border()


class DataFrameTable(FloatLayout):
    def __init__(self, dataframe, **kwargs):
        super().__init__(**kwargs)
        self.dataframe = dataframe

        # Theme configurations
        self.light_mode = {
            'bg': (1, 1, 1, 1),      # White background
            'text': (0, 0, 0, 1),    # Black text
            'border': (0, 0, 0),     # Black border
            'label': "Dark",            # 'D' for Dark Mode
            'button_bg': (0, 0, 0, 1),   # Black button background
            'button_text': (1, 1, 1, 1)  # White button text
        }
        self.dark_mode = {
            'bg': (0, 0, 0, 1),      # Black background
            'text': (1, 1, 1, 1),    # White text
            'border': (1, 1, 1),     # White border
            'label': "Light",            # 'L' for Light Mode
            'button_bg': (1, 1, 1, 1),   # White button background
            'button_text': (0, 0, 0, 1)  # Black button text
        }

        # Current theme
        self.current_theme = self.light_mode

        # Main vertical layout (fixed header + scrollable table)
        main_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.95), pos_hint={"x": 0, "top": 1})
        self.add_widget(main_layout)

        # Header Layout (Fixed at Top)
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, padding=(20, 10))
        main_layout.add_widget(header_layout)

        # Title Label (Always at Top)
        self.title_label = Label(text="[b]Data Table[/b]", markup=True, size_hint=(1, 1), font_size=22)
        header_layout.add_widget(self.title_label)

        # Scroll view and grid layout for the table
        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.grid_layout = GridLayout(cols=len(dataframe.columns), size_hint_y=None, spacing=2)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))

        # Populate the table
        self.populate_table()

        self.scroll_view.add_widget(self.grid_layout)
        main_layout.add_widget(self.scroll_view)

        # Theme Toggle Button (Bottom-Right Corner)
        self.toggle_button = Button(
            text=self.current_theme['label'],
            size_hint=(None, None),
            size=(50, 50),
            pos_hint={"right": 0.98, "y": 0.01},
            font_size=18,
            background_normal=''
        )
        self.toggle_button.bind(on_press=self.toggle_theme)
        self.add_widget(self.toggle_button)

        # Apply the initial theme
        self.apply_theme()

    def populate_table(self):
        # Add column headers
        for column in self.dataframe.columns:
            self.grid_layout.add_widget(BorderedLabel(text=f"[b]{column}[/b]", markup=True, size_hint_y=None, height=40))

        # Add rows
        for _, row in self.dataframe.iterrows():
            for value in row:
                self.grid_layout.add_widget(BorderedLabel(text=str(value), size_hint_y=None, height=30))

    def apply_theme(self):
        # Update window background
        Window.clearcolor = self.current_theme['bg']

        # Update title and toggle button colors
        self.title_label.color = self.current_theme['text']

        # Update button text and background
        self.toggle_button.text = self.current_theme['label']
        self.toggle_button.background_color = self.current_theme['button_bg']
        self.toggle_button.color = self.current_theme['button_text']

        # Update table label colors and borders
        for widget in self.grid_layout.children:
            if isinstance(widget, BorderedLabel):
                widget.update_theme(
                    self.current_theme['bg'],
                    self.current_theme['text'],
                    self.current_theme['border']
                )

    def toggle_theme(self, instance):
        # Toggle between light and dark themes
        self.current_theme = self.dark_mode if self.current_theme == self.light_mode else self.light_mode
        self.apply_theme()


class DataFrameApp(App):
    def build(self):
        # Example DataFrame
        data = {
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 35],
            'City': ['New York', 'Los Angeles', 'Chicago']
        }
        df = pd.DataFrame(data)

        # Create the table
        return DataFrameTable(df)


if __name__ == '__main__':
    DataFrameApp().run()
