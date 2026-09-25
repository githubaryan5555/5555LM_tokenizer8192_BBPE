"""
Streaming dataset preparation for 5555LM.

Input:
    fineweb_sample.txt

Tokenizer:
    tokenizers/tokenizer.json

Output:
    data/train.bin
    data/val.bin
    data/dataset_config.json

Features:
    - 90/10 train/validation split
    - Streaming input
    - Bounded RAM usage
    - UTF-8 safe
    - uint16 token IDs
    - Works with very large datasets
    - Does NOT load the entire dataset into RAM
"""

import json
import struct
from pathlib import Path

from tokenizers import Tokenizer


# ============================================================
# CONFIG
# ============================================================

RAW_DATA = Path("fineweb_sample.txt")

TOKENIZER_FILE = Path("tokenizers/tokenizer.json")

OUTPUT_DIR = Path("data")

TRAIN_FILE = OUTPUT_DIR / "train.bin"
VAL_FILE = OUTPUT_DIR / "val.bin"

DATASET_CONFIG_FILE = OUTPUT_DIR / "dataset_config.json"


# Train / validation split.
TRAIN_RATIO = 0.90


# Size of each raw-data chunk read from disk.
#
# This controls RAM usage.
#
# 1 MB is conservative.
# 4 MB or 8 MB is usually faster for large datasets.
#
# It does NOT mean the entire dataset is loaded into RAM.
CHUNK_SIZE = 1034 * 1024 * 1024


# Number of token IDs accumulated before writing them.
#
# 1 million uint16 tokens = ~2 MB.
TOKEN_BUFFER_SIZE = 10_000_000


# ============================================================
# VALIDATION
# ============================================================

def validate_configuration(tokenizer):
    """
    Make sure uint16 is safe for this tokenizer.
    """

    vocab_size = tokenizer.get_vocab_size()

    # uint16 supports:
    #
    # 0 ... 65535
    #
    # Therefore vocab_size must be <= 65536.
    if vocab_size > 65536:
        raise ValueError(
            f"Vocabulary size is {vocab_size:,}, "
            "which cannot fit into uint16."
        )

    print(f"Vocabulary size : {vocab_size:,}")
    print("Token dtype     : uint16")
    print("Token range     : 0 - 65,535")


# ============================================================
# FIND 90/10 SPLIT
# ============================================================

def find_split_position():
    """
    Find a split close to 90% of the raw file.

    The split is moved forward to the next newline so that
    we don't cut a text line in half.

    Returns:
        split_position in bytes
    """

    print()
    print("=" * 70)
    print("FINDING TRAIN / VALIDATION SPLIT")
    print("=" * 70)

    file_size = RAW_DATA.stat().st_size

    target_position = int(file_size * TRAIN_RATIO)

    print(f"Raw file size : {file_size:,} bytes")
    print(
        f"Target train  : "
        f"{target_position:,} bytes "
        f"({TRAIN_RATIO * 100:.1f}%)"
    )

    with open(RAW_DATA, "rb") as f:

        # Jump directly to ~90%.
        f.seek(target_position)

        # Move to the end of the current line.
        f.readline()

        split_position = f.tell()

    train_bytes = split_position
    val_bytes = file_size - split_position

    print()
    print(f"Actual train  : {train_bytes:,} bytes "
          f"({train_bytes / file_size * 100:.2f}%)")

    print(f"Actual val    : {val_bytes:,} bytes "
          f"({val_bytes / file_size * 100:.2f}%)")

    return split_position


# ============================================================
# TOKEN BUFFER
# ============================================================

