# MoneyGraph: подробные промпты для шести глав фронтенда

Каждый раздел ниже можно передать coding agent как самостоятельное задание. Перед работой агент обязан прочитать `FRONTEND_PLAN.md`, `INTEGRATION_PLAN.md`, `frontend/README.md`, проверить `git status` и сохранить чужие изменения. Рабочая папка — `frontend/`; существующий Vite-проект не пересоздавать.

## Промпт 1 — Foundation / MVP Skeleton

> Проверь и доведи до готовности основу MoneyGraph на React + TypeScript + Vite. Сохрани существующий стек: React Router, Axios, SCSS, Cytoscape.js. Не добавляй UI-фреймворки или state manager.
>
> Обеспечь маршруты `/dashboard`, `/network`, `/priority`, `/clusters`, `/methodology`, `/data-limitations`; `/` должен перенаправлять на `/dashboard`, неизвестный URL — безопасно возвращать на Dashboard. Общий `AppLayout` должен сохранять Sidebar и Header при смене страниц, загрузке и ошибке. Активный пункт навигации должен быть визуально и семантически различим.
>
> Реализуй поиск GID в Header: принимай только целое неотрицательное число, показывай inline-ошибку для другого ввода и переходи на `/network?gid={gid}`. Проверь submit клавишей Enter и доступное имя кнопки. Сохрани компоненты `StatCard`, `Loader`, `EmptyState`, `ErrorState` и общие SCSS-переменные. Макет должен работать при 1366×768 и узкой ширине без горизонтального разрушения основного layout.
>
> Gate: выполни `npm ci` и `npm run build`; вручную пройди шесть маршрутов, redirect, active nav, числовой и нечисловой поиск, Tab/Enter навигацию. Исправь найденные ошибки. В отчёте укажи команды, изменённые файлы и непроверенные браузерные пункты.

## Промпт 2 — Overview Dashboard и API foundation

> Реализуй Dashboard строго по контракту `GET /api/v1/summary` из `INTEGRATION_PLAN.md`. Внешний JSON использует `camelCase`: `totalNodes`, `totalEdges`, `totalTransactions`, `totalSeeds`, `totalClusters`, `roles`, `topNodes`, `topClusters`. Добавь точные TypeScript DTO. Странице запрещено вызывать Axios напрямую.
>
> Создай `getSummary()` в service layer. `VITE_API_URL` уже содержит `/api/v1`. Добавь `VITE_USE_MOCK_API`; mock fixture держи отдельно от UI, возвращай через Promise и явно помечай экран как demonstration data. Значение `false` должно включать HTTP без изменений страницы. Создай переиспользуемый hook с `data`, `loading`, `error`, `refetch`, защищённый от обновления state после unmount.
>
> Покажи KPI Clients, Relations, Seed clients, Clusters и число транзакций. Добавь шесть полос ролей в фиксированном порядке, максимум пять priority nodes и три clusters. Узел ведёт на `/network?gid=...`, кластер — `/network?cluster=...`, полный рейтинг — `/priority`. Форматирование числа, KZT и score вынеси в utils. Score оставь в шкале 0..1 и показывай с двумя знаками.
>
> Реализуй четыре состояния: loading без фальшивых нулей, success, empty при `totalNodes === 0`, error с retry. Gate: `npm run build`, сверка каждого поля с контрактом, mock-переходы и keyboard navigation. Если `/summary` на backend отсутствует, real mode отметь `NOT VERIFIED`.

## Промпт 3 — Network Graph

> Реализуй локальный направленный граф Cytoscape для `/network?gid={id}` и `/network?cluster={id}`. Сохраняй смысл query при обновлении страницы. Без параметра покажи инструкцию, с нечисловым параметром — validation error, с неизвестным идентификатором — понятную ошибку.
>
> Используй frontend DTO `GraphResponse`: `focus { type, id }`, `nodes[] { gid, role, roleScore, priorityScore, clusterId, isSeed, depth }`, `edges[] { source, target, sumKzt, transactionCount }`, `truncatedAtDepth`. Сервисы вызывают `/nodes/{gid}/graph` или `/clusters/{clusterId}/graph`; mock находится в service layer. Этот DTO считается frontend-кандидатом до согласования с backend/OpenAPI.
>
> Рисуй стрелку строго `source → target`, окрашивай узлы по шести ролям, выделяй seed и выбранный узел. По клику покажи GID, роль, role score, priority score, cluster и depth. При `truncatedAtDepth = 4` выведи предупреждение, что граница наблюдения не доказывает остановку средств. Не загружай всю сеть стартовым экраном. Добавь loading, empty, error/retry. Загружай Cytoscape отдельным route chunk.
>
> Gate: `npm run build`; проверить известный mock GID `1001`, неизвестный GID, cluster `1`, invalid query, reload URL, направление стрелок, выбор узла, отсутствие зависания.

