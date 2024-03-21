class EditorPage:
    def __init__(self, name: str, editor):
        from editor import editorstate
        self.name = name
        self.editor: editorstate.EditorState = editor

    def update(self, dt: float):
        pass

    def draw(self):
        pass