class TokenWriter:
    """
    Buffered uint16 token writer.

    Instead of calling write() once for every token, tokens are
    accumulated in memory and written in batches.

    This is substantially faster for large datasets.
    """

    def __init__(self, path):
        self.path = path

        self.file = open(path, "wb")

        self.buffer = []

        self.total_tokens = 0

    def add(self, token_ids):
        """
        Add token IDs to the buffer.
        """

        self.buffer.extend(token_ids)

        if len(self.buffer) >= TOKEN_BUFFER_SIZE:
            self.flush()

    def flush(self):
        """
        Write buffered token IDs as little-endian uint16.
        """

        if not self.buffer:
            return

        # '<' = little endian
        # 'H' = unsigned short = uint16
        #
        # Example:
        #
        # token IDs:
        # [10, 20, 300]
        #
        # become 6 bytes on disk.
        data = struct.pack(
            f"<{len(self.buffer)}H",
            *self.buffer
        )

        self.file.write(data)

        self.total_tokens += len(self.buffer)

        self.buffer.clear()

    def close(self):
        """
        Flush remaining tokens and close the file.
        """

        self.flush()

        self.file.close()


# ============================================================
# STREAMING TOKENIZATION
# ============================================================

def tokenize_range(
    tokenizer,
    start,
    end,
    output_file,
    label,
):
    """
    Stream a byte range of RAW_DATA through the tokenizer.

    Only a small chunk of the raw dataset is held in memory.

    Args:
        tokenizer:
            Hugging Face tokenizers.Tokenizer

        start:
            Starting byte offset.

        end:
            Ending byte offset.

        output_file:
            Destination .bin file.

        label:
            Human-readable name for progress output.
    """

    writer = TokenWriter(output_file)

    processed_bytes = 0

    # UTF-8 bytes that belong to a character which was split
    # across two chunks.
    leftover = b""

    with open(RAW_DATA, "rb") as src:

        src.seek(start)

        while start + processed_bytes < end:

            remaining = end - (start + processed_bytes)

            read_size = min(CHUNK_SIZE, remaining)

            data = src.read(read_size)

            if not data:
                break

            processed_bytes += len(data)

            # Combine bytes left over from the previous chunk.
            if leftover:
                data = leftover + data
                leftover = b""

            # ------------------------------------------------
            # UTF-8 SAFE DECODING
            # ------------------------------------------------

            try:

                text = data.decode("utf-8")

            except UnicodeDecodeError as error:

                # The error may be caused by an incomplete UTF-8
                # character at the end of the chunk.
                #
                # Everything before error.start is valid.
                valid_data = data[:error.start]

                leftover = data[error.start:]

                text = valid_data.decode("utf-8")

            # ------------------------------------------------
            # TOKENIZE
            # ------------------------------------------------

            if text:

                encoding = tokenizer.encode(text)

                writer.add(encoding.ids)

            # ------------------------------------------------
            # PROGRESS
            # ------------------------------------------------

            if processed_bytes % (256 * 1024 * 1024) < CHUNK_SIZE:

                percentage = (
                    processed_bytes /
                    (end - start)
                ) * 100

                print(
                    f"\r{label}: "
                    f"{percentage:6.2f}% | "
                    f"{processed_bytes:,} bytes | "
                    f"{writer.total_tokens:,} tokens",
                    end="",
                    flush=True,
                )

    # ========================================================
    # FINAL UTF-8 LEFTOVER
    # ========================================================

    if leftover:

        text = leftover.decode("utf-8")

        if text:

            encoding = tokenizer.encode(text)

            writer.add(encoding.ids)

    # Write remaining buffered tokens.
    writer.close()

    print()

    return writer.total_tokens


# ============================================================
# FILE SIZE HELPER
# ============================================================

def file_size_mb(path):
    """
    Return file size in MiB.
    """

    return path.stat().st_size / (1024 * 1024)


# ============================================================
# MAIN
# ============================================================

