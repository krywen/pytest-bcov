# Usage example
from bcov.reporter import BooleanCoverageReporter
from bcov.tracker import BooleanExpressionTracker

tracker = BooleanExpressionTracker()

"""
           OR
          /  \
        AND   AND
       /  \    /  \
    HL    OR   IE  HP
         /  \
        IS   HO
            

(has_license and (
        is_sober or has_override)
        ) 
or 
    (is_emergency and has_permission)
"""


def evaluate_complex_expression(tracker, has_license, is_sober, has_override,
                                is_emergency, has_permission):
    """Evaluate a complex boolean expression with proper tracking."""
    # Start tracking the root OR expression
    tracker.start_expression('root', 'or')

    # Left side: (has_license and (is_sober or has_override))
    tracker.start_expression('left_side', 'and')
    has_license_result = tracker.track_condition('has_license', has_license)

    if has_license_result:  # Short-circuit check for AND
        # Track the nested OR expression
        tracker.start_expression('sober_or_override', 'or')
        sober_result = tracker.track_condition('is_sober', is_sober)

        if not sober_result:  # Short-circuit check for OR
            override_result = tracker.track_condition('has_override', has_override)
            or_result = sober_result or override_result
        else:
            or_result = sober_result  # Short-circuited OR

        # Track the result of the OR expression
        tracker.track_intermediate_result(or_result)
        tracker.end_expression()  # End sober_or_override

        # Track result of the left AND
        left_result = has_license_result and or_result
    else:
        left_result = False  # Short-circuited AND

    tracker.track_intermediate_result(left_result)
    tracker.end_expression()  # End left_side

    # Only evaluate right side if left side was false (OR short-circuit)
    if not left_result:
        # Right side: (is_emergency and has_permission)
        tracker.start_expression('right_side', 'and')
        emergency_result = tracker.track_condition('is_emergency', is_emergency)

        if emergency_result:  # Short-circuit check for AND
            permission_result = tracker.track_condition('has_permission', has_permission)
            right_result = emergency_result and permission_result
        else:
            right_result = False  # Short-circuited AND

        tracker.track_intermediate_result(right_result)
        tracker.end_expression()  # End right_side
    else:
        right_result = False  # Short-circuited at the root OR

    # Final result
    final_result = left_result or right_result
    tracker.track_intermediate_result(final_result)
    tracker.end_expression()  # End root

    return final_result


"""
if (has_license and (is_sober or has_override)) or (is_emergency and has_permission):
    pass
"""

def main():
    # Example 1: Early short-circuit
    evaluate_complex_expression(tracker, False, True, False, True, True)
    # Short-circuits at has_license=False, moves to emergency path

    # Example 2: Nested short-circuit
    # evaluate_complex_expression(True, True, False, False, False)
    # # Short-circuits after is_sober=True, never evaluates has_override
    #
    # # Example 3: Complete evaluation
    # evaluate_complex_expression(True, False, True, False, False)
    # Evaluates has_override after is_sober=False

    reporter = BooleanCoverageReporter(tracker)
    print(tracker.analyze_short_circuits())
    # print(reporter.generate_report())
    print(reporter.generate_short_circuit_report())

if __name__ == "__main__":
    main()
