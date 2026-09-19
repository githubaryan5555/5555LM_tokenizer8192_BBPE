# 5555LM_tokenizer8192_BBPE
data.py
 Resolving data files: 100% 27468/27468 [00:03<00:00, 4983.25it/s]Resolving data files: 100% 27468/27468 [00:03<00:00, 12746.52it/s]Streaming and filtering FineWeb dataset...
Finished! Collected 7060 rows.
Total size: 20.00 MB
--- First text sample ---
How AP reported in all formats from tornado-stricken regionsMarch 8, 2012
When the first serious bout of tornadoes of 2012 blew through middle America in the middle of the night, they touched down in places hours from any AP bureau. Our closest video journalist was Chicago-based Robert Ray, who dropped his plans to travel to Georgia for Super Tuesday, booked several flights to the cities closest to the strikes and headed for the airport. He’d decide once there which flight to take.
He never got ...

dataeval. py

 Resolving data files: 100% 27468/27468 [00:01<00:00, 17720.70it/s]Resolving data files: 100% 27468/27468 [00:01<00:00, 18079.23it/s]Streaming and filtering FineWeb dataset...

========================================
       FINEWEB EVALUATION REPORT        
========================================
📦 Total File Size     : 20971520 bytes (20.00 MB)
📝 Total Characters    : 20,864,980
🔤 Unique Characters   : 872
📖 Total Words         : 3,517,810
📘 Unique Words        : 247,038
符号 Total Non-Alnum   : 692,300
🔑 Unique Non-Alnum    : 136
----------------------------------------

