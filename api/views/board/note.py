import json
from django.core.cache import cache
from django.http import HttpResponse


# Create your views here.
def index(request):
    # print(type(request))
    # print("Authorization:", request.headers["Authorization"])
    if request.method == "POST":
        received_data = json.loads(request.body.decode())
        return edit_note(received_data["content"], received_data["last edited"])
    else:
        return get_note()


def get_note():
    note_content = cache.get("note-content")
    note_last_edited = cache.get("note-last_edited")
    data = {"content": note_content, "last edited": note_last_edited}
    return HttpResponse(json.dumps(data))


def edit_note(note, last_edited):
    cache.set("note-content", note)
    cache.set("note-last_edited", last_edited)
    return HttpResponse(json.dumps({}))
