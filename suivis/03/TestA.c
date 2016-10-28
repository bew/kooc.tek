#include "TestA.h"

int      v_b_n_n_H_e_TestA_EOP_value = 42;
float    v_b_n_n_M_e_TestA_EOP_value = 42.0;
int	v_b_n_n_H_e_TestA_EOP_secret = 42;

kc_TestA_metadata	metadataTestA = {
  "TestA",
  "",
  {
    &f_b_n_n_D_e_TestA_EOP_get_class_name_BOS_b_n_p_U_e
  }
}

int		f_b_n_n_H_e_TestA_EOP_get_value_BOS_b_n_p_U_e(TestA *self)
{
  return (self->v_b_s_n_H_e_TestA_EOP_value_BOS_member);
}

float		f_b_n_n_M_e_TestA_EOP_get_value_BOS_b_n_p_U_e(TestA *self)
{
  return (self->v_b_s_n_M_e_TestA_EOP_value_BOS_member);
}

void		f_b_n_n_X_e_TestA_EOP_set_value_BOS_b_n_p_U_e_b_n_n_H_e(TestA *self, int number)
{
  self->v_b_s_n_H_e_TestA_EOP_value_BOS_member = number;
}

void		f_b_n_n_X_e_TestA_EOP_set_value_BOS_b_n_p_U_e_b_n_n_M_e(TestA * self, float number)
{
  self->v_b_s_n_M_e_TestA_EOP_value_BOS_member = number;
}

char		*f_b_n_n_D_e_TestA_EOP_get_class_name_BOS_b_n_p_U_e(TestA *this)
{
  this->generate_new_secret(this);
  return ("TestA");
}

void		f_b_s_n_X_e_TestA_EOP_generate_new_secret_BOS_b_n_p_U_e(TestA *that)
{
  that->v_b_n_n_H_e_TestA_EOP_secret_BOS_member *= 2;
}

void		f_b_n_n_X_e_TestA_EOP_init_BOS_b_n_p_U_e_b_n_n_H_e_b_n_n_M_e(TestA *this, int value_int, float value_float)
{
  this->v_b_s_n_H_e_TestA_EOP_value_BOS_member = value_int;
  this->v_b_s_n_M_e_TestA_EOP_value_BOS_member = value_float;
}

void		f_b_n_n_X_e_TestA_EOP_init_BOS_b_n_p_U_e_b_n_n_M_e_b_n_n_H_e(TestA *this, float value_float, int value_int)
{
  this->v_b_s_n_M_e_TestA_EOP_value_BOS_member = value_float;
  this->v_b_s_n_H_e_TestA_EOP_value_BOS_member = value_int;
}

int		f_b_n_n_H_e_TestA_EOP_get_value_BOS_()
{
  return (v_b_n_n_H_e_TestA_EOP_value);
}

float		f_b_n_n_M_e_TestA_EOP_get_value_BOS_()
{
  return (v_b_n_n_M_e_TestA_EOP_value);
}

void		f_b_n_n_X_e_TestA_EOP_set_value_BOS_b_n_n_H_e(int value)
{
  v_b_n_n_H_e_TestA_EOP_value = value;
}

void		f_b_n_n_X_e_TestA_EOP_set_value_BOS_b_n_n_M_e(float value)
{
  v_b_n_n_M_e_TestA_EOP_value = value;
}

char		*f_b_n_n_D_e_TestA_EOP_get_class_name_BOS_()
{
  f_b_s_n_X_e_TestA_EOP_generate_new_secret_BOS();
  return ("TestA");
}

void		f_b_s_n_X_e_TestA_EOP_generate_new_secret_BOS_()
{
  v_b_n_n_H_e_TestA_EOP_secret *= 2;
}


TestA		*f_b_n_p_U_e_TestA_EOP_alloc_BOS_()
{
  return (malloc(sizeof(TestA)));
}

TestA	*f_b_n_p_U_e_TestA_EOP_new_BOS_b_n_n_H_e_b_n_n_M_e(int res_int, foat res_float)
{
  TestA	*self;

  self = f_b_n_p_U_e_TestA_EOP_alloc_BOS_();
  f_b_n_n_X_e_TestA_EOP_init_BOS_b_n_p_U_e_b_n_n_H_e_b_n_n_M_e(self, res_int, res_float);
  return (self);
}

TestA	*f_b_n_p_U_e_TestA_EOP_new_BOS_b_n_n_M_e_b_n_n_H_e(float res_float, int res_int)
{
  TestA	*self;

  self = f_b_n_p_U_e_TestA_EOP_alloc_BOS_();
  f_b_n_n_X_e_TestA_EOP_init_BOS_b_n_p_U_e_b_n_n_M_e_b_n_n_H_e(self, res_float, res_int);
  return (self);
}

void	*f_b_n_n_X_e_TestA_EOP_delete_BOS_b_n_n_U_e(TestA *testA)
{
  return(free(testA));
}

