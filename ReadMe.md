# Area estimation of the Mandelbrot set
This repository contains several files each containing a sampling method.
- randommontecarlo.py utilizes the pure random sampling strategy
- hypercube.py utilizes the Latin hypercube sampling strategy
- orthogonal.py utilizes the orthogonal sampling strategy
- controlvar.py utilizes the Latin hypercube sampling strategy in combination with control variates
- controlvarortho.py utilizes the orthogonal sampling strategy in combination with control variates

Each file can be ran and returns a .csv file containing the mean estimated area, standard deviation and 95% confidence radius for 100, 1000, 10000 and 10000 random variables and 100, 500, 1000, 2500 recursion depth in the Mandelbrot set. Additionally Mandelbrotset.py can be used to visualize the set.

Authors:
- Loek van Steijn
- Sebastiaan Kruize
