import unittest

from biocontainers.github.models import GitHubConfiguration, GitHubDockerReader


class GitHubDockerTestMethods(unittest.TestCase):

    def test_get_list_recipes(self):
        config = GitHubConfiguration("https://api.github.com/repos/biocontainers/containers/git/trees/master?recursive=2",
                                     "https://raw.githubusercontent.com/BioContainers/containers/master/%%recipe_software_tool_name%%")

        reader = GitHubDockerReader(config)
        recipes = reader.get_list_recipes()
        self.assertTrue(len(recipes) > 0)

    def test_get_recipes(self):
        config = GitHubConfiguration(
            "https://api.github.com/repos/biocontainers/containers/git/trees/master?recursive=2",
            "https://raw.githubusercontent.com/BioContainers/containers/master/%%recipe_software_tool_name%%")

        reader = GitHubDockerReader(config)
        recipes = reader.read_docker_recipes()
        self.assertTrue(len(recipes) > 0)


if __name__ == '__main__':
    unittest.main()