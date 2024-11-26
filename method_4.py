# SZYMON
# Huffman Encoding

from huffman_lib import HuffmanCoding

path = "secret1.jpg"

h = HuffmanCoding(path)

output_path = h.compress()
print("Compressed file path: " + output_path)

decom_path = h.decompress(output_path)
print("Decompressed file path: " + decom_path)

final_img = h.extract_jpg_image(decom_path)
print("final img file path: " + final_img)