from utils import tabbarprovider


class EditorTabProvider(tabbarprovider.TabBarProvider):
    def __init__(self, editor):
        from editor import editorstate
        super().__init__()
        self.editor: editorstate.EditorState = editor

    def get_tab_count(self) -> int:
        return len(self.editor.pages)

    def get_tab_name(self, index: int) -> str:
        if 0 <= index < len(self.editor.pages):
            return self.editor.pages[index].name
        else:
            return "error"

    def on_tab_click(self, index: int):
        if 0 <= index < len(self.editor.pages):
            self.editor.current_page = index

    def get_selected_tab(self) -> int:
        return self.editor.current_page
