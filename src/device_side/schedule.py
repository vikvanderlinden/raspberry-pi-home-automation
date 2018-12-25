"""
    Shedules the tasks.
"""

import speech #pylint: disable=E0401
import timings #pylint: disable=E0401
import task #pylint: disable=E0401


class Schedule:
    """This class handles the shedule defined in the database"""
    def __init__(self, config, database, actions):
        self._config = config
        self._tasks = []
        self._database = database
        self._actions = actions
        self._last_check = timings.get_time()

        self.update()

    def get_config(self):
        """Return the config object"""
        return self._config

    def get_last_check(self):
        """Return the last check"""
        return self._last_check

    def get_tasks(self):
        """Returns the tasks"""
        return self._tasks

    def set_tasks(self, tasks):
        """Set the tasks"""
        self._tasks = tasks

    def get_database(self):
        """Returns the database"""
        return self._database

    def get_actions(self):
        """Returns the actions"""
        return self._actions

    def set_last_check(self, check_time=None):
        """Sets the last check"""
        if check_time is not None:
            self._last_check = check_time
        else:
            self._last_check = timings.get_time()

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
                new_tasks.append(task.Task(self.get_config(), self.get_database(), self.get_actions(), *new_task))

            self.set_tasks(new_tasks)
            speech.say("I've updated the schedule, " + str(len(new_tasks)) + " tasks are set.")

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

        current_time = timings.get_time()

        for task in self.get_tasks():
            if task.execute_in_interval(self.get_last_check(), current_time):
                tasks.append(task)

        self.set_last_check(current_time)
        return tasks
