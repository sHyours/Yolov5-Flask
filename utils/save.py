# -*- coding: utf-8 -*-
import os

def save_data_to_file(buffer, file_path, mode='w', encoding='utf-8'):
    '''
    保存字符串到指定文件
    Args:
        html:       str   字符串数据
        file_path:  str   文件路径
        mode:       str   文件打开格式，[w,r,a...]
        encoding:   str   文件编码格式 [utf-8, gbk]
    Returns:        list  True/False, message
    '''
    # 文件目录
    file_path_dir = os.path.dirname(file_path)
    # 判断目录是否存在
    if not os.path.exists(file_path_dir):
        # 目录不存在创建，makedirs可以创建多级目录
        os.makedirs(file_path_dir)
    try:
        # 保存数据到文件
        with open(file_path, mode, encoding=encoding) as f:
            f.write(buffer)
        return True, '保存成功'
    except Exception as e:
        return False, '保存失败:{}'.format(e)


if __name__ == "__main__":
    buffer = '字符串数据'  # 要保存的数据 unicode
    file_path = './a/b/1.txt'  # 文件路径
    save_data_to_file(buffer, file_path, encoding='gbk')
