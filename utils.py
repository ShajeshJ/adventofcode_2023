from importlib.resources import files
import inspect

def read_problem_input(filename: str = "input.txt") -> list[str]:
    """
    Reads the `filename` contained in the same package as the caller
    """

    caller_frame = inspect.stack()[1].frame
    caller_package = inspect.getmodule(caller_frame).__package__
    with files(caller_package).joinpath(filename).open() as f:
        return f.readlines()
