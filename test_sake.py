#!/usr/bin/env python -tt


import unittest
from sakelib import acts
import ntpath
import posixpath


# test UNICODE!!!


class TestActsFunction(unittest.TestCase):

    def setUp(self):
        # for mock sakefile 1
        lines = ["---", "#!ask=$hyness is nice",                # valid
                 "  ", "#!rΩsholme = at the last night      ",  # valid
                 "panic #! streets= london, burmingham",        # not valid
                 " #! asleep =sing me to sleep",                # not valid
                 "..."]
        self.mock_sakefile_for_macros = "\n".join(lines)

    def test_clean_path(self):
        unixpath1 = "/home/krsone/Pictures/../Desktop/"
        unixpath2 = "/home/krsone/Pictures/./me.jpg"
        windowspath1 = "C:/User/scottlarack/Pictures/../Desktop/"
        windowspath2 = "C:\\User/scottlarack/Pictures/./me.png"
        self.assertEqual(acts.clean_path(unixpath2,
                                         force_os="posix",
                                         force_start=posixpath.normpath(unixpath1)),
                         "../Pictures/me.jpg")
        self.assertEqual(acts.clean_path(windowspath2,
                                         force_os="windows",
                                         force_start=ntpath.normpath(windowspath1)),
                         "..\\Pictures\\me.png")

    def test_escp(self):
        has_no_space = "ask"
        has_one_space = "rusholme ruffians"
        has_two_cons_spaces = "shakespeare's  sister"
        has_more_spaces_and_unicode = " well i wønder"
        self.assertEqual("ask", acts.escp(has_no_space))
        self.assertEqual("\"rusholme ruffians\"", acts.escp(has_one_space))
        self.assertEqual("\"shakespeare's  sister\"", acts.escp(has_two_cons_spaces))
        self.assertEqual("\" well i wønder\"", acts.escp(has_more_spaces_and_unicode))

    def test_gather_macros(self):
        self.assertEqual(acts.gather_macros(self.mock_sakefile_for_macros),
                         {"ask": "$hyness is nice",
                          "rΩsholme": "at the last night      "})
        self.assertRaises(acts.InvalidMacroError,
                          acts.gather_macros,
                          "---\n#!f4I7 ur3=this should fail\n...")
        self.assertRaises(acts.InvalidMacroError,
                          acts.gather_macros,
                          "---\n#!===...")
        self.assertFalse(acts.gather_macros("---\nhandsome devil\n..."))

    def test_expand_macros(self):
        # ATTENTION:
        #   there is a bug in python's template substitution that
        #   prevents certain unicode-heavy strings from being replaced
        #   so 'rΩsholme' won't be subsituted, but it should be
        temp = ["---", "#!ask=shyness is nice", "$ask me, ask me, $ask me",
                "there are ruffians in $rusholme ($rΩsholme) and they steal $$",
                "$askme, ${ask}me", "..."]
        temp = "\n".join(temp)
        solution = ["---", "#!ask=shyness is nice", "$hyness is nice me, ask me, $hyness is nice me",
                    "there are ruffians in $rusholme ($rΩsholme) and they steal $",
                    "$askme, $hyness is niceme", "..."]
        solution = "\n".join(solution)
        self.assertEqual(acts.expand_macros(temp,
                                 acts.gather_macros(self.mock_sakefile_for_macros)),
                         solution)



if __name__ == '__main__':
    unittest.main()