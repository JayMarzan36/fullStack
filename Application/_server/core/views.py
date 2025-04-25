from django.shortcuts import render
from django.conf  import settings
import json, os
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

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
        # TODO get notes from database
        
        
        # TODO This is a test, delete after
        notes = {
            "userNotes": [
            {
                "note name": "Test 1",
                "note content": "From the earliest days of civilization, humans have looked up at the night sky with wonder, mapping constellations and telling stories about the stars. This innate curiosity about what lies beyond our world has driven countless discoveries and shaped entire cultures.",
            },
            {
                "note name": "Test 2", 
                "note content": "As technology advanced, so did our reach. The 20th century brought an explosion of innovation that transformed dreams of space travel into reality. The Moon landings, robotic probes, and space telescopes like Hubble revealed a universe far more complex and beautiful than we had ever imagined.",
            },
            {
                "note name": "Python Basics",
                "note content": "Python is a high-level programming language known for its simplicity and readability. Key features include dynamic typing, automatic memory management, and extensive standard libraries.",
            },
            {
                "note name": "Data Structures",
                "note content": "Common data structures in programming include arrays, linked lists, trees, and graphs. Each has specific use cases and performance characteristics worth considering.",
            },
            {
                "note name": "Web Development",
                "note content": "Modern web development involves both frontend and backend technologies. Frontend focuses on user interface while backend handles data processing and storage.",
            },
            {
                "note name": "AI Concepts",
                "note content": "Artificial Intelligence encompasses machine learning, neural networks, and natural language processing. These technologies are transforming how we approach complex problems.",
            }
            ]
        }
        
        notesRelations = Rel.main(notes)
        
        #print(notesRelations)

    return JsonResponse(notesRelations)


# TODO make view for making note
# TODO make view for viewing and deleting notes
