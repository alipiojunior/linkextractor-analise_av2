from locust import HttpUser, task, between

class LinkExtractorUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def extract_links(self):
        urls = [
            "http://example.com",
            "https://www.wikipedia.org",
            "https://github.com",
            "https://www.python.org",
            "https://www.docker.com",
            "https://www.ruby-lang.org",
            "https://redis.io",
            "https://www.google.com",
            "https://www.linux.org",
            "https://stackoverflow.com"
        ]

        for url in urls:
            self.client.get(f"/?url={url}", name="/")