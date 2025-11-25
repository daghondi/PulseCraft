"""
Safety Check Agent for pre-send message validation.

Performs safety checks on messages before they are sent to customers.
"""

import re
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional

from pulsecraft.base import BaseAgent, Message


class SafetyCheckResult(Enum):
    """Result of a safety check."""

    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


@dataclass
class SafetyCheckReport:
    """Report from safety checks on a message."""

    message_id: str
    overall_result: SafetyCheckResult = SafetyCheckResult.PASS
    checks_passed: list = field(default_factory=list)
    checks_warned: list = field(default_factory=list)
    checks_failed: list = field(default_factory=list)
    is_safe_to_send: bool = True
    metadata: dict = field(default_factory=dict)


class SafetyCheckAgent(BaseAgent):
    """
    Agent responsible for pre-send safety validation.

    Performs configurable safety checks on messages to ensure they are
    appropriate and safe to send to customers.
    """

    def __init__(
        self,
        name: str = "SafetyCheckAgent",
        safety_checks: Optional[dict] = None,
        blocked_patterns: Optional[list[str]] = None,
    ):
        """
        Initialize the safety check agent.

        Args:
            name: Agent name for audit logging
            safety_checks: Dictionary mapping check names to check functions
            blocked_patterns: List of regex patterns that should fail checks
        """
        super().__init__(name)
        self.safety_checks = safety_checks or self._default_safety_checks()
        self.blocked_patterns = blocked_patterns or self._default_blocked_patterns()

    def _default_safety_checks(self) -> dict[str, Callable]:
        """Return default safety checks."""
        return {
            "content_length": self._check_content_length,
            "blocked_patterns": self._check_blocked_patterns,
            "personalization": self._check_personalization,
            "empty_content": self._check_empty_content,
        }

    def _default_blocked_patterns(self) -> list[str]:
        """Return default blocked patterns."""
        return [
            r"(?i)\b(guarantee|guaranteed)\b",  # Avoid guarantee claims
            r"(?i)\b(free money|get rich)\b",  # Spam-like phrases
            r"(?i)\b(act now|limited time|urgent)\b",  # High-pressure tactics
        ]

    def _check_content_length(self, message: Message) -> tuple[SafetyCheckResult, str]:
        """Check if content length is appropriate."""
        content_length = len(message.content)

        if content_length == 0:
            return SafetyCheckResult.FAIL, "Message content is empty"
        elif content_length < 10:
            return SafetyCheckResult.WARN, "Message content is very short"
        elif content_length > 1000:
            return SafetyCheckResult.WARN, "Message content is very long"

        return SafetyCheckResult.PASS, "Content length is appropriate"

    def _check_blocked_patterns(self, message: Message) -> tuple[SafetyCheckResult, str]:
        """Check for blocked patterns in content."""
        for pattern in self.blocked_patterns:
            if re.search(pattern, message.content):
                return SafetyCheckResult.FAIL, f"Content contains blocked pattern: {pattern}"

        return SafetyCheckResult.PASS, "No blocked patterns found"

    def _check_personalization(self, message: Message) -> tuple[SafetyCheckResult, str]:
        """Check if message appears to be personalized."""
        # Check for unresolved template placeholders
        if re.search(r"\{[^}]+\}", message.content):
            return SafetyCheckResult.FAIL, "Message contains unresolved template placeholders"

        # Check for generic placeholder names
        generic_markers = ["Valued Customer", "Dear Customer", "Hello Friend"]
        for marker in generic_markers:
            if marker in message.content:
                return (
                    SafetyCheckResult.WARN,
                    f"Message may not be properly personalized: '{marker}'",
                )

        return SafetyCheckResult.PASS, "Message appears personalized"

    def _check_empty_content(self, message: Message) -> tuple[SafetyCheckResult, str]:
        """Check if content is effectively empty."""
        stripped = message.content.strip()

        if not stripped:
            return SafetyCheckResult.FAIL, "Message content is empty or whitespace only"

        return SafetyCheckResult.PASS, "Message has content"

    def process(self, message: Message) -> SafetyCheckReport:
        """
        Perform safety checks on a message.

        Args:
            message: Message to check

        Returns:
            SafetyCheckReport with results of all checks
        """
        start_time = time.time()

        report = SafetyCheckReport(message_id=message.message_id)

        for check_name, check_fn in self.safety_checks.items():
            try:
                result, detail = check_fn(message)

                if result == SafetyCheckResult.PASS:
                    report.checks_passed.append({"name": check_name, "detail": detail})
                elif result == SafetyCheckResult.WARN:
                    report.checks_warned.append({"name": check_name, "detail": detail})
                else:  # FAIL
                    report.checks_failed.append({"name": check_name, "detail": detail})

            except Exception as e:
                report.checks_failed.append(
                    {
                        "name": check_name,
                        "detail": f"Check raised exception: {str(e)}",
                    }
                )

        # Determine overall result
        if report.checks_failed:
            report.overall_result = SafetyCheckResult.FAIL
            report.is_safe_to_send = False
        elif report.checks_warned:
            report.overall_result = SafetyCheckResult.WARN
            report.is_safe_to_send = True  # Warnings don't block sending
        else:
            report.overall_result = SafetyCheckResult.PASS
            report.is_safe_to_send = True

        # Update message with safety check results
        message.safety_checks = {
            "overall_result": report.overall_result.value,
            "is_safe_to_send": report.is_safe_to_send,
            "checks_passed": len(report.checks_passed),
            "checks_warned": len(report.checks_warned),
            "checks_failed": len(report.checks_failed),
        }

        duration_ms = (time.time() - start_time) * 1000
        self._create_audit_record(
            input_summary=f"message_id={message.message_id}",
            output_summary=f"result={report.overall_result.value}, safe={report.is_safe_to_send}",
            duration_ms=duration_ms,
            metadata={
                "checks_passed": len(report.checks_passed),
                "checks_warned": len(report.checks_warned),
                "checks_failed": len(report.checks_failed),
            },
        )

        return report

    def add_safety_check(self, check_name: str, check_fn: Callable) -> None:
        """
        Add a custom safety check.

        Args:
            check_name: Name of the check
            check_fn: Function that takes Message and returns (SafetyCheckResult, str)
        """
        self.safety_checks[check_name] = check_fn

    def remove_safety_check(self, check_name: str) -> bool:
        """
        Remove a safety check.

        Args:
            check_name: Name of the check to remove

        Returns:
            True if check was removed, False if it didn't exist
        """
        if check_name in self.safety_checks:
            del self.safety_checks[check_name]
            return True
        return False

    def add_blocked_pattern(self, pattern: str) -> None:
        """
        Add a blocked pattern.

        Args:
            pattern: Regex pattern to block
        """
        self.blocked_patterns.append(pattern)

    def remove_blocked_pattern(self, pattern: str) -> bool:
        """
        Remove a blocked pattern.

        Args:
            pattern: Pattern to remove

        Returns:
            True if pattern was removed, False if it didn't exist
        """
        if pattern in self.blocked_patterns:
            self.blocked_patterns.remove(pattern)
            return True
        return False
