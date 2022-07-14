def recursive_delete(dirpath):
    # deleted everything in a dir, recursively.
    for item in dirpath.iterdir():
        if item.is_dir():
            recursive_delete(item)
            item.rmdir()
        else:
            item.unlink()
