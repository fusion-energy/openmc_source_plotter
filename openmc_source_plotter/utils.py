#!/usr/bin/env python3

"""Provides utilities for creating h5 files containing initial source
information"""

import h5py
import openmc
import shutil


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


def create_initial_particles(
    source: openmc.source,
    number_of_particles: int = 2000,
    openmc_exec="openmc",
    output_source_filename="initial_source.h5",
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
        output_source_filename: the filename of the initial source h5 file
            produced. Note openmc will write 'initial_source.h5' but this will
            be moved to the output_source_filename specified
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

    if output_source_filename != "initial_source.h5":
        shutil.move("initial_source.h5", output_source_filename)

    return output_source_filename
