#!/usr/bin/env python

import os
import subprocess
import tempfile

config = [
    # ('api', './_includes/api.html', False),
    # ('api_nav', './_includes/api_nav.html', False)
    # ('models', './_includes/models.html', True),
    ('models_nav', './_includes/models_nav.html', False),
    # ('js_client', './libraries/javascript/index.md')
]


if __name__ == "__main__":

    for c in config:
        param = c[0]
        filename = c[1]
        markdown_p = c[2]

        # generate the doc chunk
        proc = subprocess.Popen(['python ./utils/wiki_apidocs.py ' + param],
                                stdout=subprocess.PIPE,
                                shell=True)
        out = proc.communicate()[0]

        # convert to html with redcarpet if needed
        if markdown_p:
            cmd = 'redcarpet --parse-no_intra_emphasis --parse-autolink ' + \
                '--parse-strikethrough --parse-fenced_code'
            proc = subprocess.Popen([cmd],
                                    stdout=subprocess.PIPE,
                                    stdin=subprocess.PIPE,
                                    shell=True)
            html = proc.communicate(out)[0]
        else:
            html = out

        with open(filename) as f:
            # overwrite the current file with the tempfile
            # don't call the tempfile "tempfile", duh!
            dirname, basename = os.path.split(filename)
            temp = tempfile.NamedTemporaryFile(suffix='.tmp',
                                               dir=dirname,
                                               delete=False)
            temp.write(html)
            temp.flush()
            os.rename(temp.name, filename)
            temp.close()
