from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.graphics import Color, Line, Rectangle
import pandas as pd


# Custom Label with Border
class BorderedLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.after:
            self.border_color = Color(0, 0, 0)  # Default border (Black)
            self.border = Line(width=1)
        self.bind(pos=self.update_border, size=self.update_border)

    def update_border(self, *args):
        self.border.rectangle = (self.x, self.y, self.width, self.height)

    def update_theme(self, bg_color, text_color, border_color):
        self.color = text_color
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*bg_color)  # Background Color
            Rectangle(pos=self.pos, size=self.size)

        self.border_color.rgb = border_color
        self.update_border()


class DataFrameTable(FloatLayout):
    def __init__(self, dataframe, **kwargs):
        super().__init__(**kwargs)
        self.dataframe = dataframe

        # Themes for Light and Dark Mode
        self.light_mode = {
            'bg': (1, 1, 1, 1), 'text': (0, 0, 0, 1), 'border': (0, 0, 0),
            'button_bg': (0, 0, 0, 1), 'button_text': (1, 1, 1, 1)
        }
        self.dark_mode = {
            'bg': (0, 0, 0, 1), 'text': (1, 1, 1, 1), 'border': (1, 1, 1),
            'button_bg': (1, 1, 1, 1), 'button_text': (0, 0, 0, 1)
        }
        self.current_theme = self.light_mode

        # Main Layout (Table + ScrollView)
        main_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.95), pos_hint={"x": 0, "top": 1})
        self.add_widget(main_layout)

        # Title Header
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, padding=(20, 10))
        main_layout.add_widget(header_layout)
        self.title_label = Label(text="[b]Data Table[/b]", markup=True, font_size=22)
        header_layout.add_widget(self.title_label)

        # Initialize Animation Variables
        self.current_column = 0
        self.columns_to_add = list(self.dataframe.columns)
        self.rows_to_add = self.dataframe.values.tolist()
        self.row_count = len(self.rows_to_add) 

        # Create Grid Layout with fixed rows and columns
        # +1 for the header row
        total_rows = self.row_count + 1
        # We'll add columns dynamically, but initialize with 0
        self.grid_layout = GridLayout(
            cols=0, 
            rows=total_rows,
            size_hint_y=None,
            spacing=2
        )
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        
        # Create empty grid cells
        self.grid_cells = []
        
        # Scrollable Table
        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.scroll_view.add_widget(self.grid_layout)
        main_layout.add_widget(self.scroll_view)

        # Next Button (Bottom-Center)
        self.next_button = Button(
            text="Next", size_hint=(None, None),
            size=(100, 50), pos_hint={"center_x": 0.5, "y": 0.01},
            font_size=18, background_normal=''
        )
        self.next_button.bind(on_press=self.add_next_column)
        self.add_widget(self.next_button)

        # Toggle Theme Button (Top-Right)
        self.theme_button = Button(
            text="Toggle Theme", size_hint=(None, None),
            size=(120, 40), pos_hint={"right": 0.98, "top": 0.98},
            font_size=14, background_normal=''
        )
        self.theme_button.bind(on_press=lambda x: self.toggle_theme())
        self.add_widget(self.theme_button)

        # Apply Initial Theme
        self.apply_theme()

    def add_next_column(self, instance):
        """Adds the next column when 'Next' is pressed."""
        if self.current_column >= len(self.columns_to_add):
            return  # Stop if all columns are added

        # Add new column to the grid
        self.grid_layout.cols += 1
        column_index = self.current_column
        
        # Clear existing cells for this column (if any)
        if column_index < len(self.grid_cells):
            for cell in self.grid_cells[column_index]:
                self.grid_layout.remove_widget(cell)
        else:
            # Initialize new column in grid_cells
            self.grid_cells.append([None] * (self.row_count + 1))
        
        # Create header cell
        header = BorderedLabel(
            text=f"[b]{self.columns_to_add[column_index]}[/b]",
            markup=True,
            size_hint_y=None,
            height=40
        )
        self.grid_layout.add_widget(header)
        self.grid_cells[column_index][0] = header
        
        # Create data cells
        for i, row in enumerate(self.rows_to_add):
            cell = BorderedLabel(
                text=str(row[column_index]),
                size_hint_y=None,
                height=30
            )
            self.grid_layout.add_widget(cell)
            self.grid_cells[column_index][i + 1] = cell
        
        # Apply theme to new cells
        self.update_new_widgets()
        
        # Move to next column
        self.current_column += 1

    def update_new_widgets(self):
        """Update the theme of the newly added widgets."""
        column_index = self.current_column
        if column_index < len(self.grid_cells):
            for cell in self.grid_cells[column_index]:
                if cell and isinstance(cell, BorderedLabel):
                    cell.update_theme(
                        self.current_theme['bg'],
                        self.current_theme['text'],
                        self.current_theme['border']
                    )

    def apply_theme(self):
        """Apply the current theme to the whole UI."""
        Window.clearcolor = self.current_theme['bg']
        self.title_label.color = self.current_theme['text']

        # Update Button Appearance
        self.next_button.background_color = self.current_theme['button_bg']
        self.next_button.color = self.current_theme['button_text']
        self.theme_button.background_color = self.current_theme['button_bg']
        self.theme_button.color = self.current_theme['button_text']

        # Update Existing Table Appearance
        for col in self.grid_cells:
            for cell in col:
                if cell and isinstance(cell, BorderedLabel):
                    cell.update_theme(
                        self.current_theme['bg'],
                        self.current_theme['text'],
                        self.current_theme['border']
                    )

    def toggle_theme(self):
        """Switch between light and dark themes."""
        self.current_theme = self.dark_mode if self.current_theme == self.light_mode else self.light_mode
        self.apply_theme()


class DataFrameApp(App):
    def build(self):
        # Sample DataFrame
        data = {
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 35],
            'City': ['New York', 'Los Angeles', 'Chicago'],
            'Score': [90, 85, 88]
        }
        df = pd.DataFrame(data)
        return DataFrameTable(df)


if __name__ == '__main__':
    DataFrameApp().run()