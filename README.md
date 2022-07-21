# sr-variance-bounds

Scripts to reproduce the numerical experiments of the paper ["Stochastic
Rounding Variance and Probabilistic Bound: a New Approach"](https://hal.archives-ouvertes.fr/hal-03722888).

Before running the scripts, ensure that you have installed [Verificarlo v0.8.0](https://github.com/verificarlo/verificarlo/releases/tag/v0.8.0), Python 3, and matplotlib on your computer.

## Inner product

To reproduce Inner product experiments use the following commands:

```bash
sr-variance-bounds$ cd inner-product

# To generate figure 8 with 1 - lambda = 0.9
# The generated plot is a pdf file named inner-product-plot.pdf
sr-variance-bounds/inner-product$ verificarlo-c -O2 --function=dot_product_sr ./product.c -o product 
sr-variance-bounds/inner-product$ ./run-and-plot.py
```

## Horner experiments

To reproduce Horner polynomial evaluation experiments use the following commands:

```bash
sr-variance-bounds$ cd horner

# To generate figure 6 with 1 - lambda = 0.9
# The generated plot is a pdf file named horner-plot20.pdf
sr-variance-bounds/horner$ ./run-over-x.sh 20 64

# To generate figure 7 with 1 - lambda = 0.9
# The generated plot is a pdf file named horner-plot24-26.pdf
sr-variance-bounds/horner$ ./run-over-n.sh 24 26 26
```
