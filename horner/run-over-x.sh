#!/bin/bash

# usage:
#  ./run-over-n.sh $1 $2 $3
#
# $1 2*(polynomial degree)
# $2 denominator
# x = k/$2

if [ "$#" -ne 2 ]; then
    echo "usage: ./run-over-x.sh 2*(polynomial degree) x-denominator"
    exit 1
fi

rm -f global_*.tsv
rm -f result*.txt
k=8
while (($k<=$2))
do
rm -f resultats_*.tsv

verificarlo-c -g -O0 -o horner horner.c -lm

# polynomial coefficient generator for all values x in [8/64:1.0: 2/64]
python3 ./generator.py $1 $k $2

export VFC_BACKENDS_LOGFILE="verificarlo.log"

# Run 1 iteration of Tchebychev polynomial of degree $1 /2 with ieee norm for all values x in [8/64:1.0: 2/64]
VFC_BACKENDS="libinterflop_ieee.so" \
    ./horner $1 $k $2 > ieee_$k.tsv

# Run 30 iterations of Tchebychev polynomial of degree $1 /2 with Verificarlo for all values x in [8/64:1.0: 2/64]
    for i in $(seq 30);
    do
        VFC_BACKENDS="libinterflop_mca_int.so --precision-binary32=24 --mode=rr" \
        ./horner $1 $k $2 > resultats_$i"_"$k.tsv
        cat resultats_$i"_"$k.tsv >> global_$k.tsv
    done
((k+=2))
done

# Plot the samples
python3 ./plot-over-x.py $1 $2
