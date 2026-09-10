"""
HandoffRisk
===========

A small Python OOP system for evaluating risks when work is
transferred from one person, team, or system to another.

Example:

Developer
    ↓
QA Team
    ↓
Deployment Team

If important information is missing during the handoff,
the next team may misunderstand the work, repeat work,
or make mistakes.

HandoffRisk identifies these gaps and evaluates the
overall handoff risk.
"""


class HandoffRisk:
    """Stores handoffs and analyzes their risks."""

    def __init__(self):
        self.handoffs = {}

    def create_handoff(
        self,
        handoff_id,
        title,
        source,
        destination
    ):
        """Create a new handoff."""
        if handoff_id in self.handoffs:
            return False, "Handoff ID already exists."

        self.handoffs[handoff_id] = {
            "title": title,
            "source": source,
            "destination": destination,
            "requirements": [],
            "risks": []
        }

        return True, "Handoff created successfully."

    def get_handoff(self, handoff_id):
        """Return a handoff."""
        return self.handoffs.get(handoff_id)

    def add_requirement(
        self,
        handoff_id,
        name,
        value,
        importance="required"
    ):
        """
        Add information that should be present in the handoff.

        importance:
            required
            important
            optional
        """
        handoff = self.get_handoff(handoff_id)

        if not handoff:
            return False, "Handoff not found."

        valid_importance = {
            "required",
            "important",
            "optional"
        }

        importance = importance.lower().strip()

        if importance not in valid_importance:
            return False, (
                "Importance must be required, important, "
                "or optional."
            )

        requirement = {
            "name": name,
            "value": value,
            "importance": importance
        }

        handoff["requirements"].append(requirement)

        return True, "Handoff information added successfully."

    def add_risk(
        self,
        handoff_id,
        risk,
        severity="medium",
        likelihood="medium"
    ):
        """
        Add a possible handoff risk.

        severity:
            low, medium, high, critical

        likelihood:
            low, medium, high
        """
        handoff = self.get_handoff(handoff_id)

        if not handoff:
            return False, "Handoff not found."

        valid_severity = {
            "low",
            "medium",
            "high",
            "critical"
        }

        valid_likelihood = {
            "low",
            "medium",
            "high"
        }

        severity = severity.lower().strip()
        likelihood = likelihood.lower().strip()

        if severity not in valid_severity:
            return False, (
                "Severity must be low, medium, high, "
                "or critical."
            )

        if likelihood not in valid_likelihood:
            return False, (
                "Likelihood must be low, medium, or high."
            )

        risk_item = {
            "risk": risk,
            "severity": severity,
            "likelihood": likelihood
        }

        handoff["risks"].append(risk_item)

        return True, "Handoff risk added successfully."

    def get_missing_requirements(self, handoff_id):
        """Return required or important information that is missing."""
        handoff = self.get_handoff(handoff_id)

        if not handoff:
            return []

        missing = []

        for requirement in handoff["requirements"]:
            value = requirement["value"]

            if (
                requirement["importance"] in
                {"required", "important"}
                and not str(value).strip()
            ):
                missing.append(requirement)

        return missing

    def get_required_gaps(self, handoff_id):
        """Return only missing required information."""
        return [
            requirement
            for requirement in self.get_missing_requirements(
                handoff_id
            )
            if requirement["importance"] == "required"
        ]

    def get_important_gaps(self, handoff_id):
        """Return only missing important information."""
        return [
            requirement
            for requirement in self.get_missing_requirements(
                handoff_id
            )
            if requirement["importance"] == "important"
        ]

    def calculate_information_score(self, handoff_id):
        """
        Calculate how complete the recorded handoff information is.

        Required information has the highest weight.
        Important information has a medium weight.
        Optional information has a lower weight.
        """
        handoff = self.get_handoff(handoff_id)

        if not handoff:
            return 0

        requirements = handoff["requirements"]

        if not requirements:
            return 0

        weights = {
            "required": 3,
            "important": 2,
            "optional": 1
        }

        total_weight = 0
        completed_weight = 0

        for requirement in requirements:
            weight = weights[
                requirement["importance"]
            ]

            total_weight += weight

            if str(
                requirement["value"]
            ).strip():
                completed_weight += weight

        if total_weight == 0:
            return 0

        return round(
            (completed_weight / total_weight) * 100,
            2
        )

    def get_risk_score(self, handoff_id):
        """
        Calculate an overall risk score.

        Severity and likelihood are combined for every
        recorded risk.
        """
        handoff = self.get_handoff(handoff_id)

        if not handoff:
            return 0

        severity_scores = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4
        }

        likelihood_scores = {
            "low": 1,
            "medium": 2,
            "high": 3
        }

        score = 0

        for risk in handoff["risks"]:
            severity_score = severity_scores[
                risk["severity"]
            ]

            likelihood_score = likelihood_scores[
                risk["likelihood"]
            ]

            score += (
                severity_score *
                likelihood_score
            )

        return score

    def get_high_risks(self, handoff_id):
        """Return high and critical risks."""
        handoff = self.get_handoff(handoff_id)

        if not handoff:
            return []

        return [
            risk
            for risk in handoff["risks"]
            if risk["severity"] in {
                "high",
                "critical"
            }
        ]

    def get_critical_risks(self, handoff_id):
        """Return critical risks."""
        handoff = self.get_handoff(handoff_id)

        if not handoff:
            return []

        return [
            risk
            for risk in handoff["risks"]
            if risk["severity"] == "critical"
        ]

    def get_risk_level(self, handoff_id):
        """Classify the overall handoff risk."""
        risk_score = self.get_risk_score(
            handoff_id
        )

        required_gaps = len(
            self.get_required_gaps(handoff_id)
        )

        information_score = self.calculate_information_score(
            handoff_id
        )

        if required_gaps > 0:
            return "Critical Risk"

        if risk_score >= 20:
            return "Critical Risk"

        if risk_score >= 12:
            return "High Risk"

        if information_score < 50:
            return "High Risk"

        if risk_score >= 6:
            return "Moderate Risk"

        if information_score < 75:
            return "Moderate Risk"

        return "Low Risk"

    def get_handoff_readiness(self, handoff_id):
        """Determine whether the handoff is ready."""
        handoff = self.get_handoff(handoff_id)

        if not handoff:
            return "Not Found"

        required_gaps = self.get_required_gaps(
            handoff_id
        )

        if required_gaps:
            return "Not Ready"

        risk_level = self.get_risk_level(
            handoff_id
        )

        if risk_level == "Critical Risk":
            return "Not Ready"

        if risk_level == "High Risk":
            return "Needs Review"

        if risk_level == "Moderate Risk":
            return "Needs Review"

        return "Ready"

    def get_risk_summary(self, handoff_id):
        """Return a summary of recorded risks."""
        handoff = self.get_handoff(handoff_id)

        if not handoff:
            return {}

        summary = {
            "low": 0,
            "medium": 0,
            "high": 0,
            "critical": 0
        }

        for risk in handoff["risks"]:
            severity = risk["severity"]
            summary[severity] += 1

        return summary

    def generate_recommendation(self, handoff_id):
        """Generate a recommendation for the handoff."""
        handoff = self.get_handoff(handoff_id)

        if not handoff:
            return "Handoff not found."

        required_gaps = self.get_required_gaps(
            handoff_id
        )

        if required_gaps:
            names = [
                item["name"]
                for item in required_gaps
            ]

            return (
                "Do not complete the handoff yet. "
                "Provide the missing required information: "
                + ", ".join(names)
                + "."
            )

        critical_risks = self.get_critical_risks(
            handoff_id
        )

        if critical_risks:
            return (
                "Review the critical risks before transferring "
                "the work to the destination team."
            )

        high_risks = self.get_high_risks(
            handoff_id
        )

        if high_risks:
            return (
                "Review the high-severity risks and confirm "
                "the destination team understands the work "
                "before completing the handoff."
            )

        information_score = (
            self.calculate_information_score(
                handoff_id
            )
        )

        if information_score < 75:
            return (
                "Add the missing handoff information and "
                "clarify important details before transfer."
            )

        return (
            "The handoff appears sufficiently prepared. "
            "Confirm the destination team has received "
            "and understood the information."
        )

    def analyze_handoff(self, handoff_id):
        """Return a complete handoff-risk analysis."""
        handoff = self.get_handoff(handoff_id)

        if not handoff:
            return None

        return {
            "handoff_id": handoff_id,
            "title": handoff["title"],
            "source": handoff["source"],
            "destination": handoff["destination"],
            "requirement_count": len(
                handoff["requirements"]
            ),
            "risk_count": len(
                handoff["risks"]
            ),
            "missing_requirement_count": len(
                self.get_missing_requirements(
                    handoff_id
                )
            ),
            "required_gap_count": len(
                self.get_required_gaps(
                    handoff_id
                )
            ),
            "important_gap_count": len(
                self.get_important_gaps(
                    handoff_id
                )
            ),
            "information_score": (
                self.calculate_information_score(
                    handoff_id
                )
            ),
            "risk_score": self.get_risk_score(
                handoff_id
            ),
            "risk_level": self.get_risk_level(
                handoff_id
            ),
            "readiness": self.get_handoff_readiness(
                handoff_id
            ),
            "risk_summary": self.get_risk_summary(
                handoff_id
            ),
            "high_risks": self.get_high_risks(
                handoff_id
            ),
            "recommendation": self.generate_recommendation(
                handoff_id
            )
        }

    def display_handoff(self, handoff_id):
        """Display the complete handoff analysis."""
        analysis = self.analyze_handoff(
            handoff_id
        )

        if not analysis:
            print("\nHandoff not found.")
            return

        print("\n" + "=" * 65)
        print("HANDOFFRISK ANALYSIS")
        print("=" * 65)

        print(
            f"Handoff ID: "
            f"{analysis['handoff_id']}"
        )

        print(
            f"Title: "
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
            f"\nInformation Score: "
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

        print("\nHandoff Information:")

        requirements = self.handoffs[
            handoff_id
        ]["requirements"]

        if not requirements:
            print("  No information recorded.")
        else:
            for number, requirement in enumerate(
                requirements,
                start=1
            ):
                value = requirement["value"]

                if not str(value).strip():
                    value = "MISSING"

                print(
                    f"  {number}. "
                    f"{requirement['name']}"
                )
                print(
                    f"     Importance: "
                    f"{requirement['importance']}"
                )
                print(
                    f"     Value: "
                    f"{value}"
                )

        print("\nRisks:")

        risks = self.handoffs[
            handoff_id
        ]["risks"]

        if not risks:
            print("  No risks recorded.")
        else:
            for number, risk in enumerate(
                risks,
                start=1
            ):
                print(
                    f"  {number}. "
                    f"{risk['risk']}"
                )
                print(
                    f"     Severity: "
                    f"{risk['severity']}"
                )
                print(
                    f"     Likelihood: "
                    f"{risk['likelihood']}"
                )

        print("\nRisk Summary:")

        for severity, count in (
            analysis["risk_summary"].items()
        ):
            print(
                f"  {severity.capitalize()}: "
                f"{count}"
            )

        print("\nRecommendation:")
        print(
            f"  {analysis['recommendation']}"
        )

        print("=" * 65)

    def list_handoffs(self):
        """Return all handoffs."""
        return self.handoffs
