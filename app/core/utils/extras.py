def prepare_extras(**kwargs) -> dict:
    extras = {}
    for key, value in kwargs.items():
        if isinstance(value, Exception):
            extras[key] = type(value).__name__
        else:
            extras[key] = value
    return extras
