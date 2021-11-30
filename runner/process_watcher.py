# -*- coding: utf-8 -*-
"""This module provides functions to check a process' status based on the command used to spawn said process.
"""
from subprocess import check_output
from datetime import datetime
from dateutil import parser
from shlex import split
from shutil import which
from typing import List, Tuple

def get_executable(command: str) -> str:
    """
    Get the name of the executable that was called using the provided command.

    This function assumes that the first thing that is a valid executable in
    the provided command is the executable that was called using the command.

    The previous assumption might cause this function to be wrong if a parameter
    is passed before the command (like environment variables) is also a valid
    command (an executable in the user's PATH).

    Args:
        command: The command from which we want to extract the executable.

    Returns: The full path towards the first valid executable call that was
        found in the provided command.
    """
    command_name: str = ""
    for item in split(command_name):
        executable_path = which(item)
        if executable_path:
            command_name = executable_path

    return command_name

def get_pid(ps_output_line: str) -> int:
    """
    Extracts a process id from one of `ps`' output lines.

    This function assumes that the pid is the first element on each
    line returned by the ps command.

    Args:
        ps_output_line: A line from the `ps` program's output.

    Returns: The pid as an integer if everything went as expected. `-1`
        if there was a problem.
    """
    pid_as_string: str = ps_output_line.split()[0] # Should always be the first item.
    try:
        return int(pid_as_string)
    except ValueError:
        return -1

def get_start_time(ps_output_line: str) -> datetime:
    """
    Get the start time of a process from one of `ps`' output
    lines.

    Args:
        ps_output_line: A line returned by the command
            `ps -eo pid,lstart,cmd`.

    Returns: When the process described in `ps_output_line`
        started.

    """
    # Sample output from ps -eo pid,lstart,cmd:
    # 2954 Mon Nov 29 22:53:06 2021 vim
    time_as_string: str = ps_output_line.split()[1:6]
    time_as_datetime: datetime = parser.parse(time_as_string)
    return time_as_datetime

def get_pids_to_watch(executable_path: str) -> List[Tuple[int, datetime]]:
    """
    Find each process id's that should be watched to check if the process started by
    the provided executable path has completed it's execution.

    This function uses `get_pid()` on each line returned by the `which` command.

    Args:
        executable_path: The full path towards the executable to search process
            ids for.

    Returns: A list of process ids (index `0` of each tuple) related to the provided
        executable_path and the time at which the process started (index `1`).

    """
    process_ids_to_watch: List[Tuple[int, datetime]] = []
    ps_output = check_output(["ps", "-eo", "pid,lstart,cmd", "|", "grep", executable_path])
    for output_line in ps_output[0: -1]:
        potential_pid = get_pid(output_line)
        start_time = get_start_time(output_line)
        if potential_pid > 0:
            process_ids_to_watch.append((potential_pid, start_time))

    return process_ids_to_watch

def get_matching_pid(process_ids: List[int], spawn_time: datetime):
    current_best_match = None
    pass
