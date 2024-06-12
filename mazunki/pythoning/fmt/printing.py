#!/usr/bin/env python
# pkg(mazunki)/pythoning/fmt/printing.py

# TODO: turn formatters into general classes

print_ = print


def print(*args, **kwargs):
    try:
        from pygments import highlight, lexers, formatters
        import json
    except ModuleNotFoundError:
        return print_(*args, **kwargs)

    for arg in args:
        if isinstance(arg, dict):
            format_tuple = lambda k: "<" + ",".join(str(item)[:3] for item in k) + ">"
            format_key = lambda k: (format_tuple(k) if isinstance(k, tuple) else str(k))
            arg = {format_key(k): v for k, v in arg.items()}
            the_string = json.dumps(arg, indent="\t")
        else:
            the_string = str(arg)

        string_fmt = highlight(
            the_string, lexers.Python3Lexer(), formatters.TerminalFormatter()
        )
        kwargs["end"] = ""
        print_(string_fmt, **kwargs)
