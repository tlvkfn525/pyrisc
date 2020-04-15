// See LICENSE for license details.
#include <stdio.h>

int main(void) {
	int a;
	a = getchar();
	
	if(a == 'a') {
		puts("correct");
	} else {
		puts("wrong");	
	}
	return 0;
}
