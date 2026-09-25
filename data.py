
from datasets import load_dataset

# Stream the dataset without downloading it fully upfront
dataset = load_dataset(
    "HuggingFaceFW/fineweb", 
    name="default", 
    split="train", 
    streaming=True
)

target_size_bytes = 2000 * 1024 * 1024  # 20 MB
current_size_bytes = 0
collected_texts = []

print("Streaming and filtering FineWeb dataset...")

for row in dataset:
    # Check if the row language is English
    if row.get("language") == "en":
        text_content = row.get("text", "")
        
        # Calculate the size of the text string in bytes (UTF-8 encoding)
        text_bytes = text_content.encode("utf-8")
        text_size = len(text_bytes)
        
        if current_size_bytes + text_size > target_size_bytes:
            # Optional: slice the last text to fit precisely into 20MB if needed
            remaining_bytes = target_size_bytes - current_size_bytes
            truncated_text = text_bytes[:remaining_bytes].decode("utf-8", errors="ignore")
            collected_texts.append(truncated_text)
            current_size_bytes += len(truncated_text.encode("utf-8"))
            break
            
        collected_texts.append(text_content)
        current_size_bytes += text_size

print(f"Finished! Collected {len(collected_texts)} rows.")
print(f"Total size: {current_size_bytes / (1024 * 1024):.2f} MB")

# Example: Print the first text snippet
if collected_texts:
    print("\n--- First text sample ---")
    print(collected_texts[0][:500] + "...")
