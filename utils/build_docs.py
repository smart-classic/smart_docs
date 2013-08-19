#!/usr/bin/env python

import os
import subprocess
import tempfile

MARKER = "GENERATED DOCS INSERTED BELOW THIS LINE"

config = [
    ('api', './framework/api/index.md'),
    ('payload', './framework/models/index.md')
    # ('js_client', './libraries/javascript/index.md')
]


if __name__ == "__main__":

    for c in config:
        param = c[0]
        filename = c[1]

        # generate the doc chunk
        proc = subprocess.Popen(['python ./utils/wiki_apidocs.py ' + param],
                                stdout=subprocess.PIPE,
                                shell=True)
        chunk = proc.communicate()[0]

        with open(filename) as f:
            # find the first line after the marker
            doc = f.read()
            line_no_after_marker = doc.find('\n', doc.find(MARKER))

            # append the chunk to the docs after the marker
            new_doc = doc[:line_no_after_marker] + '\n\n\n' + chunk

            # overwrite the current file with the tempfile
            # don't call the tempfile "tempfile", duh!
            dirname, basename = os.path.split(filename)
            temp = tempfile.NamedTemporaryFile(
                suffix='.tmp',
                dir=dirname,
                delete=False)
            temp.write(new_doc)
            temp.flush()
            os.rename(temp.name, filename)
            temp.close()
