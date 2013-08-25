#include <stdint.h>
#include <limits.h>
#include <string.h> /* memset */
#include <unistd.h> /* close */

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

void kmeans_assign(Point *points, int npoints, Point *centers, int ncenters)
{
    int i, j;
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
}

int kmeans_update(Point *points, int npoints, Point *centers, int ncenters)
{
    int diff = 0;

    int total_w[ncenters];
    memset(total_w, 0, sizeof total_w);

    long r[ncenters], g[ncenters], b[ncenters];
    memset(r, 0, sizeof r);
    memset(g, 0, sizeof g);
    memset(b, 0, sizeof b);

    int i, j;
    for(i=0; i<npoints; ++i)
    {
        Point p = points[i];
        int c = p.cluster;
        int w = p.weight;
        total_w[c] += w;
        r[c] += w * p.r;
        g[c] += w * p.g;
        b[c] += w * p.b;
    }
    for(j=0; j<ncenters; ++j)
    {
        Point new_center = {
            .r = r[j]/total_w[j],
            .g = g[j]/total_w[j],
            .b = b[j]/total_w[j],
        };
        diff = max(diff, distance2(&centers[j], &new_center));
        centers[j].r = new_center.r;
        centers[j].g = new_center.g;
        centers[j].b = new_center.b;
        centers[j].weight = 1;
    }
    return diff;
}

void kmeans(Point *points, int npoints, Point *centers, int ncenters)
{
    while(1)
    {
        kmeans_assign(points, npoints, centers, ncenters);
        int diff = kmeans_update(points, npoints, centers, ncenters);
        if(diff < 2) return;
    }
}
