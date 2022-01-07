# -*- coding: utf-8 -*-
"""This module provides functions to check a process' status based on the command used to spawn said process.
"""
import os
from datetime import datetime
from shlex import split
from shutil import which
from subprocess import check_output
from typing import List, Tuple

from dateutil import parser

def get_executable(command: str) -> str:
    """ Deprecated

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
    for item in split(command):
        executable_path = which(item)
        if executable_path:
            command_name = executable_path

    if command_name == "":
        raise ValueError("The provided command contained no variable linked to an executable.")

    return command_name

def get_command_name(full_command: str) -> str:
    """
    Get the name of a command that was typed with other parameters and flags.

    This function assumes that the first thing that is a valid executable in
    the provided command is the executable that was called using the command.

    The previous assumption might cause this function to be wrong if a parameter
    is passed before the command (like environment variables) is also a valid
    command (an executable in the user's PATH).

    Args:
        full_command (str): The full command that was typed to spawn a process.

    Raises:
        ValueError: If no part of the `full_command` can be linked to an executable.
            This is verified using `which`.

    Returns:
        str: The name of the first string (separated on spaces) in `full_command` that
            could be linked to an executable.
    """
    command_name: str = ""
    for item in split(full_command):
        executable_path = which(item)
        if executable_path:
            command_name = item

    if command_name == "":
        raise ValueError("The provided command contained no variable linked to an executable.")

    return command_name

def get_pid_to_watch(process_name: str) -> int:
    """Find the process id of the process spawned by `command_name`.

    Uses `pgrep` to find the process id with the lowest time alive.

    Args:
        process_name (str): The name of the process to `pgrep` for.

    Returns:
        int: The process id of the most recent process with the provided
             name
    """
    return int(check_output(["pgrep", "--newest", process_name])[0])


def get_pid(ps_output_line: str) -> int:
    """ Deprecated

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
    """ Deprecated

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
    """ Deprecated

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


def get_matching_pid(process_ids_start_time: List[Tuple[int, datetime]], command_typed_at: datetime) -> int:
    """ Deprecated

    Matches a process id from a process start time. The smaller the gap between
    when the command was typed and the process' actual start time the better.

    This function assumes that process_ids are a list of
    Args:
        process_ids_start_time: A list of process ids and their start tim.
            This should be obtained using get_pids_to_watch().
        command_typed_at: When the command that allegedly started the process
            that we want was typed.

    Returns: The process id of the best match.

    """
    current_best_match = process_ids_start_time[0]
    to_beat: datetime = process_ids_start_time[0] - datetime
    for process_id in process_ids_start_time[1:]:
        current_time_diff: datetime = process_id[1] - datetime
        if current_time_diff < to_beat:
            current_best_match = process_ids_start_time
            to_beat = current_time_diff
    # Tuple that contains (pid, start time)
    return current_best_match[0]


def wait_for_process(pid) -> None:
    """
    Wait for a process to be done running by process id.

    Args:
        pid: The process id of the process to watch.

    """
    while True:
        try:
            os.kill(pid, 0)
        except OSError:
            # process is done
            break
