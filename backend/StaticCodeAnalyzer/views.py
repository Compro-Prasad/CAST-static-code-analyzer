from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess
import tempfile

# This can be included in database to be directly edited in django admin
commands = {
    "py": "pylint",
    "cpp": "clang",
    "js": "eslint"
}

@csrf_exempt
def analyze(request):
    """
    Analyze source code either as a uploaded file or plain text
    """
    if request.POST['by'] is None:
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
        (output, error) = (
            output.decode().replace(fp.name, friendly_name),
            error.decode().replace(fp.name, friendly_name)
        )
    return JsonResponse({ "output": output, "error": error })
