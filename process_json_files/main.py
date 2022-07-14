from pathlib import Path

from reformat import json2readable as j2d
from reformat import util


def main():

    corpus_dirp = Path(
        r"./extracted_annotations"
    )
    out_dirp = Path(
        r"./extracted_annotations_out"
    )

    out_dirp.mkdir(exist_ok=True, parents=True)
    util.recursive_delete(out_dirp)

    j2d.format_over_corpus(corpus_dirp, out_dirp, test=False)


if __name__ == "__main__":
    main()
