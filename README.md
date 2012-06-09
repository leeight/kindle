kindle
======

Using <http://www.princexml.com> to generate kindle friendly pdf.

Please run the following commands:

    prince -v kindle.html -o kindle.pdf
    prince http://localhost:9999/doc/sdcfe/newbie/feutils.text -s kindle.css -o feutils.pdf
