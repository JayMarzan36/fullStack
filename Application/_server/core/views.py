from django.shortcuts import render
from django.conf  import settings
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
        "css_file": "" if settings.DEBUG else MANIFEST["src/main.ts"]["css"][0]
    }
    return render(req, "core/index.html", context)

# Everything after this comment, should only return json objects NO HTML!!!
# Unless updating

#TODO look over Dittons examples to see how to do requests on client side

# TODO make view for homepage
@login_required
def getNotesForGraph(req):
    req.GET
    
    if req.method == "GET":
        try:
            notesFromDB = Note.objects.filter(user=req.user)
            
            notes ={}
            
            userNotes = []
            
            for i in notesFromDB:
                userNotes.append({"note name":i.title,"note content" : i.content})
            
            notes["userNotes"] = userNotes
            
            returnData = Rel.main(notes)
            
        except Exception as e:
            data = {"data":{
                "nodes": [
                    { id: 'node 1' },
                    { id: 'node 2' },
                    { id: 'node 3' },
                    { id: 'node 4' },
                ],
                "links": [
                    { "source": 'node 1', "target": 'node 2' },
                    { "source": 'node 4', "target": 'node 3' },
                    { "source": 'node 1', "target": 'node 4' },
                ]}
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
        
        return JsonResponse({"note":model_to_dict(note)})
        
        


# TODO make view for making note
# TODO make view for viewing and deleting notes
