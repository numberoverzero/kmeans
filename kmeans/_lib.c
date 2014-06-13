#include <stdint.h>


// UTIL

uint32_t max(uint32_t x, uint32_t y) { return x > y ? x : y; }
uint32_t clamp(uint32_t x, uint32_t low, uint32_t high) {
    if(x < low) {
        return low;
    }
    if(x > high) {
        return high;
    }
    return x;
}


// POINT

typedef struct {
    uint64_t r, g, b;
    uint32_t cluster;
    uint32_t weight;
} Point;

void Points_zero(Point* points, uint32_t npoints)
{
    for(npoints--; npoints > 0; npoints--)
    {
        points[npoints].r = 0;
        points[npoints].g = 0;
        points[npoints].b = 0;
        points[npoints].weight = 0;
    }
}

void Point_normalize(Point* point)
{
    uint32_t w = point->weight;
    if(w == 0) {
        return;
    }
    point->r /= w;
    point->g /= w;
    point->b /= w;
}

void Point_copy(Point* point, Point* other)
{
    // Don't copy cluster or weight
    point->r = other->r;
    point->g = other->g;
    point->b = other->b;
}

void Point_add(Point* point, Point* other)
{
    // Multiply by weight since we're "expanding" the other point
    uint32_t w = other->weight;
    point->r += w * other->r;
    point->g += w * other->g;
    point->b += w * other->b;
    point->weight += w;
}

uint64_t Point_distance(Point* p1, Point* p2)
{
    return (p1->r - p2->r) * (p1->r - p2->r)
         + (p1->g - p2->g) * (p1->g - p2->g)
         + (p1->b - p2->b) * (p1->b - p2->b);
}


// KMEANS

void kmeans_init_centers(Point *centers, uint32_t ncenters)
{
    for(uint32_t j = 0; j < ncenters; ++j)
    {
        centers[j].weight = 1;
        centers[j].cluster = j;
    }
}

void kmeans_assign(Point *points, uint64_t npoints,
    Point *centers, uint32_t ncenters)
{
    for(uint64_t i = 0; i < npoints; ++i)
    {
        uint64_t min_dist = UINT64_MAX;
        for(uint32_t j = 0; j < ncenters; ++j)
        {
            uint64_t dist = Point_distance(&points[i], &centers[j]);
            if(dist < min_dist)
            {
                min_dist = dist;
                points[i].cluster = centers[j].cluster;
            }
        }
    }
}

uint64_t kmeans_update(Point *points, uint64_t npoints,
        Point *centers, Point *temp_centers, uint32_t ncenters)
{
    uint64_t diff = 0;
    Points_zero(temp_centers, ncenters);

    uint32_t j;
    for(uint64_t i = 0; i < npoints; ++i)
    {
        j = points[i].cluster;
        Point_add(&temp_centers[j], &points[i]);
    }

    for(j = 0; j < ncenters; ++j)
    {
        Point_normalize(&temp_centers[j]);
        diff = max(diff, Point_distance(&centers[j], &temp_centers[j]));
        Point_copy(&centers[j], &temp_centers[j]);
    }
    return diff;
}

void kmeans(Point *points, uint64_t npoints, Point *centers,
            uint32_t ncenters, uint32_t tolerance, uint32_t max_iterations)
{
    uint32_t delta;
    uint32_t remaining_iterations;
    Point temp_centers[ncenters];

    if(max_iterations <= 0) {
        delta = 0;
        remaining_iterations = 1;
    } else {
        delta = -1;
        remaining_iterations = max_iterations;
    }

    kmeans_init_centers(centers, ncenters);
    kmeans_init_centers(temp_centers, ncenters);

    while(remaining_iterations > 0)
    {
        remaining_iterations += delta;

        kmeans_assign(points, npoints, centers, ncenters);
        uint64_t diff = kmeans_update(points, npoints,
            centers, temp_centers, ncenters);

        if(diff <= tolerance || remaining_iterations < 1) return;
    }
}
