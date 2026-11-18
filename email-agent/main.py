import sys
from agent.config import AgentConfig, WorkScheduleGuard
from agent.orchestrator import EmailTriageAgent


def main() -> None:
    config = AgentConfig.from_env()
    schedule_guard = WorkScheduleGuard(
        timezone_str=config.timezone,
        start_hour=config.work_start_hour,
        end_hour=config.work_end_hour,
    )

    if not schedule_guard.is_working_time():
        print("Outside working hours. Skipping execution.")
        sys.exit(0)

    agent = EmailTriageAgent(config)
    agent.run()


if __name__ == "__main__":
    main()
