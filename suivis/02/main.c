#include <stdio.h>
#include "Test.h"

int	main()
{
  int	res_int;
  float	res_float;
  Test	test1;
  f_b_n_n_X_e_Test_EOP_init_BOS_b_n_p_U_e(&test1);
  Test	*test2;
  Test	*test3;
  Test	*test4;

  res_int = f_b_n_n_H_e_Test_EOP_get_value_BOS_b_n_p_U_(&test1);
  res_float = f_b_n_n_M_e_Test_EOP_get_value_BOS_b_n_p_U_(&test1);
  f_b_n_n_X_e_Test_EOP_set_value_BOS_b_n_p_U_e_b_n_n_H_e(&test1, 21);
  f_b_n_n_X_e_Test_EOP_set_value_BOS_b_n_p_U_e_b_n_n_M_e(&test1, 21.0);
  test1.v_b_n_n_H_e_Test_EOP_secret = 21;
  printf("Class name : %s\n", f_b_n_n_X_e_Test_EOP_get_class_name_BOS_b_n_p_U_e(&test1));

  test2	= f_b_n_p_U_e_Test_EOP_alloc_BOS_();
  test3 = f_b_n_p_U_e_Test_EOP_new_BOS_b_n_n_H_e_b_n_n_M_e(res_int, res_float);
  test4	= f_b_n_p_U_e_Test_EOP_new_BOS_b_n_n_M_e_b_n_n_H_e(res_float, res_int);
  f_b_n_n_X_e_Test_EOP_delete_BOS_b_n_n_U_e(test2);
  f_b_n_n_X_e_Test_EOP_delete_BOS_b_n_n_U_e(test3);
  f_b_n_n_X_e_Test_EOP_delete_BOS_b_n_n_U_e(test4);

  res_int = f_b_n_n_H_e_Test_EOP_get_value_BOS_();
  res_float = f_b_n_n_M_e_Test_EOP_get_value_BOS_();
  f_b_n_n_X_e_Test_EOP_set_value_BOS_b_n_n_H_e(21);
  f_b_n_n_X_e_Test_EOP_set_value_BOS_b_n_n_M_e(21.0);
  f_b_n_n_X_e_Test_EOP_get_class_name_BOS_();
  v_b_n_n_H_e_Test_EOP_secret = 21;
  printf("Class name : %s\n", f_b_n_n_X_e_Test_EOP_get_class_name_BOS_());

  return (0);
}
