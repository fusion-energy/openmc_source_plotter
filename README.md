
A Python package for plotting the locations, directions or energy distributions of OpenMC source particles

# Installation

```bash
pip install openmc_source_plotter
```

temporary fix
For fixed source sources it is currently necessary to use openmc version 0.11
and also to point the ```openmc_exec``` path to the openmc executable
This can be installed with:
```bash
conda install -c conda-forge openmc=0.11
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

# plots the particle energy distribution
plot = osp.plot_source_energy(
    source=my_source,
    number_of_particles=2000,
    energy_bins=np.linspace(0, 20e6, 100),
    openmc_exec="/home/jshim/miniconda3/envs/openmc_0_11_0/bin/openmc",
)

plot.show()
```
![openmc particle source energy plot](https://user-images.githubusercontent.com/8583900/143615694-a3578115-f8a2-4971-bf26-458177b4f113.png)


Plot of energy distribution of two sources

```python
import openmc_source_plotter as osp
import openmc
import numpy as np

# initialises a new source object
my_dt_source = openmc.Source()

# sets the energy distribution to a Muir distribution DT neutrons
my_dt_source.energy = openmc.stats.Muir(e0=14080000.0, m_rat=5.0, kt=20000.0)

# initialises a new source object
my_dd_source = openmc.Source()
# sets the energy distribution to a Muir distribution DD neutrons
my_dd_source.energy = openmc.stats.Muir(e0=2080000.0, m_rat=2.0, kt=20000.0)

# plots the particle energy distribution
plot = osp.plot_source_energy(
    source=[my_dt_source, my_dd_source],
    number_of_particles=10000,
    energy_bins=np.linspace(0, 20e6, 100),
    openmc_exec="/home/jshim/miniconda3/envs/openmc_0_11_0/bin/openmc",
)

plot.show()
```

![openmc particle source energy plot](https://user-images.githubusercontent.com/8583900/151376414-fb1555eb-61d1-4c82-bc4d-a05f62819c5d.png)

```python
import openmc_source_plotter as osp
import openmc

# initializes a new source object
my_source = openmc.Source()

# sets the direction to isotropic
my_source.angle = openmc.stats.Isotropic()

# plots the particle energy distribution
plot = osp.plot_source_direction(
    source=my_source,
    number_of_particles=100,
    openmc_exec="/home/jshim/miniconda3/envs/openmc_0_11_0/bin/openmc",
)

plot.show()
```
![openmc particle source direction plot](https://user-images.githubusercontent.com/8583900/143615706-3b3a8467-0233-42d6-a66c-d536c80a01d8.png)

# Usage

See the [examples folder](https://github.com/fusion-energy/openmc_source_plotter/tree/main/examples) for example usage scripts.
