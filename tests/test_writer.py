from mock import Mock, patch
import unittest

from solution import DebugWriter

DUMMY_MESSAGE = "debug message"

class TestWriter(unittest.TestCase):

    def setUp(self):
        super(TestWriter, self).setUp()
        self.patcher = patch('solution.sys.stdout.write')
        self.mock_stdout = self.patcher.start()

    def tearDown(self):
        super(TestWriter, self).tearDown()
        self.patcher.stop()

    def test_no_output(self):
        writer_obj = DebugWriter(False)
        writer_obj.write_debug(DUMMY_MESSAGE)
        self.assertFalse(self.mock_stdout.called)

    def test_with_output(self):
        writer_obj = DebugWriter(True)
        writer_obj.fd = Mock()
        writer_obj.write_debug(DUMMY_MESSAGE)
        writer_obj.fd.write.assert_called_once_with(DUMMY_MESSAGE + "\n")

