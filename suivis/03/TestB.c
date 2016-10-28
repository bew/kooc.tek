#include "TestB.h"

int      v_b_n_n_H_e_TestB_EOP_value = 42;
float    v_b_n_n_M_e_TestB_EOP_value = 42.0;
int      v_b_n_n_H_e_TestB_EOP_secret = 42;

kc_TestA_metadata	metadataTestA = {
  "TestB",
  "TestA",
  {
    &f_b_n_n_D_e_TestA_EOP_get_class_name_BOS_b_n_p_U_e,
    &f_b_n_n_D_e_TestB_EOP_get_class_name_BOS_b_n_p_U_e    
  }
}

char	*f_b_n_n_D_e_TestB_EOP_get_class_name_BOS_b_n_p_U_e(TestB *self)
{
  self->f_b_n_n_X_e_TestB_EOP_generate_new_secret_BOS_();
  return ("TestB");
}

void	f_b_n_n_X_e_TestB_EOP_init_BOS_b_n_p_U_e_b_n_n_H_e_b_n_n_M_e(TestB *self, int val_int, float val_float)
{
  f_b_n_n_X_e_TestA_EOP_init_BOS_b_n_p_U_e_b_n_n_H_e_b_n_n_M_e(self->super, val_int, val_float);
}

void	f_b_n_n_X_e_TestB_EOP_init_BOS_b_n_p_U_e_b_n_n_M_e_b_n_n_H_e(TestB *self, float val_float, int val_int)
{
  f_b_n_n_X_e_TestA_EOP_init_BOS_b_n_p_U_e_b_n_n_M_e_b_n_n_H_e(self->super, val_float, val_int);
}

char            *f_b_n_n_D_e_TestB_EOP_get_class_name_BOS_()
{
  f_b_n_n_X_e_TestB_EOP_generate_new_secret_BOS_();
  return ("TestB");
}

void            f_b_n_n_X_e_TestB_EOP_generate_new_secret_BOS_()
{
  v_b_n_n_H_e_TestB_EOP_secret_BOS_member *= 2;
}

TestB		*f_b_n_p_U_e_TestB_EOP_alloc_BOS_()
{
  TestB *self;

  self = malloc(sizeof(TestB));
  self->super = f_b_n_p_U_e_TestA_EOP_alloc_BOS_();
  return (self);
}

TestB	*f_b_n_p_U_e_TestB_EOP_new_BOS_b_n_n_H_e_b_n_n_M_e(int res_int, foat res_float)
{
  TestB *self;

  self = f_b_n_p_U_e_TestB_EOP_alloc_BOS_();
  f_b_n_n_X_e_TestB_EOP_init_BOS_b_n_p_U_e_b_n_n_H_e_b_n_n_M_e(self, res_int, res_float);
  return (self);
}

TestB	*f_b_n_p_U_e_TestB_EOP_new_BOS_b_n_n_M_e_b_n_n_H_e(float res_float, int res_int)
{
  TestB *self;

  self = f_b_n_p_U_e_TestB_EOP_alloc_BOS_();
  f_b_n_n_X_e_TestB_EOP_init_BOS_b_n_p_U_e_b_n_n_M_e_b_n_n_H_e(self, res_float, res_int);
  return (self);
}

void	*f_b_n_n_X_e_TestB_EOP_delete_BOS_b_n_n_U_e(TestB *testB)
{
  f_b_n_n_X_e_TestA_EOP_delete_BOS_b_n_n_U_e(testB->super);
  free(testB);
}
