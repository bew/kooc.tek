@import "file"
@import "file"

@module ModA
{
int a;
char a;

void *function(void **);
}

@implementation ModA
{
int a = 42;
char a = '0';

void *function(void **b)
  {
    // 'a' should be mangled
    // 'b' should not be mangled
    a = **b;
  }
}

@class MyClass : ModA
{
@member int a = 42;
}
