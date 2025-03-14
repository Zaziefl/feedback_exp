from otree.api import *

class ResultsWaitPage(WaitPage):
    pass

class PaymentOverview(Page):
    def vars_for_template(self):
        conversion_rate = 1 / 50  # Convert points to EUR

        # Convert Part 1 earnings (stored in points) to EUR
        earnings_part1_decision_points = self.participant.dictator_payoff  # Stored in points
        earnings_part1_partner_points = self.participant.recipient_payoff  # Stored in points

        earnings_part1_decision_euros = earnings_part1_decision_points * conversion_rate  # Convert
        earnings_part1_partner_euros = earnings_part1_partner_points * conversion_rate  # Convert

        # Convert Part 2 earnings (stored in points) to EUR
        earnings_part2_points = self.participant.vars.get("earnings_part2", 0)
        earnings_part2_euros = earnings_part2_points * conversion_rate

        show_up_fee = 5.00

        # Correct total earnings calculation in EUR
        total_earnings = earnings_part1_decision_euros + earnings_part1_partner_euros + earnings_part2_euros + show_up_fee

        return dict(
            earnings_total_euros=round(total_earnings, 2),
            earnings_part1_decision_euros=round(earnings_part1_decision_euros, 2),
            earnings_part1_partner_euros=round(earnings_part1_partner_euros, 2),
            earnings_part2_euros=round(earnings_part2_euros, 2),
            show_up_fee=round(show_up_fee, 2)
        )

    def before_next_page(self):
        pass

page_sequence = [PaymentOverview]