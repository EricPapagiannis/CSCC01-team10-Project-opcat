import unittest
from data_comparison.proposed_change import *
import data_parsing.Planet as Planet
import data_parsing.Star as Star
import data_parsing.System as System


class testing_constructors(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(testing_constructors, self).__init__(*args, **kwargs)
        self.planet = Planet.Planet("A")
        self.star = Star.Star("B")
        self.system = System.System("C")
        self.p = Planet.Planet("Z")

    def test_init_addition(self):
        a = Addition("exoplanet.eu", self.planet)
        self.assertEqual(a.origin, "exoplanet.eu")
        self.assertEqual(a.object_ptr, self.planet)
        self.assertEqual(a.get_object_name(), "A")

    def test_init_modification(self):
        a = Modification("NASA", self.planet, self.p, "fieldname", 10, 15)
        self.assertEqual(a.get_object_name(), "A")
        self.assertEqual(a.OEC_object, self.planet)
        self.assertEqual(a.origin, "NASA")
        self.assertEqual(a.field_modified, "fieldname")
        self.assertEqual(a.value_in_origin_catalogue, 10)
        self.assertEqual(a.value_in_OEC, 15)


class testing_merge(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(testing_merge, self).__init__(*args, **kwargs)
        self.planet1 = Planet.Planet("A")
        self.planet2 = Planet.Planet("B")
        self.planet3 = Planet.Planet("C")
        self.planet4 = Planet.Planet("RR")
        self.planet5 = Planet.Planet("UU")
        self.planet6 = Planet.Planet("dddddd")
        self.p = Planet.Planet("Z")

    def test_merge_both_empty(self):
        l1 = []
        l2 = []
        result = merge_changes(l1, l2)
        self.assertTrue(isinstance(result, list))
        self.assertEqual(len(result), 0)

    def test_merge_one_empty_1(self):
        a = Addition("source", self.planet1)
        l1 = []
        l2 = []
        l1.append(a)
        result = merge_changes(l1, l2)
        self.assertTrue(isinstance(result, list))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], a)

    def test_merge_one_empty_2(self):
        a = Addition("source", self.planet1)
        b = Addition("source", self.planet3)
        l1 = []
        l2 = []
        l2.append(a)
        l2.append(b)
        result = merge_changes(l1, l2)
        self.assertTrue(isinstance(result, list))
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], a)
        self.assertEqual(result[1], b)

    def test_merge_1(self):
        a = Modification("aaa", self.planet1, self.p, "fieldname", 10, 11)
        b = Addition("source", self.planet2)
        c = Addition("source", self.planet3)
        d = Addition("source", self.planet4)
        e = Addition("source", self.planet5)
        l1 = []
        l2 = []
        l1.append(b)
        l1.append(d)
        l2.append(a)
        l2.append(c)
        l2.append(e)
        result = merge_changes(l1, l2)
        self.assertTrue(isinstance(result, list))
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].get_object_name(), a.get_object_name())
        self.assertEqual(result[1].get_object_name(), b.get_object_name())
        self.assertEqual(result[2].get_object_name(), c.get_object_name())
        self.assertEqual(result[3].get_object_name(), d.get_object_name())
        self.assertEqual(result[4].get_object_name(), e.get_object_name())

    def test_merge_2(self):
        a = Modification("aaa", self.planet1, self.p, "fieldname", 10, 11)
        b = Addition("source", self.planet2)
        c = Addition("source", self.planet3)
        d = Modification("source", self.planet4, self.p, "field", 5, 6)
        e = Modification("source", self.planet5, self.p, "field", 1, 2)
        l1 = []
        l2 = []
        l1.append(a)
        l1.append(b)
        l1.append(e)
        l2.append(c)
        l2.append(d)
        result = merge_changes(l1, l2)
        self.assertTrue(isinstance(result, list))
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].get_object_name(), a.get_object_name())
        self.assertEqual(result[1].get_object_name(), b.get_object_name())
        self.assertEqual(result[2].get_object_name(), c.get_object_name())
        self.assertEqual(result[3].get_object_name(), d.get_object_name())
        self.assertEqual(result[4].get_object_name(), e.get_object_name())


