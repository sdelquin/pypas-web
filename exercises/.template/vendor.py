import inspect


def launch(func):
    try:
        import args
    except ModuleNotFoundError:
        print('You have to create "args.py" with the main function arguments!')
    else:
        user_args = args.__dict__
        kwargs = {}
        for param in inspect.signature(func).parameters.keys():
            if param not in user_args:
                print(f'Parameter "{param}" must be defined in "args.py"')
                break
            kwargs[param] = user_args[param]
        else:
            func(**kwargs)  # type: ignore
