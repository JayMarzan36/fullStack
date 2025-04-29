from django.shortcuts import render
from django.conf import settings
import json, os
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.forms.models import model_to_dict

from .models import Note


from .relations import main as Rel
from .relations import parseFile as Paf


# Load manifest when server launches
MANIFEST = {}
if not settings.DEBUG:
    f = open(f"{settings.BASE_DIR}/core/static/manifest.json")
    MANIFEST = json.load(f)


# Create your views here.
@login_required
def index(req):
    context = {
        "asset_url": os.environ.get("ASSET_URL", ""),
        "debug": settings.DEBUG,
        "manifest": MANIFEST,
        "js_file": "" if settings.DEBUG else MANIFEST["src/main.ts"]["file"],
        "css_file": "" if settings.DEBUG else MANIFEST["src/main.ts"]["css"][0],
    }
    return render(req, "core/index.html", context)

@login_required
def getNotesForGraph(req):
    req.GET

    if req.method == "GET":
        try:
            notesFromDB = Note.objects.filter(user=req.user)

            notes = {}

            userNotes = []

            for i in notesFromDB:
                userNotes.append({"note name": i.title, "note content": i.content})

            notes["userNotes"] = userNotes

            if len(notes["userNotes"]) <= 1:
                returnData = {
                    "data": {
                        "nodes": [{"id": notes["userNotes"][0]["note name"]}],
                        "links": [],
                    }
                }
            else:
                returnData = Rel.main(notes)

        except Exception as e:
            data = {
                "data": {
                    "nodes": [
                        {"id": "Make a note 1"},
                        {"id": "Make a note 2"},
                        {"id": "Make a note 3"},
                        {"id": "Make a note 4"},
                    ],
                    "links": [
                        {"source": "Make a note 1", "target": "Make a note 2"},
                        {"source": "Make a note 2", "target": "Make a note 3"},
                        {"source": "Make a note 3", "target": "Make a note 4"},
                    ],
                }
            }

            data = json.dumps(data)
            returnData = json.loads(data)

    return JsonResponse(returnData)


@login_required
def note(req):
    if req.method == "POST":
        body = json.loads(req.body)

        note = Note.objects.create(
            user=req.user,
            title=body["title"],
            content=body["content"],
        )

        return JsonResponse({"note": model_to_dict(note)})

    elif req.method == "PATCH":
        body = json.loads(req.body)

        if body["oldTitle"] != body["title"]:
            deletedNote = Note.objects.get(title=body["oldTitle"])
            deletedNote.delete()

            note = Note.objects.create(
                user=req.user,
                title=body["title"],
                content=body["content"],
            )

            return JsonResponse({"note": model_to_dict(note)})

        elif body["oldTitle"] == body["title"]:
            note = Note.objects.get(title=body["title"])
            note.content = body["content"]
            note.save()
            return JsonResponse({"note": model_to_dict(note)})

    elif req.method == "DELETE":
        try:
            body = json.loads(req.body)

            print(body["title"])

            note = Note.objects.get(title=body["title"], user=req.user)

            note.delete()

            return JsonResponse(
                {"status": "success", "message": "Note deleted successfully"}
            )

        except Note.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Note not found"}, status=404
            )

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

@login_required
def getNotes(req):
    req.GET
    if req.method == "GET":
        try:
            notesFromDB = Note.objects.filter(user=req.user)

            notes = {}

            userNotes = []

            for i in notesFromDB:
                userNotes.append({"note name": i.title, "note content": i.content})

            notes["userNotes"] = userNotes

        except Exception as e:
            notes = {"error": "error"}

        notes = json.dumps(notes)

        returnData = json.loads(notes)

        return JsonResponse(returnData)
