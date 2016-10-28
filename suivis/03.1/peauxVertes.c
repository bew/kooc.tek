#include "peauxVertes.h"

kc_PeauxVertes_metadata	PeauxVertes_metadata =
  {
    "PeauxVertes",
    "",
    {
      &V_A_BEG_n_W_X_BEG_p__BEG_t_BEG_n_T_11_PeauxVertes_BEG_p__BEG_o___END_END_END_BEG_o___END_END_END_END_CLASS_11_PeauxVertes_7_attaque,
      &V_A_BEG_n_W_X_BEG_p__BEG_t_BEG_n_T_11_PeauxVertes_BEG_p__BEG_o___END_END_END_BEG_o___END_END_END_END_CLASS_11_PeauxVertes_5_clean,
      &V_A_BEG_n_W_X_BEG_p__BEG_t_BEG_n_T_11_PeauxVertes_BEG_p__BEG_o___END_END_END_BEG_o___END_END_END_END_CLASS_11_PeauxVertes_5_magie,
    }
  };

kc_Orque_metadata	Orque_metadata =
  {
    "Orque",
    "PeauxVertes",
    {
      &V_A_BEG_n_W_X_BEG_p__BEG_t_BEG_n_T_5_Orque_BEG_p__BEG_o___END_END_END_BEG_o___END_END_END_END_CLASS_5_Orque_7_attaque,
      &V_A_BEG_n_W_X_BEG_p__BEG_t_BEG_n_T_5_Orque_BEG_p__BEG_o___END_END_END_BEG_o___END_END_END_END_CLASS_5_Orque_5_clean,
      &V_A_BEG_n_W_X_BEG_p__BEG_t_BEG_n_T_5_Orque_BEG_p__BEG_o___END_END_END_BEG_o___END_END_END_END_CLASS_5_Orque_5_magie,
    }
  };

kc_Gobelin_metadata	Gobelin_metadata =
  {
    "Gobelin",
    "PeauxVertes",
    {
      &V_A_BEG_n_W_X_BEG_p__BEG_t_BEG_n_T_11_PeauxVertes_BEG_p__BEG_o___END_END_END_BEG_o___END_END_END_END_CLASS_11_PeauxVertes_7_attaque,
      &V_A_BEG_n_W_X_BEG_p__BEG_t_BEG_n_T_7_Gobelin_BEG_p__BEG_o___END_END_END_BEG_o___END_END_END_END_CLASS_7_Gobelin_5_clean,
      &V_A_BEG_n_W_X_BEG_p__BEG_t_BEG_n_T_7_Gobelin_BEG_p__BEG_o___END_END_END_BEG_o___END_END_END_END_CLASS_7_Gobelin_5_magie,
    }
  };


void	A_BEG_n_T_11_PeauxVertes_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_CLASS_11_PeauxVertes_16_PeauxVertes_init(kc_PeauxVertes_interface *obj)
{
  obj->instance.A_BEG_n_W_H_BEG_o___END_END_CLASS_11_PeauxVertes_14_PeauxVertes_pv = 0;
  obj->instance.A_BEG_n_W_H_BEG_o___END_END_CLASS_11_PeauxVertes_19_PeauxVertes_attaque = 0;
  obj->instance.A_BEG_n_W_H_BEG_o___END_END_CLASS_11_PeauxVertes_19_PeauxVertes_agilite = 0;
}
void	V_A_BEG_n_T_11_PeauxVertes_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_CLASS_11_PeauxVertes_17_PeauxVertes_clean() {}

void	V_A_BEG_n_T_11_PeauxVertes_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_CLASS_11_PeauxVertes_19_PeauxVertes_attaque()
{
  puts("Le peau-verte attaque !");
};

void	V_A_BEG_n_T_11_PeauxVertes_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_CLASS_11_PeauxVertes_17_PeauxVertes_magie()
{
  puts("Le peau-verte lance un sort !");
};



void	V_A_BEG_n_W_X_BEG_p__BEG_t_BEG_n_T_11_PeauxVertes_BEG_p__BEG_o___END_END_END_BEG_o___END_END_END_END_CLASS_11_PeauxVertes_5_clean(kc_Orque_interface *obj)
{
  obj->instance.A_BEG_n_W_H_BEG_o___END_END_CLASS_11_PeauxVertes_14_PeauxVertes_pv = 16;
  obj->instance.A_BEG_n_W_H_BEG_o___END_END_CLASS_11_PeauxVertes_19_PeauxVertes_attaque = 15;
  obj->instance.A_BEG_n_W_H_BEG_o___END_END_CLASS_11_PeauxVertes_19_PeauxVertes_agilite = 8;
}
void	V_A_BEG_n_T_5_Orque_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_CLASS_5_Orque_11_Orque_clean(kc_Orque_interface *obj);
void	V_A_BEG_n_T_5_Orque_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_CLASS_5_Orque_13_Orque_attaque(kc_Orque_interface *obj)
{
  puts("L'orque attaque avec une massue !");
}
void	V_A_BEG_n_T_5_Orque_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_CLASS_5_Orque_11_Orque_magie(kc_Orque_interface *obj)
{
  puts("L'orque fait un rituel chamanique !");
}


void	A_BEG_n_T_7_Gobelin_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_CLASS_7_Gobelin_12_Gobelin_init(kc_Gobelin_interface *obj)
{
  obj->instance.A_BEG_n_W_H_BEG_o___END_END_CLASS_11_PeauxVertes_14_PeauxVertes_pv = 10;
  obj->instance.A_BEG_n_W_H_BEG_o___END_END_CLASS_11_PeauxVertes_19_PeauxVertes_attaque = 9;
  obj->instance.A_BEG_n_W_H_BEG_o___END_END_CLASS_11_PeauxVertes_19_PeauxVertes_agilite = 18;
  obj->instance.A_BEG_n_W_H_BEG_o___END_END_CLASS_7_Gobelin_17_Gobelin_Parchemin = 3;
}

void	V_A_BEG_n_T_7_Gobelin_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_CLASS_7_Gobelin_13_Gobelin_clean(){}

void	V_A_BEG_n_T_7_Gobelin_BEG_p__BEG_o___END_END_END_BEG_f_W_X_BEG_o___END_END_CLASS_7_Gobelin_13_Gobelin_magie(kc_Gobelin_interface *obj);
{
  if (obj->instance.A_BEG_n_W_H_BEG_o___END_END_CLASS_7_Gobelin_17_Gobelin_Parchemin > 0)
    {
      puts("Le gobelin jette une boule de feu !");
      obj->instance.->A_BEG_n_W_H_BEG_o___END_END_CLASS_7_Gobelin_17_Gobelin_Parchemin -= 1;
    }
  else
    puts("Plus de parchemins !");
}
