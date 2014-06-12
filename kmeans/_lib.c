#include <stdio.h>
#include <stdint.h>
#include <limits.h>
#include <string.h> /* memset */
#include <unistd.h> /* close */


// UTIL

int max(int x, int y) { return x > y ? x : y; }
int clamp(int x, int low, int high) {
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
    int r, g, b;
    int cluster;
    int weight;
} Point;

void Point_initialize(Point* points, int npoints)
{
    int i;
    for(i=0; i<npoints; ++i)
    {
        points[i].r = 0;
        points[i].g = 0;
        points[i].b = 0;
        points[i].weight = 0;
    }
}

void Point_normalize(Point* point)
{
    int w = point->weight;
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
    int w = other->weight;
    point->r += w * other->r;
    point->g += w * other->g;
    point->b += w * other->b;
    point->weight += w;
}

int Point_distance(Point* p1, Point* p2)
{
    return (p1->r - p2->r) * (p1->r - p2->r)
         + (p1->g - p2->g) * (p1->g - p2->g)
         + (p1->b - p2->b) * (p1->b - p2->b);
}


// KMEANS

void kmeans_init_centers(Point *centers, int ncenters)
{
    int j;
    for(j=0; j<ncenters; ++j)
    {
        centers[j].weight = 1;
        centers[j].cluster = j;
    }
}

void kmeans_assign(Point *points, int npoints, Point *centers, int ncenters)
{
    int i, j;
    for(i=0; i<npoints; ++i)
    {
        int min_dist = INT_MAX;
        for(j=0; j<ncenters; ++j)
        {
            int dist = Point_distance(&points[i], &centers[j]);
            if(dist < min_dist)
            {
                min_dist = dist;
                points[i].cluster = centers[j].cluster;
            }
        }
    }
}

int kmeans_update(Point *points, int npoints,
        Point *centers, Point *temp_centers, int ncenters)
{
    int diff = 0;
    Point_initialize(temp_centers, ncenters);

    int i, j;
    for(i=0; i<npoints; ++i)
    {
        j = points[i].cluster;
        Point_add(&temp_centers[j], &points[i]);
    }

    for(j=0; j<ncenters; ++j)
    {
        Point_normalize(&temp_centers[j]);
        diff = max(diff, Point_distance(&centers[j], &temp_centers[j]));
        Point_copy(&centers[j], &temp_centers[j]);
    }
    return diff;
}

void kmeans(Point *points, int npoints, Point *centers,
            int ncenters, int tolerance, int max_iterations)
{
    int delta, remaining_iterations;
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
        int diff = kmeans_update(points, npoints,
            centers, temp_centers, ncenters);

        printf("%6d || %d || %3d\n", diff, tolerance, remaining_iterations);
        if(diff <= tolerance || remaining_iterations < 1) return;
    }
}
