#!/usr/bin/env python3

"""Provides functions for plotting source information"""

import tempfile
from typing import List, Union

import numpy as np
import openmc
import plotly.graph_objects as go

from .utils import create_initial_particles, get_particle_data, save_plot


def plot_source_energy(
    source: Union[openmc.Source, List[openmc.Source]],
    number_of_particles: int = 2000,
    openmc_exec="openmc",
    energy_bins: np.array = np.linspace(0, 20e6, 50),
    filename: str = None,
):
    """makes a plot of the energy distribution OpenMC source(s)

    Args:
        source: The openmc.Source object or list of openmc.Source objects to plot.
        number_of_particles: The number of source samples to obtain, more will
            take longer but produce a smoother plot.
        energy_bins: A numpy array of energy bins to use as energy bins.
        openmc_exec: The path of the openmc executable to use
        filename: the filename to save the plot as should end with the correct
            extention supported by matplotlib (e.g .png) or plotly (e.g .html)
    """

    figure = go.Figure()

    if isinstance(source, openmc.Source):
        source = [source]

    for single_source in source:
        tmp_filename = tempfile.mkstemp(suffix=".h5", prefix=f"openmc_source_")[1]
        create_initial_particles(
            source=single_source,
            number_of_particles=number_of_particles,
            openmc_exec=openmc_exec,
            output_source_filename=tmp_filename,
        )

        print("getting particle data", tmp_filename)
        data = get_particle_data(tmp_filename)

        e_values = data["e_values"]

        # Calculate pdf for source energies
        probability, bin_edges = np.histogram(e_values, energy_bins, density=True)

        # Plot source energy histogram
        figure.add_trace(
            go.Scatter(
                x=energy_bins[:-1],
                y=probability * np.diff(energy_bins),
                line={"shape": "hv"},
                hoverinfo="text",
                name=tmp_filename,
            )
        )

    figure.update_layout(
        title="Particle energy",
        xaxis={"title": "Energy (eV)"},
        yaxis={"title": "Probability"},
        showlegend=True,
    )

    plotting_package = 'plotly'  # not matplotlib option for now
    save_plot(plotting_package=plotting_package, filename=filename, figure=figure)

    return figure


def plot_source_position(
    source: Union[openmc.Source, List[openmc.Source]],
    number_of_particles: int = 2000,
    openmc_exec="openmc",
    filename: str = None,
):
    """makes a plot of the initial creation postions of an OpenMC source(s)

    Args:
        source: The openmc.Source object or list of openmc.Source objects to plot.
        number_of_particles: The number of source samples to obtain.
        openmc_exec: The path of the openmc executable to use
    """

    figure = go.Figure()

    if isinstance(source, openmc.Source):
        source = [source]

    for single_source in source:
        tmp_filename = tempfile.mkstemp(suffix=".h5", prefix=f"openmc_source_")[1]
        create_initial_particles(
            source=single_source,
            number_of_particles=number_of_particles,
            openmc_exec=openmc_exec,
            output_source_filename=tmp_filename,
        )

        data = get_particle_data(tmp_filename)

        text = ["Energy = " + str(i) + " eV" for i in data["e_values"]]

        figure.add_trace(
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

    figure.update_layout(title="Particle production coordinates - coloured by energy")

    plotting_package = 'plotly'  # not matplotlib option for now
    save_plot(plotting_package=plotting_package, filename=filename, figure=figure)

    return figure


def plot_source_direction(
    source: Union[openmc.Source, List[openmc.Source]],
    number_of_particles: int = 2000,
    openmc_exec="openmc",
    filename: str = None,
):
    """makes a plot of the initial creation directions of the particle source

    Args:
        source: The openmc.Source object or list of openmc.Source objects to plot.
        number_of_particles: The number of source samples to obtain.
        openmc_exec: The path of the openmc executable to use
    """
    figure = go.Figure()

    if isinstance(source, openmc.Source):
        source = [source]

    for single_source in source:
        tmp_filename = tempfile.mkstemp(suffix=".h5", prefix=f"openmc_source_")[1]
        create_initial_particles(
            source=single_source,
            number_of_particles=number_of_particles,
            openmc_exec=openmc_exec,
            output_source_filename=tmp_filename,
        )
        data = get_particle_data(tmp_filename)

        figure.add_trace(
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

    figure.update_layout(title="Particle initial directions")

    plotting_package = 'plotly'  # not matplotlib option for now
    save_plot(plotting_package=plotting_package, filename=filename, figure=figure)

    return figure
