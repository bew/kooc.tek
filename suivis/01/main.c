#include "test.h"

int		main()
{
  test_t	*test;
  char		my_buf[MAXBUF];
  char		fmt[13];

  test = test_new("KOOC rulez\n");
  test_print(test);
  free(test);
  printf("Tape un truc (c-D pour finir):");
  sprintf(fmt, "%%%ds", MAXBUF);
  scanf(fmt, my_buf);
  test = test_new(my_buf);
  test_print(test);
  free(test);

  int		foo;
  float		bar;
  int		res_int;
  float		res_float;

  foo = 21;
  bar = A_BEG_n_W_M_BEG_o___END_END_MODULE_4_Test_1_a;
  A_BEG_n_W_H_BEG_o___END_END_MODULE_4_Test_1_a = foo;
  res_int = A_BEG_n_W_H_BEG_o___END_END_BEG_n_W_M_BEG_o___END_END_BEG_f_W_H_BEG_o___END_END_MODULE_4_Test_1_f(foo, bar);
  res_float = A_BEG_n_W_H_BEG_o___END_END_BEG_n_W_M_BEG_o___END_END_BEG_f_W_M_BEG_o___END_END_MODULE_4_Test_1_f(foo, bar);
  A_BEG_n_W_H_BEG_p__BEG_q_c_BEG_o___END_END_END_END_BEG_n_W_M_BEG_p__BEG_q_c_BEG_o___END_END_END_END_BEG_f_W_X_BEG_o___END_END_MODULE_4_Test_1_f(&foo, &bar);

  res_float = A_BEG_n_W_H_BEG_o___END_END_BEG_f_W_M_BEG_o___END_END_MODULE_4_Test_1_f(foo);
  res_float = A_BEG_n_W_M_BEG_o___END_END_BEG_f_W_M_BEG_o___END_END_MODULE_4_Test_1_f(bar);
  res_int = A_BEG_n_W_M_BEG_o___END_END_BEG_f_W_H_BEG_o___END_END_MODULE_4_Test_1_f(foo);
  res_int = A_BEG_n_W_H_BEG_o___END_END_BEG_f_W_H_BEG_o___END_END_MODULE_4_Test_1_f(bar);
  A_BEG_n_W_H_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_MODULE_4_Test_1_f(&foo);
  A_BEG_n_W_M_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_MODULE_4_Test_1_f(&bar);

  return 0;
}
