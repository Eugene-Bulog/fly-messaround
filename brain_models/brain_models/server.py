import asyncio
import json
import logging
import random
from pathlib import Path
from typing import Annotated

import typer
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware


LOGGER = logging.getLogger(__name__)


app = FastAPI()

# Allow frontend running to connect
# obviously not secure for a deployed solution
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/ws/brain-activity")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """Websocket to stream outputs from python code to frontend."""
    await websocket.accept()
    logging.info("Frontend connected to Python stream!")
    # temporarily load some neurons
    example_path = Path("brain_models/example_neurons.json")
    with example_path.open("r") as f:
        dummy_ids = json.load(f)

    time_counter = 0.0
    try:
        while True:
            # TODO: Later, replace this block with PyTorch model inference
            # Generating hardcoded/randomized responses for now
            activations = [
                [nid, round(random.uniform(0.1, 1.0), 3)] for nid in dummy_ids
            ]

            frame_data = {"time": round(time_counter, 2), "values": activations}

            await websocket.send_text(json.dumps(frame_data))

            time_counter += 0.1
            await asyncio.sleep(0.1)  # Stream at ~10 FPS

    except Exception:
        logging.exception("Connection closed")


def run_server(
    socket_port: Annotated[
        int, typer.Option(help="Port to run the websocket app on.")
    ] = 8000,
) -> None:
    """Run the brain server/websocket."""
    uvicorn.run(app, host="127.0.0.1", port=socket_port)


if __name__ == "__main__":
    typer.run(run_server)
