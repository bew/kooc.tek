#include "test.h"
#include "test.h"
#include "test.h"


int	A_BEG_n_W_H_BEG_o___END_END_MODULE_4_Test_1_a;
char	A_BEG_n_W_D_BEG_o___END_END_MODULE_4_Test_1_a = 'a';
float	A_BEG_n_W_M_BEG_o___END_END_MODULE_4_Test_1_a = 42.0;
double	A_BEG_n_W_N_BEG_o___END_END_MODULE_4_Test_1_a;

static char	S_BEG_n_W_D_BEG_o___END_END_MODULE_4_Test_1_b = 'b';
static float	S_BEG_n_W_M_BEG_o___END_END_MODULE_4_Test_1_b = 21.0;

int		A_BEG_n_W_H_BEG_o___END_END_BEG_n_W_M_BEG_o___END_END_BEG_f_W_H_BEG_o___END_END_MODULE_4_Test_1_f(int foo, float bar)
{
  return foo+((int)bar);
}

float		A_BEG_n_W_H_BEG_o___END_END_BEG_n_W_M_BEG_o___END_END_BEG_f_W_M_BEG_o___END_END_MODULE_4_Test_1_f(int foo, float bar)
{
  return ((float)foo)+bar;
}

void		A_BEG_n_W_H_BEG_p__BEG_q_c_BEG_o___END_END_END_END_BEG_n_W_M_BEG_p__BEG_q_c_BEG_o___END_END_END_END_BEG_f_W_X_BEG_o___END_END_MODULE_4_Test_1_f(const int *foo, const float *bar)
{
  printf("int: %i && float: %f\n", *foo, *bar);
}

float		A_BEG_n_W_H_BEG_o___END_END_BEG_f_W_M_BEG_o___END_END_MODULE_4_Test_1_f(int foo)
{
  return (float)foo;
}

float		A_BEG_n_W_M_BEG_o___END_END_BEG_f_W_M_BEG_o___END_END_MODULE_4_Test_1_f(float bar)
{
  return bar;
}

int		A_BEG_n_W_M_BEG_o___END_END_BEG_f_W_H_BEG_o___END_END_MODULE_4_Test_1_f(float bar)
{
  return (int)bar;
}

int		A_BEG_n_W_H_BEG_o___END_END_BEG_f_W_H_BEG_o___END_END_MODULE_4_Test_1_f(int foo)
{
  return foo;
}

void		A_BEG_n_W_H_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_MODULE_4_Test_1_f(int *foo)
{
  *foo = S_BEG_n_W_D_BEG_o___END_END_MODULE_4_Test_1_b;
}

void		A_BEG_n_W_M_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_MODULE_4_Test_1_f(float *bar)
{
  *bar = S_BEG_n_W_M_BEG_o___END_END_MODULE_4_Test_1_b;
}
