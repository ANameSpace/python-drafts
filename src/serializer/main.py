import csv, json

def task_1() -> None:
    with (open("t1/animals.csv", 'r', encoding='utf-8', newline='') as csv_file,
          open("t1/zoo.json", 'w', encoding='utf-8') as json_file):
        json.dump(list(csv.DictReader(csv_file)), json_file, ensure_ascii=False, indent=2)

salary: dict[str, int] = {"Разработчик": 120_000, "Менеджер": 100_000, "Дизайнер": 90_000}
def task_2() -> None:
    with (open("t2/csv_file.csv", 'r', encoding='utf-8', newline='') as original_file,
          open("t2/employees_with_salary.csv", 'w', encoding='utf-8', newline='') as new_file):
        r = csv.DictReader(original_file); w = csv.DictWriter(new_file, fieldnames=r.fieldnames + ['Зарплата'])
        w.writerows({**row, 'Зарплата': salary.get(row['Должность'], 0)} for row in r)

task_1() # 1.5
task_2() # 2.2