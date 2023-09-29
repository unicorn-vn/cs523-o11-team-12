import os
from utils.file_helpers import split_file, write_temp_file

# Hàm để sắp xếp và trộn các tệp tạm thời
def merge_sorted_files(sf, sorted_files, output_file, rv, k, output_buffer=0):
    sf.progress_label.setText('Đang trộn file...')
    with open(output_file, 'a') as out:
        # Mở các tệp tạm thời và đọc dữ liệu ban đầu
        temp_files = [open(file, 'r') for file in sorted_files]
        data = [file.readline() for file in temp_files]
        temp_content = ""
        
        while data:
            # Tìm phần tử nhỏ nhất
            if (rv):
                min_val = max(data, key=lambda x: x.split(',')[k])
            else:
                min_val = min(data, key=lambda x: x.split(',')[k])
            min_idx = data.index(min_val)
            
            # Ghi phần tử nhỏ nhất vào tệp kết quả
            if (output_buffer == 0):
                out.write(min_val)
            else:
                if (len(temp_content) > output_buffer):
                    out.write(temp_content)
                    temp_content = ""
                else:
                    temp_content += min_val
            # out.write(min_val)
            
            # Đọc tiếp dữ liệu từ tệp đó
            data[min_idx] = temp_files[min_idx].readline()
            
            # Kiểm tra xem tệp đó còn dữ liệu không
            if not data[min_idx]:
                temp_files[min_idx].close()
                del temp_files[min_idx]
                del data[min_idx]

# Hàm sắp xếp ngoại bộ
def external_sort(sf, input_file, output_file, chunk_size=1024, rv=False, col=0, output_buffer=0):
    temp_dir = './temp_files/'
    chunks = split_file(input_file, chunk_size)
    sorted_files = []

    # Sắp xếp từng phần nhỏ và lưu vào các tệp tạm thời
    for i, chunk in enumerate(chunks):
        chunk.sort(key=lambda x: x.split(',')[col], reverse=rv)
        temp_file = write_temp_file(sf, chunk, temp_dir)
        sorted_files.append(temp_file)

    with open(input_file, 'r') as inp:
        first_line = inp.readline()
        with open(output_file, 'w') as out:
            out.write(first_line)

    # Trộn các tệp tạm thời để có kết quả cuối cùng
    merge_sorted_files(sf, sorted_files, output_file, rv, col, output_buffer)

    # Xóa tệp tạm thời và thư mục tạm thời
    for temp_file in sorted_files:
        os.remove(temp_file)
    # os.rmdir(temp_dir)
