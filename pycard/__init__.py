try:
    import rst_directive
except ImportError:
    print("WARNING: Could not import rst_directive. Make sure it is "
    "properly symlinked in the app directory. The file is shipped with "
    "pygments and you can find it using "
    "$ find / -name 'rst-directive.py'\n")
