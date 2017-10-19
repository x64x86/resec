import argparse
import hashlib
import os


class WriteFileTest():
    
    def __init__(self):
        """ Initializing of test directory, number of test files, file size, append block size, rewrite block size"""
        args = arg_parser()
        self.test_dir = args[0]
        self.file_count = args[1]
        self.file_size = args[2]
        self.append_size = args[3]
        self.rewrite_size = args[4]
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

    def _md5(self, file_d):
        """ Calculating md5 hash of opened file"""
        md5_hash = hashlib.md5()
        file_d.seek(0)
        for chunk in iter(lambda: file_d.read(4096), b""):
            md5_hash.update(chunk)
        return md5_hash.hexdigest()
    
    def _write_block(self, file_name, block_size, mode, start):
        """ Writes a block of random data to file. Returns md5 hash of the whole file
        start=0 writes at the beginning of the file
        start=1 appends file
        """
        with open(file_name, mode) as file:
            if not start:
                file.seek(0)
            file.write(os.urandom(block_size))
            file.flush()
            os.fsync(file)
            md5_hash = self._md5(file)
            file.close()
        return md5_hash

    def _write_files(self, block_size, mode='ab+', start=0):
        """ Writing random data with a size of block_size bytes into all test files
        start=0 writes at the beginning of the file
        start=1 appends file
        """
        md5_list = []
        for i in range(0, self.file_count):
            file_name = os.path.join(self.test_dir, 'file_' + str(i))
            md5_hash = self._write_block(file_name, block_size, mode, start)
            md5_list.append(md5_hash)
            print('{0} {1} bytes {2}'.format(file_name, self.file_size, md5_hash))
        return md5_list
    
    def create_files(self):
        """ Creating test files"""
        print('Creating {0} test files...'.format(self.file_count))
        md5_list = self._write_files(self.file_size, 'wb+', 0)
        print('Done')
        return md5_list

    def append_files(self):
        """ Appending a block of bytes to all the test files"""
        print('Appending {0} bytes to {1} test files...'.format(self.rewrite_size, self.file_count))
        self.file_size += self.append_size
        md5_list = self._write_files(self.append_size, 'ab+', 1)
        print('Done')
        return md5_list

    def rewrite_first_bytes(self):
        """ Rewriting first bytes of all the test files"""
        print('Rewriting first {0} bytes in {1} test files...'.format(self.rewrite_size, self.file_count))
        if self.rewrite_size > self.file_size:
            self.file_size = self.rewrite_size
        md5_list = self._write_files(self.rewrite_size, 'rb+', 0)
        print('Done')
        return md5_list


def arg_parser():
     """ Parsing of commanline arguments"""
     parser = argparse.ArgumentParser(description='Write file test')
     parser.add_argument('--dir', type=str, default='write_file', help='test directory name, \'write_file\' by default')
     parser.add_argument('--count', type=int, default=10, help='number of test files, 10 by default')
     parser.add_argument('--size', type=int, default=1024, help='file size, 1024 bytes by default')
     parser.add_argument('--append_size', type=int, default=100, help='size of block to append, 100 bytes by default')
     parser.add_argument('--rewrite_size', type=int, default=100, help='size of block to rewrite, 100 bytes by default')
     args = parser.parse_args()
     return (args.dir, args.count, args.size, args.append_size, args.rewrite_size)


def main():

    w = WriteFileTest()
    w.create_files()
    w.append_files()
    w.rewrite_first_bytes()


if __name__ == '__main__':
    main()
