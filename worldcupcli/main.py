#===========================
# دانشجو: سید امیرسام حسینی غنچه
# شماره دانشجویی: 404130613
# عنوان پروژه: شبیه ساز جام جهانی
# تاریخ تحویل: ۱۴۰۵/۰۴/۲۷
#===========================


from classes.Colors import Colors
from classes.WorldCupSimulator import WorldCupSimulator


def main():
    sim = WorldCupSimulator()

    while True:
        print("\n=============== World Cup Simulator ===============")
        print("[1]: Load teams from CSV")
        print("[2]: Draw groups (automatic seeding)")
        print("[3]: Run group stage and display standings")
        print("[4]: Run full simulation (group + knockout) and display champion")
        print("[5]: Simulate 1000 times and report championship percentages")
        print("[6]: Display bracket of last simulation")
        print("[7]: Exit")
    
        choice = input("\nEnter your choice: ").strip()

        if choice == '1':
            filename = 'worldcup_2026_teams.csv' # The given file name - replace it with your own filename if needed.
            try:
                sim.load_teams_from_csv(filename)
                print(Colors.GREEN + f"{len(sim.teams)} teams loaded successfully from {filename}." + Colors.ENDC)
            except Exception as e:
                print(Colors.DANGER + f"Error: {e}" + Colors.ENDC)

        elif choice == '2':
            if not sim.teams:
                print(Colors.DANGER + f"Please load teams first (option 1)." + Colors.ENDC)
            else: 
                sim.seed_and_draw_groups()
                print(Colors.GREEN + "Group draw successfull." + Colors.ENDC)

        elif choice == '3':
            if not sim.groups:
                print(Colors.DANGER + "Please draw groups first (option 2)." + Colors.ENDC)
            else:
                sim.run_group_stage(should_print=True)

        elif choice == '4':
            if not sim.teams:
                print(Colors.DANGER + "Please load teams first (option 1)." + Colors.ENDC)
            else:
                sim.run_full_simulation()

        elif choice == '5':
            if not sim.teams:
                print(Colors.DANGER + "Please load teams first (option 1)." + Colors.ENDC)
            else:
                n = 1000
                sim.most_likely_champion(n)

        elif choice == '6':
            if not sim.round_of_16:
                print(Colors.DANGER + "Please run a full simulation first (option 4)." + Colors.ENDC)
            else:
                sim.display_bracket()

        elif choice == '7':
            break

        else:
            print(Colors.WARNING + "Invalid option." + Colors.ENDC)


if __name__ == "__main__":
    main()