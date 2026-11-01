from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ANNOTATIONS = DATA / "body-annotations-male-cns-v1.0-minconf-0.5.feather"
TRANSMITTERS = DATA / "body-neurotransmitters-male-cns-v1.0.feather"
WEIGHTS = DATA / "connectome-weights-male-cns-v1.0-minconf-0.5.feather"
NPZ, META = ROOT / "brain.npz", ROOT / "brain_meta.parquet"
ATLAS = ROOT / "web_data" / "atlas.npz"  # written by brain/atlas.py
