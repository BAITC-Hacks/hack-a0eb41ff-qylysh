# MoneyGraph: статус интеграции после коммитов

Проверяемая ревизия: `734917d` (`main`, объединены frontend `7f9310d` и backend `9af1389`). Проверка относится только к этому состоянию репозитория. Рабочее дерево до проверки было чистым.

## Что пришло от команд

- Frontend реализовал страницы Overview, Network, Priority, Clusters и информационные страницы. Запросы собраны в `frontend/src/api/services.ts`; по умолчанию включены явно помеченные демонстрационные данные. `VITE_USE_MOCK_API=false` включает HTTP.
- Backend дошёл до главы 4: валидация Parquet, ориентированный граф и признаки. SQLite snapshot, роли, кластеры, рейтинг и domain API ещё отсутствуют. `app/api/router.py` содержит только пустой router с prefix `/api/v1`.

## Матрица API

| Endpoint | Frontend | Backend | Статус интеграции |
|---|---|---|---|
| `GET /health` | не используется | реализован | служебная проверка |
| `GET /api/v1/summary` | сервис и frozen DTO готовы | отсутствует | BLOCKED |
| `GET /api/v1/nodes` | сервис и предварительный DTO готовы | отсутствует | BLOCKED |
| `GET /api/v1/nodes/{gid}` | сервис и предварительный DTO готовы | отсутствует | BLOCKED |
| `GET /api/v1/nodes/{gid}/graph` | сервис и предварительный DTO готовы | отсутствует | BLOCKED |
| `GET /api/v1/clusters` | сервис и предварительный DTO готовы | отсутствует | BLOCKED |
| `GET /api/v1/clusters/{cluster_id}` | сервис готов, сейчас не используется экраном | отсутствует | BLOCKED |
| `GET /api/v1/clusters/{cluster_id}/graph` | сервис и предварительный DTO готовы | отсутствует | BLOCKED |
| `GET /api/v1/top-nodes` | имя зарезервировано; Priority использует `/nodes` | отсутствует | не подключён |

## Контрактные различия для следующего стыка

1. `/summary` уже заморожен в [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md#3-замороженный-контракт-summary): внешний `camelCase`. Существующие backend schemas сериализуют внутренние поля `snake_case`; отдельной внешней summary schema пока нет.
2. Предварительный frontend `GraphResponse` требует `focus`, `truncatedAtDepth`, у узлов — `depth` и поля `roleScore`, `priorityScore`, `clusterId`, `isSeed`; у рёбер — `sumKzt`, `transactionCount`. Нынешняя backend `GraphResponse` имеет другие имена и не содержит части полей. Это пока схемы будущего API, не ответ работающего endpoint.
3. Предварительный `NodeDetails` фронтенда требует `transactionCount`, тогда как backend `NodeRecord` содержит отдельно `in_tx` и `out_tx`. Значение агрегата и внешнее имя нужно закрепить перед handler.
4. Предварительный `ClusterDetails` фронтенда требует `description`, которого нет в backend `ClusterRecord`. Уточнить, вычисляется ли оно из snapshot или UI использует `hypothesis`.
5. Frontend посылает на `/nodes` параметры `page`, `pageSize`, `search`, `role`; исходный backend план упоминает `page`, `limit`, `minPriority`, `isSeed`, `cluster`. Написание, default и ограничения пагинации надо закрепить до реализации.
6. Для локального real mode пока не настроен ни CORS в FastAPI, ни proxy в Vite. Один из способов должен быть реализован вместе с domain endpoint.

Не менять фронтенд под текущие внутренние Python-схемы автоматически: внешние DTO для graph/node/cluster ещё не согласованы.

## Проверки

| Проверка | Результат |
|---|---|
| Чистота дерева до работы | PASS |
| Frontend `npm ci` | PASS: 112 packages, 0 vulnerabilities |
| Frontend TypeScript build под временным Node 22.23.2 | PASS |
| Frontend Vite production build под временным Node 22.23.2 | PASS |
| Backend `pytest -q` | PASS: 65 tests, 1 warning о deprecation в Starlette TestClient |
| Backend `check_data` | PASS: 2248 nodes, 3119 edges, 4840 transactions, 81 seeds |
| Backend `check_graph` | PASS: 2248 nodes, 3119 edges, 19 isolated nodes retained |
| Backend `check_features` | PASS: 2248 GID, 20 columns, 444 depth-4 flags |
| Прямой HTTP через FastAPI TestClient | `/health` и `/openapi.json` = 200; `/api/v1/summary`, `/nodes`, `/clusters` = 404 |
| Real API / OpenAPI против DTO | BLOCKED: domain endpoints отсутствуют |
| Сквозной Parquet → SQLite → API → React | BLOCKED: snapshot и domain endpoints отсутствуют |

Системный Node этой машины — 18.17.1; Vite требует 20.19+ или 22.12+. Сборка выполнена временным Node 22.23.2. Единственный warning тестов касается установленной комбинации FastAPI/Starlette/httpx; тесты прошли. В OpenAPI нет путей `/api/v1/*`.

## Следующий интеграционный шаг

Дождаться backend глав 5–11 или хотя бы честной реализации summary на рассчитанном snapshot. Затем согласовать внешние DTO, включить real mode, сравнить ответы и OpenAPI поле в поле, проверить ошибки 404/422 и CORS. Mock mode не засчитывается как сквозная интеграция.
