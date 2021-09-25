import traceback

def f():
    g()

def g():
    stack = traceback.format_stack()
    last = stack[-1].replace(' ', '')
    for line in traceback.format_stack():
        print(line.strip())

f()
