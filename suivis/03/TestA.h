#ifndef TESTA_H_
# define TESTA_H_

typedef struct	kooc_s_TestA {
  int		v_b_n_n_H_e_TestA_EOP_value_BOS_member;
  float		v_b_n_n_M_e_TestA_EOP_value_BOS_member;
  int		v_b_n_n_H_e_TestA_EOP_secret_BOS_member;
}		TestA;

int		f_b_n_n_H_e_TestA_EOP_get_value_BOS_b_n_p_U_e(TestA *);
float		f_b_n_n_M_e_TestA_EOP_get_value_BOS_b_n_p_U_e(TestA *);

void		f_b_n_n_X_e_TestA_EOP_set_value_BOS_b_n_p_U_e_b_n_n_H_e(TestA *, int value);
void		f_b_n_n_X_e_TestA_EOP_set_value_BOS_b_n_p_U_e_b_n_n_M_e(TestA *, float value);
char		*f_b_n_n_D_e_TestA_EOP_get_class_name_BOS_b_n_p_U_e(TestA *);

/*attention c'est virtual */
void		f_b_s_n_X_e_TestA_EOP_generate_new_secret_BOS_b_n_p_U_e(TestA *);

void		f_b_n_n_X_e_TestA_EOP_init_BOS_b_n_p_U_e_b_n_n_H_e_b_n_n_M_e(TestA *,int value_int, float value_float);
void		f_b_n_n_X_e_TestA_EOP_init_BOS_b_n_p_U_e_b_n_n_M_e_b_n_n_H_e(TestA *, float value_float, int value_int);


extern int      v_b_n_n_H_e_TestA_EOP_value;
extern float    v_b_n_n_M_e_TestA_EOP_value;
extern int	v_b_n_n_H_e_TestA_EOP_secret;


int		f_b_n_n_H_e_TestA_EOP_get_value_BOS_(); /* no param, BOS ?? */
float		f_b_n_n_M_e_TestA_EOP_get_value_BOS_();
void		f_b_n_n_X_e_TestA_EOP_set_value_BOS_b_n_n_H_e(int value);
void		f_b_n_n_X_e_TestA_EOP_set_value_BOS_b_n_n_M_e(float value);
char		*f_b_n_n_D_e_TestA_EOP_get_class_name_BOS_();
void		f_b_n_n_X_e_TestA_EOP_generate_new_secret_BOS_();

TestA		*f_b_n_p_U_e_TestA_EOP_alloc_BOS_();
TestA		*f_b_n_p_U_e_TestA_EOP_new_BOS_b_n_n_M_e_b_n_n_H_e(float res_float, int res_int);
TestA		*f_b_n_p_U_e_TestA_EOP_new_BOS_b_n_n_H_e_b_n_n_M_e(int res_int, foat res_float);

void		*f_b_n_n_X_e_TestA_EOP_delete_BOS_b_n_n_U_e(TestA *);

typedef struct	kc_TestA_vtable
{
  char		*(*get_class_name)(kc_TestA_interface *);
}		kc_TestA_vtable;

typedef struct		kc_TestA_metadata
{
  char			*kc_TestA_name;
  char			*kc_TestA_inheritance_list;
  kc_TestA_vtable	vtable;
}			kc_TestA_metadata;

typedef	struct		kc_TestA_interface
{
  kc_TestA_metadata	*meta;
  TestA			instance;
}			kc_TestA_interface;

#endif /* !TESTA_H_ */
