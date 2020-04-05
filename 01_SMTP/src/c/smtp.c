#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>
#include <curl/curl.h>

typedef struct cfg {
  char *server;
  char *from_address;
  char *to_address;
  char *message;
} cfg_t;

// I used https://curl.haxx.se/libcurl/c/smtp-mail.html as reference

struct upload_status {
  int lines_read;
};

static char *payload_text[];
 
static size_t payload_source(void *ptr, size_t size, size_t nmemb, void *userp)
{
  struct upload_status *upload_ctx = (struct upload_status *)userp;
  const char *data;
 
  if((size == 0) || (nmemb == 0) || ((size*nmemb) < 1)) {
    return 0;
  }
 
  // this isn't going to work, we need to make an array of strings where the elements
  // match the headers on a SMPT message payload, using the different parts of the cfg 
  // struct where relevant. 
  data = cfg.message;
 
  if(data) {
    size_t len = strlen(data);
    memcpy(ptr, data, len);
    upload_ctx->lines_read++;
 
    return len;
  }
 
  return 0;
}


/* 
 * Entry function for sending mail via SMTP.
 * The input argument is a configuration structure
 * with the necessary data to form an email message
 * and send it to a specific server.
*/
void send_mail(cfg_t *cfg) {
  printf("Arguments: %s %s %s %s\n", cfg->server, cfg->from_address, cfg->to_address, cfg->message);
  CURL *curl = curl_easy_init();
  CURLcode res = CURLE_OK;
  struct curl_slist *recipient = NULL;
  struct upload_status upload_ctx;
  upload_ctx.lines_read = 0;

  if (curl) {
    curl_easy_setopt(curl, CURLOPT_URL, cfg.server);
    curl_easy_setopt(curl, CURLOPT_MAIL_FROM, cfg.from_address);
    recipient = curl_slist_append(recipient, cfg.to_address);
    curl_easy_setopt(curl,  CURLOPT_MAIL_RCPT, recipient);
    curl_easy_setopt(curl, CURLOPT_READFUNCTION, payload_source);
    curl_easy_setopt(curl, CURLOPT_READDATA, &upload_ctx);
    curl_easy_setopt(curl, CURLOPT_UPLOAD, 1L);
    
    res = curl_easy_perform(curl);

    if(res != CURLE_OK)
      printf("curl_easy_perform() failed: %s\n", curl_easy_strerror(res)); 
  
    curl_slist_free_all(recipient);
    curl_easy_cleanup(curl);
  }
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
    fprintf(stderr, "Usage: %s <server> <from> <to> <message>\n", argv[0]);
    exit(1);
  }

  cfg.server = strdup(argv[1]);
  cfg.from_address = strdup(argv[2]);
  cfg.to_address = strdup(argv[3]);
  cfg.message = strdup(argv[4]);
  
  payload_text = malloc(5);	

  send_mail(&cfg);

  return 0;
}
