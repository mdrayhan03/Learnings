import sys

# Target SLA Threshold: 99.99% (Four Nines)
SLA_TARGET = 99.99

# Simulated incident logs representing unexpected production crashes
UNPLANNED_CRASH_LOGS = [
    {"incident_name": "PostgreSQL Connection Pool Exhaustion", "duration_minutes": 18.5},
    {"incident_name": "Redis Cache Cluster Desync", "duration_minutes": 12.0},
    {"incident_name": "Broken Production Deployment (Nginx Gateway 502)", "duration_minutes": 14.2},
    {"incident_name": "Third-Party SMS Gateway Timeout Loop", "duration_minutes": 5.1}
]

def run_availability_audit():
    print("=" * 60)
    print("         PRODUCTION SYSTEM RELIABILITY AUDITOR")
    print("=" * 60)
    
    # Total minutes in a standard calendar year (365 days * 24 hours * 60 minutes)
    TOTAL_YEAR_MINUTES = 365 * 24 * 60
    
    # Calculate the exact allowed maximum downtime for 99.99%
    max_allowed_downtime = TOTAL_YEAR_MINUTES * ((100 - SLA_TARGET) / 100)
    
    # Aggregate total minutes lost due to unexpected outages
    total_unplanned_downtime = sum(crash["duration_minutes"] for crash in UNPLANNED_CRASH_LOGS)
    
    # Calculate realized uptime minutes
    realized_uptime_minutes = TOTAL_YEAR_MINUTES - total_unplanned_downtime
    
    # Compute true final availability ratio percentage
    actual_availability_percentage = (realized_uptime_minutes / TOTAL_YEAR_MINUTES) * 100
    
    # Calculate remaining headroom or amount over budget
    remaining_error_budget = max_allowed_downtime - total_unplanned_downtime
    
    # Display Telemetry Parameters
    print(f"Operational Window : {TOTAL_YEAR_MINUTES:,} minutes (1 Year)")
    print(f"Realized System Uptime: {realized_uptime_minutes:,} minutes")
    print(f"Aggregated Outage Time: {total_unplanned_downtime:.2f} minutes")
    print("-" * 60)
    
    print(f"📊 SLA COMPLIANCE TELEMETRY:")
    print(f"  • Contractual Target Threshold : {SLA_TARGET}%")
    print(f"  • Realized System Availability : {actual_availability_percentage:.4f}%")
    print("-" * 60)
    
    print(f"📉 ERROR BUDGET ACCOUNTING:")
    print(f"  • Max Allowed Downtime Limit  : {max_allowed_downtime:.2f} minutes/year")
    
    if remaining_error_budget >= 0:
        print(f"  • Remaining Error Budget     : ✅ {remaining_error_budget:.2f} minutes remaining")
        print("\n🏆 AUDIT RESULT: PASSED")
        print("  -> System conforms to the 99.99% High Availability SLA.")
    else:
        print(f"  • Remaining Error Budget     : ❌ {abs(remaining_error_budget):.2f} minutes BREACHED")
        print("\n🚨 AUDIT RESULT: CRITICAL FAILURE")
        print("  -> SLA breached. Freeze new feature deployments and stabilize infrastructure immediately.")
    print("=" * 60)

if __name__ == "__main__":
    run_availability_audit()