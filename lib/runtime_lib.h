
#ifndef _KOOC_RUNTIME_LIB_
# define _KOOC_RUNTIME_LIB_

# define CLASS_NAME(o) (*((char**)(o)))
# define INHERITANCE_LIST(o) (*((char**)(o + sizeof(char*))))

char	**my_str_to_wordtab(char *str, char *separators);

#endif
