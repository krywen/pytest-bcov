from bcov.tracker import BooleanExpressionTracker


class BooleanCoverageReporter:
    """
    creates human-readable reports from the collected data:
    """
    def __init__(self, tracker: BooleanExpressionTracker):
        self.tracker = tracker

    def generate_short_circuit_report(self):
        """Generates the final coverage report including short-circuit analysis."""
        # First analyze all the data we collected
        short_circuit_data = self.tracker.analyze_short_circuits()

        # Then format it for the report
        report_lines = []
        report_lines.append("Boolean Coverage Report")
        report_lines.append("=====================")

        # Add short-circuit information to the report
        report_lines.append("\nShort-circuit Analysis:")
        for circuit in short_circuit_data:
            report_lines.append(f"  • {circuit['triggered_by']} was (always?) {circuit['value']}, "
                                f"skipped: {', '.join(circuit['skipped_conditions'])}")

        return "\n".join(report_lines)

    def generate_report(self) -> str:
        """Generate a coverage report similar to pytest-cov's format."""
        lines = []

        # Add report header
        lines.append("---------- boolean coverage report ----------")

        # Add coverage data
        for location, condition in self.tracker.conditions.items():
            lines.append(f"\n{location}:")
            lines.append(f"  True:  {condition.true_count}")
            lines.append(f"  False: {condition.false_count}")

        return "\n".join(lines)
