from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from s3.movie_upload import S3Repository

router = APIRouter()
s3_repository = S3Repository()

@router.post("/upload_movie")
async def upload_movie(movieFile: UploadFile = File(...)):
    movie_path = f"temp/{movieFile.filename}"
    os.makedirs("temp", exist_ok=True)  # Создаем временную директорию

    with open(movie_path, "wb") as f:
        f.write(await movieFile.read())

    movie_uploaded = s3_repository.upload_file("movies", movieFile.filename, movie_path)

    os.remove(movie_path)

    if movie_uploaded:
        return {"message": "Movie uploaded successfully!"}
    raise HTTPException(status_code=500, detail="Failed to upload movie.")


@router.post("/upload_poster")
async def upload_poster(posterFile: UploadFile = File(...)):
    poster_path = f"temp/{posterFile.filename}"
    os.makedirs("temp", exist_ok=True)  # Создаем временную директорию

    with open(poster_path, "wb") as f:
        f.write(await posterFile.read())

    poster_uploaded = s3_repository.upload_file("posters", posterFile.filename, poster_path)

    os.remove(poster_path)

    if poster_uploaded:
        return {"message": "Poster uploaded successfully!"}
    raise HTTPException(status_code=500, detail="Failed to upload poster.")
