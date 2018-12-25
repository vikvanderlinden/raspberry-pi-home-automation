"""
    Handles the tasks.
"""

from math import floor
import time
import timings #pylint: disable=E0401

def read_temp_raw(sensorpath):
    """Reads the raw temperature"""
    temperature_file = open(sensorpath, 'r')
    lines = temperature_file.readlines()
    temperature_file.close()

    return lines

def current_temperature(sensorpath):
    """Reads the current temperature"""
    lines = read_temp_raw(sensorpath)

    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(sensorpath)

    equals_pos = lines[1].find('t=')

    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000

        return temp_c

    return False

def log_temperature(configuration, database):
    """Logs the temperature"""
    temp = current_temperature(configuration.get('sensor.basepath') + configuration.get('sensor.tempsens'))

    database.insert("temperatures", {"temperature": "%f"}, [temp])

class Task:
    """Handles the tasks defined in the database"""
    # Choose right (used) variables when database is created
    def __init__(self, config, database, actions, action_id, start_time, end_time, interval):
        self._config = config
        self._database = database
        self._actions = actions
        self._action_id = action_id
        self._start_time = timings.get_time(start_time)
        self._end_time = None
        if end_time is not None:
            self._end_time = timings.get_time(end_time)
        self._interval = interval
        self._last_run_time = 0

    def get_config(self):
        """Returns the configuration object"""
        return self._config

    def get_database(self):
        """Returns the database object"""
        return self._database

    def get_actions(self):
        """Returns the actions"""
        return self._actions

    def get_action_id(self):
        """Returns the id"""
        return self._action_id

    def get_start_time(self):
        """Returns the start time"""
        return self._start_time

    def get_end_time(self):
        """Returns the end time"""
        return self._end_time

    def get_interval(self):
        """Returns the interval"""
        return self._interval

    def get_last_run_time(self):
        """Returns the last time the task ran"""
        return self._last_run_time

    def set_last_run_time(self):
        """Set the last time the task ran"""
        self._last_run_time = timings.get_time()

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
            executable(self.get_config(), self.get_database())

            return True
        return False
