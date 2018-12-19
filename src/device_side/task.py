from math import floor
from speech import *
from time import *


# TEMPORARY TESTFUNCTION
def log_temperature():
    """Mimicks the temperature logging for now"""
    print("taking temperature.")

class Task:
    """Handles the tasks defined in the database"""
    # Choose right (used) variables when database is created
    def __init__(self, actions, action_id, start_time, end_time, interval):
        self.__actions = actions
        self.__action_id = action_id
        self.__start_time = get_time(start_time)
        self.__end_time = None
        if end_time is not None:
            self.__end_time = get_time(end_time)
        self.__interval = interval
        self.__last_run_time = 0

    def get_actions(self):
        """Returns the actions"""
        return self.__actions

    def get_action_id(self):
        """Returns the id"""
        return self.__action_id

    def get_start_time(self):
        """Returns the start time"""
        return self.__start_time

    def get_end_time(self):
        """Returns the end time"""
        return self.__end_time

    def get_interval(self):
        """Returns the interval"""
        return self.__interval

    def get_last_run_time(self):
        """Returns the last time the task ran"""
        return self.__last_run_time

    def set_last_run_time(self):
        """Set the last time the task ran"""
        self.__last_run_time = get_time()

    def execute_in_interval(self, interval_start, interval_end):
        """Returns whether the task should be executed in a given interval"""
        # Switch interval in case needed
        if interval_end < interval_start:
            interval_start, interval_end = interval_end, interval_start

        task_start = self.get_start_time()
        task_end = self.get_end_time()
        task_interval = self.get_interval()

        # If interval is Null, the task needs to be executed only once, on the task_start time
        if task_interval is None:
            if interval_start < task_start <= interval_end:
                return True

            return False

        # Basic wrong cases (interval before or after task start-stop)
        if interval_end < task_start or (task_end is not None and interval_start >= task_end):
            return False

        # If last execution was less than interval ago, no execution
        if abs(self.get_last_run_time() - interval_end) < task_interval:
            return False

        # Estimate the iteration that would be the end of the interval and
        #   the start of the interval, check the integer numer of iterations inbetween
        upper_i = floor((interval_end - task_start) / task_interval)
        lower_i = floor((interval_start - task_start) / task_interval)

        if lower_i == upper_i:
            return False

        return True

    def run(self):
        """Run a task"""
        executable_name = self.get_actions().get_executable(self.get_action_id())

        if executable_name is not False:
            possibles = globals().copy()
            possibles.update(locals())
            executable = possibles.get(executable_name)

            if not executable:
                raise NotImplementedError("Method %s not implemented" % executable_name)

            self.set_last_run_time()
            executable()

            return True
        return False
