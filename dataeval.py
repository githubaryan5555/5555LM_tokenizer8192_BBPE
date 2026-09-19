
from collections import Counter
import string
from datasets import load_dataset

# 1. Stream and collect up to 20MB of English text from FineWeb
dataset = load_dataset(
    "HuggingFaceFW/fineweb", 
    name="default", 
    split="train", 
    streaming=True
)

target_size_bytes = 20 * 1024 * 1024  # 20 MB
current_size_bytes = 0
collected_texts = []

print("Streaming and filtering FineWeb dataset...")

for row in dataset:
    if row.get("language") == "en":
        text_content = row.get("text", "")
        text_bytes = text_content.encode("utf-8")
        text_size = len(text_bytes)
        
        if current_size_bytes + text_size > target_size_bytes:
            remaining_bytes = target_size_bytes - current_size_bytes
            truncated_text = text_bytes[:remaining_bytes].decode("utf-8", errors="ignore")
            collected_texts.append(truncated_text)
            current_size_bytes += len(truncated_text.encode("utf-8"))
            break
            
        collected_texts.append(text_content)
        current_size_bytes += text_size

# Combine all chunks into a single master string for evaluation
full_text = "".join(collected_texts)

# 2. Perform Detailed Evaluation Calculations
file_size_bytes = len(full_text.encode("utf-8"))
file_size_mb = file_size_bytes / (1024 * 1024)

# Words breakdown
words = full_text.split()
total_words = len(words)
unique_words = set(w.lower() for w in words)

# Characters breakdown
total_chars = len(full_text)
char_counts = Counter(full_text)

# Non-alphanumeric breakdown
non_alpha_num_chars = [c for c in full_text if not c.isalnum() and not c.isspace()]
non_alpha_num_counts = Counter(non_alpha_num_chars)
unique_non_alpha_num = set(non_alpha_num_chars)

# 3. Print out the Comprehensive Evaluation Report
print("\n" + "="*40)
print("       FINEWEB EVALUATION REPORT        ")
print("="*40)
print(f"📦 Total File Size     : {file_size_bytes} bytes ({file_size_mb:.2f} MB)")
print(f"📝 Total Characters    : {total_chars:,}")
print(f"🔤 Unique Characters   : {len(char_counts):,}")
print(f"📖 Total Words         : {total_words:,}")
print(f"📘 Unique Words        : {len(unique_words):,}")
print(f"符号 Total Non-Alnum   : {len(non_alpha_num_chars):,}")
print(f"🔑 Unique Non-Alnum    : {len(unique_non_alpha_num)}")
print("-" * 40)

print("\n--- Top 10 Most Common Non-Alphanumeric Characters ---")
for char, count in non_alpha_num_counts.most_common(10):
    print(f"'{char}' : {count:,} occurrences")

print("\n--- First text sample snippet ---")
if collected_texts:
    print(collected_texts[0][:300] + "...")
