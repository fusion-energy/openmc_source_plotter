import openmc
import matplotlib.pyplot as plt


class Material(openmc.Material):

    def plot_gamma_emission(
        self,
        threshold,
    ):
        
        import lineid_plot

        energies_to_label = []
        labels=[]
        atoms = self.get_nuclide_atoms()
        dists = []
        probs = []
        for nuc, num_atoms in atoms.items():
            source_per_atom = openmc.data.decay_photon_energy(nuc)
            if source_per_atom is not None:
                # dists.append(source_per_atom)
                # probs.append(num_atoms)
                if num_atoms>threshold:
                    energies_to_label.append(source_per_atom.x)
                    labels.append(str(source_per_atom.p))
        # return openmc.data.combine_distributions(dists, probs)

        # ps = self.decay_photon_energy.p
        # xs = self.decay_photon_energy.x

        # for x,p in zip(xs,ps):
        #     print(p)
        #     if p > threshold:

        # print(energies_to_label)
        # print(labels)

        lineid_plot.plot_line_ids(self.decay_photon_energy.x, self.decay_photon_energy.p, energies_to_label, labels)
# my_material.nuclides[0]
# NuclideTuple(name='Xe135', percent=1, percent_type='ao')

        
        # plt.plot()
        plt.xlabel('Energy (eV)')
        # plt.xscale('log')
        plt.ylabel('Probability')
        return plt

openmc.Material = Material