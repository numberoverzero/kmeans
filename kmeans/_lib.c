#include <stdint.h>
#include <limits.h>

typedef struct {
    int r, g, b;
    int cluster;
    int weight;
} Point;

int max(int x, int y) { return x > y ? x : y; }
int min(int x, int y) { return x < y ? x : y; }
int clamp(int x, int low, int high) { return max(low, min(x, high)); }

int distance2(Point* p1, Point* p2)
{
    return (p1->r - p2->r) * (p1->r - p2->r)
         + (p1->g - p2->g) * (p1->g - p2->g)
         + (p1->b - p2->b) * (p1->b - p2->b);
}

/* Updates the center point based on the average of the cluster points
   and returns the diff between old center and new center */
int update_center(Point *center, Point *points, int npoints)
{
    int total_w = 0;
    long r = 0, g = 0, b = 0;
    int cluster = center->cluster;
    int i;
    for(i=0; i<npoints; ++i)
    {
        Point p = points[i];
        if(p.cluster != cluster) continue;
        int w = p.weight;
        total_w += w;
        r += w * p.r;
        g += w * p.g;
        b += w * p.b;
    }
    Point new_center = {
        .r = r/total_w,
        .g = g/total_w,
        .b = b/total_w,
    };
    int diff = distance2(center, &new_center);
    center->r = new_center.r;
    center->g = new_center.g;
    center->b = new_center.b;
    center->weight = 1;
    return diff;
}

void kmeans(Point *points, int npoints, Point *centers, int ncenters)
{
    int i, j;
    while(1)
    {
        // Assignment Step
        for(i=0; i<npoints; ++i)
        {
            int min_dist = INT_MAX;
            for(j=0; j<ncenters; ++j)
            {
                int dist = distance2(&points[i], &centers[j]);
                if(dist < min_dist)
                {
                    min_dist = dist;
                    points[i].cluster = centers[j].cluster;
                }
            }
        }

        // Update Step
        int diff = 0;
        for(j=0; j<ncenters; ++j)
        {
            int center_diff = update_center(&(centers[j]), points, npoints);
            diff = max(diff, center_diff);
        }
        if(diff < 2) return;
    }
}
