import argparse
import csv
from statistics import median
from collections import defaultdict
from tabulate import tabulate

def read_csv_files(file_paths):
    """Чтение CSV файлов и сбор трат на кофе по студентам"""
    student_spending = defaultdict(list)
    try:
        for file_path in file_paths:
            with open(file_path, 'r', encoding='utf-8') as f:
                # Читаем заголовки
                reader = csv.DictReader(f)
                for row in reader:
                    student = row['student'].strip()
                    try:
                        coffee_spent = int(row['coffee_spent'])
                        student_spending[student].append(coffee_spent)
                    # Если не можем преобразовать coffe_spent в int, либо такая колонка отсутсвует
                    except (ValueError, KeyError):
                        continue
        return student_spending
    except:
        print("Не удалось прочитать ваши файлы")
        return None


def calculate_median_report(student_spending):
    """Расчёт медианных трат и сортировка"""
    results = []
    for student, spending in student_spending.items():
        if spending:  # только если есть данные
            results.append({
                'student': student,
                'median_coffee': median(spending)
            })
    # Сортируем по убыванию медианы
    results.sort(key=lambda x: x['median_coffee'], reverse=True)
    return results


def main():
    # Допустимые отчеты
    AVAILABLE_REPORTS = {
        'median-coffee': calculate_median_report,
    }

    # Создание необходимых флагов
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', nargs='+', required=True)
    parser.add_argument('--report', required=True)
    args = parser.parse_args()

    # Проверяем допустим ли отчет
    if args.report not in AVAILABLE_REPORTS:
        print(f"Ошибка: отчёт '{args.report}' не поддерживается")
        print(f"Доступные отчёты: {', '.join(AVAILABLE_REPORTS.keys())}")
        return

    # Читаем данные
    student_spending = read_csv_files(args.files)

    if not student_spending:
        print("Нет данных для обработки")
        return

    # Строим отчет на основе флага --report
    report_function = AVAILABLE_REPORTS[args.report]
    results = report_function(student_spending)

    # Выводим таблицу
    table_data = [[r['student'], r['median_coffee']] for r in results]
    print(tabulate(table_data, headers=['student', 'median_coffee'], tablefmt='grid'))

if __name__ == '__main__':
    main()