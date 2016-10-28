@import "file"
@import "file"

@module A
{
int a;
char a;

void *function(void **);
}

@implementation A
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
