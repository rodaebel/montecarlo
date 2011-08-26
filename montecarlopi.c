/* C program to compute Pi using Monte Carlo Integration.
 *
 * On a system with GNU make installed just type 'make montecarlopi' to
 * compile this program.
 *
 * Otherwise invoke the C compiler by typing:
 *   cc montecarlopi.c -o montecarlopi
 */

#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#define DEFAULT_ITERATIONS 1000000
#define RANDOM_SEED (unsigned)time(NULL)/2


int main(int argc, char *argv[])
{
  int num_iter = DEFAULT_ITERATIONS;
  int i, count = 0;
  double x, y;
  double z;
  double pi;

  if (argc == 2)
    num_iter = atoi(argv[1]);

  srand(RANDOM_SEED);

  for (i=0; i<num_iter; i++) {
    x = (double)rand()/RAND_MAX;
    y = (double)rand()/RAND_MAX;
    z = x*x+y*y;
    if (z <= 1) count++;
  }

  pi = (double)count/num_iter*4;

  printf("%g\n", pi);

  return 0;
}
