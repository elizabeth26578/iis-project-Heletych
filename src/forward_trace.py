
import clips
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
rules_path = project_root / "knowledge" / "rules.clp"

env = clips.Environment()
env.load(str(rules_path))
env.reset()

print("ЛАБОРАТОРНА РОБОТА №5")
print("КРОК 1. ПРЯМИЙ ЛАНЦЮГ ВИВЕДЕННЯ")
print("-" * 60)

initial_facts = list(env.facts())
trace = []

while True:
    activations = list(env.activations())

    if not activations:
        break

    rule_name = activations[0].name
    before = {f.index: str(f) for f in env.facts()}

    fired = env.run(1)

    if fired == 0:
        break

    after = {f.index: str(f) for f in env.facts()}
    new_facts = [
        value for index, value in after.items()
        if index not in before
    ]

    trace.append((rule_name, new_facts))

    print(f"\nКрок {len(trace)}")
    print(f"Спрацювало правило: {rule_name}")

    if new_facts:
        for fact in new_facts:
            print(f"Новий факт: {fact}")
    else:
        print("Нових фактів немає")

print("\n" + "=" * 60)
print("ПІДСУМКИ ПРЯМОГО ВИВЕДЕННЯ")
print("=" * 60)

print(f"Спрацювало правил: {len(trace)}")
print(
    "Породжено фактів:",
    sum(len(facts) for _, facts in trace)
)

print("\nФакти після виконання:")
for fact in env.facts():
    print(fact)
    
