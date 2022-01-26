#!/usr/bin/env python3

"""Provides functions for plotting source information"""

from typing import List

import numpy as np
import plotly.graph_objects as go

from .utils import get_particle_data


def plot_energy_from_initial_sources(
    energy_bins: np.array = np.linspace(0, 20e6, 50),
    input_filenames: List[str] = ["initial_source.h5"],
):
    """makes a plot of the energy distribution of multiple sources"""

    fig = go.Figure()

    for input_filename in input_filenames:
        print('getting particle data', input_filename)
        data = get_particle_data(input_filename)

        e_values = data["e_values"]

        # Calculate pdf for source energies
        probability, bin_edges = np.histogram(e_values, energy_bins, density=True)

        # Plot source energy histogram
        fig.add_trace(
            go.Scatter(
                x=energy_bins[:-1],
                y=probability * np.diff(energy_bins),
                line={"shape": "hv"},
                hoverinfo="text",
                name=input_filename,
            )
        )

    fig.update_layout(
        title="Particle energy",
        xaxis={"title": "Energy (eV)"},
        yaxis={"title": "Probability"},
        showlegend=True,
    )

    return fig


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