## Промпт 4 — Priority и Node Details

> Реализуй ранжированный список узлов и детали выбранного узла. Все параметры храни в URL: `page`, `search`, `role`, `gid`. Запрос списка должен поддерживать server pagination по 20 записей. Порядок: `priorityScore DESC`, tie-breaker `gid ASC`. Изменение фильтра сбрасывает страницу на первую.
>
> Используй frontend DTO `NodeListResponse { items, page, pageSize, total }` и `NodeDetails` с GID, ролью, role/priority scores, cluster, seed/depth, evidence, in/out degree, in/out KZT и transaction count. Сервис работает с `/nodes` и `/nodes/{gid}`; до согласования backend это frontend-кандидат. Mock должен давать больше 20 записей, чтобы проверить следующую страницу и отсутствие дублей.
>
> В таблице покажи ключевые поля, роль цветом и ссылку на `/network?gid=...`. Клик по GID открывает доступную detail panel. Evidence опиши как объяснение вычисленных сигналов, не обвинение. Явно напиши, что priority score является очередью проверки, а не вероятностью преступления. Обработай loading, empty, error/retry и неизвестный GID.
>
> Gate: `npm run build`; проверить страницы 1/2, back/forward URL state, GID search, все role filters, unknown GID, переход в граф, score с двумя знаками.

## Промпт 5 — Clusters, Methodology, Data limitations

> Реализуй список кластеров через `/clusters` и кандидаты DTO `ClusterListResponse` / `ClusterDetails`: `clusterId`, `nodeCount`, `seedCount`, `internalVolumeKzt`, nullable `topGid`, `hypothesis`, `description`. Карточка показывает все поля и ведёт на `/network?cluster={clusterId}`. Добавь loading, empty, error/retry и mock marker.
>
> На Methodology объясни шесть ролей, различие `roleScore` и `priorityScore`, порядок аналитической работы и необходимость человеческой проверки. Не заявляй точность, которой нет, и не описывай score как вероятность преступления.
>
> На Data limitations явно укажи: июль 2026; порог переводов ≥5 000 KZT; 81 seed; наблюдение исходящих переводов; глубина четыре хопа; нет ground-truth labels; отсутствующее ребро не доказывает отсутствующую реальную связь. Информация должна легко читаться на 1366×768 и мобильной ширине.
>
> Gate: `npm run build`; проверить карточки, KZT, nullable top GID, cluster links, полноту шести ограничений и отсутствие недоказанных утверждений. Сумму размеров кластеров сверять с summary только после появления согласованного backend snapshot.

## Промпт 6 — Финальная проверка и передача

> Выполни чистую проверку frontend на поддерживаемом Node.js: `npm ci`, затем `npm run build`. Исправь TypeScript, Sass и bundle-проблемы. Раздели маршруты на lazy chunks, если тяжёлый Cytoscape попадает в стартовый bundle.
>
> В mock mode пройди `/dashboard`, `/network?gid=1001`, `/network?gid=999999`, `/network?cluster=1`, `/priority`, `/priority?page=2`, `/clusters`, `/methodology`, `/data-limitations`. Проверь loading/success/empty/error там, где fixture позволяет состояние, retry, back/forward, refresh, Tab/Enter и ширину 1366×768.
>
> В real mode выключи `VITE_USE_MOCK_API`, сравни реальные JSON с TypeScript DTO и OpenAPI поле в поле: casing, типы, nullability, query, pagination, 404/422. Не записывай `PASS`, если endpoint отсутствует. В таком случае укажи `NOT VERIFIED` и точную причину.
>
> Подготовь отчёт: завершённые главы, файлы, команды и фактический вывод, endpoint/DTO, mock или real mode, проверенные UI states, известные проблемы. Не называй mock успешной backend-интеграцией.
