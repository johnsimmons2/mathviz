import psim
from psim.simulation.fieldsimulation import FieldSimulation
from psim.simulation.particlesimulator import ParticleSimulation
from psim.simulation.sandsimulation import SandSimulation


def main():
    psim.addSimulation(ParticleSimulation(5))
    psim.addSimulation(FieldSimulation(50))
    psim.addSimulation(SandSimulation(15))
    psim.start()

if __name__ == "__main__":
    main()

# from unitons import Uniton, PRIMES, AMOUNT

# def getUnitons():
#     AMOUNT
#     nums = []
#     for i in range(AMOUNT):
#         nums.append(Uniton(i))
#     return nums
# UNITONS = getUnitons()

# Notes:
# Prune chains during sleep
# Chemical signaling to other networks
# Periodic waves to add a temporal behavior
# Uncertainty / noise to all data

# Environment has criteria for survival