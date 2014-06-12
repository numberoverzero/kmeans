kmeans
===================
.. image:: https://travis-ci.org/numberoverzero/kmeans.png?branch=master
   :target: https://travis-ci.org/numberoverzero/kmeans

python wrapper for a basic c implementation of the k-means algorithm.

Installation
===================
::

    pip install kmeans

Usage
===================
::

    import kmeans
    means = kmeans.kmeans(points, k)

``points`` should be a list of tuples of the form ``(data, weight)`` where ``data`` is a list with length 3.

For example, finding two mean colors for a group of pixels::

    pixels = [
        [(15, 20, 25), 1],  # [(r,g,b), count]
        [(17, 31, 92), 5],
        # ... Lots more ...
    ]

    mean_pixels = kmeans.kmeans(pixels, 2)

In this case, the weights passed in may be the frequency of the pixels occuring in an image, or some preference to pull the means towards a color.

Inspiration
===================

http://charlesleifer.com/blog/using-python-to-generate-awesome-linux-desktop-themes/

I wanted to apply the implementation there to images much larger than 200x200.  Running a 4k x 3k image was approaching 60 seconds on a nice computer, so I decided to rewrite the kmeans implementation in c.
