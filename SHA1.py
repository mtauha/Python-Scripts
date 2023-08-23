#! /usr/bin/env python3
import struct

def left_rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

def sha1(message):
    # Initialize variables (buffers)
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0
    
    # Pre-processing: Padding the message
    original_byte_len = len(message)
    message += b'\x80'
    message += b'\x00' * ((56 - (len(message) % 64)) % 64)
    message += struct.pack('>Q', original_byte_len * 8)
    
    # Break message into 512-bit blocks
    for i in range(0, len(message), 64):
        block = message[i:i + 64]
        words = list(struct.unpack('>16L', block))  # Extend to 80 words
        words.extend([0] * (80 - 16))  # Initialize the rest with zeros
        
        # Main loop
        for j in range(16, 80):
            words[j] = left_rotate((words[j - 3] ^ words[j - 8] ^ words[j - 14] ^ words[j - 16]), 1)
        
        # Initialize hash value for this chunk
        a, b, c, d, e = h0, h1, h2, h3, h4
        
        # Main loop
        for j in range(80):
            if j < 20:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif j < 40:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif j < 60:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6
            
            temp = left_rotate(a, 5) + f + e + k + words[j]
            e, d, c, b, a = d, c, left_rotate(b, 30), a, temp
        
        # Add this chunk's hash to result so far
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF

    # Produce the final hash
    return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)

# Example usage:
message = b'Hello, SHA-1!'
print("SHA-1 Hash:", sha1(message))
