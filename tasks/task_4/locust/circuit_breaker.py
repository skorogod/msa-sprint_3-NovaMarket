import logging
import time

from locust import HttpUser, constant, task

SERVICE = "127.0.0.1:9090"
FALLBACK = "127.0.0.1:9091"

log = logging.getLogger("circuit")


def state(upstream):
    if upstream == SERVICE:
        return "CLOSED  (ответил сервис)"
    if upstream == FALLBACK:
        return "OPEN    (fallback, сервис не вызывали)"
    return "ERROR   (сервис ошибся -> fallback)"


class CircuitBreakerUser(HttpUser):
    wait_time = constant(1)
    fixed_count = 1  # один пользователь

    def call(self, path):
        start = time.monotonic()
        with self.client.get(f"/logistics/{path}", name=f"/logistics/{path}",
                             catch_response=True) as r:
            upstream = r.headers.get("X-Upstream", "-")
            took = time.monotonic() - start
            log.info("%-6s -> %s  %.1fs  %s", path, r.status_code, took, state(upstream))

            if upstream.endswith(FALLBACK):
                r.success()
            return upstream

    @task
    def scenario(self):
        log.info("===== 1. Сервис здоров")
        self.call("fast")

        log.info("===== 2. Сервис ломается: 3 ошибки 503 и 2 таймаута")
        for path in ["error", "error", "error", "slow", "slow"]:
            self.call(path)

        log.info("===== 3. Circuit должен быть открыт: /fast отвечает fallback")
        opened_at = time.monotonic()
        for _ in range(3):
            self.call("fast")

        log.info("===== 4. Ждём, пока пройдут 30 секунд")
        while self.call("fast") != SERVICE:
            time.sleep(4)

        log.info("===== 5. Сервис снова отвечает. Circuit был открыт %.0f с",
                 time.monotonic() - opened_at)
        log.info("")
