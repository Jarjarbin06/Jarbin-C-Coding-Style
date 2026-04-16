#include <stdio.h>

int main(void)
{
    int x = 5;
    int y = 10;

    int result;

    __asm__("movl %1, %%eax;"
            "addl %2, %%eax;"
            "movl %%eax, %0;"
            : "=r"(result)
            : "r"(x), "r"(y)
            : "%eax");

    printf("%d\n", result);

    return 0;
}