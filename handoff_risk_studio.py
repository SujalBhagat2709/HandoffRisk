"""
HandoffRisk Studio
==================

Interactive command-line interface for the HandoffRisk system.
"""

from handoff_risk import HandoffRisk


class HandoffRiskStudio:
    """Interactive interface for HandoffRisk."""

    def __init__(self):
        self.system = HandoffRisk()

    def run(self):
        """Start the interactive studio."""
        while True:
            self.show_menu()

            choice = input("\nEnter your choice: ").strip()

            if choice == "1":
                self.create_handoff()
            elif choice == "2":
                self.add_information()
            elif choice == "3":
                self.add_risk()
            elif choice == "4":
                self.view_all_handoffs()
            elif choice == "5":
                self.view_handoff_details()
            elif choice == "6":
                self.analyze_handoff()
            elif choice == "7":
                self.show_recommendation()
            elif choice == "8":
                print("\nThank you for using HandoffRisk Studio.")
                break
            else:
                print("\nInvalid choice. Please try again.")

    def show_menu(self):
        """Display the main menu."""
        print("\n" + "=" * 60)
        print("               HANDOFFRISK STUDIO")
        print("=" * 60)
        print("1. Create Handoff")
        print("2. Add Handoff Information")
        print("3. Add Risk")
        print("4. View All Handoffs")
        print("5. View Handoff Details")
        print("6. Analyze Handoff")
        print("7. Show Recommendation")
        print("8. Exit")
        print("=" * 60)

    def create_handoff(self):
        """Create a new handoff."""
        print("\n--- Create Handoff ---")

        handoff_id = input("Handoff ID: ").strip()
        title = input("Handoff title: ").strip()
        source = input("From: ").strip()
        destination = input("To: ").strip()

        success, message = self.system.create_handoff(
            handoff_id,
            title,
            source,
            destination
        )

        print(f"\n{message}")

    def add_information(self):
        """Add information required for a handoff."""
        print("\n--- Add Handoff Information ---")

        handoff_id = input("Handoff ID: ").strip()

        if not self.system.get_handoff(handoff_id):
            print("\nHandoff not found.")
            return

        name = input("Information name: ").strip()
        value = input(
            "Information value "
            "(leave blank if missing): "
        ).strip()

        importance = input(
            "Importance "
            "(required/important/optional): "
        ).strip()

        success, message = self.system.add_requirement(
            handoff_id,
            name,
            value,
            importance
        )

        print(f"\n{message}")

    def add_risk(self):
        """Add a risk to a handoff."""
        print("\n--- Add Handoff Risk ---")

        handoff_id = input("Handoff ID: ").strip()

        if not self.system.get_handoff(handoff_id):
            print("\nHandoff not found.")
            return

        risk = input("Risk description: ").strip()

        severity = input(
            "Severity "
            "(low/medium/high/critical): "
        ).strip()

        likelihood = input(
            "Likelihood "
            "(low/medium/high): "
        ).strip()

        success, message = self.system.add_risk(
            handoff_id,
            risk,
            severity,
            likelihood
        )

        print(f"\n{message}")

    def view_all_handoffs(self):
        """Display all handoffs."""
        print("\n--- All Handoffs ---")

        handoffs = self.system.list_handoffs()

        if not handoffs:
            print("\nNo handoffs created yet.")
            return

        for handoff_id, handoff in handoffs.items():
            information_count = len(
                handoff["requirements"]
            )

            risk_count = len(
                handoff["risks"]
            )

            print(f"\nID: {handoff_id}")
            print(f"Title: {handoff['title']}")
            print(
                f"From: {handoff['source']}"
            )
            print(
                f"To: {handoff['destination']}"
            )
            print(
                f"Information Items: "
                f"{information_count}"
            )
            print(
                f"Risks: "
                f"{risk_count}"
            )

    def view_handoff_details(self):
        """Display complete handoff details."""
        print("\n--- Handoff Details ---")

        handoff_id = input("Handoff ID: ").strip()

        self.system.display_handoff(
            handoff_id
        )

    def analyze_handoff(self):
        """Display a summary analysis."""
        print("\n--- Analyze Handoff ---")

        handoff_id = input("Handoff ID: ").strip()

        analysis = self.system.analyze_handoff(
            handoff_id
        )

        if not analysis:
            print("\nHandoff not found.")
            return

        print("\n" + "=" * 60)
        print("HANDOFFRISK ANALYSIS SUMMARY")
        print("=" * 60)

        print(
            f"Handoff: "
            f"{analysis['title']}"
        )

        print(
            f"From: "
            f"{analysis['source']}"
        )

        print(
            f"To: "
            f"{analysis['destination']}"
        )

        print(
            f"Information Score: "
            f"{analysis['information_score']}%"
        )

        print(
            f"Risk Score: "
            f"{analysis['risk_score']}"
        )

        print(
            f"Risk Level: "
            f"{analysis['risk_level']}"
        )

        print(
            f"Readiness: "
            f"{analysis['readiness']}"
        )

        print(
            f"Missing Required Information: "
            f"{analysis['required_gap_count']}"
        )

        print(
            f"Missing Important Information: "
            f"{analysis['important_gap_count']}"
        )

        print(
            f"Total Risks: "
            f"{analysis['risk_count']}"
        )

        print("=" * 60)

    def show_recommendation(self):
        """Display the handoff recommendation."""
        print("\n--- HandoffRisk Recommendation ---")

        handoff_id = input("Handoff ID: ").strip()

        recommendation = self.system.generate_recommendation(
            handoff_id
        )

        print(
            f"\nRecommendation:\n{recommendation}"
        )


if __name__ == "__main__":
    studio = HandoffRiskStudio()
    studio.run()
