# NovaMarket

Учебный проект: архитектура маркетплейса на микросервисах. Описание компании и целей: [context/project.txt](context/project.txt).

| Задание | О чём | Что внутри |
|---|---|---|
| [Задание 1](tasks/task_1/README.md) | Событийная архитектура и сага оформления заказа | Список сервисов, каталог событий, C2-диаграмма, Saga-хореография |
| [Задание 2](tasks/task_2/README.md) | История покупок | CQRS: отдельный сервис истории заказов, ADR, C2-диаграмма |
| [Задание 3](tasks/task_3/README.md) | Автомасштабирование | HPA в Kubernetes по RPS и памяти, Prometheus Adapter, тест в Locust |
| [Задание 4](tasks/task_4/README.md) | Защита в NGINX | Rate limiter отдельно для web и mobile, Circuit breaker для логистики, тесты в Locust |

Шаблоны C4 для PlantUML лежат в [templates/](templates/).
