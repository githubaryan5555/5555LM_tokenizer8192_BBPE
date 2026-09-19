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
