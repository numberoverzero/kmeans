#include <stdint.h>

uint64_t max(uint32_t x, uint32_t y) { return x > y ? x : y; }


typedef struct {
    uint8_t r, g, b;
    uint32_t center;
    uint32_t count;
} Point;


typedef struct {
    uint64_t r, g, b;
    uint32_t count;
} Center;


void Centers_zero(Center* centers, uint32_t n)
{
    for(n--; n > 0; n--)
    {
        centers[n].r = 0;
        centers[n].g = 0;
        centers[n].b = 0;
        centers[n].count = 0;
    }
}

void Center_normalize(Center* center)
{
    // No need to change center->count since the center will
    // get cleared before it's used again
    uint32_t w = center->count;
    if(w == 0) {
        return;
    }
    center->r /= w;
    center->g /= w;
    center->b /= w;
}

void Center_copy(Center* center, Center* other)
{
    // Don't copy center count
    center->r = other->r;
    center->g = other->g;
    center->b = other->b;
}

void Center_accumulate(Center* center, Point* point)
{
    // Multiply by count since we're "expanding" the other point
    uint32_t c = point->count;
    center->r += c * point->r;
    center->g += c * point->g;
    center->b += c * point->b;
    center->count += c;
}

uint64_t CenterCenter_distance(Center* c1, Center* c2)
{
    // count does not impact distance
    return (c1->r - c2->r) * (c1->r - c2->r)
         + (c1->g - c2->g) * (c1->g - c2->g)
         + (c1->b - c2->b) * (c1->b - c2->b);
}
uint64_t PointCenter_distance(Point* p, Center* c)
{
    // count does not impact distance
    return (p->r - c->r) * (p->r - c->r)
         + (p->g - c->g) * (p->g - c->g)
         + (p->b - c->b) * (p->b - c->b);
}


void kmeans_assign(Point *points, uint64_t npoints,
    Center *centers, uint32_t ncenters)
{
    for(uint64_t i = 0; i < npoints; ++i)
    {
        uint64_t min_dist = UINT64_MAX;
        for(uint32_t j = 0; j < ncenters; ++j)
        {
            uint64_t dist = PointCenter_distance(&points[i], &centers[j]);
            if(dist < min_dist)
            {
                min_dist = dist;
                points[i].center = j;
            }
        }
    }
}

uint64_t kmeans_update(Point *points, uint64_t npoints,
        Center *centers, Center *temp_centers, uint32_t ncenters)
{
    uint32_t j;
    uint64_t diff = 0;

    Centers_zero(temp_centers, ncenters);
    for(uint64_t i = 0; i < npoints; ++i)
    {
        j = points[i].center;
        Center_accumulate(&temp_centers[j], &points[i]);
    }

    for(j = 0; j < ncenters; ++j)
    {
        Center_normalize(&temp_centers[j]);
        diff = max(diff, CenterCenter_distance(&centers[j], &temp_centers[j]));
        Center_copy(&centers[j], &temp_centers[j]);
    }
    return diff;
}

void kmeans(Point *points, uint64_t npoints, Center *centers,
            uint32_t ncenters, uint32_t tolerance, uint32_t max_iterations)
{
    uint32_t delta, remaining_iterations;
    Center temp_centers[ncenters];

    if(max_iterations <= 0) {
        delta = 0;
        remaining_iterations = 1;
    } else {
        delta = -1;
        remaining_iterations = max_iterations;
    }

    while(remaining_iterations > 0)
    {
        remaining_iterations += delta;

        kmeans_assign(points, npoints, centers, ncenters);
        uint64_t diff = kmeans_update(points, npoints,
            centers, temp_centers, ncenters);

        if(diff <= tolerance || remaining_iterations < 1) return;
    }
}