def main():

    # ========================================================
    # CHECK INPUTS
    # ========================================================

    if not RAW_DATA.exists():
        raise FileNotFoundError(
            f"Raw dataset not found:\n"
            f"    {RAW_DATA.resolve()}"
        )

    if not TOKENIZER_FILE.exists():
        raise FileNotFoundError(
            f"Tokenizer not found:\n"
            f"    {TOKENIZER_FILE.resolve()}"
        )

    # Create output directory.
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ========================================================
    # LOAD TOKENIZER
    # ========================================================

    print("=" * 70)
    print("5555LM STREAMING DATASET PREPARATION")
    print("=" * 70)

    print()
    print(f"Raw data       : {RAW_DATA}")
    print(f"Tokenizer      : {TOKENIZER_FILE}")
    print(f"Output dir     : {OUTPUT_DIR}")
    print(f"Train ratio    : {TRAIN_RATIO:.2f}")
    print(f"Val ratio      : {1.0 - TRAIN_RATIO:.2f}")
    print(f"Chunk size     : {CHUNK_SIZE / 1024 / 1024:.1f} MiB")
    print(
        f"Token buffer   : "
        f"{TOKEN_BUFFER_SIZE:,} tokens"
    )

    print()
    print("Loading tokenizer...")

    tokenizer = Tokenizer.from_file(
        str(TOKENIZER_FILE)
    )

    validate_configuration(tokenizer)

    vocab_size = tokenizer.get_vocab_size()

    # ========================================================
    # FIND SPLIT
    # ========================================================

    split_position = find_split_position()

    file_size = RAW_DATA.stat().st_size

    # ========================================================
    # TOKENIZE TRAIN
    # ========================================================

    print()
    print("=" * 70)
    print("TOKENIZING TRAIN")
    print("=" * 70)

    train_tokens = tokenize_range(
        tokenizer=tokenizer,
        start=0,
        end=split_position,
        output_file=TRAIN_FILE,
        label="Train",
    )

    # ========================================================
    # TOKENIZE VALIDATION
    # ========================================================

    print()
    print("=" * 70)
    print("TOKENIZING VALIDATION")
    print("=" * 70)

    val_tokens = tokenize_range(
        tokenizer=tokenizer,
        start=split_position,
        end=file_size,
        output_file=VAL_FILE,
        label="Val",
    )

    # ========================================================
    # DATASET CONFIG
    # ========================================================

    total_tokens = train_tokens + val_tokens

    actual_train_ratio = (
        train_tokens / total_tokens
        if total_tokens > 0
        else 0
    )

    actual_val_ratio = (
        val_tokens / total_tokens
        if total_tokens > 0
        else 0
    )

    config = {
        "raw_data": str(RAW_DATA),
        "tokenizer": str(TOKENIZER_FILE),

        "vocab_size": vocab_size,

        "token_dtype": "uint16",
        "token_bytes": 2,

        "requested_train_ratio": TRAIN_RATIO,
        "requested_val_ratio": 1.0 - TRAIN_RATIO,

        "actual_train_ratio": actual_train_ratio,
        "actual_val_ratio": actual_val_ratio,

        "raw_file_bytes": file_size,

        "train_raw_bytes": split_position,
        "val_raw_bytes": file_size - split_position,

        "train_tokens": train_tokens,
        "val_tokens": val_tokens,
        "total_tokens": total_tokens,

        "train_file": str(TRAIN_FILE),
        "val_file": str(VAL_FILE),
    }

    with open(
        DATASET_CONFIG_FILE,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            config,
            f,
            indent=2,
        )

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print()
    print("=" * 70)
    print("DATASET READY")
    print("=" * 70)

    print()
    print("RAW DATA")
    print("-" * 70)
    print(f"Size       : {file_size_mb(RAW_DATA):,.2f} MiB")
    print(f"Train raw  : {split_position:,} bytes")
    print(f"Val raw    : {file_size - split_position:,} bytes")

    print()
    print("TOKENS")
    print("-" * 70)
    print(f"Train      : {train_tokens:,}")
    print(f"Validation : {val_tokens:,}")
    print(f"Total      : {total_tokens:,}")

    print()
    print("TOKEN RATIO")
    print("-" * 70)
    print(f"Train      : {actual_train_ratio * 100:.2f}%")
    print(f"Validation : {actual_val_ratio * 100:.2f}%")

    print()
    print("OUTPUT FILES")
    print("-" * 70)
    print(
        f"Train      : {TRAIN_FILE} "
        f"({file_size_mb(TRAIN_FILE):,.2f} MiB)"
    )
    print(
        f"Validation : {VAL_FILE} "
        f"({file_size_mb(VAL_FILE):,.2f} MiB)"
    )
    print(f"Config     : {DATASET_CONFIG_FILE}")

    print()
    print("=" * 70)
    print("DONE")
    print("=" * 70)


if __name__ == "__main__":
    main()
