String formatName(String name, String lastName, [String? patronymic]) {
  return '$lastName $name ${patronymic ?? ''}';
}

num? calculate(num a, num b, String operation) {
  switch (operation) {
    case '+':
      return a + b;
    case '-':
      return a - b;
    case '*':
      return a * b;
    case '/':
      if (b == 0) return null;
      return a / b;
    default:
      return null;
  }
}

void countSigns(List<int> numbers) {
  int positiveCount = 0, negativeCount = 0, zeroCount = 0;

  for (var number in numbers) {
    if (number > 0) {
      positiveCount++;
    } else if (number < 0) {
      negativeCount++;
    } else {
      zeroCount++;
    }
  }

  print('Положительных: $positiveCount');
  print('Отрицательных: $negativeCount');
  print('Нулевых: $zeroCount');
}

List<int> transformList(List<int> list, int Function(int) transformer) =>
  list.map(transformer).toList();

int sumDigits(int n) {
  if (n < 10) {
    return n;
  }
  return (n % 10) + sumDigits(n ~/ 10);
}

void main() {
  print('Задача 1:');
  print(formatName('Иван', 'Иванов'));
  print(formatName('Иван', 'Иванов', 'Иванович'));

  print('Задача 2:');
  print('1 + 2 = ${calculate(1, 2, '+')}');
  print('1 - 2 = ${calculate(1, 2, '-')}');
  print('1 * 2 = ${calculate(1, 2, '*')}');
  print('1 / 2 = ${calculate(1, 2, '/')}');
  print('1 / 0 = ${calculate(1, 0, '/')}');
  print('1 q 0 = ${calculate(1, 0, 'q')}');

  print('Задача 3:');
  countSigns([-2, -1, 0, 1, 2]);

  print('Задача 4:');
  List<int> origList = [1, 2, 3, 4];
  List<int> newList = transformList(origList, (x) => x + 1);
  print('$origList -> $newList');

  print('Задача 5:');
  print('Сумма цифр 1: ${sumDigits(1)}');
  print('Сумма цифр 123: ${sumDigits(123)}');
}