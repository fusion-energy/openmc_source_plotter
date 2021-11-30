
A Python package for plotting the locations, directions or energy distributions of OpenMC source particles

# Installation

```bash
pip install openmc_source_plotter
```

# Features

The package provides functions to:

- create the initial_source.h5 for a give openmc.source
- extract the locations, directions and energy of particles
- provides convenient plotting functions for
    - direction
    - energy
    - location

# Example plots

Plot of energy distribution of the source

```python
import openmc_source_plotter as osp
import openmc
import numpy as np

# initialises a new source object
my_source = openmc.Source()

# sets the energy distribution to a Muir distribution neutrons for DT fusion neutrons
my_source.energy = openmc.stats.Muir(e0=14080000.0, m_rat=5.0, kt=20000.0)

# makes an initial_source.h5 file with details of the particles
osp.create_initial_particles(
    source=my_source,
    number_of_particles=10000,
)

# plots the particle energy distribution
plot = osp.plot_energy_from_initial_source(
    energy_bins=np.linspace(0, 20e6, 100)
)

plot.show()
```
![openmc particle source energy plot](https://user-images.githubusercontent.com/8583900/143615694-a3578115-f8a2-4971-bf26-458177b4f113.png)


```python
import openmc_source_plotter as osp
import openmc

# initializes a new source object
my_source = openmc.Source()

# sets the direction to isotropic
my_source.angle = openmc.stats.Isotropic()

# makes an initial_source.h5 file with details of the particles
initial_source_filename = osp.create_initial_particles(
    source=my_source,
    number_of_particles=100,
)

# plots the particle energy distribution
plot = osp.plot_direction_from_initial_source(input_filename=initial_source_filename)

plot.show()
```
![openmc particle source direction plot](https://user-images.githubusercontent.com/8583900/143615706-3b3a8467-0233-42d6-a66c-d536c80a01d8.png)

# Usage

See the [examples folder](https://github.com/fusion-energy/openmc_source_plotter/tree/main/examples) for example usage scripts.
