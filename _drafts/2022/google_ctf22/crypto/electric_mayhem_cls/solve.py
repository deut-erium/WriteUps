import json
import os
# with open("traces.json") as f:
#     traces = json.load(f)

# cts = [i['ct'] for i in traces]
# pts = [i['pt'] for i in traces]
# pms = [i['pm'] for i in traces]


main_template = """\
#include <stdio.h>
#include <stdlib.h>
#include "aes.h"
#include "elmoasmfunctionsdef.h"
static uint32_t N = 1;
static uint8_t key[16] = {key};
static uint8_t in[16] = {{}};
int main() {{
  // Read #traces.
  LoadN(&N);
  struct AES_ctx ctx;
  AES_init_ctx(&ctx, key);
  for (uint32_t i = 0; i < N; i++) {{
    for (uint32_t j = 0; j < sizeof(in); j++) {{
      randbyte(&in[j]);
    }}
    starttrigger();
    AES_ECB_encrypt(&ctx, in);
    endtrigger();
    for (uint32_t j = 0; j < sizeof(in); j++) {{
      printbyte(&in[j]);
    }}
  }}
  endprogram();
  return 0;
}}"""


def read_trace(path):
    with open(path) as f:
        data = list(map(float,f.read().strip().split()))
    return data

def get_traces(key:bytes,ntrace=50):
    key_init = "{"+", ".join(map(str,list(key)))+"}"
    new_main = main_template.format(key=key_init)
    with open("firmware/main.c","w") as f:
        f.write(new_main)
    os.chdir("firmware")
    os.system("make clean;make all")
    os.chdir("../elmo")
    os.system("./elmo ../firmware/firmware.bin -Ntrace "+str(ntrace))
    os.chdir("output/traces")
    all_traces = [read_trace(i) for i in os.listdir()]
    os.chdir('../../../')
    return all_traces



