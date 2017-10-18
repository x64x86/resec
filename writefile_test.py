import os
import hashlib

class WriteFileTest():

    DEFAULT_DIR = 'Write_test'
    
    def __init__(self, test_dir=DEFAULT_DIR, file_count=10, file_size=1024):
        self.test_dir = test_dir
        self.file_count = file_count
        self.file_size = file_size
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

    def _md5(self, file):
        md5_hash = hashlib.md5()
        file.seek(0)
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)
        return md5_hash.hexdigest()
    
    def _write_block(self, file_name, size, mode='wb+'):
        """ Writes a block of random data to file. Returns md5 hash of the whole file
        mode=wb+ writes at the beginning of the file.
        mode=ab+ appends file
        """
        with open(file_name, mode) as file:
            file.write(os.urandom(size))
            file.flush()
            os.fsync(file)
            md5_hash = self._md5(file)
            file.close()
        return md5_hash

    def create_files(self):
        md5_list = []
        for i in range(0, self.file_count):
            file_name = os.path.join(self.test_dir, 'file_' + str(i))
            md5_hash = self._write_block(file_name, self.file_size)
            md5_list.append(md5_hash)
        return md5_list

    def append_files(self, block_size=100):
        md5_list = []
        for i in range(0, self.file_count):
            file_name = os.path.join(self.test_dir, 'file_' + str(i))
            md5_hash = self._write_block(file_name, block_size, 'ab+')
            md5_list.append(md5_hash)
        return md5_list
    

def main():
    w = WriteFileTest()
    m = w.create_files()
    print(m)
    m = w.append_files()
    print(m)

if __name__ == '__main__':
    main()
