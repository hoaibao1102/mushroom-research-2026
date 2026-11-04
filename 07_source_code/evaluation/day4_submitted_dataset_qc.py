# Dataset Quality Check Script for Day 4
import os
import hashlib
import cv2
import json

def compute_sha256(file_path):
    sha256_hash = hashlib.sha256()
    if not os.path.exists(file_path): return "NOT_FOUND"
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(65536), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

print("QC Check Utility Script Loaded Successfully.")
