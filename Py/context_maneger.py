"""
Code snippet: context maneger
"""

from contextlib import contextmanager

@contextmanager
def temp_file(content):
    import tempfile
    tmp = tempfile.NamedTemporaryFile(delete=False)
    try:
        tmp.write(content.encode())
        tmp.close()
        yield tmp.name
    finally:
        import os
        os.unlink(tmp.name)

with temp_file("Hello, World!") as file_path:
    with open(file_path, "r") as f:
        print(f.read())  # Hello, World!