import os
import json
import glob
from fastapi import APIRouter, Depends, Path, Query, File, UploadFile, Form
from starlette.responses import FileResponse

persistent_folder = "/persistent"
app_data_folder = os.path.join(persistent_folder,"app-data")
stories_file_path = os.path.join(app_data_folder,"story-*.json")

router = APIRouter()

async def get_stories():
    stories = []
    json_files = glob.glob(stories_file_path)
    for json_file in json_files:
        with open(json_file,'r') as read_file:
            story = json.load(read_file)
        stories.append(story)
        
    return stories

async def get_story(id):

    story_path = os.path.join(app_data_folder,f"story-{id}.json")
    if os.path.exists(story_path):
        with open(story_path,'r') as read_file:
            story = json.load(read_file)
    else:
        story = {}
    
    return story

@router.get(
    "/stories",
    tags=["Stories"],
    summary="Get list of stories",
    description="Get list of stories"
)
async def stories_index():

    stories = await get_stories()
        
    return stories

@router.get(
    "/stories/{id}",
    tags=["Stories"],
    summary="Gets information for story",
    description="Gets information for story"
)
async def get_information_for_story(
    id: int = Path(..., description="Story ID")
):
    story = await get_story(id)

    return story
    

@router.post(
    "/stories",
    tags=["Stories"],
    summary="Create a new story",
    description="Create a new story"
)
async def create_story(
    story: dict = {}
):
    print("Add Story:",story)

    json_files = glob.glob(stories_file_path)

    # Save Story
    id = len(json_files) + 1
    story["id"] = id
    story_path = os.path.join(app_data_folder,f"story-{id}.json")
    with open(story_path, 'w') as f:
        json.dump(story, f)
    # make story folder
    os.mkdir(os.path.join(app_data_folder,str(id)))
    os.mkdir(os.path.join(app_data_folder,str(id), "input"))
    os.mkdir(os.path.join(app_data_folder,str(id), "output"))
    return story

@router.put(
    "/stories/{id}",
    tags=["Stories"],
    summary="Update story",
    description="Update story"
)
async def update_story(
    story: dict = {},
    id: int = Path(..., description="The Story ID"),
):
    print("Update Story:",story)

    updated_story = await get_story(id)
    for key in story:
        updated_story[key] = story[key]        
        
    # Save
    story_path = os.path.join(app_data_folder,f"story-{id}.json")
    with open(story_path, 'w') as f:
        json.dump(updated_story, f)

    return updated_story

@router.get(
    "/stories/{id}/input_images"
)
async def get_input_images_list(
    id: int = Path(..., description="Story ID")
):
    image_paths = glob.glob(os.path.join(app_data_folder,str(id),"input","*.*"))

    return image_paths

@router.get(
    "/stories/{id}/title_images"
)
async def get_title_images_list(
    id: int = Path(..., description="Story ID")
):
    image_paths = glob.glob(os.path.join(app_data_folder,str(id),"output","title*.png"))

    return image_paths

@router.get(
    "/stories/{id}/storyline_images/{line}"
)
async def get_storyline_images_list(
    id: int = Path(..., description="Story ID"),
    line: int = Path(..., description="Story ID")
):
    image_paths = glob.glob(os.path.join(app_data_folder,str(id),"output",f"storyline_{line}*.png"))

    return image_paths

@router.get("/get_image")
async def get_image(
    path: str = Query(..., description="Image path")
):
    print(path)
    return FileResponse(path, media_type="image/png")

@router.post("/stories/{id}/upload_input_image/{filename}")
async def upload_input_image(
    id: int = Path(..., description="Story ID"),
    file: bytes = File(...),
    filename: str = Path(...)
):
    print("Input file:", len(file), type(file), filename)

    # Save the image
    image_path = os.path.join(app_data_folder,str(id),"input", filename)
    with open(image_path, "wb") as output:
        output.write(file)

    return {"filename": filename}