class TabBarProvider:
    def __init__(self):
        pass        # Nothing to do, TabBarProvider is a pure interface

    def get_tab_count(self) -> int:
        return 0

    def get_tab_name(self, index: int) -> str:
        return ""

    def on_tab_click(self, index: int):
        pass

    def get_selected_tab(self) -> int:
        return 0