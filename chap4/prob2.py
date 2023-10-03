import random

hero_hp = random.randrange(50, 101)
monster_hp = random.randrange(50, 101)
count = 0

while hero_hp > 0 and monster_hp > 0:
    count += 1
    hero_attack = random.randrange(-10, 40)
    monster_attack = random.randrange(-10, 40)

    hero_success = random.choice([True, False])
    monster_success = random.choice([True, False])

    # 전투 메시지 문자열 생성
    hero_message = f"hero(HP:{hero_hp}, attack:{hero_attack}) {'success' if hero_success else 'fail'}"
    monster_message = f"monster(HP:{monster_hp}, attack:{monster_attack}) {'success' if monster_success else 'fail'}"

    # 전투 메시지 출력
    print(hero_message + " <-> " + monster_message)

    if hero_success:
        monster_hp -= max(0, hero_attack)
    if monster_success:
        hero_hp -= max(0, monster_attack)
print("------------------------------------------------------------------")
count = str(count)
if hero_hp <= 0:
    print(count + "번의 전투 진행\nmonster 승리!")
elif monster_hp <= 0:
    print(count + "번의 전투 진행\nhero 승리!")
