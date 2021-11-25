#!/usr/bin/env python3

"""Provides utilities for creating h5 files containing initial source
information and then plotting that information"""

import h5py
import numpy as np
import openmc
import plotly.graph_objects as go


def create_initial_particles(
    source: openmc.source, number_of_particles: int = 2000, openmc_exec="openmc"
) -> str:
    """Accepts an openmc source and creates an initial_source.h5 file that can
    be used to find propties of the source particles such as initial x,y,z
    coordinates, direction and energy.

    Note, I've found it easiest to install the latest version of openmc as this
    has the write_initial_source for fixed source problems and then in a
    new empty conda environment I have installed openmc version 0.11.0 with the
    'conda install -c conda-forge openmc==0.11.0' command. I then go back to
    the conda environment with the latest openmc version and run the python
    script while setting the path to openmc_0.11.0 as the openmc_exec argument.
    In my case it is '/home/jshimwell/miniconda3/envs/openmc_0_11_0/bin/openmc'

    Args:
        source: the openmc source to use
        number_of_particles: the number of particles to sample
        openmc_exec: the path of openmc executable or executable name if it
            appears in your system $PATH. Defaults to 'openmc' which will use
            the default openmc in your system $PATH environmental variable.
    Returns:
        The filename of the initial source file created (initial_source.h5)
    """

    # no real materials are needed for finding the source
    mats = openmc.Materials([])

    # just a minimal geometry
    outer_surface = openmc.Sphere(r=100000, boundary_type="vacuum")
    cell = openmc.Cell(region=-outer_surface)
    universe = openmc.Universe(cells=[cell])
    geom = openmc.Geometry(universe)

    # Instantiate a Settings object
    settings = openmc.Settings()
    settings.run_mode = "fixed source"
    settings.particles = number_of_particles
    settings.batches = 1
    settings.inactive = 0
    settings.write_initial_source = True
    settings.source = source

    model = openmc.model.Model(geom, mats, settings)

    model.export_to_xml()

    openmc.run(openmc_exec=openmc_exec)

    return "initial_source.h5"


def get_particle_data(input_filename: str):

    f = h5py.File(input_filename, "r")
    dset = f["source_bank"]

    x_values = []
    y_values = []
    z_values = []
    x_dir = []
    y_dir = []
    z_dir = []
    e_values = []

    for particle in dset:
        x_values.append(particle[0][0])
        y_values.append(particle[0][1])
        z_values.append(particle[0][2])
        x_dir.append(particle[1][0])
        y_dir.append(particle[1][1])
        z_dir.append(particle[1][2])
        e_values.append(particle[2])

    return {
        "x_values": x_values,
        "y_values": y_values,
        "z_values": z_values,
        "x_dir": x_dir,
        "y_dir": y_dir,
        "z_dir": z_dir,
        "e_values": e_values,
    }


def plot_energy_from_initial_source(
    energy_bins: np.array = np.linspace(0, 20e6, 50),
    input_filename: str = "initial_source.h5",
):
    """makes a plot of the energy distribution of the source"""

    data = get_particle_data(input_filename)

    e_values = data["e_values"]

    # Calculate pdf for source energies
    probability, bin_edges = np.histogram(e_values, energy_bins, density=True)
    fig = go.Figure()

    # Plot source energy histogram
    fig.add_trace(
        go.Scatter(
            x=energy_bins[:-1],
            y=probability * np.diff(energy_bins),
            line={"shape": "hv"},
            hoverinfo="text",
            name="particle direction",
        )
    )

    fig.update_layout(
        title="Particle energy",
        xaxis={"title": "Energy (eV)"},
        yaxis={"title": "Probability"},
    )

    return fig


def plot_position_from_initial_source(input_filename="initial_source.h5"):
    """makes a plot of the initial creation locations of the particle source"""

    data = get_particle_data(input_filename)

    text = ["Energy = " + str(i) + " eV" for i in data["e_values"]]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter3d(
            x=data["x_values"],
            y=data["y_values"],
            z=data["z_values"],
            hovertext=text,
            text=text,
            mode="markers",
            marker={
                "size": 2,
                "color": data["e_values"],
            },
        )
    )

    fig.update_layout(title="Particle production coordinates - coloured by energy")

    return fig


def plot_direction_from_initial_source(input_filename="initial_source.h5"):
    """makes a plot of the initial creation directions of the particle source"""

    data = get_particle_data(input_filename)

    fig = go.Figure()

    fig.add_trace(
        {
            "type": "cone",
            "cauto": False,
            "x": data["x_values"],
            "y": data["y_values"],
            "z": data["z_values"],
            "u": data["x_dir"],
            "v": data["y_dir"],
            "w": data["z_dir"],
            "cmin": 0,
            "cmax": 1,
            "anchor": "tail",
            "colorscale": "Viridis",
            "hoverinfo": "u+v+w+norm",
            "sizemode": "absolute",
            "sizeref": 30,
            "showscale": False,
        }
    )

    fig.update_layout(title="Particle initial directions")

    return fig
