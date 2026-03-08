class MarksBook {
  final List<String> students = [];
  final List<String> subjects = [];
  final List<List<int>> marks = [];

  MarksBook() {
    students.addAll(['Студент 1', 'Студент 2', 'Студент 3']);
    subjects.addAll(['Русский язык', 'Математика']);
    marks.addAll([
      [5, 5],
      [4, 3],
      [3, 2],
    ]);
  }

  Map<String, double> getAverageMarks() => Map.fromIterables(
    students,
    marks.map((studentMarks) => studentMarks.fold(0.0, (total, mark) => total + mark) / studentMarks.length),
  );

  Map<int, int> countMarks() => marks
    .expand((g) => g)
    .fold(<int, int>{}, (map, grade) {
      map[grade] = (map[grade] ?? 0) + 1;
      return map;
  });

  Map<String, List<String>> getSubjectWithStudentsByMark(int mark) => Map.fromIterables(
    subjects,
    List.generate(subjects.length, (subjectIndex) => [
      for (int i = 0; i < students.length; i++)
        if (marks[i][subjectIndex] == mark) students[i],
    ]),
  );

  ({int count, List<String> names}) getTopStudentsWithMark(int mark) {
    final counts = {
      for (var i = 0; i < students.length; i++)
        students[i]: marks[i].where((element) => element == mark).length,
    };
    final max = counts.values.fold(0, (a, b) => a > b ? a : b);
    return (
      count: max, 
      names: counts.entries
        .where((e) => e.value == max)
        .map((e) => e.key)
        .toList()
    );
  }

  Map<String, List<String>> getStudentWithSubjectsByCondition(
    bool Function(int mark) func,
  ) => {
    for (var i = 0; i < students.length; i++)
      students[i]: [
        for (var j = 0; j < subjects.length; j++)
          if (func(marks[i][j])) subjects[j],
      ],
  };

  List<({String student, String subject})> getPairsByMark(int mark) => [
    for (var i = 0; i < students.length; i++)
      for (var j = 0; j < subjects.length; j++)
        if (marks[i][j] == mark) (student: students[i], subject: subjects[j]),
  ];
}



void main() {
  final marksBook = MarksBook();

  // Разделить студентов на три категории по среднему баллу: отличники (средний ≥ 4.5), хорошисты (средний от 3.5 до 4.5), остальные — и вывести для каждой категории список имён.
  print('Задание 1');
  var data1 = marksBook.getAverageMarks().entries.fold(
    (group1: <String>[], group2: <String>[], group3: <String>[]),
    (acc, entry) => switch (entry.value) {
      >= 4.5 => (group1: [...acc.group1, entry.key], group2: acc.group2, group3: acc.group3),
      >= 3.5 => (group1: acc.group1, group2: [...acc.group2, entry.key], group3: acc.group3),
      _      => (group1: acc.group1, group2: acc.group2, group3: [...acc.group3, entry.key]),
    },
  );
  print('отличники ${data1.group1.join(', ')}');
  print('хорошисты ${data1.group2.join(', ')}');
  print('остальные ${data1.group3.join(', ')}');


  // Подсчитать и вывести, сколько раз в журнале встречается каждая оценка (2, 3, 4, 5).
  print('Задание 2');
  for (int mark in [2, 3, 4, 5]) {
    print('$mark: ${marksBook.countMarks()[mark] ?? 0} раз');
  }

  // Для каждого предмета вывести список студентов, получивших по нему 5.
  print('Задание 3');
  marksBook.getSubjectWithStudentsByMark(5).forEach((subject, students) {
    print('$subject: ${students.isEmpty ? 'нет' : students.join(', ')}');
  });

  // Вывести предметы, по которым нет ни одной двойки.
  print('Задание 4');
  marksBook.getSubjectWithStudentsByMark(2).forEach((subject, students) {
    if (students.isEmpty) print(subject);
  });

  // Вывести предмет, по которому выставлено больше всего двоек (и количество двоек).
  print('Задание 5');
  var result5 = marksBook.getSubjectWithStudentsByMark(2).entries
      .fold(MapEntry<String, List<String>>('нет', []), (subject1, subject2) => subject1.value.length > subject2.value.length ? subject1 : subject2);
    print('Предмет ${result5.key} (${result5.value.length} двоек)');

  // Определить студента (или студентов) с наибольшим количеством пятёрок и вывести их имена и количество пятёрок.
  print('Задание 6');
  var data6 = marksBook.getTopStudentsWithMark(5);
  print('${data6.count}: ${data6.names.join(', ')}');


  // Для каждого студента при необходимости вывести количество предметов, по которым оценка ниже 4, и перечень этих предметов.
  print('Задание 7');
  marksBook.getStudentWithSubjectsByCondition((mark) => mark < 4).forEach((student, subject) {
    print('$student: ${subject.isEmpty ? 'нет' : subject.join(', ')}');
  });

  // Сформировать и вывести все пары «студент — предмет», по которым стоит 5.
  print('Задание 8');
  marksBook.getPairsByMark(5).forEach((pair) {
    print('${pair.student} - ${pair.subject}');
  });
}