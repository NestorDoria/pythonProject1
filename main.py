from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Configurar la carpeta estática para servir archivos HTML y otros recursos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

uploaded_videos_folder = "uploaded_videos"
next_video_id = 1


@app.get("/")
async def get_homepage():
    return FileResponse("static/pagina.html")


@app.get("/play/{video_id}")
async def play_video(video_id: int):
    video_path = os.path.join(uploaded_videos_folder, f"video{video_id}.mp4")
    if os.path.exists(video_path):
        return FileResponse(video_path, media_type="video/mp4")
    else:
        return JSONResponse(content={"message": "Video not found"}, status_code=404)


@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    global next_video_id
    if next_video_id > 3:
        return JSONResponse(content={"message": "Se ha alcanzado el límite máximo de videos subidos (3)"},
                            status_code=400)
    video_id = next_video_id
    next_video_id += 1
    video_path = os.path.join(uploaded_videos_folder, f"video{video_id}.mp4")
    with open(video_path, "wb") as video_file:
        video_file.write(file.file.read())
    return FileResponse("static/pagina.html")


@app.post("/delete-video/{video_id}")
async def delete_video(video_id: int):
    video_path = os.path.join(uploaded_videos_folder, f"video{video_id}.mp4")
    if os.path.exists(video_path):
        os.remove(video_path)
        return JSONResponse(content={"message": f"Video {video_id} ha sido eliminado exitosamente."}, status_code=200)
    else:
        return JSONResponse(content={"message": f"Video {video_id} no encontrado."}, status_code=404)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
