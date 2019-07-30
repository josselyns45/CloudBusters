# CloudBustersProton
import cgi
import subprocess
import tempfile

from bottle import request, route, run

@route("/")
def index():
    return """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
    "http://www.w3.org/TR/html4/strict.dtd">
<title>CCQ Job Submission</title>
<form action="/hack/ccq" method="POST">
<p><textarea name="script" rows="24" cols="80"></textarea>
<p><input type="submit" name="submit" value="Submit">
<p><input type="submit" name="submit" value="Status">
</form>"""

def output_link(output):
    new = output.split("\n")
    new_output = new[0] + "\n" + new[1] + "\n"
    new = new[2:]
    for item in new:
        if len(item) < 4:
            break
        j = item.split()
        name = "/hack/output/%s%s" % (j[1], j[0])
        new_output += (cgi.escape(item) +
            " <a href=\"%s.o\">stdout</a>" % name +
            " <a href=\"%s.e\">stderr</a>" % name + "\n")
    return new_output

@route("/ccq", method="POST")
def ccq():
    script = request.forms.get("script").replace("\r\n", "\n")
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(script)
    f.close()

    output = ""
    if request.forms.get("submit") == "Submit":
        try:
            submit_output = subprocess.check_output("ccqsub %s" % f.name,
                stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as e:
            submit_output = e.output
        output += "<pre>" + cgi.escape(submit_output) + "</pre>"

    try:
        stat_output = subprocess.check_output("ccqstat",
            stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        stat_output = e.output
    output += "<pre>" + output_link(stat_output) + "</pre>"

    return """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
    "http://www.w3.org/TR/html4/strict.dtd">
<title>CCQ Job Submission Status</title>
<p><a href="/hack">Back</a>
%s""" % output

@route("/output/<name>")
def output(name):
    f = open(name)
    output = f.read()
    f.close()
    return """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
    "http://www.w3.org/TR/html4/strict.dtd">
<title>CCQ Job Submission Status</title>
<pre>%s</pre>""" % cgi.escape(output)

run(host='localhost', port=8080)

