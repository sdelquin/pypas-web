def run():
    pass  # TODO


# DO NOT TOUCH THE CODE BELOW
if __name__ == '__main__':
    import inspect

    try:
        import args
    except ModuleNotFoundError:
        print('You have to create "args.py" with the main function arguments!')
    else:
        params = inspect.signature(run).parameters.keys()
        kwargs = {p: args.__dict__.get(p) for p in params}
        run(**kwargs)  # type: ignore
