import os
import unittest
import time

from arc_frejya.utils.web_helpers.web_factory import get_web


class TestOpenNavigators(unittest.TestCase):
    """Test class to open navigators (get_web())."""

    def test_default_nav(self):
        """Test to open default Frejya navigator (no params)."""
        print('Test 1: Open default Frejya navigator (Chrome).')
        web = get_web()
        self.assertEqual(web.driver.name, 'chrome')
        print("Wait 2 Seconds.")
        time.sleep(2)
        web.close()

    def test_edge_nav(self):
        """Test to open Edge navigator (Browser: Edge)."""
        print('Test 2: Open Edge navigator (Browser: Edge).')
        web = get_web(browser='Edge')
        self.assertEqual(web.driver.name, 'msedge')
        print("Wait 2 Seconds.")
        time.sleep(2)
        web.close()

    def test_workspace_nav(self):
        """Test to open workspace navigator (Workspace: example_project)."""
        print('Test 3: Open workspace navigator (Workspace: example_project -> Firefox).')
        web = get_web(workspace='example_project')
        self.assertEqual(web.driver.name, 'firefox')
        print("Wait 2 Seconds.")
        time.sleep(2)
        web.close()
        gecko_log_path = os.path.dirname(os.path.abspath(__file__)) + os.sep + "geckodriver.log"
        if os.path.isfile(gecko_log_path):
            os.remove(gecko_log_path)

    def test_workspace_browser_nav(self):
        """Test to open workspace/browser navigator (Workspace: example_project, Browser: Chrome)."""
        print('Test 4: Open workspace/browser navigator (Workspace: example_project -> Firefox, Browser: Chrome).')
        web = get_web(browser='Chrome', workspace='example_project')
        self.assertEqual(web.driver.name, 'chrome')
        print("Wait 2 Seconds.")
        time.sleep(2)
        web.close()


if __name__ == '__main__':
    unittest.main()