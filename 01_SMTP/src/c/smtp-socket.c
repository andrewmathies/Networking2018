#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define SEPARATOR "\n\r"

typedef struct cfg {
  char *server;
  char *from_address;
  char *to_address;
  char *message;
} cfg_t;

struct addrinfo hints, *infoptr;

/* 
 *  * Entry function for sending mail via SMTP.
 *   * The input argument is a configuration structure
 *    * with the necessary data to form an email message
 *     * and send it to a specific server.
 *     */
void send_mail(cfg_t *cfg) {
  printf("Arguments: %s %s %s %s\n", cfg->server, cfg->from_address, cfg->to_address, cfg->message);
  char *port = "25";

  hints.ai_family = AF_INET;
  hints.ai_socktype = SOCK_STREAM;
  hints.ai_protocol = IPPROTO_TCP;

  int retval = getaddrinfo(cfg->server, port, &hints, &infoptr);
  if (retval) {
      fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(retval));
      exit(1);
  }

  printf("got addresses!\n");

  struct addrinfo *p;
  char host[256];
  int sock;

  for (p = infoptr; p != NULL; p = p->ai_next) {
      struct sockaddr_in* saddr = (struct sockaddr_in*)p->ai_addr;
      printf("address: %s\n", inet_ntoa(saddr->sin_addr));
      sock = socket(p->ai_family, p->ai_socktype, p->ai_protocol);
      
      if (sock < 0) {
	 fprintf(stderr, "couldn't create socket\n");
         continue;
      }

      printf("created socket!\n"); 

      if(connect(sock, p->ai_addr, p->ai_addrlen) < 0) {
         fprintf(stderr, "failed to connect\n");
         continue;
      }

      printf("connected\n");
      
      char buffer[256];
      memset(buffer, 0, 256);
      read(sock, buffer, 256);
      
      printf("recieved data: %s\n", buffer);

      close();
  }

  freeaddrinfo(infoptr);
}

int main(int argc, char **argv) {
  int c;
  
  cfg_t cfg = {
    .server = NULL,
    .from_address = NULL,
    .to_address = NULL,
    .message = NULL
  };
  
  if (argc < 5) {
    fprintf(stderr,
	    "Usage: %s <server> <from> <to> <message>\n",
	    argv[0]);
    exit(1);
  }

  cfg.server = strdup(argv[1]);
  cfg.from_address = strdup(argv[2]);
  cfg.to_address = strdup(argv[3]);
  cfg.message = strdup(argv[4]);
  
  send_mail(&cfg);

  return 0;
}
