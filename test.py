import pytest
from main import read_csv_files, calculate_median_report

# Наборы файлов для тестирования
@pytest.mark.parametrize("files,expected_students,expected_top_student,expected_top_median", [
    # Тест 1: Только math.csv
    (
            ['testing/math2.csv'],
            ['Артем Белов', 'Вера Сокол', 'Олег Мороз'],
            'Олег Мороз',
            600
    ),

    # Тест 2: math.csv + physics.csv
    (
            ['testing/math2.csv', 'testing/physics2.csv'],
            ['Артем Белов', 'Вера Сокол', 'Олег Мороз'],
            'Артем Белов',
            510
    ),

    # Тест 3: Все файлы кроме history
    (
            ['testing/math2.csv', 'testing/physics2.csv', 'testing/prog2.csv', 'testing/english.csv'],
            ['Артем Белов', 'Вера Сокол', 'Олег Мороз', 'Нина Климова', 'Юрий Лесной'],
            'Олег Мороз',
            600
    ),
])
def test_different_file_sets(files, expected_students, expected_top_student, expected_top_median):

    # Читаем файлы
    student_spending = read_csv_files(files)

    # Формируем отчёт
    results = calculate_median_report(student_spending)

    # Проверяем количество студентов
    assert len(results) == len(expected_students)

    # Проверяем имена всех студентов
    result_names = [r['student'] for r in results]
    for name in expected_students:
        assert name in result_names

    # Проверяем первого студента (с максимальной медианой)
    assert results[0]['student'] == expected_top_student
    assert results[0]['median_coffee'] == expected_top_median


# Отдельные тесты для каждого набора

def test_math_and_physics():
    """math.csv + physics.csv"""
    student_spending = read_csv_files(['testing/math2.csv', 'testing/physics2.csv'])
    results = calculate_median_report(student_spending)

    # Всё те же 3 студента, но с новыми тратами
    assert len(results) == 3

    for r in results:
        if r['student'] == 'Артем Белов':
            # [450,500,520,580] -> медиана (500+520)/2 = 510
            assert r['median_coffee'] == 510
        elif r['student'] == 'Вера Сокол':
            # [200,250,320] -> медиана 250
            assert r['median_coffee'] == 250
        elif r['student'] == 'Олег Мороз':
            # [600,380,420] -> медиана 420
            assert r['median_coffee'] == 420


def test_history():
    "тест history.csv"
    files = ['testing/history.csv']
    student_spending = read_csv_files(files)
    results = calculate_median_report(student_spending)

    # Должно быть 3 cтудента
    assert len(results) == 3

    # Проверяем порядок сортировки (по убыванию медианы)
    expected_order = ['Олег Мороз', 'Артем Белов', 'Вера Сокол']
    for i, expected_name in enumerate(expected_order):
        assert results[i]['student'] == expected_name

    # Проверяем конкретные медианы
    expected_medians = {
        'Олег Мороз': 680,  # [680] -> 680
        'Артем Белов': 500,  # [480,520] -> 500
        'Вера Сокол': 295,  # [280, 310] -> 295
    }

    for r in results:
        assert r['median_coffee'] == expected_medians[r['student']]


# Протестируем с помощью фикстуры
@pytest.fixture
def english_and_history_test():
    """Фикстура с данными из history.csv и english.csv"""
    return read_csv_files(['testing/english.csv', 'testing/history.csv'])

def test_with_fixture_english_and_history(english_and_history_test):
    """Используем фикстуру math_data"""
    results = calculate_median_report(english_and_history_test)

    # Должно быть 5 студентов
    assert len(results) == 5
    assert results[0]['student'] == 'Олег Мороз'
