from controllers.round_controller import enter_scores
from controllers.tournament_controller import create_tournament, launch_tournament
from views.views import show_tournament_sorted_results, show_tournament_current_rounds_list, show_main_menu, \
    show_database_menu

show_main_menu()
user_input = input("Quel est votre choix? ")
if user_input == "1":
    tournament1 = create_tournament()
    launch_tournament(tournament1)
elif user_input == "2":
    show_database_menu()
