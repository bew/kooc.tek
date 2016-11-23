NAME =		simple_module

SRCS =\
      ./main_simple.kc \
      ./simple.kc \
      ./simple.kh \

all: $(NAME)

$(NAME): $(SRCS)
	kooc $^
	gcc -o $(NAME) *.c

clean:
	rm -f ./main_simple.c ./simple.c ./simple.h

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
