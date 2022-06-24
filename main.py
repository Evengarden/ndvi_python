from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from earth_engine import show_ndvi, edit_geojson, get_map

app = FastAPI()
app.mount("/static", StaticFiles(directory='./', html=True), name="static")


@app.patch("/add")
def add_fields(latitude: float = 0, longitude: float = 0):
    print(latitude, longitude)
    edit_geojson(latitude, longitude)
    return 'success'


@app.get("/getSnapshot")
def get_snapshot():
    get_map()
    return RedirectResponse('static/index.html')


@app.get("/getImageNDVI")
def image_ndvi():
    try:
        show_ndvi()
        return RedirectResponse('static/index.html')

    finally:
        return 'wrong coordinates'
