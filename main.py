import os
import tempfile
import requests
from flask.helpers import send_file
from img import resize_image

CHHUNK_SIZE = 1024


def hello_world(request):
    if request.args and "url" in request.args:
        url = request.args.get("url")
        with tempfile.NamedTemporaryFile(delete=False) as f:
            r = requests.get(url)
            r.raise_for_status()
            for chunk in r.iter_content(CHHUNK_SIZE):
                f.write(chunk)

        resized_image = resize_image(f.name, 320)
        filename = os.path.split(resized_image)[-1]
        return send_file(open(resized_image, "rb"), attachment_filename=filename)

    return "no url provided"
