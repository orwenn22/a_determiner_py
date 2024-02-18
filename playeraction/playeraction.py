class PlayerAction(object):
    import testobj

    def __init__(self):
        self.action_name = "default"        # needs to be replaced in subclasses
        pass

    def on_click(self, player: testobj.TestObj, action_index: int):
        """
        Called when the button corresponding to the action is clicked.
        If we need to do something else than change the players' current action when clicking (for example
        instantly consuming an item ?), then this should be overwritten by the subclass.
        :param player: the player performing the action
        :param action_index: the index of the action in the player's actions
        """
        player.current_action = action_index
        print("clicked action", action_index)
        pass

    def on_update(self, player: testobj.TestObj, dt: float):
        """
        Called every frame on the player's update if the action is selected
        :param player: the player performing the action
        :param dt: delta time in seconds
        """
        pass

    def on_draw(self, player: testobj.TestObj):
        """
        Called every frame on the player's draw if the action is selected
        :param player: the player performing the action
        """
        pass
