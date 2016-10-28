
#ifndef peauxVertes_KMOD_h_
# define peauxVertes_KMOD_h_

typedef struct __attribute__((packed))	kc_PeauxVertes_instance
{
  int		A_BEG_n_W_H_BEG_o___END_END_CLASS_11_PeauxVertes_14_PeauxVertes_pv;
  int		A_BEG_n_W_H_BEG_o___END_END_CLASS_11_PeauxVertes_19_PeauxVertes_attaque;
  int		A_BEG_n_W_H_BEG_o___END_END_CLASS_11_PeauxVertes_19_PeauxVertes_agilite;
}		kc_PeauxVertes_instance;

typedef struct			kc_PeauxVertes_vtable
{
  void	(*V_A_BEG_n_W_X_BEG_p__BEG_t_BEG_n_T_11_PeauxVertes_BEG_p__BEG_o___END_END_END_BEG_o___END_END_END_END_CLASS_11_PeauxVertes_7_attaque)(PeauxVertes *self);
  void	(*V_A_BEG_n_W_X_BEG_p__BEG_t_BEG_n_T_11_PeauxVertes_BEG_p__BEG_o___END_END_END_BEG_o___END_END_END_END_CLASS_11_PeauxVertes_5_clean)(PeauxVertes *self);
  void	(*V_A_BEG_n_W_X_BEG_p__BEG_t_BEG_n_T_11_PeauxVertes_BEG_p__BEG_o___END_END_END_BEG_o___END_END_END_END_CLASS_11_PeauxVertes_5_magie)(PeauxVertes *self);
}				kc_PeauxVertes_vtable;

typedef struct			kc_PeauxVertes_metadata
{
  char				*name;
  char				*inheritance_list;
  kc_PeauxVertes_vtable		vtable;
}				kc_PeauxVertes_metadata;

typedef struct			kc_PeauxVertes_interface
{
  kc_PeauxVertes_metadata	*meta;
  kc_PeauxVertes_instance	instance;
}				kc_PeauxVertes_interface;

void	A_BEG_n_T_11_PeauxVertes_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_CLASS_11_PeauxVertes_16_PeauxVertes_init(PeauxVertes *self);
void	V_A_BEG_n_T_11_PeauxVertes_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_CLASS_11_PeauxVertes_17_PeauxVertes_clean(PeauxVertes *self);
void	V_A_BEG_n_T_11_PeauxVertes_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_CLASS_11_PeauxVertes_19_PeauxVertes_attaque(PeauxVertes *self);
void	V_A_BEG_n_T_11_PeauxVertes_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_CLASS_11_PeauxVertes_17_PeauxVertes_magie(PeauxVertes *self);



typedef struct __attribute__((packed))	kc_Orque_instance
{
  int		A_BEG_n_W_H_BEG_o___END_END_CLASS_11_PeauxVertes_14_PeauxVertes_pv;
  int		A_BEG_n_W_H_BEG_o___END_END_CLASS_11_PeauxVertes_19_PeauxVertes_attaque;
  int		A_BEG_n_W_H_BEG_o___END_END_CLASS_11_PeauxVertes_19_PeauxVertes_agilite;
}		kc_Orque_instance;

typedef struct			kc_Orque_vtable
{
  void	(*V_A_BEG_n_W_X_BEG_p__BEG_t_BEG_n_T_5_Orque_BEG_p__BEG_o___END_END_END_BEG_o___END_END_END_END_CLASS_5_Orque_7_attaque)(Orque *self);
  void	(*V_A_BEG_n_W_X_BEG_p__BEG_t_BEG_n_T_5_Orque_BEG_p__BEG_o___END_END_END_BEG_o___END_END_END_END_CLASS_5_Orque_5_clean)(Orque *self);
  void	(*V_A_BEG_n_W_X_BEG_p__BEG_t_BEG_n_T_5_Orque_BEG_p__BEG_o___END_END_END_BEG_o___END_END_END_END_CLASS_5_Orque_5_magie)(Orque *self);
}				kc_Orque_vtable;

typedef struct		kc_Orque_metadata
{
  char			*name;
  char			*inheritance_list;
  kc_Orque_vtable	vtable;
}			kc_Orque_metadata;

typedef struct		kc_Orque_interface
{
  kc_Orque_metadata	*meta;
  kc_Orque_instance	instance;
}			kc_Orque_interface;

void	A_BEG_n_T_5_Orque_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_CLASS_5_Orque_10_Orque_init(Orque *self);
void	V_A_BEG_n_T_5_Orque_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_CLASS_5_Orque_11_Orque_clean(Orque *self);
void	V_A_BEG_n_T_5_Orque_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_CLASS_5_Orque_13_Orque_attaque(Orque *self);
void	V_A_BEG_n_T_5_Orque_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_CLASS_5_Orque_11_Orque_magie(Orque *self);


typedef struct __attribute__((packed))	kc_Gobelin_instance
{
  int		A_BEG_n_W_H_BEG_o___END_END_CLASS_11_PeauxVertes_14_PeauxVertes_pv;
  int		A_BEG_n_W_H_BEG_o___END_END_CLASS_11_PeauxVertes_19_PeauxVertes_attaque;
  int		A_BEG_n_W_H_BEG_o___END_END_CLASS_11_PeauxVertes_19_PeauxVertes_agilite;
  int		A_BEG_n_W_H_BEG_o___END_END_CLASS_7_Gobelin_17_Gobelin_Parchemin;
}		kc_Gobelin_instance;

typedef struct			kc_Gobelin_vtable
{
  void	(*V_A_BEG_n_W_X_BEG_p__BEG_t_BEG_n_T_7_Gobelin_BEG_p__BEG_o___END_END_END_BEG_o___END_END_END_END_CLASS_7_Gobelin_7_attaque)(Gobelin *self);
  void	(*V_A_BEG_n_W_X_BEG_p__BEG_t_BEG_n_T_7_Gobelin_BEG_p__BEG_o___END_END_END_BEG_o___END_END_END_END_CLASS_7_Gobelin_5_clean)(Gobelin *self);
  void	(*V_A_BEG_n_W_X_BEG_p__BEG_t_BEG_n_T_7_Gobelin_BEG_p__BEG_o___END_END_END_BEG_o___END_END_END_END_CLASS_7_Gobelin_5_magie)(Gobelin *self);
}				kc_Gobelin_vtable;

typedef struct		kc_Gobelin_metadata
{
  char			*name;
  char			*inheritance_list;
  kc_Gobelin_vtable	vtable;
}			kc_Gobelin_metadata;

typedef struct		kc_Gobelin_interface
{
  kc_Gobelin_metadata	*meta;
  kc_Gobelin_instance	instance;
}			kc_Gobelin_interface;

void	A_BEG_n_T_7_Gobelin_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_CLASS_7_Gobelin_12_Gobelin_init(Gobelin *self);
void	V_A_BEG_n_T_7_Gobelin_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_CLASS_7_Gobelin_13_Gobelin_clean(Gobelin *self);
void	V_A_BEG_n_T_7_Gobelin_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_CLASS_7_Gobelin_13_Gobelin_magie(Gobelin *self);

#endif
