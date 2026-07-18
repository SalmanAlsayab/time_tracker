import pytest
from win32process import GetWindowThreadProcessId
import psutil

main_testdata = [
    # stable current handle stays the same
    (1, 1, 1, 1, 1),
    # a new handle appears but does not survive long enough to replace current
    (1, 1, 2, 2, 1),
    # a new handle is seen and the current handle flips after the third different value
    (1, 1, 2, 3, 2),
    # repeated next handle becomes current after two strikes
    (1, 2, 2, 2, 2),
    # repeated next handle, then a third value keeps current at the repeated next handle
    (1, 2, 2, 3, 2),
    # sequential new handles commit the previous next handle as current
    (1, 2, 3, 4, 3),
    # return to original before the next handle commits
    (1, 2, 1, 2, 1),
    # third value repeats and the second value stays current
    (1, 2, 3, 3, 2),
    # alternate next handle then repeat the second new handle keeps current at the first next handle
    (1, 3, 2, 2, 3),
    # new handle appears only once after the initial switch, so current remains the previous one
    (1, 2, 3, 2, 2),
]


@pytest.mark.parametrize("a,b,c,d,expected", main_testdata)
def test_main(a, b, c, d, expected):
    """main module that handles application tracking logic"""
    args = iter((a, b, c, d))
    hwnd = next(args)
    current_handle = hwnd
    next_handle = 0
    strikes: int = 0
    # check_duplicates_timer: int = 0
    for i in range(3):
        hwnd = next(args)

        # 1 strike = 2 seconds of not using app saved in current session
        if strikes == 2:
            current_handle = next_handle
            next_handle = 0
            strikes = 0
        # make sure current session data is inserted and only once

        if current_handle != hwnd:
            current_next_handle = next_handle
            if current_next_handle == 0:
                next_handle = hwnd
                strikes += 1
            elif current_next_handle == hwnd:
                strikes += 1
            else:
                current_handle = next_handle
                next_handle = hwnd
                strikes = 0
        else:
            strikes = 0
        print(hwnd)
    assert current_handle == expected


handles_testdata = [
    983134,
    66582,
    262236,
    66582,
    262236,
    983134,
    65832,
    66582,
    262802,
    262236,
]


@pytest.mark.parametrize("handle", handles_testdata)
def test_find_exe_path(handle):
    print(f"current handle = {handle}")
    thread_id, pid = GetWindowThreadProcessId(handle)
    process = psutil.Process(abs(pid))
    exe_path = process.exe()


def test_cli_import_initializes_file_logging():
    from loguru import logger
    import importlib

    logger.remove()
    importlib.import_module("src.cli")

    assert logger._core.handlers
