"""Tests for the evo_optimizers.py module."""

import unittest
import warnings

import budeff

import isambard.optimisation.evo_optimizers as ev_opts
from isambard.optimisation.evo_optimizers import Parameter
from isambard.modelling.scwrl import scwrl_available
import isambard.specifications as specs

warnings.filterwarnings("ignore")


@unittest.skipUnless(scwrl_available(), "External program not detected.")
class TestOptimizers(unittest.TestCase):
    """Tests the GA optimizer."""

    def tiny_opt_run(self, optimizer):
        """Perform a tiny run of an optimizer."""
        specification = specs.CoiledCoil.from_parameters
        sequences = ['EIAALKQEIAALKK'] * 2
        parameters = [
            Parameter.static('Oligomeric State', 2),
            Parameter.static('Helix Length', 14),
            Parameter.dynamic('Radius', 5.0, 1.0),
            Parameter.dynamic('Pitch', 180, 100),
            Parameter.dynamic('PhiCA', -78, 27),
        ]
        opt = optimizer(specification, sequences, parameters,
                        lambda x: budeff.get_interaction_energy(x).total_energy)
        opt.run_opt(5, 2, cores=1)
        self.assertTrue(opt.best_model)

    def test_ga(self):
        """Performs a tiny run of the GA"""
        self.tiny_opt_run(ev_opts.GA)

    def test_pso(self):
        """Performs a tiny run of the PSO"""
        self.tiny_opt_run(ev_opts.PSO)

    def test_de(self):
        """Performs a tiny run of the DE"""
        self.tiny_opt_run(ev_opts.DE)

    def test_cmaes(self):
        """Performs a tiny run of the CMAES"""
        self.tiny_opt_run(ev_opts.CMAES)
