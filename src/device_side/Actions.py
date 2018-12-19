from Speech import *


class Actions:
    """This class handles the actions defined in the database"""
    def __init__(self, database):
        self.__action_list = dict()
        self.__database = database
        self.update()

    def get_action_list(self):
        """Returns a list of actions"""
        return self.__action_list

    def set_action_list(self, actions):
        """Sets the list of actions"""
        self.__action_list = actions

    def get_database(self):
        """Returns the database"""
        return self.__database

    def update(self):
        """Updates the actions from the database"""
        new_actions = self.get_database().get("actions", "id, executable", "WHERE active = 1")

        actions = dict()

        if new_actions is not False:
            for action in new_actions:
                actions[action[0]] = action[1]

            self.set_action_list(actions)
            say("I've updated the actions, " + str(len(actions)) + " actions are defined.")

    def get_executable(self, action_id):
        """Returns the executable of the action"""
        return self.get_action_list().get(action_id, False)
