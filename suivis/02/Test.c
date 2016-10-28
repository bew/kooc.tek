#include "Test.h"

static int	A_BEG_n_W_H_BEG_o___END_END_MODULE_4_Test_5_value = 42;
static float	A_BEG_n_W_M_BEG_o___END_END_MODULE_4_Test_5_value = 42.0;

int		A_BEG_n_W_H_BEG_o___END_END_MODULE_4_Test_6_secret = 42;


int		A_BEG_n_T_4_Test_BEG_p__BEG_o___END_END_END_BEG_f_W_H_BEG_o___END_END_MODULE_4_Test_9_get_value(Test *self)
{
  return (self->A_BEG_n_W_H_BEG_o___END_END_MODULE_4_Test_5_value);
}

float		A_BEG_n_T_4_Test_BEG_p__BEG_o___END_END_END_BEG_f_W_M_BEG_o___END_END_MODULE_4_Test_9_get_value(Test *self)
{
  return (self->A_BEG_n_W_M_BEG_o___END_END_MODULE_4_Test_5_value);
}

void		A_BEG_n_T_4_Test_BEG_p__BEG_o___END_END_END_BEG_n_W_H_BEG_o___END_END_BEG_f_W_X_BEG_o___END_END_MODULE_4_Test_9_set_value(Test *self, int number)
{
  self->A_BEG_n_W_H_BEG_o___END_END_MODULE_4_Test_5_value = number;
}

void		A_BEG_n_T_4_Test_BEG_p__BEG_o___END_END_END_BEG_n_W_M_BEG_o___END_END_BEG_f_W_X_BEG_o___END_END_MODULE_4_Test_9_set_value(Test *self, float number)
{
  self->A_BEG_n_W_M_BEG_o___END_END_MODULE_4_Test_5_value = number;
}

char		*A_BEG_n_T_4_Test_BEG_p__BEG_o___END_END_END_BEG_f_W_D_BEG_o___END_END_MODULE_4_Test_14_get_class_name(Test *this)
{
  A_BEG_n_T_4_Test_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_MODULE_4_Test_19_generate_new_secret(this);
  return ("Test");
}

static void	A_BEG_n_T_4_Test_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_MODULE_4_Test_19_generate_new_secret(Test *this)
{
  this->A_BEG_n_W_H_BEG_o___END_END_MODULE_4_Test_6_secret *= 2;
}

void		A_BEG_n_T_4_Test_BEG_p__BEG_o___END_END_END_BEG_n_W_H_BEG_o___END_END_BEG_n_W_M_BEG_o___END_END_BEG_f_W_X_BEG_o___END_END_MODULE_4_Test_4_init(Test *this, int value_int, float value_float)
{
  this->A_BEG_n_W_H_BEG_o___END_END_MODULE_4_Test_5_value = value_int;
  this->A_BEG_n_W_M_BEG_o___END_END_MODULE_4_Test_5_value = value_float;
}

void		A_BEG_n_T_4_Test_BEG_p__BEG_o___END_END_END_BEG_n_W_M_BEG_o___END_END_BEG_n_W_H_BEG_o___END_END_BEG_f_W_X_BEG_o___END_END_MODULE_4_Test_4_init(Test *this, float value_float, int value_int)
{
  this->A_BEG_n_W_M_BEG_o___END_END_MODULE_4_Test_5_value = value_float;
  this->A_BEG_n_W_H_BEG_o___END_END_MODULE_4_Test_5_value = value_int;
}

void		A_BEG_n_T_4_Test_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_MODULE_4_Test_4_init(Test *this)
{
  this->A_BEG_n_W_M_BEG_o___END_END_MODULE_4_Test_5_value = value_float = 42;
  this->A_BEG_n_W_H_BEG_o___END_END_MODULE_4_Test_5_value = value_int =42;
  this->A_BEG_n_W_H_BEG_o___END_END_MODULE_4_Test_6_secret = 42;
}

Test	*A_BEG_f_T_4_Test_BEG_p__BEG_o___END_END_END_MODULE_4_Test_5_alloc()
{
  Test	*Test;

  Test = malloc(sizeof(Test));
  A_BEG_n_T_4_Test_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_MODULE_4_Test_4_init(Test);
  return (Test);
}

Test	*A_BEG_n_W_H_BEG_o___END_END_BEG_n_W_M_BEG_o___END_END_BEG_f_T_4_Test_BEG_p__BEG_o___END_END_END_MODULE_4_Test_3_new(int res_int, foat res_float)
{
  Test	*self;

  self = A_BEG_f_T_4_Test_BEG_p__BEG_o___END_END_END_MODULE_4_Test_5_alloc();
  A_BEG_n_T_4_Test_BEG_p__BEG_o___END_END_END_BEG_n_W_H_BEG_o___END_END_BEG_n_W_M_BEG_o___END_END_BEG_f_W_X_BEG_o___END_END_MODULE_4_Test_4_init(self, res_int, res_float);
  return (self);
}

Test	*A_BEG_n_W_M_BEG_o___END_END_BEG_n_W_H_BEG_o___END_END_BEG_f_T_4_Test_BEG_p__BEG_o___END_END_END_MODULE_4_Test_3_new(float res_float, int res_int)
{
  Test	*self;

  self = A_BEG_f_T_4_Test_BEG_p__BEG_o___END_END_END_MODULE_4_Test_5_alloc();
  A_BEG_n_T_4_Test_BEG_p__BEG_o___END_END_END_BEG_n_W_M_BEG_o___END_END_BEG_n_W_H_BEG_o___END_END_BEG_f_W_X_BEG_o___END_END_MODULE_4_Test_4_init(self, res_float, res_int);
  return (self);
}

void	*A_BEG_n_T_4_Test_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_MODULE_4_Test_6_delete(Test *Test)
{
  free(Test);
}

int		A_BEG_f_W_H_BEG_o___END_END_MODULE_4_Test_9_get_value()
{
  return (A_BEG_n_W_H_BEG_o___END_END_MODULE_4_Test_5_value);
}

float		A_BEG_f_W_M_BEG_o___END_END_MODULE_4_Test_9_get_value()
{
  return (A_BEG_n_W_M_BEG_o___END_END_MODULE_4_Test_5_value);
}

void		A_BEG_n_W_H_BEG_o___END_END_BEG_f_W_X_BEG_o___END_END_MODULE_4_Test_9_set_value(int value)
{
  A_BEG_n_W_H_BEG_o___END_END_MODULE_4_Test_5_value = value;
}

void		A_BEG_n_W_M_BEG_o___END_END_BEG_f_W_X_BEG_o___END_END_MODULE_4_Test_9_set_value(float value)
{
  A_BEG_n_W_M_BEG_o___END_END_MODULE_4_Test_5_value = value;
}

char		*A_BEG_f_W_D_BEG_p__BEG_o___END_END_END_MODULE_4_Test_14_get_class_name()
{
  A_BEG_f_W_X_BEG_o___END_END_MODULE_4_Test_14_get_class_name();
  return ("Test");
}

static void	S_BEG_f_W_X_BEG_o___END_END_MODULE_4_Test_19_generate_new_secret()
{
  A_BEG_n_W_H_BEG_o___END_END_MODULE_4_Test_6_secret *= 2;
}
