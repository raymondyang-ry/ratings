from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random
import datacleaning as dc
import elo 

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

f = "top_50.csv"
df = dc.clean_data(f)
all_choices = df["clean_title"].to_list()[0:10]
data = dict(zip(all_choices, [1500 for _ in range(len(all_choices))]))

left, right = random.sample(all_choices, 2)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    global left
    global right
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "left_text": left,
        "right_text": right
    })

@app.get("/click/{direction}")
async def register_click(direction: str):

    global left
    global right
    expected_score = elo.expected(data[left], data[right])
    print(left,right, expected_score)
    data[left] = elo.elo(data[left], expected_score, 1)
    data[right] = elo.elo(data[right], expected_score, 0)
    left, right = random.sample(all_choices, 2)
    return { "left_text": left,  "right_text": right, "leaderboard": get_leaderboard_data(data)} 

def get_leaderboard_data(data:dict):
    sorted_data = sorted(data.items(), key=lambda item: item[1], reverse=True)
    # print(sorted_data)
    # print([{"choice": choice_id, "count": count} for choice_id, count in sorted_data])
    return [{"choice": choice_id, "count": count} for choice_id, count in sorted_data]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
