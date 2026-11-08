from locust import HttpUser, between, task


class ClientUser(HttpUser):
    abstract = True
    wait_time = between(0.5, 1.5)
    client_type = None

    @task
    def api(self):
        headers = {"X-Client-Type": self.client_type} if self.client_type else {}
        self.client.get("/api/products", headers=headers,
                        name=f"/api/ [{self.client_type or 'unknown'}]")


class WebUser(ClientUser):
    client_type = "web"        # лимит 50 r/s


class MobileUser(ClientUser):
    client_type = "mobile"     # лимит 30 r/s


class UnknownUser(ClientUser):
    client_type = None         # без заголовка, лимит 30 r/s
