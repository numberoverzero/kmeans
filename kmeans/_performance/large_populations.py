from kmeans import kmeans
from kmeans._performance import timer, random_points

samples = [
    # ~ Common "large" image sizes
    (1920 * 1200,  3),
    (1920 * 1200,  5),
    (1920 * 1200, 15),

    # Personal benchmarks
    (747116, 5),   # Unique pixels in 1920 x 1080 image
    (1095169, 5),  # Unique pixels in 15530 x 8591 image

    # Max unique pixels in rgb 256 image
    (16581375, 5)
]

print "Generating random points"
max_sample = max(sample[0] for sample in samples)
points = random_points(max_sample)
print "Random points generated"

def run_test(n, k):
    points.set_len(n)
    t = timer()
    kmeans(points, k)
    elapsed = t()
    return elapsed

def run_tests(tests, echo=False):
    results = []
    for n, k in tests:
        elapsed = run_test(n, k)
        results.append([n, k, elapsed])
        if echo:
            print "N {:9} K {:3} E {}".format(*results[-1])

run_tests(samples, echo=True)
