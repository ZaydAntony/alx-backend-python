#!/usr/bin/env python3
"""Unit and integration tests for client.GithubOrgClient."""

from __future__ import annotations

import unittest
from typing import Any, Dict, List
from unittest.mock import Mock, patch, PropertyMock

from parameterized import parameterized, parameterized_class

import client
import utils
import fixtures


class TestGithubOrgClient(unittest.TestCase):
    #Unit tests for GithubOrgClient methods that can be isolated."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name: str, mock_get_json: Mock) -> None:
        #GithubOrgClient.org should return value from get_json and call get_json once."""
        mock_get_json.return_value = {"login": org_name}
        gh = client.GithubOrgClient(org_name)
        self.assertEqual(gh.org, mock_get_json.return_value)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self) -> None:
        #_public_repos_url should return the repos_url obtained from the org property."""
        fake_payload = {"repos_url": "https://api.github.com/orgs/test-org/repos"}
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mocked_org:
            mocked_org.return_value = fake_payload
            gh = client.GithubOrgClient("test-org")
            self.assertEqual(gh._public_repos_url, fake_payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: Mock) -> None:
            #public_repos should return repository names from get_json and call helpers once."""
        repos_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = repos_payload
        with patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test-org/repos"
            gh = client.GithubOrgClient("test-org")
            self.assertEqual(gh.public_repos(), ["repo1", "repo2"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(mock_url.return_value)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo: Dict[str, Any], license_key: str, expected: bool) -> None:
        #has_license should correctly identify if a repo has the given license key."""
        self.assertEqual(client.GithubOrgClient.has_license(repo, license_key), expected)


@parameterized_class(("org_payload", "repos_payload", "expected_repos", "apache2_repos"), [
    (fixtures.org_payload, fixtures.repos_payload,
     fixtures.expected_repos, fixtures.apache2_repos),
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
        #Integration tests for GithubOrgClient that use fixture payloads."""

    @classmethod
    def setUpClass(cls) -> None:
        #Start patching requests.get and set side_effect to return fixture payloads."""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def _side_effect(url: str, *args: Any, **kwargs: Any) -> Mock:
            m = Mock()
            # if the url is the repos URL, return repos payload; otherwise org payload
            if url.endswith("/repos"):
                m.json.return_value = cls.repos_payload
            else:
                m.json.return_value = cls.org_payload
            return m

        mock_get.side_effect = _side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        #Stop the requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos_integration(self) -> None:
        #public_repos should return the expected list from fixtures."""
        gh = client.GithubOrgClient(self.org_payload.get("login"))
        self.assertEqual(gh.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        #public_repos when filtering by license should return expected repos with apache-2.0."""
        gh = client.GithubOrgClient(self.org_payload.get("login"))
        self.assertEqual(gh.public_repos(license="apache-2.0"), self.apache2_repos)
