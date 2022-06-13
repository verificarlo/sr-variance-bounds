#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define real float

// initialize arrays with positive floating-points between 0 and 1
// condition number of U and V is 1.
real *random_array(long n) {
  real *A = malloc(n * sizeof(real));
  for (int i = 0; i < n; i++) {
    A[i] = (float)rand() / (float)RAND_MAX;
  }
  return A;
}

// compute the inner product. This function will be instrumented with
// verificarlo mca-int backend.
__attribute__((noinline)) void dot_product_sr(long n, real *U, real *V) {
  real res = 0.0;
  for (int i = 0; i < n; i++) {
    res += U[i] * V[i];
  }
  printf("%.17lf\n", res);
}

int main(int argc, char *argv[]) {
  // seed RNG with fixed seed 0
  srand(0);
  assert(argc == 3);
  long n = strtol(argv[1], NULL, 10);
  long repetitions = strtol(argv[2], NULL, 10);
  real res;
  real *U = random_array(n);
  real *V = random_array(n);

  // errors are computed against a reference value
  // computed in quadruple precision (float128)
  __float128 res_q = 0.0;
  for (int i = 0; i < n; i++) {
    __float128 u = U[i];
    __float128 v = V[i];
    res_q += u * v;
  }
  printf("%.17lf\n", (double)res_q);

  for (int r = 0; r < repetitions; r++) {
    dot_product_sr(n, U, V);
  }

  free(U);
  free(V);
  return (0);
}
