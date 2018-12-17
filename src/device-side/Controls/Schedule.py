from Speech import *
from Time import *
from Task import *


class Schedule:
    """This class handles the shedule defined in the database"""
    def __init__(self, database, actions):
        self.__tasks = []
        self.__database = database
        self.__actions = actions
        self.__last_check = get_time()

        self.update()

    def get_last_check(self):
        """Return the last check"""
        return self.__last_check

    def get_tasks(self):
        """Returns the tasks"""
        return self.__tasks

    def set_tasks(self, tasks):
        """Set the tasks"""
        self.__tasks = tasks

    def get_database(self):
        """Returns the database"""
        return self.__database

    def get_actions(self):
        """Returns the actions"""
        return self.__actions

    def set_last_check(self, check_time=None):
        """Sets the last check"""
        if check_time is not None:
            self.__last_check = check_time
        else:
            self.__last_check = get_time()

    def update(self):
        """Updates the schedule from the DB"""
        self.set_last_check()

        new_schedule = self.get_database().get(
            "tasks", "action_id, start_time, end_time, `interval`",
            "WHERE end_time > NOW() OR end_time IS NULL")
        new_tasks = []

        # PROCESS TASKS
        if new_schedule is not False:
            for new_task in new_schedule:
                new_tasks.append(Task(self.get_actions(), *new_task))

            self.set_tasks(new_tasks)
            say("I've updated the schedule, " + str(len(new_tasks)) + " tasks are set.")

    def run(self):
        """checks and executes items between last check and now"""
        to_run_tasks = self.items_after_last_check()

        if to_run_tasks != []:
            for task in to_run_tasks:
                task.run()

            print("Ran " + str(len(to_run_tasks)) + " tasks")

    def items_after_last_check(self):
        """ Returns the items to be executed between the last check and current time """
        tasks = []

        current_time = get_time()

        for task in self.get_tasks():
            if task.execute_in_interval(self.get_last_check(), current_time):
                tasks.append(task)

        self.set_last_check(current_time)
        return tasks
