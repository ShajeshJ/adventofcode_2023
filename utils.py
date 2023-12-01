from importlib.resources import files
import inspect

def read_problem_input() -> list[str]:
    """
    Reads the input.txt file contained in the same package as the calling file
    """

    caller_frame = inspect.stack()[1].frame
    caller_package = inspect.getmodule(caller_frame).__package__
    with files(caller_package).joinpath("input.txt").open() as f:
        return f.readlines()
