from crewai.flow import Flow, start, listen, router
from app.crews.scrape_agents import (
    nlp_agent,
    planner,
    codegen,
    executor,
    modeler,
    auditor,
)


class ScrapeFlow(Flow):
    """Event-driven scraping flow."""

    model = "gpt-4o-mini"

    @start()
    def parse_prompt(self, prompt: str):
        return nlp_agent.run(prompt)

    @listen(parse_prompt)
    def choose_strategy(self, intent):
        return planner.run(intent)

    @router(choose_strategy, routes=["dynamic", "static"])
    def branch(self, strategy):
        return "dynamic" if strategy.get("tool") == "playwright" else "static"

    @listen(branch.dynamic)
    def build_dynamic_code(self, spec):
        return codegen.run(spec)

    @listen(branch.static)
    def build_static_code(self, spec):
        return codegen.run(spec)

    @listen([build_dynamic_code, build_static_code])
    def execute_scraper(self, mod_path):
        return executor.run(mod_path)

    @listen(execute_scraper)
    def persist(self, rows):
        return modeler.run(rows)

    @listen(persist)
    def audit(self, table_name):
        return auditor.run(table_name)

