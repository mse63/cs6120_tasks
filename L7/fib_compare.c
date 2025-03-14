#include <math.h>
#include <stdio.h>

// 1. Tree Recursion (Naive Recursive Approach)
int fib_tree(int n) {
  if (n <= 1)
    return n;
  return fib_tree(n - 1) + fib_tree(n - 2);
}

// 2. Tail Recursion (Efficient Recursive Approach)
int fib_tail_helper(int n, int a, int b) {
  if (n == 0)
    return a;
  if (n == 1)
    return b;
  return fib_tail_helper(n - 1, b, a + b);
}
int fib_tail(int n) { return fib_tail_helper(n, 0, 1); }

// 3. Iterative Approach
int fib_iter(int n) {
  if (n <= 1)
    return n;
  int a = 0, b = 1, c;
  for (int i = 2; i <= n; i++) {
    c = a + b;
    a = b;
    b = c;
  }
  return b;
}

// 4. Exponential Formula Approach (Using Binet's Formula)
int fib_exp(int n) {
  double sqrt5 = sqrt(5);
  double phi = (1 + sqrt5) / 2; // Golden ratio
  return round(pow(phi, n) / sqrt5);
}

int main() {
  int n = 4;
  printf("Fibonacci(%d) using tree recursion: %d\n", n, fib_tree(n));
  printf("Fibonacci(%d) using tail recursion: %d\n", n, fib_tail(n));
  printf("Fibonacci(%d) using iteration: %d\n", n, fib_iter(n));
  printf("Fibonacci(%d) using exponential formula: %d\n", n, fib_exp(n));
  return 0;
}
