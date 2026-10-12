
"""ЛР5. Зворотне виведення та підсистема пояснень.
Тема: Діагностика несправностей автомобіля.
Запуск: python3 src/inference.py
"""

HYPOTHESES = [
    ("H1", "двигун або автоматична коробка передач", "P", "R2"),
    ("H2", "кузовні системи", "B", "R3"),
    ("H3", "шасі", "C", "R4"),
    ("H4", "взаємодія електронних блоків", "U", "R5"),
]

RULES = {
    "R1": "Якщо отримано DTC, визначити ймовірну зону несправності.",
    "R2": "Якщо перша позиція DTC — P, зона: двигун або АКПП.",
    "R3": "Якщо перша позиція DTC — B, зона: кузовні системи.",
    "R4": "Якщо перша позиція DTC — C, зона: шасі.",
    "R5": "Якщо перша позиція DTC — U, зона: електронні блоки.",
}

COSTS = {
    "has_dtc": 1,
    "dtc_code": 2,
    "manufacturer": 3,
}

QUESTIONS = {
    "has_dtc": "Чи є зчитаний код DTC? (так/ні)",
    "dtc_code": "Введіть код DTC (наприклад, P0300)",
    "manufacturer": "Введіть виробника автомобіля",
}


class BackwardChainer:
    def __init__(self, ordered=True, answers=None):
        self.ordered = ordered
        self.answers = answers or {}
        self.known = {}
        self.trace = []
        self.questions = 0
        self.total_cost = 0
        self.fired = 0
        self.active_hypothesis = None
        self.proof = []
        self.result = None

    def why(self, parameter):
        hypothesis = self.active_hypothesis

        if hypothesis:
            hid, name, prefix, rule = hypothesis
            return (
                f"\nЧОМУ: Запит потрібен для перевірки "
                f"гіпотези {hid}: {name}.\n"
                f"Правило {rule}: {RULES[rule]}\n"
                f"Для перевірки потрібно встановити "
                f"наявність та першу позицію DTC.\n"
            )

        return (
            "\nЧОМУ: Для діагностики необхідно "
            "визначити наявність коду DTC.\n"
        )

    def ask(self, parameter):
        if parameter in self.known:
            return self.known[parameter]

        while True:
            if parameter in self.answers:
                value = str(self.answers[parameter]).strip()
            else:
                value = input(
                    f"\n{QUESTIONS[parameter]}\n"
                    "Відповідь (або 'чому'): "
                ).strip()

            if value.lower() == "чому":
                print(self.why(parameter))
                if parameter in self.answers:
                    raise ValueError("Некоректна тестова відповідь")
                continue

            if parameter == "has_dtc":
                if value.lower() not in ("так", "ні"):
                    print("Введіть 'так' або 'ні'.")
                    continue
                value = value.lower() == "так"

            elif parameter == "dtc_code":
                value = value.upper()
                if (
                    len(value) != 5
                    or value[0] not in "PBCU"
                    or not value[1:].isalnum()
                ):
                    print("Некоректний DTC. Приклад: P0300")
                    continue

            elif not value:
                print("Значення не може бути порожнім.")
                continue

            self.known[parameter] = value
            self.questions += 1
            self.total_cost += COSTS[parameter]

            self.trace.append(
                f"Запит: {parameter} = {value}; "
                f"вартість = {COSTS[parameter]}"
            )
            return value

    def prove(self, hypothesis):
        self.active_hypothesis = hypothesis
        hid, name, prefix, rule = hypothesis

        print(f"\nПеревірка {hid}: {name}")

        conditions = ["dtc_code", "has_dtc"]

        if self.ordered:
            conditions.sort(key=lambda p: COSTS[p])

        for parameter in conditions:
            value = self.ask(parameter)

            if parameter == "has_dtc" and not value:
                self.trace.append(
                    f"{hid} спростовано: DTC відсутній"
                )
                return False

            if parameter == "dtc_code":
                if value[0] != prefix:
                    self.trace.append(
                        f"{hid} спростовано: "
                        f"префікс {value[0]} не {prefix}"
                    )
                    return False

        code = self.known["dtc_code"]

        self.fired += 2

        self.proof = [
            f"Вхідний факт: DTC = {code}",
            f"Правило {rule}: {RULES[rule]}",
            f"Правило R1: {RULES['R1']}",
            f"Висновок: ймовірна зона — {name}",
        ]

        self.trace.extend(self.proof[1:])
        self.result = hypothesis
        return True

    def how(self):
        if not self.result:
            print("\nЯК: Підтвердженого висновку немає.")
            return

        print("\nПОЯСНЕННЯ «ЯК»:")
        print("-" * 55)

        for index, step in enumerate(self.proof, 1):
            print(f"{index}. {step}")

        print(
            "\nВажливо: DTC вказує на ймовірну зону "
            "несправності, а не на конкретну зламану деталь."
        )

    def show_trace(self):
        print("\nТРАСА ВИВЕДЕННЯ:")
        print("-" * 55)

        for index, step in enumerate(self.trace, 1):
            print(f"{index}. {step}")

    def summary(self):
        print("\nСТАТИСТИКА:")
        print(f"Спрацювало правил: {self.fired}")
        print(f"Запитів до користувача: {self.questions}")
        print(f"Сумарна вартість: {self.total_cost}")

    def run(self, verbose=True):
        if verbose:
            print("\nЛабораторна робота №5")
            print("Діагностика несправностей автомобіля")
            print(
                "Режим:",
                "з упорядкуванням" if self.ordered
                else "без упорядкування"
            )
            print("-" * 55)

        for hypothesis in HYPOTHESES:
            if self.prove(hypothesis):
                print(
                    "\nВИСНОВОК: Ймовірна зона "
                    f"несправності — {hypothesis[1]}."
                )

                code = self.known["dtc_code"]
                if code[1] in "12":
                    print(
                        "Увага: інтерпретація коду може "
                        "залежати від виробника автомобіля."
                    )

                if verbose:
                    self.how()
                    self.show_trace()
                    self.summary()

                return hypothesis

        print(
            "\nУсі гіпотези спростовано. "
            "Недостатньо даних для визначення "
            "зони несправності."
        )

        if verbose:
            self.show_trace()
            self.summary()

        return None


