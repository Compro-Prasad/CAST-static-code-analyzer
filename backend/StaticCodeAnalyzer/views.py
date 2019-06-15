from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess
import tempfile
import re

# This can be included in database to be directly edited in django admin
commands = {
    "py": "pylint",
    "cpp": "clang -Wall",
    "js": "eslint"
}


def get_py_errors(text):
    def extractError(line):
        x = re.search('^.*:(\d+):(\d+): ([A-Z]\d+: .*)', line)
        if x:
            return {
                "line": int(x.group(1)) - 1,
                "col": int(x.group(2)),
                "text": x.group(3)
            }
        return None
    return filter(
        lambda x: x is not None,
        map(extractError, text.split('\n'))
    )


def get_cpp_errors(text):
    def extractError(line):
        x = re.search('^.*:(\d+):(\d+): ([a-z]+: .*)$', line)
        if x:
            return {
                "line": int(x.group(1)) - 1,
                "col": int(x.group(2)),
                "text": x.group(3)
            }
        return None
    return filter(
        lambda x: x is not None,
        map(extractError, text.split('\n'))
    )



def get_js_errors(text):
    def extractError(line):
        x = re.search('^  (\d+):(\d+)  ([a-z]+  .*)$', line)
        if x:
            return {
                "line": int(x.group(1)) - 1,
                "col": int(x.group(2)),
                "text": x.group(3)
            }
        return None
    return filter(
        lambda x: x is not None,
        map(extractError, text.split('\n'))
    )


getErrors = {
    'py': get_py_errors,
    'js': get_js_errors,
    'cpp': get_cpp_errors
}


@csrf_exempt
def analyze(request):
    """
    Analyze source code either as a uploaded file or plain text
    """
    if request.method != "POST" or request.POST['by'] is None:
        return HttpResponse(status=403)
    if request.POST['by'] == 'upload':
        f = request.FILES['file']
    language = request.POST['language']
    with tempfile.NamedTemporaryFile(suffix="."+language) as fp:
        if request.POST['by'] == 'upload':
            fp.write(f.read())
        else:
            fp.write(request.POST['text'].encode())
        fp.flush()
        if language in commands.keys():
            cmd = commands[language] + " " + fp.name
        else:
            cmd = "echo 'Language not supported'"
        (output, error) = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        ).communicate()
        try:
            friendly_name = f.name
        except NameError:
            friendly_name = "test." + language
        output = output.decode() + "\n" + error.decode()
        output.replace(fp.name, friendly_name)
    return JsonResponse({
        "output": output,
        "errors": list(getErrors[language](output)),
        "file": friendly_name
    })
