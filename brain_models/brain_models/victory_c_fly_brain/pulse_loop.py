from collections.abc import Iterator
from typing import Literal

import numpy as np
import torch

from brain_models.victory_c_fly_brain.brain import stimuli
from brain_models.victory_c_fly_brain.brain.connectome import Brain
from brain_models.victory_c_fly_brain.brain.engine import W_SYN
from brain_models.victory_c_fly_brain.brain.loop import BrainLoop
from brain_models.victory_c_fly_brain.brain.paths import NPZ


class PulseLoop:
    """A simulated loop of brain activity, pulsing a specified input signal.

    Parameters
    ----------
    input_group, optional
        Name of input neuron group to pulse. See `brain/shiu_groups.json`
        for full list. By default `sugar`
    input_side, optional
        Either `L` or `R`, or None. Limits input group to a sepcific hemishpere,
        or uses both if None. By default None

    Raises
    ------
    ValueError
        If input group or input side invalid.
    """

    def __init__(
        self, input_group: str = "sugar", input_side: Literal["L", "R"] | None = None
    ) -> None:
        if input_side not in [None, "L", "R"]:
            msg = f"Input side `{input_side}` not recognised. Please use `L` or `R`"
            raise ValueError(msg)

        try:
            stim_idx = stimuli.group(name=input_group, side=input_side)
        except KeyError as e:
            msg = (
                f"Input group `{input_group}` not found. "
                "Please use one of the groups in "
                "`brain_models/brain_models/victory_c_fly_brain/brain/"
                "shiu_groups.json`"
            )
            raise ValueError(msg) from e

        brain_map = np.load(NPZ)
        self.body_id_map = brain_map["body_ids"]

        self.loop = BrainLoop(
            brain=Brain(),
            n_run=1,
            stim_idx=stim_idx,
            device="cuda" if torch.cuda.is_available() else "cpu",
            params={"w_syn": W_SYN},
        )

    def run_pulse(
        self,
        pulse_freq_s: int = 5,
        pulse_strength_hz: int = 100,
        sampling_ms: int = 100,
        normalize_factor: float = 5.0,
    ) -> Iterator[tuple[float, list[list[int | float]]]]:
        """Generate brain activity over a timestep.

        Pulses with a signal applied for `pulse_freq_s`, then disabled for
        another `pulse_freq_s`, on repeat. Each yield runs one timestep
        of this activity.

        All times are in *simulated* time, not real time.

        Parameters
        ----------
        pulse_freq_s, optional
            Length of alternating on/off pulse, in seconds, by default 5
        pulse_strength_hz, optional
            Strength in Hz of the signal sent to input neurons, by default 100
        sampling_ms, optional
            Length of timetep to sample activity over, in miliseconds, by default 100
        normalize_factor, optional
            Factor by which to normalise outputs of the spiking model, in order to
            output range [0, 1], by default 5.0

        Yields
        ------
        time_counter
            Time in simulated miliseconds since loop began.
        activations
            List of [neruon body id, activation value] for all spiking neurons.
            Activation values are normalised and clamped to [0, 1] range.
        """
        time_counter = 0.0
        while True:
            if time_counter % (pulse_freq_s * 2) < pulse_freq_s:
                self.loop.set_rates(pulse_strength_hz)
            else:
                self.loop.set_rates(0)

            readouts = self.loop.run(sampling_ms)[0][0]
            readouts = readouts.cpu().numpy()
            readouts = np.clip(readouts / normalize_factor, 0, 1)
            activations = (
                np.stack([self.body_id_map[readouts > 0], readouts[readouts > 0]])
                .transpose(1, 0)
                .tolist()
            )

            yield time_counter, activations
