"""Skeleton agent implementations."""

from crewai import Agent

nlp_agent = Agent("nlp-intent")
planner = Agent("planner")
codegen = Agent("codegen")
executor = Agent("executor")
modeler = Agent("data-model")
auditor = Agent("audit")

