# 生成器
def get_file_content(filename, chunk_size=1024):
    with open(filename, encoding='utf-8') as file:  # 打开文件
        while True:
            content = file.read(chunk_size)  # 只读文件,读取1024字节

            # 如果为空，跳出
            if not content:
                break

            # 生成器,如果不为空，继续读取下一个
            yield content

