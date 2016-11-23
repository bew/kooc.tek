#include "runtime_lib.h"
#include <stdlib.h>
#include <string.h>

int		check_inheritance_list(const char *class_name, void *object)
{
    char	**kinds = my_str_to_wordtab(INHERITANCE_LIST(object), " ");
    int		ans = 0;
    int		i = 0;

    if (!strcmp(CLASS_NAME(object), class_name))
	ans = 1;
    else
	while (kinds[i] != NULL) {
	    if (!strcmp(kinds[i], class_name)) {
		ans = 42;
		break;
	    }
	    ++i;
	}
    free(kinds);
    return ans;
}

int		isKindOfStr(void *object, const char *class_name)
{
    return check_inheritance_list(class_name, object);
}


int		isKindOf(void *object, void *other)
{
    return check_inheritance_list(CLASS_NAME(other), object);
}


int		isInstanceOfStr(void *object, const char *class_name)
{
    return !!strcmp(CLASS_NAME(object), class_name);
}


int		isInstanceOf(void *object, void *other)
{
    return !!strcmp(CLASS_NAME(object), CLASS_NAME(other));
}
