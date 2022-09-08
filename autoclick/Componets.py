from random import uniform

# Click frequency modifier
def comp_humanoid(cs):
    perc = (cs.delay * (cs.vol / 2)) / 100
    minSample = cs.delay - perc
    maxSample = cs.delay + perc
    cs.delay = uniform(minSample, maxSample)
    return cs
