all: folders client server

all: folders server client

server: bin/server
client: bin/client

folders:
	@mkdir -p src obj bin tmp obj/server obj/client obj/utils

# SERVER

bin/server: obj/server/server.o obj/utils/utils.o obj/server/files.o obj/server/handler.o#obj/server/handler.o obj/server/task.o obj/server/db.o obj/server/escalonador.o obj/server/program.o
	gcc -g obj/utils/utils.o obj/server/server.o obj/server/files.o obj/server/handler.o -o bin/server

obj/server/server.o: src/server/server.c
	gcc -Wall -g -c src/server/server.c -o obj/server/server.o

obj/server/handler.o: src/server/handler.c
	gcc -Wall -g -c src/server/handler.c -o obj/server/handler.o

obj/server/files.o: src/server/files.c
	gcc -Wall -g -c src/server/files.c -o obj/server/files.o

# CLIENT

bin/client: obj/client/client.o obj/utils/utils.o
	gcc -g obj/client/client.o obj/utils/utils.o -o bin/client

obj/client/client.o: src/client/client.c
	gcc -Wall -g -c src/client/client.c -o obj/client/client.o

# UTILS

obj/utils/utils.o: src/utils/utils.c
	gcc -Wall -g -c src/utils/utils.c -o obj/utils/utils.o

clean:
	rm -f obj/server/* obj/client/* obj/utils/* tmp/* bin/*
	@rmdir bin obj/client obj/server obj/utils obj tmp