#include <stdio.h>
#include "TestA.h"
#include "TestB.h"

int	main()
{
  int	res_int;
  float	res_float;
  TestA	testA1;
  TestA	*testA2;
  TestA	*testA3;
  TestA	*testA4;
  TestB testB1;
  TestB	*testB2;
  TestB	*testB3;
  TestB	*testB4;


  res_int = f_b_n_n_H_e_TestA_EOP_get_value_BOS_b_n_p_U_(&testA1);
  res_float = f_b_n_n_M_e_TestA_EOP_get_value_BOS_b_n_p_U_(&testA1);
  f_b_n_n_X_e_TestA_EOP_set_value_BOS_b_n_p_U_e_b_n_n_H_e(&testA1, 21);
  f_b_n_n_X_e_TestA_EOP_set_value_BOS_b_n_p_U_e_b_n_n_M_e(&testA1, 21.0);
  testA1.v_b_n_n_H_e_TestA_EOP_secret_BOS_member = 21;

  testA2 = f_b_n_p_U_e_TestA_EOP_alloc_BOS_();
  testA3 = f_b_n_p_U_e_TestA_EOP_new_BOS_b_n_n_H_e_b_n_n_M_e(res_int, res_float);
  testA4 = f_b_n_p_U_e_TestA_EOP_new_BOS_b_n_n_M_e_b_n_n_H_e(res_float, res_int);
  f_b_n_n_X_e_TestA_EOP_delete_BOS_b_n_n_U_e(testA2);
  f_b_n_n_X_e_TestA_EOP_delete_BOS_b_n_n_U_e(testA3);
  f_b_n_n_X_e_TestA_EOP_delete_BOS_b_n_n_U_e(testA4);

  res_int = f_b_n_n_H_e_TestA_EOP_get_value_BOS_();
  res_float = f_b_n_n_M_e_TestA_EOP_get_value_BOS_();
  f_b_n_n_X_e_TestA_EOP_set_value_BOS_b_n_n_H_e(21);
  f_b_n_n_X_e_TestA_EOP_set_value_BOS_b_n_n_M_e(21.0);
  f_b_n_n_X_e_TestA_EOP_get_class_name_BOS_();
  v_b_n_n_H_e_TestA_EOP_secret = 21;
  printf("Class name : %s\n", f_b_n_n_X_e_TestA_EOP_get_class_name_BOS_());

  res_int = f_b_n_n_H_e_TestA_EOP_get_value_BOS_b_n_p_U_(&testB1);
  res_float = f_b_n_n_M_e_TestA_EOP_get_value_BOS_b_n_p_U_(&testB1);
  f_b_n_n_X_e_TestA_EOP_set_value_BOS_b_n_p_U_e_b_n_n_H_e(&testB1, 21);
  f_b_n_n_X_e_TestA_EOP_set_value_BOS_b_n_p_U_e_b_n_n_M_e(&testB1, 21.0);
  testB1.v_b_n_n_H_e_TestB_EOP_secret_BOS_member = 21;

  testB2 = f_b_n_p_U_e_TestB_EOP_alloc_BOS_();
  testB3 = f_b_n_p_U_e_TestB_EOP_new_BOS_b_n_n_H_e_b_n_n_M_e(res_int, res_float);
  testB4 = f_b_n_p_U_e_TestB_EOP_new_BOS_b_n_n_M_e_b_n_n_H_e(res_float, res_int);
  f_b_n_n_X_e_TestB_EOP_delete_BOS_b_n_n_U_e(testB2);
  f_b_n_n_X_e_TestB_EOP_delete_BOS_b_n_n_U_e(testB3);
  f_b_n_n_X_e_TestB_EOP_delete_BOS_b_n_n_U_e(testB4);

  res_int = f_b_n_n_H_e_TestB_EOP_get_value_BOS_();
  res_float = f_b_n_n_M_e_TestB_EOP_get_value_BOS_();
  f_b_n_n_X_e_TestB_EOP_set_value_BOS_b_n_n_H_e(21);
  f_b_n_n_X_e_TestB_EOP_set_value_BOS_b_n_n_M_e(21.0);
  f_b_n_n_D_e_TestB_EOP_get_class_name_BOS_();
  v_b_n_n_H_e_TestB_EOP_secret = 21;
  printf("Class name : %s\n", f_b_n_n_D_e_TestB_EOP_get_class_name_BOS_());

  return (0);
}
