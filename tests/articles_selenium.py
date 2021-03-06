#!/usr/bin/env python
# coding=utf-8

import unittest

from flask.ext.testing import LiveServerTestCase
from selenium import webdriver

from xunta import create_app


class Articles(LiveServerTestCase):
    def create_app(self):
        app = create_app('test')
        return app

    def setUp(self):
        self.driver = webdriver.Firefox()

    def login(self):
        url = "http://localhost:5000/login"
        driver = self.driver
        driver.get(url)
        email = driver.find_elements_by_xpath("//input[@name='email']")[0]
        email.send_keys("selenium@example.com")
        password = driver.find_elements_by_xpath("//input[@name='password']")[0]
        password.send_keys("selenium@example.com")
        submit_button = driver.find_element_by_name('login')
        submit_button.click()
        self.assertIn("http://localhost:5000", driver.current_url)

    def test_create_articles_redirect(self):
        self.login()
        driver = self.driver
        driver.get("http://localhost:5000/create/articles/")
        title = driver.find_elements_by_xpath("//input[@name='title']")[0]
        title.send_keys("this is a test")
        tag = driver.find_elements_by_xpath("//input[@name='tag']")[0]
        tag.send_keys("test")
        content = driver.find_elements_by_xpath("//textarea[@name='content']")[0]
        content.send_keys("this is a test")
        slug = driver.find_elements_by_xpath("//input[@name='slug']")[0]
        slug.send_keys("hello-world")
        submit_button = driver.find_element_by_name('post')
        submit_button.click()
        self.assertIn("http://localhost:5000/articles/hello-world", driver.current_url)
        assert "this is a test" in driver.title

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
