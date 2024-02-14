from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

all_choices = ["op1", "op2", "op3", "op4", "op5", "op6"]
data = dict(zip(all_choices, [0 for _ in range(len(all_choices))]))

# current_choice_id = "1"  # Start with the first choice
left, right = random.sample(all_choices, 2)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    global left
    global right
    print("updating button")
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "left_text": left,
        "right_text": right
    })

@app.get("/click/{direction}")
async def register_click(direction: str):
    # ... (Click counter logic - same as before) 

    global left
    global right
    print(left,right)
    if direction == "left":
        data[left] += 1
    elif direction == "right":
        data[right] += 1
    left, right = random.sample(all_choices, 2)
    print(data)
    return { "left_text": left,  "right_text": right, "leaderboard": get_leaderboard_data(data)} 

def get_leaderboard_data(data:dict):
    sorted_data = sorted(data.items(), key=lambda item: item[1], reverse=True)
    # print(sorted_data)
    print([{"choice": choice_id, "count": count} for choice_id, count in sorted_data])
    return [{"choice": choice_id, "count": count} for choice_id, count in sorted_data]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
