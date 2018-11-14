import unittest

import logging

from biocontainers.github.models import GitHubConfiguration, GitHubDockerReader, GitHubCondaReader

logger = logging.getLogger('biocontainers.tests')
logging.basicConfig(level=logging.INFO)

class GitHubTestMethods(unittest.TestCase):
    def test_get_list_docker_recipes(self):
        config = GitHubConfiguration(
            "https://api.github.com/repos/biocontainers/containers/git/trees/master?recursive=2",
            "https://raw.githubusercontent.com/BioContainers/containers/master/%%recipe_software_tool_name%%")

        reader = GitHubDockerReader(config)
        recipes = reader.get_list_recipes()
        self.assertTrue(len(recipes) > 0)

    def test_get_docker_recipes(self):
        config = GitHubConfiguration(
            "https://api.github.com/repos/biocontainers/containers/git/trees/master?recursive=2",
            "https://raw.githubusercontent.com/BioContainers/containers/master/%%recipe_software_tool_name%%")

        reader = GitHubDockerReader(config)
        recipes = reader.read_docker_recipes()
        self.assertTrue(len(recipes) > 0)

    def test_get_list_conda_recipes(self):
        config = GitHubConfiguration("https://api.github.com/repositories/42372094/git/trees/master?recursive=2",
                                     "https://raw.githubusercontent.com/bioconda/bioconda-recipes/master/%%recipe_software_tool_name%%")

        reader = GitHubCondaReader(config)
        recipes = reader.get_list_recipes()
        self.assertTrue(len(recipes) > 0)

    def test_get_conda_recipes(self):
        config = GitHubConfiguration("https://api.github.com/repositories/42372094/git/trees/master?recursive=2",
                                     "https://raw.githubusercontent.com/bioconda/bioconda-recipes/master/%%recipe_software_tool_name%%")

        reader = GitHubCondaReader(config)
        recipes = reader.read_conda_recipes()
        self.assertTrue(len(recipes) > 0)


if __name__ == '__main__':
    unittest.main()
