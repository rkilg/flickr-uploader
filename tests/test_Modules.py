# content of test_StrUni.py

import sys
import time
import unittest
import test.support
# -----------------------------------------------------------------------------
import lib.niceprint as niceprint
import lib.UPLDRConstants as UPLDRConstantsClass
# -----------------------------------------------------------------------------


class TestNicePrintMethods(unittest.TestCase):

    def test_niceprint(self):

        # with captured_stdout() as s:
        #     print "hello"
        # assert s.getvalue() == "hello\n", 'not ok'
        np = niceprint.niceprint()

        with test.support.captured_stdout() as s:
            np.niceprint('hello')

        print(s.getvalue())
        print('type:{}'.format(type(s)))
        npre = '\[[0-9. :]+\].+hello$'
        self.assertRegexpMatches(s.getvalue(), npre)

        """
        self, s, fname='uploadr'
        Print a message with the format:
            [2017.11.19 01:53:57]:[PID       ][PRINT   ]:[uploadr] Some Message
        """


class TestMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_RUN(self):
        print(eval(time.strftime('int("%j")+int("%H")*100'
                                 '+int("%M")*10+int("%S")')))
        self.assertTrue(
            1 <= eval(
                time.strftime('int("%j")+int("%H")*100'
                              '+int("%M")*10+int("%S")')) <= 3415)
        for j in range(1, 366 + 1):
            for h in range(24):
                for m in range(60):
                    for s in range(60):
                        self.assertTrue(1 <= j+h*100+m*10+s <= 3415)

    def test_Unicode(self):
        np = niceprint.niceprint()
        for i in range(1, 500):
            if sys.version_info < (3, ):
                if i < 127:
                    self.assertFalse(np.isThisStringUnicode(chr(i)))
                    self.assertTrue(np.isThisStringUnicode(
                                      unicode(chr(i).decode('utf-8'))))  # noqa
            else:
                self.assertFalse(np.isThisStringUnicode(chr(i)))


class TestUPLDRConstantsMethods(unittest.TestCase):
    """ TestUPLDRConstantsMethods
    """
    def test_nuMediaCount(self):
        """ test_nuMediaCount
        """
        UPLDRConstants = UPLDRConstantsClass.UPLDRConstants()

        for j in range(1, 20):
            UPLDRConstants.nuMediacount = j
            self.assertEqual(UPLDRConstants.nuMediacount, j)


if __name__ == '__main__':
    # unittest.main()

    suite = unittest.TestLoader().loadTestsFromTestCase(TestMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestNicePrintMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(
        TestUPLDRConstantsMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
