

## Licence

## Viewer

The frontend viewer (`viewer/`) is built with [fly-connectome-template][repo_template] by [Mert Cobanov][author_template].

**[Cobanov Template Attribution License 1.0](LICENSE_VIEWER)** is a custom,
attribution-required source-available license, not an OSI-approved license.

MaleCNS data remains **CC BY 4.0**, credited to FlyEM / HHMI Janelia, University
of Cambridge, MRC Laboratory of Molecular Biology and Google Research.
Flybody remains **Apache-2.0**. Their licenses are separate from the template's;
see [third-party notices](THIRD_PARTY_NOTICES.md).

[repo_template]: https://github.com/cobanov/fly-connectome-template
[author_template]: https://github.com/cobanov

## Brain Models

The spiking brain model currently used in `brain_models/victory_c_fly_brain` is taken from [victory-c/fly-brain][repo_brain].

Said code is [MIT-licensed](LICENSE_BRAIN_MODEL). The connectome data, including the prebuilt files that brain.fetch downloads, is derived from the male CNS v1.0 and licensed CC-BY 4.0; cite Berg et al., Cell 2026 (doi:10.1016/j.cell.2026.08.015). [CITATION.cff](CITATION.cff) has the references.

Connectome: male CNS v1.0, HHMI Janelia FlyEM and Google Research. Neuron model and stimulus sets: Shiu et al., Nature 2024. FlyWire cell types: Schlegel et al. / Dorkenwald et al., Nature 2024. Bicycle model: Meijaard et al., Proc. R. Soc. A 2007.

[repo_brain]: https://github.com/victory-c/fly-brain
