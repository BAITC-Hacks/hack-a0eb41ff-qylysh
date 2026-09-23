# MoneyGraph: статус интеграции после backend главы 12

Базовая ревизия: `1b18b9c` (`main`, включает backend `81cd137`). Описанные ниже исправления интеграции находятся в текущем рабочем дереве и ещё не закоммичены.

## Что пришло от команд

- Frontend реализовал страницы Overview, Network, Priority, Clusters и информационные страницы. Запросы собраны в `frontend/src/api/services.ts`; после интеграции по умолчанию используется реальный API. `VITE_USE_MOCK_API=true` включает явно помеченные демонстрационные данные.
- Backend завершил pipeline до SQLite snapshot, CSV и восьми domain endpoint. На реальном наборе получены 2248 узлов, 3119 рёбер, 4840 транзакций, 81 seed, 91 кластер и рейтинг 2248 узлов.

## Матрица API

| Endpoint | Frontend | Backend | Статус интеграции |
|---|---|---|---|
| `GET /health` | не используется | реализован | служебная проверка |
| `GET /api/v1/summary` | Overview | реализован | PASS: реальный Dashboard |
| `GET /api/v1/nodes` | Priority | реализован | PASS: 20 записей и фильтры |
| `GET /api/v1/nodes/{gid}` | детали в Priority | реализован | PASS: 18-значный GID |
| `GET /api/v1/nodes/{gid}/graph` | Network | реализован | PASS: реальный граф по GID |
| `GET /api/v1/clusters` | Clusters | реализован | PASS: 91 кластер |
| `GET /api/v1/clusters/{cluster_id}` | сервис готов, сейчас не используется экраном | реализован | PASS: прямой API запрос |
| `GET /api/v1/clusters/{cluster_id}/graph` | Network | реализован | PASS: прямой API запрос |
| `GET /api/v1/top-nodes` | Priority использует `/nodes` | реализован | PASS: прямой API запрос |

## Исправления на границе frontend/backend

1. Все реальные GID имеют 18 цифр и превышают `Number.MAX_SAFE_INTEGER`. Пример: `100000000011452100` после преобразования в JavaScript number становится `100000000011452096`. Внешний JSON и TypeScript теперь используют десятичные строки для GID, `topGid`, graph `source`/`target` и GID focus. Внутренние Parquet и SQLite сохраняют int64. Backend и frontend исправлены совместно; контракт обновлён в [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md#3-замороженный-контракт-summary).
2. Добавлен CORS для локальных origin `localhost:5173` и `127.0.0.1:5173`; браузерный preflight теперь проходит.
3. Frontend больше не посылает пустой `role=` на `/nodes`. Ранее это давало 422 на странице Priority с фильтром «All roles»; после правки страница показывает реальные 2248 записей.
4. Frontend в отсутствии `.env` теперь использует real API; демонстрационный режим включается только явно через `VITE_USE_MOCK_API=true`.

## Проверки

| Проверка | Результат |
|---|---|
| Чистота дерева до работы | PASS |
| Frontend `npm ci` | PASS: 112 packages, 0 vulnerabilities |
| Frontend TypeScript build под временным Node 22.23.2 | PASS |
| Frontend Vite production build под временным Node 22.23.2 | PASS |
| Backend `pytest -q` после правок | PASS: 79 tests, 1 warning о deprecation в Starlette TestClient |
| Backend pipeline на исходных Parquet | PASS: 2248 nodes, 3119 edges, 91 clusters, 2248 ranked nodes; SQLite и CSV созданы во временном каталоге |
| Реальный API через FastAPI TestClient | PASS: все 8 domain routes, 18-значный GID, граф 86 nodes/88 edges, cluster graph 277 nodes, 404/422 |
| CORS preflight и GET с Origin | PASS: `access-control-allow-origin: http://localhost:5173` |
| Frontend TypeScript и Vite production build | PASS под Node 22.23.2 |
| Chrome headless, real Dashboard | PASS: 2248 clients, 3119 relations, 91 clusters, top GID сохранён точно |
| Chrome headless, real Network GID | PASS: выбран исходный 18-значный GID, граф загрузился |
| Chrome headless, real Priority | PASS после исправления пустого role filter: 2248 matching nodes |
| Chrome headless, real Clusters | PASS: карточки кластеров загружены |
| Chrome headless, real cluster graph | PASS: кластер 0, 277 узлов |
| Chrome headless, real Priority details | PASS: карточка исходного 18-значного GID |
| Chrome headless, real role filter | PASS: coordinator без ошибки 422 |

Системный Node этой машины — 18.17.1; Vite требует 20.19+ или 22.12+. Для проверки использован временный Node 22.23.2. Единственный warning тестов касается установленной комбинации FastAPI/Starlette/httpx; тесты прошли. Browser smoke выполнен на локальных Vite и Uvicorn с реальным snapshot.

## Оставшиеся ограничения

- Системный Node 18 не подходит для локального `npm run dev/build`; разработчикам нужен Node 20.19+ или 22.12+.
- Автоматического интерактивного browser test suite в репозитории нет. Headless Chrome проверил отображение страниц, API и переход по URL, но не все действия мышью и клавиатурой.
- Backend snapshot надо создать командой из `backend/README.md` перед запуском API. Если его нет, API возвращает 503.