class testing_sort(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(testing_sort, self).__init__(*args, **kwargs)
        self.planet1 = Planet.Planet("A")
        self.planet2 = Planet.Planet("B")
        self.p3 = Planet.Planet("C")
        self.planet4 = Planet.Planet("RR")
        self.planet5 = Planet.Planet("UU")
        self.planet6 = Planet.Planet("dddddd")
        self.p = Planet.Planet("Z")

    def test_sort1(self):
        a = Modification("aaa", self.planet1, self.p, "fieldname", 10, 11)
        b = Addition("source", self.planet2)
        c = Addition("source", self.p3)
        d = Modification("source", self.planet4, self.p, "field", 5, 6)
        e = Modification("source", self.planet5, self.p, "field", 1, 2)
        L = [c, e, d, b, a]
        result = merge_sort_changes(L)
        self.assertTrue(isinstance(result, list))
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].get_object_name(), a.get_object_name())
        self.assertEqual(result[1].get_object_name(), b.get_object_name())
        self.assertEqual(result[2].get_object_name(), c.get_object_name())
        self.assertEqual(result[3].get_object_name(), d.get_object_name())
        self.assertEqual(result[4].get_object_name(), e.get_object_name())

    def test_sort_order(self):
        self.p1 = Planet.Planet("a")
        self.p2 = Planet.Planet("b")
        self.p3 = Planet.Planet("c")
        self.p4 = Planet.Planet("d")
        self.p5 = Planet.Planet("e")
        self.p6 = Planet.Planet("f")
        a = Modification("aaa", self.p1, self.p, "fieldname", 10, 11)
        b = Addition("source", self.p2)
        c = Addition("source", self.p3)
        d = Modification("source", self.p4, self.p, "field", 5, 6)
        e = Modification("source", self.p5, self.p, "field", 1, 2)
        f = Modification("source", self.p6, self.p, "field", 3, 4)

        L = [b, a, d, c, f, e]
        result = merge_sort_changes(L)
        self.assertTrue(isinstance(result, list))
        self.assertEqual(len(result), 6)
        self.assertEqual(result[0].get_object_name(), a.get_object_name())
        self.assertEqual(result[1].get_object_name(), b.get_object_name())
        self.assertEqual(result[2].get_object_name(), c.get_object_name())
        self.assertEqual(result[3].get_object_name(), d.get_object_name())
        self.assertEqual(result[4].get_object_name(), e.get_object_name())
        self.assertEqual(result[5].get_object_name(), f.get_object_name())

    def test_sort2(self):
        a = Modification("aaa", self.planet1, self.p, "fieldname", 10, 11)
        b = Addition("source", self.planet2)
        c = Addition("source", self.p3)
        d = Modification("source", self.planet4, self.p, "field", 5, 6)
        e = Modification("source", self.planet5, self.p, "field", 1, 2)
        L = [a, b, c, d, e]
        result = merge_sort_changes(L)
        print(result)
        self.assertTrue(isinstance(result, list))
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].get_object_name(), a.get_object_name())
        self.assertEqual(result[1].get_object_name(), b.get_object_name())
        self.assertEqual(result[2].get_object_name(), c.get_object_name())
        self.assertEqual(result[3].get_object_name(), d.get_object_name())
        self.assertEqual(result[4].get_object_name(), e.get_object_name())

    def test_sort3(self):
        a = Modification("aaa", self.planet1, self.p, "fieldname", 10, 11)
        b = Addition("source", self.planet2)
        c = Addition("source", self.p3)
        d = Modification("source", self.planet4, self.p, "field", 5, 6)
        e = Modification("source", self.planet5, self.p, "field", 1, 2)
        L = [a, b, e, d, c]
        result = merge_sort_changes(L)
        self.assertTrue(isinstance(result, list))
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].get_object_name(), a.get_object_name())
        self.assertEqual(result[1].get_object_name(), b.get_object_name())
        self.assertEqual(result[2].get_object_name(), c.get_object_name())
        self.assertEqual(result[3].get_object_name(), d.get_object_name())
        self.assertEqual(result[4].get_object_name(), e.get_object_name())

    def test_sort_empty(self):
        L = []
        result = merge_sort_changes(L)
        self.assertTrue(isinstance(result, list))
        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
