'''Кварги не стал проверять, так как в задаче гарантировано их отсутствие.'''
def strict(func):
    def wrapper(*args, **kwargs):
        *func_arguments, func_return = func.__annotations__
        for pos, key in enumerate(func_arguments):
            if not kwargs and not isinstance(args[pos], func.__annotations__[key]):
                raise TypeError
        return func(*args, **kwargs)
    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b
