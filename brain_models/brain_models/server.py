import asyncio
import json
import logging
from typing import Annotated, Literal

import typer
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from brain_models.victory_c_fly_brain.pulse_loop import PulseLoop


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
async def websocket_endpoint(
    websocket: WebSocket,
) -> None:
    """Simulate pulses on a spiking model of the fly brain."""
    await websocket.accept()
    logging.info("Frontend connected to Python stream")

    pulse_loop = PulseLoop(
        input_group=app.state.input_group, input_side=app.state.input_side
    )

    try:
        for time, activations in pulse_loop.run_pulse(
            pulse_freq_s=app.state.pulse_freq_s,
            pulse_strength_hz=app.state.pulse_strength_hz,
            sampling_ms=app.state.sampling_ms,
            normalize_factor=app.state.normalize_factor,
        ):
            frame_data = {"time": time, "values": activations}

            await websocket.send_text(json.dumps(frame_data))
            await asyncio.sleep(0.1)  # Stream at ~10 FPS

    except Exception:
        logging.exception("Connection closed")


def run_server(  # noqa: PLR0913
    socket_port: Annotated[
        int, typer.Option(help="Port to run the websocket app on.")
    ] = 8000,
    input_group: Annotated[
        str,
        typer.Option(
            help="Name of input group to simulate pulses on. "
            "See brain_models/victory_c_fly_brain/brain/"
            "shiu_groups.json for options."
        ),
    ] = "sugar",
    input_side: Annotated[
        Literal["L", "R"] | None,
        typer.Option(
            help="Either `L` or `R`, or None. Limits input group "
            "to a sepcific hemishpere, or uses both if None"
        ),
    ] = None,
    pulse_freq_s: Annotated[
        int, typer.Option(help="Length of alternating on/off pulse, in seconds.")
    ] = 5,
    pulse_strength_hz: Annotated[
        int, typer.Option(help="Strength in Hz of the signal sent to input neurons.")
    ] = 100,
    sampling_ms: Annotated[
        int,
        typer.Option(help="Length of timetep to sample activity over, in miliseconds."),
    ] = 100,
    normalize_factor: Annotated[
        float,
        typer.Option(
            help="Factor by which to normalise outputs of the "
            "spiking model, in order to output range [0, 1]."
        ),
    ] = 5.0,
) -> None:
    """Run the brain server/websocket.

    Pulses a signal to input neurons, alternating on/off. Returns from the websocket
    the activations of all visible neurons on the simulated brain model.
    """
    app.state.input_group = input_group
    app.state.input_side = input_side
    app.state.pulse_freq_s = pulse_freq_s
    app.state.pulse_strength_hz = pulse_strength_hz
    app.state.sampling_ms = sampling_ms
    app.state.normalize_factor = normalize_factor

    uvicorn.run(app, host="127.0.0.1", port=socket_port)


if __name__ == "__main__":
    typer.run(run_server)
