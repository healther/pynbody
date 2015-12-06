#include <stdio.h>
#include <stdlib.h>
#include "mtwist.h"

int main(void) {
   int i;
   mt_seed32(42424242);
   for(i = 0; i < 10; ++i) {
      printf("%f\n", mt_ldrand());
   }
   return EXIT_SUCCESS;
}