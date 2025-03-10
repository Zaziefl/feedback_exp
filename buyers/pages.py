from otree.api import *
from .models import C
from django.utils.safestring import mark_safe


class Instruction(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return dict(
            first=self.round_number == 1
        )

class TransitionPage(Page):
    template_name = "buyers/transition.html"

    def is_displayed(self):
        return self.round_number in [1, 7, 11]

    def vars_for_template(self):
        if self.player.field_maybe_none('experimental_condition') is None:
            self.player.set_experimental_condition()

        condition = self.player.experimental_condition

        if condition == "default":
            transition_text = """
                <p>In the coming rounds, the rules for leaving a rating are as follows:</p>
                <p>If you select an item, a <b>positive rating is left automatically</b>. 
                You can change it to a negative rating at a cost of <b>-2 points</b>.
                If you decide not to change the rating, a positive rating will always be published.</p>
                
                <p>For example, the ratings for an item can look like this:</p>
                
                <img src="/static/pictures/Default.png" width="250px"/>
            """
        elif condition == "omitted":
            transition_text = """
                <p>In the coming rounds, the rules for leaving a rating are as follows:</p>
                <p>If you select an item, you can choose to leave a rating (positive or negative). Leaving a rating costs <b>-2 points</b>. 
                If you decide to leave a rating, this rating will be visible to other participants who offered the same item in a later round. 
                You can also choose not to leave a rating. If you decide not to leave a rating, no rating will be shown to other participants. 
                However, participants will be informed that the item was selected, but <b>no rating was given</b>.</p
                                
                <p>For example, the ratings for an item can look like this:</p>
                
                <img src="/static/pictures/Omitted.png" width="250px"/>
            """
        else:  # Control condition
            transition_text = """
                <p>In the coming rounds, the rules for leaving a rating are as follows:</p>
                <p>If you select an item, you can choose to leave a rating (positive or negative). Leaving a rating costs <b>-2 points</b>. 
                If you decide to leave a rating, this rating will be visible to other participants who offered the same item in a later round. 
                You can also choose not to leave a rating. 
                If you decide not to leave a rating, other participants will not know you selected the item and no rating will be shown.</p>
                
                <p>For example, the ratings for an item can look like this:</p>
                
                <img src="/static/pictures/Control.png" width="250px"/>
            """

        return {"transition_text": mark_safe(transition_text)}


class Quiz(Page):
    form_model = 'player'
    form_fields = ['quiz1', 'quiz2', 'quiz3', 'quiz4', 'quiz5', 'quiz6', 'quiz7', 'quiz8']

    def is_displayed(self):
        return self.round_number == 1

class Answers(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return dict(
            quiz1=self.player.field_display('quiz1'),
            quiz2=self.player.field_display('quiz2'),
            quiz3=self.player.field_display('quiz3'),
            quiz4=self.player.field_display('quiz4'),
            quiz5=self.player.field_display('quiz5'),
            quiz6=self.player.field_display('quiz6'),
            quiz7=self.player.field_display('quiz7'),
            quiz8=self.player.field_display('quiz8'),
            quiz1_correct="2 points",
            quiz2_correct="1 out of 5 (20%)",
            quiz3_correct="You earn 10 points",
            quiz4_correct="The number of positive and negative ratings",
            quiz5_correct="0 times (you never see the same item again)",
            quiz6_correct="You lose 5 points",
            quiz7_correct="You neither gain nor lose points",
            quiz8_correct="It is set by a participant in a prior session"
        )

class Start(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return dict(
            first=self.round_number == 1
        )

class Choice(Page):
    form_model = 'player'
    form_fields = ['selected_item']

    def vars_for_template(self):
        if self.player.field_maybe_none('experimental_condition') is None:
            self.player.set_experimental_condition()

        if self.player.field_maybe_none('item_id') is None:
            print(f"[DEBUG] Player {self.player.id_in_group} missing item_id in round {self.round_number}")
            self.subsession.assign_items()

        item_id = self.player.field_maybe_none('item_id') or "Unavailable"
        item_quality = "Good" if self.player.field_maybe_none('item_quality') else "Bad"
        earnings = C.good_item_bonus if self.player.field_maybe_none('item_quality') else C.bad_item_penalty

        # Check if feedback should be displayed
        feedback_rounds = {4, 5, 6, 9, 10, 14, 15, 16}
        ratings_visible = self.round_number in feedback_rounds

        positive_ratings = 0
        negative_ratings = 0
        no_rating_given = 0

        # Retrieve past feedback
        if 'item_feedback' in self.session.vars and item_id in self.session.vars['item_feedback']:
            feedback_data = self.session.vars['item_feedback'][item_id]
            if ratings_visible:
                positive_ratings = feedback_data.get('positive', 0)
                negative_ratings = feedback_data.get('negative', 0)
                if self.player.experimental_condition == "omitted":
                    no_rating_given = feedback_data.get('no_rating', 0)

        print(f"[DEBUG] Round {self.round_number} - Showing feedback? {ratings_visible}")
        print(f"[DEBUG] Retrieved feedback for item {item_id}: {positive_ratings} positive, {negative_ratings} negative, {no_rating_given} no rating")

        return {
            "item_id": item_id,
            "item_quality": item_quality,
            "earnings": earnings,
            "experimental_condition": self.player.experimental_condition,
            "ratings_visible": ratings_visible,
            "positive_ratings": positive_ratings if ratings_visible else 0,
            "negative_ratings": negative_ratings if ratings_visible else 0,
            "no_rating_given": no_rating_given if (ratings_visible and self.player.experimental_condition == "omitted") else 0,
            "num_ratings_per_item": self.player.num_ratings_per_item,
            "num_positive_ratings": self.player.num_positive_ratings,
            "num_negative_ratings": self.player.num_negative_ratings
        }

    def before_next_page(self):
        if self.player.field_maybe_none('experimental_condition') is None:
            self.player.set_experimental_condition()

        if self.player.field_maybe_none('item_id') is None:
            print(f"[ERROR] Player {self.player.id_in_group} missing item_id before moving to next page in round {self.round_number}")
            self.subsession.assign_items()

class Feedback(Page):
    form_model = 'player'

    def is_displayed(self):
        return True

    def get_form_fields(self):
        if self.player.selected_item:
            if self.player.experimental_condition == 'control' or self.player.experimental_condition == 'omitted':
                return ['feedback']
            elif self.player.experimental_condition == 'default':
                return ['default_feedback_changed']
        return []

    def vars_for_template(self):
        return {
            "item_selected": self.player.selected_item,
            "item_quality": "Good" if self.player.item_quality else "Bad",
            "earnings": self.player.earnings,
            "experimental_condition": self.player.experimental_condition,
            "pre_set_positive": (self.player.experimental_condition == 'default')
        }

    def before_next_page(self):
        if self.player.selected_item is not None:
            item_id = self.player.item_id
            if item_id not in self.session.vars['truly_seen_items']:
                self.session.vars['truly_seen_items'].add(item_id)
                print(f"[DEBUG] Item {item_id} marked as TRULY SEEN after Feedback page")

        self.player.calculate_earnings()

        if 'item_feedback' not in self.session.vars:
            self.session.vars['item_feedback'] = {}

        # Store feedback
        if self.player.selected_item:
            item_id = self.player.item_id
            if item_id not in self.session.vars['item_feedback']:
                self.session.vars['item_feedback'][item_id] = {'positive': 0, 'negative': 0, 'no_rating': 0}

            feedback = self.player.field_maybe_none('feedback')

            # Control condition
            if self.player.experimental_condition == 'control':
                if feedback == 1:
                    self.session.vars['item_feedback'][item_id]['positive'] += 1
                elif feedback == -1:
                    self.session.vars['item_feedback'][item_id]['negative'] += 1

            # Omitted condition
            elif self.player.experimental_condition == 'omitted':
                if feedback == 0 or feedback is None:
                    self.player.no_feedback_given = True
                    self.session.vars['item_feedback'][item_id]['no_rating'] += 1
                elif feedback == 1:
                    self.session.vars['item_feedback'][item_id]['positive'] += 1
                elif feedback == -1:
                    self.session.vars['item_feedback'][item_id]['negative'] += 1

            # Default condition
            elif self.player.experimental_condition == 'default':
                if self.player.field_maybe_none(
                        'default_feedback_changed'):
                    self.player.earnings += C.feedback_cost
                    self.session.vars['item_feedback'][item_id]['negative'] += 1
                else:
                    self.session.vars['item_feedback'][item_id]['positive'] += 1

class Results(Page):
    def is_displayed(self):
        return self.round_number == C.NUM_ROUNDS

    def vars_for_template(self):
        total_earnings = sum([p.earnings for p in self.player.in_all_rounds()])
        self.participant.payoff = total_earnings

        return {
            'total_earnings': total_earnings
        }


class QuizWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == 1  # Only apply in round 1

    def after_all_players_arrive(self):
        pass


page_sequence = [Instruction, Quiz, Answers, QuizWaitPage, Start, TransitionPage, Choice, Feedback]