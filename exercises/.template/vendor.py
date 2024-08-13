"""
This module provides some utilities to support a proper running of pypas software.
Please do not modify unless you know what you're doing.
"""

import inspect
import typing

import rich


def launch(func: typing.Callable):
    """Launch func looking its args within args.py file"""
    if func_params := inspect.signature(func).parameters.keys():
        try:
            import args
        except ModuleNotFoundError:
            rich.print('[red]You have to create [b]args.py[/b] with the main function arguments!')
        else:
            user_args = args.__dict__
            kwargs = {}
            for param in func_params:
                if param not in user_args:
                    rich.print(f'[red]Parameter [b]{param}[/b] must be defined in [b]args.py[/b]')
                    rich.print(f'[dim italic]{param} = value')
                    break
                kwargs[param] = user_args[param]
            else:
                func(**kwargs)  # type: ignore
    else:
        func()
