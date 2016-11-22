NAME =		libkrt.so

CFLAGS =	-Wall -Werror -Wextra -fPIC -I.

LDFLAGS =	-shared

SRCS =\
      ./runtime_kooc.c	\
      ./str_to_wordtab.c	\

OBJS = $(SRCS:.c=.o)

all: $(NAME)

$(NAME): $(OBJS)
	gcc -o $@ $(LDFLAGS) $^

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
