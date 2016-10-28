#ifndef TESTB_H_
# define TESTB_H_

#include "TestA.h"

typedef struct	kooc_s_TestB {
  TestA		*super;
  int		v_b_n_n_H_e_TestB_EOP_secret_BOS_member;
  float		v_b_n_n_M_e_TestB_EOP_useless_BOS_member;
}		TestB;

/*virtual ??? */

char	*f_b_n_n_D_e_TestB_EOP_get_class_name_BOS_b_n_p_U_e(TestB *);

void	f_b_n_n_X_e_TestB_EOP_init_BOS_b_n_p_U_e_b_n_n_H_e_b_n_n_M_e(TestB *, int, float);
void	f_b_n_n_X_e_TestB_EOP_init_BOS_b_n_p_U_e_b_n_n_M_e_b_n_n_H_e(TestB *, float, int);

extern int      v_b_n_n_H_e_TestB_EOP_value;
extern float    v_b_n_n_M_e_TestB_EOP_value;
extern int      v_b_n_n_H_e_TestB_EOP_secret;


int             f_b_n_n_H_e_TestB_EOP_get_value_BOS_();
float           f_b_n_n_M_e_TestB_EOP_get_value_BOS_();
void            f_b_n_n_X_e_TestB_EOP_set_value_BOS_b_n_n_H_e(int value);
void            f_b_n_n_X_e_TestB_EOP_set_value_BOS_b_n_n_M_e(float value);
char            *f_b_n_n_D_e_TestB_EOP_get_class_name_BOS_();
void            f_b_n_n_X_e_TestB_EOP_generate_new_secret_BOS_();

TestB	*f_b_n_p_U_e_TestB_EOP_alloc_BOS_();
TestB	*f_b_n_p_U_e_TestB_EOP_new_BOS_b_n_n_H_e_b_n_n_M_e(int res_int, foat res_float);
TestB	*f_b_n_p_U_e_TestB_EOP_new_BOS_b_n_n_M_e_b_n_n_H_e(float res_float, int res_int);
void	*f_b_n_n_X_e_TestB_EOP_delete_BOS_b_n_n_U_e(TestB *testB);

typedef struct	kc_TestB_vtable
{
  char		*(*get_class_name)(kc_TestA_interface *);
}		kc_TestB_vtable;

typedef struct		kc_TestB_metadata
{
  char			*kc_TestB_name;
  char			*kc_TestB_inheritance_list;
  kc_TestB_vtable	vtable;
}			kc_TestB_metadata;

typedef	struct		kc_TestB_interface
{
  kc_TestB_metadata	*meta;
  TestB			instance;
}			kc_TestB_interface;


#endif /* !TESTB_H_ */
