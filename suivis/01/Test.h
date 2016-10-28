#ifndef TEST_H_
# define TEST_H_

#define MAXBUF 4200

typedef struct	test_s
{
  int		size;
  char		st[MAXBUF];
}		test_t;

static inline test_t	*test_new(char *str)
{
  test_t		*test;

  if (!str)
    return (0);
  test = calloc(1, sizeof (test_t));
  test->size = strlen(str) > MAXBUF ? MAXBUF : strlen(str);
  memcpy(test->st, str, test->size);
  return (test);
}

static inline void	test_print(test_t *test)
{
  printf("%s", test->st);
}

extern int	A_BEG_n_W_H_BEG_o___END_END_MODULE_4_Test_1_a;
extern char	A_BEG_n_W_D_BEG_o___END_END_MODULE_4_Test_1_a;
extern float	A_BEG_n_W_M_BEG_o___END_END_MODULE_4_Test_1_a;
extern double	A_BEG_n_W_N_BEG_o___END_END_MODULE_4_Test_1_a;

int		A_BEG_n_W_H_BEG_o___END_END_BEG_n_W_M_BEG_o___END_END_BEG_f_W_H_BEG_o___END_END_MODULE_4_Test_1_f(int foo, float bar);
float		A_BEG_n_W_H_BEG_o___END_END_BEG_n_W_M_BEG_o___END_END_BEG_f_W_M_BEG_o___END_END_MODULE_4_Test_1_f(int foo, float bar);
void		A_BEG_n_W_H_BEG_p__BEG_q_c_BEG_o___END_END_END_END_BEG_n_W_M_BEG_p__BEG_q_c_BEG_o___END_END_END_END_BEG_f_W_X_BEG_o___END_END_MODULE_4_Test_1_f(const int *foo, const float *bar);
float		A_BEG_n_W_H_BEG_o___END_END_BEG_f_W_M_BEG_o___END_END_MODULE_4_Test_1_f(int foo);
float		A_BEG_n_W_M_BEG_o___END_END_BEG_f_W_M_BEG_o___END_END_MODULE_4_Test_1_f(float bar);
int		A_BEG_n_W_M_BEG_o___END_END_BEG_f_W_H_BEG_o___END_END_MODULE_4_Test_1_f(float bar);
int		A_BEG_n_W_H_BEG_o___END_END_BEG_f_W_H_BEG_o___END_END_MODULE_4_Test_1_f(int foo);
void		A_BEG_n_W_H_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_MODULE_4_Test_1_f(int *foo);
void		A_BEG_n_W_M_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_MODULE_4_Test_1_f(float *bar);

#endif
