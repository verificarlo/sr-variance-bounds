#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <assert.h>

int main(int argc, char *argv[])
{
  FILE *filePointer;
  FILE *fileOut;
  assert(argc == 4);
  int N = strtol(argv[1], NULL, 10);

  // numerator denominator 
  int num = strtol(argv[2], NULL, 10);
  int den = strtol(argv[3], NULL, 10);
  
  // number of coefficients
  int k = (N/2) +1;
  
  // coef
  float a[k];

  // read all coef
  char tagstr[60] = "result";
  char val[3]; 
  sprintf(val, "%d", N);
  char temp[10] = ".txt"; 
  strcat(tagstr, val);
  strcat(tagstr, temp); 

  //2
  filePointer = fopen(tagstr, "r");
  
  //3
  if (filePointer == NULL)
  {
    printf("File is not available \n");
  }
  else
  {
       for (int i = 0; i <  k; i++)
    {
        fscanf(filePointer, "%f", &a[i]);      
      }
    }
  fclose(filePointer);

  // x value
  float x = ((float)num)/((float)den);
  
  float res = a[k-1];
  float x2 = x * x;

  for (int i = k-2; i >= 0; i--) 
  {
    res = res * x2;
    res = res + a[i];
  }
         printf("%.17lf\n", res); 
  return (0);
}
