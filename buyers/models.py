from otree.api import *
import pandas as pd
import os
import random

class C(BaseConstants):
    NAME_IN_URL = 'buyers'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 16
    endowment = 10
    good_item_bonus = 10
    bad_item_penalty = -5
    feedback_cost = -2
    number_items = 26

    # Experiment Conditions
    CONDITIONS = ['control', 'default', 'omitted']

    # File path for items
    CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), "items.csv")

    # Quiz questions
    QUESTION1 = 'How many points does it cost to leave a rating for an item?'
    QUESTION2 = 'How often can a good item turn out to be bad for you, or a bad item turn out to be good?'
    QUESTION3 = 'What happens if you select an item that has good quality?'
    QUESTION4 = 'What information do you have about the items before you make a choice?'
    QUESTION5 = 'How many times will you be presented with the same item?'
    QUESTION6 = 'What happens if you select an item that has poor quality?'
    QUESTION7 = 'What happens if you decide not to select an item?'
    QUESTION8 = 'How is quality of the item determined?'


class Subsession(BaseSubsession):
    def creating_session(self):
        try:
            items_df = pd.read_csv(C.CSV_FILE_PATH)
            if items_df.empty:
                raise Exception("Error: items.csv is empty.")
            self.session.vars['items'] = items_df.to_dict(orient='records')
        except FileNotFoundError:
            raise Exception(f"File not found: {C.CSV_FILE_PATH}. Ensure the items.csv file is correctly placed in /si.")

        random.shuffle(self.session.vars['items'])
        self.session.vars['seen_items'] = set()
        self.session.vars['group_item_history'] = {}
        self.session.vars['truly_seen_items'] = set()

        self.session.vars['item_rating_count'] = {item['id']: 0 for item in self.session.vars['items']}
        self.session.vars['positive_rating_count'] = {item['id']: 0 for item in self.session.vars['items']}
        self.session.vars['negative_rating_count'] = {item['id']: 0 for item in self.session.vars['items']}

        # Group assignment
        players = self.get_players()
        random.shuffle(players)
        group_size = 2 if len(players) % 2 == 0 else 3
        group_matrix = [players[i:i + group_size] for i in range(0, len(players), group_size)]
        self.set_group_matrix(group_matrix)

        for group_idx, group in enumerate(group_matrix):
            for player in group:
                player.participant.vars['group_id'] = group_idx
                if group_idx not in self.session.vars['group_item_history']:
                    self.session.vars['group_item_history'][group_idx] = set()

        # Condition assignment
        num_players = len(players)
        conditions = C.CONDITIONS * (num_players // len(C.CONDITIONS)) + C.CONDITIONS[:num_players % len(C.CONDITIONS)]
        random.shuffle(conditions)
        for i, player in enumerate(players):
            condition_sequence = random.sample(C.CONDITIONS, len(C.CONDITIONS))
            player.participant.vars['condition_sequence'] = condition_sequence

    def assign_items(self):
        players = self.get_players()
        available_groups = sorted(self.session.vars['group_item_history'].keys())
        if 0 not in available_groups:
            available_groups.insert(0, 0)

        assign_new_item = self.round_number in {1, 2, 3, 7, 8, 11, 12, 13}
        assign_seen_item = self.round_number in {4, 5, 6, 9, 10, 14, 15, 16}

        assigned_items = {}
        used_up_items = self.session.vars.get('used_up_items', set())
        already_assigned_seen_items = set()

        print(f"[DEBUG] Assigning {'NEW' if assign_new_item else 'SEEN'} items in round {self.round_number}")

        # Step 1: Determine available items
        if assign_new_item:
            available_items = [
                item for item in self.session.vars['items']
                if item['id'] not in self.session.vars['seen_items']
            ]
        elif assign_seen_item:
            available_items = [
                item for item in self.session.vars['items']
                if item['id'] in self.session.vars['truly_seen_items'] and item['id'] not in used_up_items
            ]

        random.shuffle(available_items)

        #Assign item to group
        for group_id in available_groups:
            print(f"[DEBUG] Assigning item to Group {group_id}")

            if group_id not in self.session.vars['group_item_history']:
                self.session.vars['group_item_history'][group_id] = set()

            assigned_item = None

            # Assign new items in new rounds
            if assign_new_item and available_items:
                assigned_item = available_items.pop(0)
                self.session.vars['seen_items'].add(assigned_item['id'])
                self.session.vars['group_item_history'][group_id].add(assigned_item['id'])
                print(f"[DEBUG] Group {group_id} assigned NEW item {assigned_item['id']}")

            # Assign seen items in seen rounds
            elif assign_seen_item:
                valid_seen_items = [
                    item for item in available_items
                    if item['id'] in self.session.vars['truly_seen_items']  # Item was seen
                       and item['id'] not in already_assigned_seen_items  # Ensure unique seen item per round
                       and item['id'] not in self.session.vars['group_item_history'][group_id]  # Group has not seen it
                ]

                if valid_seen_items:
                    assigned_item = valid_seen_items.pop(0)
                    self.session.vars['group_item_history'][group_id].add(assigned_item['id'])
                    already_assigned_seen_items.add(assigned_item['id'])  # Mark as assigned in this round
                    available_items = [item for item in available_items if
                                       item['id'] != assigned_item['id']]  # Remove globally
                    print(f"[DEBUG] Group {group_id} assigned SEEN item {assigned_item['id']}")

                    #the item has been seen twice
                    seen_count = sum(
                        assigned_item['id'] in history for history in self.session.vars['group_item_history'].values()
                    )
                    if seen_count >= 2:
                        used_up_items.add(assigned_item['id'])
                else:
                    print(f"[WARNING] No valid seen items left for Group {group_id}, assigning a new item instead.")
                    assign_new_item = True
                    assign_seen_item = False

            # Fallback: Assign a new item if no valid seen item was available
            if not assigned_item:
                fallback_items = [
                    item for item in self.session.vars['items']
                    if item['id'] not in self.session.vars['seen_items']
                ]
                if fallback_items:
                    assigned_item = fallback_items.pop(0)
                    self.session.vars['seen_items'].add(assigned_item['id'])
                    self.session.vars['group_item_history'][group_id].add(assigned_item['id'])
                    print(f"[DEBUG] Group {group_id} assigned UNIQUE NEW fallback item {assigned_item['id']}")
                else:
                    print(
                        f"[CRITICAL ERROR] No available items (new or seen) for Group {group_id} in round {self.round_number}")
                    assigned_item = random.choice(self.session.vars['items'])
                    self.session.vars['seen_items'].add(assigned_item['id'])
                    self.session.vars['group_item_history'][group_id].add(assigned_item['id'])
                    print(
                        f"[DEBUG] Emergency assignment: Group {group_id} assigned fallback item {assigned_item['id']}")

            assigned_items[group_id] = assigned_item

        #Assign Item to Player
        for player in players:
            group_id = player.participant.vars['group_id']
            assigned_item = assigned_items.get(group_id, None)

            if assigned_item:
                player.item_id = assigned_item['id']
                player.item_quality_original = assigned_item['quality']
                player.item_quality = assigned_item['quality']
                player.item_quality_flipped = False
                if random.random() < 0.2:
                    player.item_quality = not assigned_item['quality']
                    player.item_quality_flipped = True

                item_id = player.item_id
                player.num_ratings_per_item = self.session.vars['item_rating_count'].get(item_id, 0)
                player.num_positive_ratings = self.session.vars['positive_rating_count'].get(item_id, 0)
                player.num_negative_ratings = self.session.vars['negative_rating_count'].get(item_id, 0)

        self.session.vars['used_up_items'] = used_up_items

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    experimental_condition = models.StringField()
    condition_sequence = models.StringField()
    item_id = models.StringField()
    item_quality = models.BooleanField(choices=[[False, 'Bad'], [True, 'Good']])
    item_quality_original = models.BooleanField(choices=[[False, 'Bad'], [True, 'Good']])
    item_quality_flipped = models.BooleanField(initial=False)
    selected_item = models.BooleanField(blank=True)
    feedback = models.IntegerField(choices=[(1, 'Positive'), (-1, 'Negative'), (0, 'No Rating')], blank=True)
    default_feedback_changed = models.BooleanField(
        label="Do you want to change the automatic positive rating to a negative rating?",
        choices=[[True, "Yes"], [False, "No"]],
        initial=False)
    no_feedback_given = models.BooleanField(initial=False)
    earnings = models.IntegerField(initial=0)
    num_ratings_per_item = models.IntegerField(initial=0)
    num_positive_ratings = models.IntegerField(initial=0)
    num_negative_ratings = models.IntegerField(initial=0)
    num_ratings_given = models.IntegerField(initial=0)

    def set_experimental_condition(self):
        round_phase = 0 if self.round_number <= 6 else 1 if self.round_number <= 10 else 2
        self.experimental_condition = self.participant.vars['condition_sequence'][round_phase]
        self.condition_sequence = ','.join(self.participant.vars['condition_sequence'])

    def calculate_earnings(self):
        self.earnings = C.endowment

        if self.selected_item:
            self.earnings += C.good_item_bonus if self.item_quality else C.bad_item_penalty

        feedback = self.field_maybe_none('feedback')

        if self.experimental_condition in ['control', 'omitted']:
            if feedback in [1, -1]:
                self.earnings += C.feedback_cost
            elif self.experimental_condition == 'omitted' and feedback == 0:
                self.no_feedback_given = True

        elif self.experimental_condition == 'default':
            if self.field_maybe_none('default_feedback_changed') or False:
                self.earnings += C.feedback_cost

        #earnings accumulate across rounds
        self.participant.payoff += self.earnings

        if "earnings_part2" not in self.participant.vars:
            self.participant.vars["earnings_part2"] = 0

        self.participant.vars["earnings_part2"] += self.earnings

        # Update player’s personal rating count
        if feedback in [1, -1]:
            self.num_ratings_given += 1

            item_id = self.item_id  # The item they rated

            # Ensure the item exists in the session's tracking variables
            if item_id in self.session.vars['item_rating_count']:
                self.session.vars['item_rating_count'][item_id] += 1
            else:
                self.session.vars['item_rating_count'][item_id] = 1

            if feedback == 1:
                if item_id in self.session.vars['positive_rating_count']:
                    self.session.vars['positive_rating_count'][item_id] += 1
                else:
                    self.session.vars['positive_rating_count'][item_id] = 1
            elif feedback == -1:
                if item_id in self.session.vars['negative_rating_count']:
                    self.session.vars['negative_rating_count'][item_id] += 1
                else:
                    self.session.vars['negative_rating_count'][item_id] = 1

    # Quiz Answers
    quiz1 = models.IntegerField(label=C.QUESTION1, choices=[[0, '2 points'], [1, '5 points'], [2, '0 points']])
    quiz2 = models.IntegerField(label=C.QUESTION2, choices=[[0, '3 out of 5 (60%)'], [1, '2 out of 5 (40%)'],
                                                            [2, '1 out of 5 (20%)']])
    quiz3 = models.IntegerField(label=C.QUESTION3, choices=[[0, 'You earn 10 points'], [1, 'You lose 5 points'],
                                                            [2, 'It has no effect on points']])
    quiz4 = models.IntegerField(label=C.QUESTION4, choices=[[0, 'Whether they are good or bad'],
                                                            [1, 'The number of positive and negative ratings'],
                                                            [2, 'Whether someone picked them before']])
    quiz5 = models.IntegerField(label=C.QUESTION5, choices=[[0, '0 times (you never see the same item again)'], [1, 'Between 1 and 3 times'],
                                                            [2, 'It differs per round']])
    quiz6 = models.IntegerField(label=C.QUESTION6, choices=[[0, 'You lose 5 points'], [1, 'You lose 2 points'],
                                                            [2, 'You lose 10 points']])
    quiz7 = models.IntegerField(label=C.QUESTION7, choices=[[0, 'You neither gain nor lose points'],
                                                            [1, 'You gain 5 points'],
                                                            [2, 'You lose 2 points']])
    quiz8 = models.IntegerField(label=C.QUESTION8, choices=[[0, 'It is randomly generated each round'],
                                                            [1, 'It is set by a participant in a prior session'],
                                                            [2, 'It is based on prior ratings']])