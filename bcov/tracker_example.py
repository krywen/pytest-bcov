# Usage example
from bcov.tracker import BooleanCoverageTracker

tracker = BooleanCoverageTracker()


def track_boolean_expression(has_license, is_sober):
    tracker.start_expression("has_license and is_sober", "driver.py:3")

    result = (tracker.track_condition("has_license", has_license) and
              tracker.track_condition("is_sober", is_sober))

    tracker.end_expression()
    return result

def main():

    # Test some combinations
    track_boolean_expression(True, True)
    track_boolean_expression(False, True)  # is_sober won't be evaluated due to short-circuit

    # Get coverage information
    print(tracker.get_missing_combinations("has_license and is_sober"))
    print(tracker.get_short_circuit_stats("has_license and is_sober"))

if __name__ == "__main__":
    main()