--- Top 10 Most Common Non-Alphanumeric Characters ---
'.' : 208,660 occurrences
',' : 189,562 occurrences
'-' : 57,784 occurrences
''' : 33,718 occurrences
'’' : 23,419 occurrences
'"' : 23,098 occurrences
':' : 22,672 occurrences
')' : 21,352 occurrences
'(' : 20,589 occurrences
'?' : 9,799 occurrences

--- First text sample snippet ---
How AP reported in all formats from tornado-stricken regionsMarch 8, 2012
When the first serious bout of tornadoes of 2012 blew through middle America in the middle of the night, they touched down in places hours from any AP bureau. Our closest video journalist was Chicago-based Robert Ray, who drop...

train_tokenizer.py

============================================================
8192-VOCAB BYTE-LEVEL BPE TRAINER
============================================================
Input file : fineweb_sample.txt
Target vocab : 8192

Vocabulary layout:
  0..255      = 256 byte tokens
  256         = [-UNK-]
  257         = [-BOS-]
  258         = [-EOS-]
  259..8191   = learned BPE tokens

Training split:
  /tmp/bbpe_jwu_wmol/train.txt

Evaluation split:
  /tmp/bbpe_jwu_wmol/eval.txt

Training BPE...

============================================================
TOKENIZER EVALUATION
============================================================
Evaluation characters : 2,087,942
Evaluation bytes      : 2,097,143
Generated tokens      : 563,286
Bytes / token         : 3.7231
Characters / token    : 3.7067
UNK tokens            : 0
UNK rate              : 0.000000%

Special-token counts:
  [-UNK-] : 0
  [-BOS-] : 0
  [-EOS-] : 0

Round-trip decode     : PASS

Byte-ID check:
  IDs 0..255 present  : PASS

Special-ID check:
  256..258 correct    : PASS

Sample encoding:
TEXT:
'ystem language in a\n> format that even starts with the first 2 characters matching a locale\n> in SWORD, this code would allow you to just pass that directly to\n> SWORD without matching a SWORD locale '

TOKENS:
['y', 'stem', 'Ġlanguage', 'Ġin', 'Ġa', 'Ċ', '>', 'Ġformat', 'Ġthat', 'Ġeven', 'Ġstarts', 'Ġwith', 'Ġthe', 'Ġfirst', 'Ġ2', 'Ġcharacters', 'Ġmatch', 'ing', 'Ġa', 'Ġloc', 'ale', 'Ċ', '>', 'Ġin', 'ĠS', 'W', 'OR', 'D', ',', 'Ġthis', 'Ġcode', 'Ġwould', 'Ġallow', 'Ġyou', 'Ġto', 'Ġjust', 'Ġpass', 'Ġthat', 'Ġdirectly', 'Ġto', 'Ċ', '>', 'ĠS', 'W', 'OR', 'D', 'Ġwithout', 'Ġmatch', 'ing', 'Ġa', 'ĠS', 'W', 'OR', 'D', 'Ġloc', 'ale', 'Ġprec', 'ise', 'ly', '.', 'Ċ', 'What', 'ĠI', 'Ġsaid', 'Ġwasn', "'t", 'Ġquite', 'Ġright', '.', 'Ċ', 'We', 'Ġset', 'Ġa', 'Ġcustom', 'Ġloc', 'ale', 'Ġd', 'ir', 'Ġwith', 'ĠL']

IDS:
[88, 965, 2756, 291, 260, 198, 29, 5566, 330, 808, 5227, 349, 265, 680, 383, 4296, 3446, 281, 260, 1053, 973, 198, 29, 291, 318, 54, 1936, 35, 11, 414, 2905, 585, 1298, 334, 285, 616, 1142, 330, 3421, 285, 198, 29, 318, 54, 1936, 35, 1266, 3446, 281, 260, 318, 54, 1936, 35, 1053, 973, 4206, 798, 312, 13, 198, 1773, 306, 634, 2528, 609, 2121, 927, 13, 198, 1055, 959, 260, 1585, 1053, 973, 292, 348, 349, 410]
============================================================

FINAL CHECKS
============================================================
Vocabulary size : 8192
Byte IDs        : 0..255
UNK ID          : 256
BOS ID          : 257
EOS ID          : 258
Learned IDs     : 259..8191

Created: tokenizer.json
Created: tokenizer_config.json

Tokenizer training completed successfully.


tokenizer_eval.py

Loaded: tokenizer.json
Vocabulary size: 8192
Vocabulary checks: PASS

======================================================================
INTERACTIVE TOKENIZER EVALUATION
======================================================================
Type text and press Enter.
Type :q to quit.

TEXT > wolf

----------------------------------------------------------------------
ORIGINAL:
'wolf'

TOKEN IDS:
[86, 4311]

TOKENS:
   0 | ID   86 | 'w'
   1 | ID 4311 | 'olf'

DECODED:
'wolf'

ROUND TRIP: PASS ✅
----------------------------------------------------------------------

TEXT > Cat 🔥🔥🔥🗣️🗣️🗣️

----------------------------------------------------------------------
ORIGINAL:
'Cat 🔥🔥🔥🗣️🗣️🗣️'

TOKEN IDS:
[34, 269, 220, 172, 253, 242, 98, 172, 253, 242, 98, 172, 253, 242, 98, 172, 253, 245, 96, 171, 116, 237, 172, 253, 245, 96, 171, 116, 237, 172, 253, 245, 96, 171, 116, 237]

TOKENS:
   0 | ID   34 | 'C'
   1 | ID  269 | 'at'
   2 | ID  220 | 'Ġ'
   3 | ID  172 | 'ð'
   4 | ID  253 | 'Ł'
   5 | ID  242 | 'Ķ'
   6 | ID   98 | '¥'
   7 | ID  172 | 'ð'
   8 | ID  253 | 'Ł'
   9 | ID  242 | 'Ķ'
  10 | ID   98 | '¥'
  11 | ID  172 | 'ð'
  12 | ID  253 | 'Ł'
  13 | ID  242 | 'Ķ'
  14 | ID   98 | '¥'
  15 | ID  172 | 'ð'
  16 | ID  253 | 'Ł'
  17 | ID  245 | 'Ĺ'
  18 | ID   96 | '£'
  19 | ID  171 | 'ï'
  20 | ID  116 | '¸'
  21 | ID  237 | 'ı'
  22 | ID  172 | 'ð'
  23 | ID  253 | 'Ł'
  24 | ID  245 | 'Ĺ'
  25 | ID   96 | '£'
  26 | ID  171 | 'ï'
  27 | ID  116 | '¸'
  28 | ID  237 | 'ı'
  29 | ID  172 | 'ð'
  30 | ID  253 | 'Ł'
  31 | ID  245 | 'Ĺ'
  32 | ID   96 | '£'
  33 | ID  171 | 'ï'
  34 | ID  116 | '¸'
  35 | ID  237 | 'ı'

DECODED:
'Cat 🔥🔥🔥🗣️🗣️🗣️'

ROUND TRIP: PASS ✅
----------------------------------------------------------------------

TEXT > Ġood

----------------------------------------------------------------------
ORIGINAL:
'Ġood'

TOKEN IDS:
[128, 254, 513]

TOKENS:
   0 | ID  128 | 'Ä'
   1 | ID  254 | 'ł'
   2 | ID  513 | 'ood'

DECODED:
'Ġood'

ROUND TRIP: PASS ✅
----------------------------------------------------------------------

TEXT > 🎺🎺👀👀👀🌷💐🌸🌹🌸💐🌷💐🌷💐🌸💮🌹💮🌹💮🌹🌿🌼🌾🌿🌼🏵️☘️🌿☘️⛄⛰️☃️☃️🏞️⛄🏜️🌳🪨🌱🌥️☁️🌚🌚EEEEEĠood

----------------------------------------------------------------------
ORIGINAL:
'🎺🎺👀👀👀🌷💐🌸🌹🌸💐🌷💐🌷💐🌸💮🌹💮🌹💮🌹🌿🌼🌾🌿🌼🏵️☘️🌿☘️⛄⛰️☃️☃️🏞️⛄🏜️🌳🪨🌱🌥️☁️🌚🌚EEEEEĠood'

TOKEN IDS:
[172, 253, 236, 118, 172, 253, 236, 118, 172, 253, 239, 222, 172, 253, 239, 222, 172, 253, 239, 222, 172, 253, 234, 115, 172, 253, 240, 238, 172, 253, 234, 116, 172, 253, 234, 117, 172, 253, 234, 116, 172, 253, 240, 238, 172, 253, 234, 115, 172, 253, 240, 238, 172, 253, 234, 115, 172, 253, 240, 238, 172, 253, 234, 116, 172, 253, 240, 106, 172, 253, 234, 117, 172, 253, 240, 106, 172, 253, 234, 117, 172, 253, 240, 106, 172, 253, 234, 117, 172, 253, 234, 123, 172, 253, 234, 120, 172, 253, 234, 122, 172, 253, 234, 123, 172, 253, 234, 120, 172, 253, 237, 113, 171, 116, 237, 158, 246, 246, 171, 116, 237, 172, 253, 234, 123, 158, 246, 246, 171, 116, 237, 158, 249, 226, 158, 249, 108, 171, 116, 237, 158, 246, 225, 171, 116, 237, 158, 246, 225, 171, 116, 237, 172, 253, 237, 252, 171, 116, 237, 158, 249, 226, 172, 253, 237, 250, 171, 116, 237, 172, 253, 234, 111, 172, 253, 103, 101, 172, 253, 234, 109, 172, 253, 234, 98, 171, 116, 237, 158, 246, 223, 171, 116, 237, 172, 253, 234, 248, 172, 253, 234, 248, 6058, 6058, 36, 128, 254, 513]

TOKENS:
   0 | ID  172 | 'ð'
   1 | ID  253 | 'Ł'
   2 | ID  236 | 'İ'
   3 | ID  118 | 'º'
   4 | ID  172 | 'ð'
   5 | ID  253 | 'Ł'
   6 | ID  236 | 'İ'
   7 | ID  118 | 'º'
   8 | ID  172 | 'ð'
   9 | ID  253 | 'Ł'
  10 | ID  239 | 'ĳ'
  11 | ID  222 | 'Ģ'
  12 | ID  172 | 'ð'
  13 | ID  253 | 'Ł'
  14 | ID  239 | 'ĳ'
  15 | ID  222 | 'Ģ'
  16 | ID  172 | 'ð'
  17 | ID  253 | 'Ł'
  18 | ID  239 | 'ĳ'
  19 | ID  222 | 'Ģ'
  20 | ID  172 | 'ð'
  21 | ID  253 | 'Ł'
  22 | ID  234 | 'Į'
  23 | ID  115 | '·'
  24 | ID  172 | 'ð'
  25 | ID  253 | 'Ł'
  26 | ID  240 | 'Ĵ'
  27 | ID  238 | 'Ĳ'
  28 | ID  172 | 'ð'
  29 | ID  253 | 'Ł'
  30 | ID  234 | 'Į'
  31 | ID  116 | '¸'
  32 | ID  172 | 'ð'
  33 | ID  253 | 'Ł'
  34 | ID  234 | 'Į'
  35 | ID  117 | '¹'
  36 | ID  172 | 'ð'
  37 | ID  253 | 'Ł'
  38 | ID  234 | 'Į'
  39 | ID  116 | '¸'
  40 | ID  172 | 'ð'
  41 | ID  253 | 'Ł'
  42 | ID  240 | 'Ĵ'
  43 | ID  238 | 'Ĳ'
  44 | ID  172 | 'ð'
  45 | ID  253 | 'Ł'
  46 | ID  234 | 'Į'
  47 | ID  115 | '·'
  48 | ID  172 | 'ð'
  49 | ID  253 | 'Ł'
  50 | ID  240 | 'Ĵ'
  51 | ID  238 | 'Ĳ'
  52 | ID  172 | 'ð'
  53 | ID  253 | 'Ł'
  54 | ID  234 | 'Į'
  55 | ID  115 | '·'
  56 | ID  172 | 'ð'
  57 | ID  253 | 'Ł'
  58 | ID  240 | 'Ĵ'
  59 | ID  238 | 'Ĳ'
  60 | ID  172 | 'ð'
  61 | ID  253 | 'Ł'
  62 | ID  234 | 'Į'
  63 | ID  116 | '¸'
  64 | ID  172 | 'ð'
  65 | ID  253 | 'Ł'
  66 | ID  240 | 'Ĵ'
  67 | ID  106 | '®'
  68 | ID  172 | 'ð'
  69 | ID  253 | 'Ł'
  70 | ID  234 | 'Į'
  71 | ID  117 | '¹'
  72 | ID  172 | 'ð'
  73 | ID  253 | 'Ł'
  74 | ID  240 | 'Ĵ'
  75 | ID  106 | '®'
  76 | ID  172 | 'ð'
  77 | ID  253 | 'Ł'
  78 | ID  234 | 'Į'
  79 | ID  117 | '¹'
  80 | ID  172 | 'ð'
  81 | ID  253 | 'Ł'
  82 | ID  240 | 'Ĵ'
  83 | ID  106 | '®'
  84 | ID  172 | 'ð'
  85 | ID  253 | 'Ł'
  86 | ID  234 | 'Į'
  87 | ID  117 | '¹'
  88 | ID  172 | 'ð'
  89 | ID  253 | 'Ł'
  90 | ID  234 | 'Į'
  91 | ID  123 | '¿'
  92 | ID  172 | 'ð'
  93 | ID  253 | 'Ł'
  94 | ID  234 | 'Į'
  95 | ID  120 | '¼'
  96 | ID  172 | 'ð'
  97 | ID  253 | 'Ł'
  98 | ID  234 | 'Į'
  99 | ID  122 | '¾'
 100 | ID  172 | 'ð'
 101 | ID  253 | 'Ł'
 102 | ID  234 | 'Į'
 103 | ID  123 | '¿'
 104 | ID  172 | 'ð'
 105 | ID  253 | 'Ł'
 106 | ID  234 | 'Į'
 107 | ID  120 | '¼'
 108 | ID  172 | 'ð'
 109 | ID  253 | 'Ł'
 110 | ID  237 | 'ı'
 111 | ID  113 | 'µ'
 112 | ID  171 | 'ï'
 113 | ID  116 | '¸'
 114 | ID  237 | 'ı'
 115 | ID  158 | 'â'
 116 | ID  246 | 'ĺ'
 117 | ID  246 | 'ĺ'
 118 | ID  171 | 'ï'
 119 | ID  116 | '¸'
 120 | ID  237 | 'ı'
 121 | ID  172 | 'ð'
 122 | ID  253 | 'Ł'
 123 | ID  234 | 'Į'
 124 | ID  123 | '¿'
 125 | ID  158 | 'â'
 126 | ID  246 | 'ĺ'
 127 | ID  246 | 'ĺ'
 128 | ID  171 | 'ï'
 129 | ID  116 | '¸'
 130 | ID  237 | 'ı'
 131 | ID  158 | 'â'
 132 | ID  249 | 'Ľ'
 133 | ID  226 | 'Ħ'
 134 | ID  158 | 'â'
 135 | ID  249 | 'Ľ'
 136 | ID  108 | '°'
 137 | ID  171 | 'ï'
 138 | ID  116 | '¸'
 139 | ID  237 | 'ı'
 140 | ID  158 | 'â'
 141 | ID  246 | 'ĺ'
 142 | ID  225 | 'ĥ'
 143 | ID  171 | 'ï'
 144 | ID  116 | '¸'
 145 | ID  237 | 'ı'
 146 | ID  158 | 'â'
 147 | ID  246 | 'ĺ'
 148 | ID  225 | 'ĥ'
 149 | ID  171 | 'ï'
 150 | ID  116 | '¸'
 151 | ID  237 | 'ı'
 152 | ID  172 | 'ð'
 153 | ID  253 | 'Ł'
 154 | ID  237 | 'ı'
 155 | ID  252 | 'ŀ'
 156 | ID  171 | 'ï'
 157 | ID  116 | '¸'
 158 | ID  237 | 'ı'
 159 | ID  158 | 'â'
 160 | ID  249 | 'Ľ'
 161 | ID  226 | 'Ħ'
 162 | ID  172 | 'ð'
 163 | ID  253 | 'Ł'
 164 | ID  237 | 'ı'
 165 | ID  250 | 'ľ'
 166 | ID  171 | 'ï'
 167 | ID  116 | '¸'
 168 | ID  237 | 'ı'
 169 | ID  172 | 'ð'
 170 | ID  253 | 'Ł'
 171 | ID  234 | 'Į'
 172 | ID  111 | '³'
 173 | ID  172 | 'ð'
 174 | ID  253 | 'Ł'
 175 | ID  103 | 'ª'
 176 | ID  101 | '¨'
 177 | ID  172 | 'ð'
 178 | ID  253 | 'Ł'
 179 | ID  234 | 'Į'
 180 | ID  109 | '±'
 181 | ID  172 | 'ð'
 182 | ID  253 | 'Ł'
 183 | ID  234 | 'Į'
 184 | ID   98 | '¥'
 185 | ID  171 | 'ï'
 186 | ID  116 | '¸'
 187 | ID  237 | 'ı'
 188 | ID  158 | 'â'
 189 | ID  246 | 'ĺ'
 190 | ID  223 | 'ģ'
 191 | ID  171 | 'ï'
 192 | ID  116 | '¸'
 193 | ID  237 | 'ı'
 194 | ID  172 | 'ð'
 195 | ID  253 | 'Ł'
 196 | ID  234 | 'Į'
 197 | ID  248 | 'ļ'
 198 | ID  172 | 'ð'
 199 | ID  253 | 'Ł'
 200 | ID  234 | 'Į'
 201 | ID  248 | 'ļ'
 202 | ID 6058 | 'EE'
 203 | ID 6058 | 'EE'
 204 | ID   36 | 'E'
 205 | ID  128 | 'Ä'
 206 | ID  254 | 'ł'
 207 | ID  513 | 'ood'

DECODED:
'🎺🎺👀👀👀🌷💐🌸🌹🌸💐🌷💐🌷💐🌸💮🌹💮🌹💮🌹🌿🌼🌾🌿🌼🏵️☘️🌿☘️⛄⛰️☃️☃️🏞️⛄🏜️🌳🪨🌱🌥️☁️🌚🌚EEEEEĠood'

ROUND TRIP: PASS ✅
----------------------------------------------------------------------

