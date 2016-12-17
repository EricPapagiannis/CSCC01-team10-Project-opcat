import storage_manager.storage_manager as STORAGE
import data_comparison.proposed_change as Change
import pickle
import unittest
import data_parsing.Planet as Planet


class TestStorageManager(unittest.TestCase):
    def test_read_file(self):
        expected = "Contents of plain text file\n\n+++++++++\n"
        path = "storage_manager_test_files/plain_file"
        self.assertEqual(STORAGE.read_file(path), expected)

    def test_read_empty_file(self):
        expected = ""
        path = "storage_manager_test_files/empty_file"
        self.assertEqual(STORAGE.read_file(path), expected)

    def test_read_nonexistant_file(self):
        path = "storage_manager_test_files/NO_SUCH_FILE"
        with self.assertRaises(FileNotFoundError):
            STORAGE.read_file(path)

    def test_manual(self):
        STORAGE.MANUAL_PATH = "storage_manager_test_files/mock_manual"
        expected = "*******\ncontents of mock manual file\n*******\n"
        self.assertEqual(STORAGE.manual(), expected)

    def test_write_changes_to_memory(self):
        # make a mock list of proposed changes
        STORAGE.PROPOSED_CHANGES_PATH = \
            "storage_manager_test_files/mock_changes_storage_file2"
        p = Planet.Planet("a")
        p.lastupdate = "16/11/20"
        p2 = Planet.Planet("b")
        p2.lastupdate = "16/11/20"
        c1 = Change.Addition("origin str", p)
        c2 = Change.Modification("Origin str", p, p2, "field", 10, 15)
        changes_list = [c1, c2]
        # write the list to memory
        STORAGE.write_changes_to_memory(changes_list)
        # retrieve the list and make sure that nothing have been changed
        retrieved = STORAGE.read_changes_from_memory()
        self.assertEquals(len(retrieved), 2)
        self.assertEquals(retrieved[0].__class__.__name__, "Addition")
        self.assertEquals(retrieved[0].origin, "origin str")
        self.assertEquals(retrieved[0].get_object_name(), p.name)
        self.assertEquals(retrieved[1].__class__.__name__, "Modification")
        self.assertEquals(retrieved[1].origin, "Origin str")
        self.assertEquals(retrieved[1].get_object_name(), p.name)
        self.assertEquals(retrieved[1].field_modified, "field")
        self.assertEquals(retrieved[1].value_in_origin_catalogue, 10)
        self.assertEquals(retrieved[1].value_in_OEC, 15)

    def test_read_changes_from_memory_empty_file(self):
        STORAGE.PROPOSED_CHANGES_PATH = \
            "storage_manager_test_files/empty_file"
        self.assertEquals(STORAGE.read_changes_from_memory(), [])

    def test_read_changes_from_memory(self):
        # reads changes from a mock file containing 50 proposed changes stored
        # and compares retrieved info with expected values
        STORAGE.PROPOSED_CHANGES_PATH = \
            "storage_manager_test_files/mock_changes_storage_file"
        extracted = STORAGE.read_changes_from_memory()
        valid_class_names = ["ProposedChange", "Addition", "Modification"]
        for i in extracted:
            self.assertTrue(i.__class__.__name__ in valid_class_names)
        self.assertEqual(extracted[0].get_object_name(), "11 Com b")
        self.assertEqual(extracted[1].get_object_name(), "11 Com b")
        self.assertEqual(extracted[2].get_object_name(), "11 UMi b")
        self.assertEqual(extracted[3].get_object_name(), "11 UMi b")

    def test_clean_config_file(self):
        STORAGE.CONFIG_PATH = "storage_manager_test_files/mock_config_file"
        STORAGE.clean_config_file()
        with open(STORAGE.CONFIG_PATH, "rb") as test_file:
            retrieved = pickle.load(test_file)
        resultList = list(retrieved.keys())

        answer = ['black_list', 'last_update', 'auto_update_settings',
                  'repo_url', 'branch_number']
        self.assertTrue(
            len(resultList) == len(answer) and all(
                resultList.count(i) == answer.count(i) for i in resultList))
        self.assertEquals(retrieved["last_update"], "Never")

    def test_config_set_get_simple(self):
        STORAGE.CONFIG_PATH = "storage_manager_test_files/mock_config_file"
        STORAGE.clean_config_file()
        STORAGE.config_set("key1", "TEST string")
        STORAGE.config_set("key2", [1, 14, 44])
        self.assertEqual(STORAGE.config_get("key1"), "TEST string")
        self.assertEqual(STORAGE.config_get("key2"), [1, 14, 44])
        STORAGE.clean_config_file()

    def test_config_set_get_object(self):
        STORAGE.CONFIG_PATH = "storage_manager_test_files/mock_config_file"
        STORAGE.clean_config_file()
        p = Planet.Planet("a")
        p.lastupdate = "16/11/20"
        test_object = Change.Addition("origin", p)
        STORAGE.config_set("key", test_object)
        retrieved = STORAGE.config_get("key")
        self.assertEqual(retrieved.__class__.__name__, "Addition")
        self.assertEqual(retrieved.origin, "origin")


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
