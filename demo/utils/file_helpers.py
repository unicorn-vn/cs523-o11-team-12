import os
import tempfile

# Hàm để chia tệp thành các phần nhỏ
def split_file(input_file, chunk_size):
    chunks = []
    with open(input_file, 'r') as f:
        f.readline()
        chunk = f.readlines(chunk_size)
        while chunk:
            chunks.append(chunk)
            chunk = f.readlines(chunk_size)
    return chunks

# Hàm để ghi dữ liệu vào tệp tạm thời
def write_temp_file(sf, data, temp_dir):
    temp_file = tempfile.mktemp(dir=temp_dir)
    sf.progress_label.setText(f'Đang ghi file {temp_file}...')
    with open(temp_file, 'w') as f:
        f.writelines(data)
    return temp_file