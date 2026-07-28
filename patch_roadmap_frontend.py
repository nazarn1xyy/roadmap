#!/usr/bin/env python3
"""
patch_roadmap_frontend.py
Обновляет ТОЛЬКО frontend-таски в Supabase (tasks_state, id=1).
Существующие backend-таски сохраняются без изменений.
"""
import urllib.request
import json

SUPABASE_URL = "https://iiksxgmckztwptwcftok.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlpa3N4Z21ja3p0d3B0d2NmdG9rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODQ1NDA2MDksImV4cCI6MjEwMDExNjYwOX0.hzh4npHyquBhnrsKmraiJYESmzQ_Xb1m0iARQGmNwDQ"

NEW_FRONTEND = [
    {
        "week": 1,
        "title": "Критичні баги в нещодавніх фічах",
        "dates": "20 лип. — 26 лип.",
        "tasks": [
            {"day": "Пн, 28.07", "text": "[БАГ] TeacherDashboardPage: підключити дані розкладу з useTeacherDashboardQuery(data.todaySchedule). Зараз хардкод 'Немає занять'.", "done": False},
            {"day": "Вт, 29.07", "text": "[БАГ] TeacherDashboardPage: відобразити реальні групи з useGroupsQuery() замість хардкоду. Підключити блок оголошень.", "done": False},
            {"day": "Ср, 30.07", "text": "[БАГ] TeacherDashboardPage: замінити mockActivityData на реальні дані здачі робіт з API.", "done": False},
            {"day": "Чт, 31.07", "text": "[БАГ] TestPassingPage: прибрати MOCK_DEMO_QUESTIONS — якщо API повернув [] показати EmptyState, не демо-тест.", "done": False},
            {"day": "Пт, 01.08", "text": "[БАГ] TestPassingPage: результат — не рахувати локальний mockCorrect якщо resultData.score undefined. Показати 'Результат обробляється...'.", "done": False},
            {"day": "Сб, 02.08", "text": "[БАГ] GradebookPage: прибрати mock-fallback студентів/курсів/груп. Якщо API повертає [] — EmptyState.", "done": False},
            {"day": "Нд, 03.08", "text": "Резервний день / ревʼю виправлених багів тижня 1.", "done": False}
        ]
    },
    {
        "week": 2,
        "title": "Інтеграція API та підготовка контрактів",
        "dates": "27 лип. — 02 серп.",
        "tasks": [
            {"day": "Пн, 04.08", "text": "[ФРОНТ-КОНТРАКТ] ChatPage: прибрати BYPASS BACKEND. Відновити перевірку ключів через API. Додати стан 'locked' якщо ключ є в БД але не в sessionStorage.", "done": False},
            {"day": "Вт, 05.08", "text": "StudentSchedulePage: додати Select вибору групи з useGroupsQuery() замість хардкоду 'g1'. Skeleton-loader.", "done": False},
            {"day": "Ср, 06.08", "text": "GradebookPage: Select семестру (1/2) при додаванні колонки замість хардкоду '1'. Середній бал у рядку студента.", "done": False},
            {"day": "Чт, 07.08", "text": "[ФРОНТ-КОНТРАКТ] Типізувати TeacherDashboardResponse: { todaySchedule, groups, announcements } в useQueries.ts. Прибрати 'as any'.", "done": False},
            {"day": "Пт, 08.08", "text": "[ФРОНТ-КОНТРАКТ] Типізувати відповідь API сторінок: замінити (remotePage as any) у AboutPageEditor та DynamicPageEditor на нормальний PageResponse.", "done": False},
            {"day": "Сб, 09.08", "text": "ReportsPage: skeleton-loader, EmptyState, типізувати ReportItem. Перевірити disabled на кнопці якщо report.url відсутній.", "done": False},
            {"day": "Нд, 10.08", "text": "Резервний день.", "done": False}
        ]
    },
    {
        "week": 3,
        "title": "Offline UI, доступність, Edge Cases",
        "dates": "03 серп. — 09 серп.",
        "tasks": [
            {"day": "Пн, 11.08", "text": "Додати OfflineIndicator компонент (banner) який зʼявляється при window offline/online events. Підключити до StudentLayout та TeacherLayout.", "done": False},
            {"day": "Вт, 12.08", "text": "Зробити offline-fallback сторінку PWA: при відкритті некешованого маршруту офлайн показати '/offline.html' замість браузерної помилки.", "done": False},
            {"day": "Ср, 13.08", "text": "QA адаптиву GradebookPage на Mobile: горизонтальний скрол таблиці, ширина MOBILE_COL_WIDTH, touch-взаємодія з клітинками.", "done": False},
            {"day": "Чт, 14.08", "text": "A11y: перевірити aria-labels у модалках TestConstructorPage та TestPassingPage. Додати role='dialog', aria-modal, focus trap.", "done": False},
            {"day": "Пт, 15.08", "text": "QA темної/світлої теми: знайти hardcoded кольори (не з tokens). GradebookPage solidBg, AboutPageEditor.", "done": False},
            {"day": "Сб, 16.08", "text": "Lighthouse A11y audit (ціль 90+). Виправити проблеми з контрастністю та відсутніми label.", "done": False},
            {"day": "Нд, 17.08", "text": "Резервний день.", "done": False}
        ]
    },
    {
        "week": 4,
        "title": "Тестування та Полірування",
        "dates": "10 серп. — 16 серп.",
        "tasks": [
            {"day": "Пн, 18.08", "text": "Написати Vitest unit-тести: formatDate, formatFullName, isPast. Тест для useAuth (mock store). Ціль: 15+ тестів.", "done": False},
            {"day": "Вт, 19.08", "text": "Lighthouse Performance (ціль 90+). Lazy-loading Recharts якщо не зроблено. Перевірити preload критичних ресурсів.", "done": False},
            {"day": "Ср, 20.08", "text": "E2E User Flow: Студент → Вхід → Тест → Відповідь → Результат. Записати баги як окремі таски.", "done": False},
            {"day": "Чт, 21.08", "text": "Виправлення TypeScript warnings та ESLint помилок ('as any' в StudentDashboardPage, ContactsPageEditor).", "done": False},
            {"day": "Пт, 22.08", "text": "Фінальна перевірка збірки: tsc -b && vite build. Перевірити розмір чанків, circular imports.", "done": False}
        ]
    },
    {
        "week": 5,
        "title": "Реліз",
        "dates": "17 серп. — 25 серп.",
        "tasks": [
            {"day": "Сб, 23.08", "text": "UAT тестування з бекендером. Staging deploy. Список блокерів для prod.", "done": False},
            {"day": "Нд, 24.08", "text": "Code Freeze. Тільки хотфікси P0. Оновити README.", "done": False},
            {"day": "Пн, 25.08", "text": "Фінальна перевірка prod-збірки. Smoke test основних user flows на production URL.", "done": False},
            {"day": "Вт, 26.08", "text": "🚀 РЕЛІЗ. Запуск PortalMPMEK в production.", "done": False}
        ]
    }
]


def get_current_state():
    url = f"{SUPABASE_URL}/rest/v1/tasks_state?id=eq.1&select=state"
    req = urllib.request.Request(url, headers={
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
    })
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    return data[0]["state"] if data else {}


def update_state(state):
    body = json.dumps({"state": state}).encode("utf-8")
    url = f"{SUPABASE_URL}/rest/v1/tasks_state?id=eq.1"
    req = urllib.request.Request(
        url, data=body, method="PATCH",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        }
    )
    with urllib.request.urlopen(req) as resp:
        print(f"HTTP {resp.status} — Updated!")


def main():
    print("Fetching current state from Supabase...")
    state = get_current_state()
    print(f"Current frontend weeks: {len(state.get('frontend', []))}")
    print(f"Current backend weeks: {len(state.get('backend', []))}")
    state["frontend"] = NEW_FRONTEND
    print("Uploading new frontend tasks...")
    update_state(state)
    print("Done! Frontend roadmap updated in Supabase.")
    total = sum(len(w["tasks"]) for w in NEW_FRONTEND)
    print(f"Total weeks: {len(NEW_FRONTEND)}, Total tasks: {total}")


if __name__ == "__main__":
    main()
