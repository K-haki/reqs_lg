import unittest
import unit_readid

def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

class TestFileContent(unittest.TestCase):
    def test_file_content(self):
        actual_path = 'difficulty0.txt'
        expected_path = 'text_expected.txt'

        # 读取预期内容的文件
        expected_content = read_file(expected_path)
        unit_readid.r_id()
        # 读取文件内容
        actual_content = read_file(actual_path)

        # 断言实际内容与预期内容是否相等
        self.assertEqual(actual_content, expected_content)

if __name__ == '__main__':
    unittest.main()
    