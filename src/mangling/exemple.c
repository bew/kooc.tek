typedef int toto;

// simple
int variable;
toto variable;
static long unsigned int variable;
int variable[69];
extern void *variable;
const int *variable;
static int * const variable;
volatile unsigned short *variable[42];

// harder
void **(**functionPointer)(int);
struct toto *function(void **, int, ...);

// mad
static double (*functionPointer)(toto **, int, ...);
volatile void (*functionPointer)(void const (*)(int));
