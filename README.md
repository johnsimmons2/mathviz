# Setup
- setup conda or venv
- install requirements in `requirements.txt`
- Run `python main.py` to start. 

# About
## Controls
- `SPACEBAR` to pause a simulation
- `ARROW KEYS (L, R)` to change current simulation view 
- `ARROW KEYS (U, D)` to increase cursor size where relevant
- `D` to enter debug mode for more views

## Particle Simulation
This is a sandbox to play around with rules to emulate different phenomena such as electromagnetic attraction/repulsion. The debugmode will enable the field view to see the "charge" diffusion through the corresponding field.

## Sand Simulation
This simulation is an exercise in interacting and manipulating various systems in this program. Hopefully if I can get a reasonable sand-game that allows easy extensibility, then the systems themselves will be easy to use for other experiments.

## Field Simulation
This was the first demo simulation and utilization of the field code. It is not efficient, but it is useful for my purposes of visualizing. In this simulation I have recreated John Conway's game of life. This is a main point of interest as my goal is to have a similar agnosticism that each cell in the game of life has for each particle in the particle simulator. E.g, a given particle 'feels' gravity or electromagnetism inherently without the computer program or programmer 'telling' it to (see how patterns in Conway's game of life arise).

## Motivation
The main motivation for this project is to gain an understanding of physics, graphics programming, and primarily to research emergent behavior for use in evolutionary algorithms. My end goal, as disparate as this sounds, is to create an environment for meaningful topological evolution of neural networks (See HyperNEAT and related).

The main question I had was related to the evolutionary algorithm research happening right now, they all rely on what the engineer or researcher has decided is the "base" era. For example, if we wanted to explore the depth and width of possibilities under biology with natural selection, we would not say that an 100% thermodynamically isolated, closed system with an arbitrary choice of variables is sufficient to explain or produce all that we see in the natural world. Similarly, I believe that the choices made to signify a network's "DNA" (and the mutations) are arbitrary and not atomic enough. Conway's game of life probably would not work if we had engineered a set of 27 highly specific rules instead, and these arbitrary choices, as harmless as they appear, seem very arbitrary to me.

### Where does particle physics come in?
In a long tangent to the original motivation, I am interested in seeing what kind of behavior of the universe, in a 2D simplified model, I could emulate with the simplest rules. According to electro-weak theory, the fundamental forces of the universe were unified at the earliest moment of the universe. If this is the case, then are what we experience as "laws" of reality incidental of entropy cooling the universe down and allowing weaker forces to emerge? And if so, why do they emerge? Could the universe have just been so hot that the short-distance forces had no time to interact? Or do the forces fundamentally act differently or fundamentally split from one another under certain circumstances? 

The end goal is pseudo-chemical evolution simulation essentially. Little balls that interact with special rules that make them *look* like they form atoms or molecules.

If these fundamental forces are important and caused the "evolution" of quarks and gluons into a specific universal environment, then they must certainly affect what life could evolve in this universe. The amount of UV radiation we receive on earth, the radius of orbits, the elements needed for known biological life, etc; these all are foundationally formed by the laws of our universe from the beginning. However, modern evolutionary algorithms attempt to inject an engineered ecosystem into a system which does not conserve energy, nor provide any sort of natural selection against the parent system. The networks are babies dropped into a white room, and if they are comfortable they have no reason to compete or grow.

### Other important factors
Evolutionary algorithms I see today arbitrate speciation instead of allowing natural selection. For example, a Liger exists, two species creating a new one, however in evolutionary algorithms there is no avenue for two things defined as separate species to procreate. This could be argued to be semantic, since "species" is defined by the researcher anyway. But that is why I find this problematic. Taxonomy exists for a reason to observe nature, not the other way around.

Another issue I find is that there is no avenue for networks to predate eachother or enter into symbiotic/parysitic relationships. It is as if two people give birth to a giraffe; completely separate food chains only 'competing' by some randomly chosen variable. The world of evolutionary algorithms is littered with complex, non-interacting vertibrae but where are the plants? Prokaryotes? 