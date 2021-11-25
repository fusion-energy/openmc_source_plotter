import openmc_source_plotter as osp
import openmc

# initialises a new source object
my_source = openmc.Source()

# sets the location of the source to x=0 y=0 z=0
my_source.space = openmc.stats.Point((0, 0, 0))

# sets the direction to isotropic
my_source.angle = openmc.stats.Isotropic()

# sets the energy distribution to 100% 14MeV neutrons
my_source.energy = openmc.stats.Discrete([14e6], [1])

# makes an initial_source.h5 file with details of the particles
initial_source_filename = osp.create_initial_particles(
    source=my_source,
    number_of_particles=10,
    openmc_exec="/home/jshim/miniconda3/envs/openmc_0_11_0/bin/openmc",
)

# gets the particle corrdiantes, energy and direction
data = osp.get_particle_data(initial_source_filename)

print(data)
