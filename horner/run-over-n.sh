#!/bin/bash

# usage:
#  ./run-over-n.sh $1 $2 $3
#
# $1 numerator
# $2 denominator 
# $3 max polynomial degree

if [ "$#" -ne 3 ]; then
    echo "usage: ./run-over-n.sh x-numerator x-denominator degree-max"
fi

rm -f global_*.tsv
rm -f result*.txt

# k polynomial degree
k=8
while (($k<=$3))
do
rm -f resultats_*.tsv


verificarlo-c -g -O0 -o horner horner.c -lm

# polynomial coefficient generator for all values n in [8:$3:2] and x = $1 / $2
python3 ./generator.py $k $1 $2

export VFC_BACKENDS_LOGFILE="verificarlo.log"

VFC_BACKENDS="libinterflop_ieee.so" \
./horner $k $1 $2 > ieee_$k.tsv

# Run 30 iterations of Tchebychev polynomial with Verificarlo for all values n in [8:$3:2] and x = $1 / $2
    for i in $(seq 30);
    do
        VFC_BACKENDS="libinterflop_mca_int.so --precision-binary32=24 --mode=rr" \
        ./horner $k $1 $2 > resultats_$i"_"$k.tsv       
        cat resultats_$i"_"$k.tsv >> global_$k.tsv 
    done
((k+=2)) 
done

# Plot the samples
python3 ./plot-over-n.py $1 $2 $3
