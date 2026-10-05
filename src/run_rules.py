import clips
from pathlib import Path


def main():
    env = clips.Environment()

    project_root = Path(__file__).resolve().parent.parent
    rules_path = project_root / "knowledge" / "rules.clp"

    print("Лабораторна робота №4")
    print("Тема: Діагностика несправностей автомобіля")
    print("-" * 60)

    try:
        env.load(str(rules_path))
        print("Базу знань успішно завантажено.")

        env.reset()

        print("\nПочаткові факти:")
        print("-" * 60)

        for fact in env.facts():
            print(fact)

        print("\nРезультат роботи продукційної системи:")
        print("-" * 60)

        fired = env.run()

        print("-" * 60)
        print(f"Кількість спрацювань правил: {fired}")

        print("\nФакти після виконання правил:")
        print("-" * 60)

        for fact in env.facts():
            print(fact)

    except clips.CLIPSError as error:
        print("Помилка CLIPS:")
        print(error)


if __name__ == "__main__":
    main()