def experiment():
    print("\nПОРІВНЯЛЬНИЙ ЕКСПЕРИМЕНТ")
    print("Тестовий випадок: DTC = P0300")
    print("=" * 65)

    answers = {
        "has_dtc": "так",
        "dtc_code": "P0300",
    }

    results = []

    for ordered in (False, True):
        engine = BackwardChainer(
            ordered=ordered,
            answers=answers
        )

        result = engine.run(verbose=False)

        results.append({
            "mode": (
                "Зворотний з упорядкуванням"
                if ordered
                else "Зворотний без упорядкування"
            ),
            "rules": engine.fired,
            "questions": engine.questions,
            "cost": engine.total_cost,
            "result": result[1] if result else "Не визначено",
        })

        engine.show_trace()

    print("\nПІДСУМКОВА ТАБЛИЦЯ:")
    print("-" * 90)
    print(
        f"{'Режим':<35}"
        f"{'Правил':<10}"
        f"{'Запитів':<10}"
        f"{'Вартість':<10}"
        "Висновок"
    )
    print("-" * 90)

    for item in results:
        print(
            f"{item['mode']:<35}"
            f"{item['rules']:<10}"
            f"{item['questions']:<10}"
            f"{item['cost']:<10}"
            f"{item['result']}"
        )

    print(
        "\nПримітка: прямий ланцюг CLIPS "
        "запускається окремо на базі ЛР4."
    )


def main():
    print("=" * 55)
    print("ІНТЕЛЕКТУАЛЬНА ДІАГНОСТИКА АВТОМОБІЛЯ")
    print("Лабораторна робота №5")
    print("=" * 55)

    print("\nОберіть режим:")
    print("1 — Інтерактивна діагностика")
    print("2 — Порівняльний експеримент")
    print("3 — Діагностика без упорядкування")

    choice = input("\nВаш вибір: ").strip()

    if choice == "1":
        BackwardChainer(ordered=True).run()
    elif choice == "2":
        experiment()
    elif choice == "3":
        BackwardChainer(ordered=False).run()
    else:
        print("Некоректний вибір режиму.")


if __name__ == "__main__":
    main()
